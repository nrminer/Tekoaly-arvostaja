import logging
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, File, Form, HTTPException, Request, UploadFile
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from starlette.requests import Request as StarletteRequest
from starlette.responses import JSONResponse

from cv_service import (
    ALLOWED_MARKETS,
    ALLOWED_SENIORITY,
    extract_text_from_upload,
    run_cv_review,
)
from app_config import APP_CONFIG, CV_MIN_CHARS, INTERVIEW_TIMER_SECONDS_DEFAULT
from interview_models import InterviewTarget, normalize_timer_seconds
from interview_service import (
    active_session_count,
    answer_turn as interview_answer_turn,
    end_session as interview_end_session,
    finalize_session as interview_finalize_session,
    session_exists as interview_session_exists,
    start_session as interview_start_session,
    synthesize_speech as interview_synthesize_speech,
)

_INTERVIEW_AVAILABLE = True
from security_audit import log_event, rollup
from security_config import (
    SecurityConfigLockedError,
    assert_unchanged,
    extract_client_ip,
    get_fingerprint,
    get_limits,
    get_limits_view,
    is_trusted_proxy,
)
from security_headers import SecurityHeadersMiddleware
from security_ip_intel import get_stats as get_ip_intel_stats
from security_middleware import BodySizeLimitMiddleware, VPNChallengeMiddleware
from security_turnstile import is_configured as turnstile_is_configured, verify_turnstile_token

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

LIMITS = get_limits()


def _rate_limit_key(request: Request) -> str:
    return extract_client_ip(request)


limiter = Limiter(key_func=_rate_limit_key, default_limits=[LIMITS.default_rate_limit])

app = FastAPI(title="Universal CV Review Assistant API", version="3.2.0")
app.state.limiter = limiter


async def _rate_limit_handler(request: StarletteRequest, exc: RateLimitExceeded) -> JSONResponse:
    retry_after = getattr(exc, "retry_after", None) or 60
    peer = (request.client.host if request.client else "anon") or "anon"
    client_ip = extract_client_ip(request)
    log_event(
        "rate_limit_exceeded",
        peer_ip=peer,
        client_ip=client_ip,
        trusted_peer=is_trusted_proxy(peer),
        path=request.url.path,
        method=request.method,
        status_code=429,
        retry_after=retry_after,
    )
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Liikaa pyyntöjä hetkessä. Odota hetki ja yritä uudelleen. / Too many requests. Please wait a moment and try again.",
            "retry_after_seconds": retry_after,
        },
        headers={"Retry-After": str(retry_after)},
    )


app.add_exception_handler(RateLimitExceeded, _rate_limit_handler)

app.add_middleware(VPNChallengeMiddleware)
app.add_middleware(BodySizeLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
_cors_raw = os.environ.get("CORS_ORIGINS", "").strip()
_cors_origins: list[str] = [o.strip() for o in _cors_raw.split(",") if o.strip()]
if not _cors_origins:
    _cors_origins = ["http://localhost:3000", "http://localhost:3001"]
if "*" in _cors_origins:
    logger.warning(
        "CORS_ORIGINS contains '*' — all origins are trusted. "
        "Set CORS_ORIGINS to your frontend URL before deploying to production."
    )

app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=_cors_origins,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept", "Accept-Language"],
    max_age=600,
)

api_router = APIRouter(prefix="/api")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@api_router.get("/")
async def root() -> dict[str, str]:
    return {"message": "Universal CV Review Assistant API is running"}


@api_router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "universal-cv-reviewer", "privacy_mode": "no_server_storage"}


@api_router.get("/app-config")
async def app_config() -> dict[str, Any]:
    return APP_CONFIG


@api_router.get("/security/limits")
async def security_limits(request: Request) -> dict[str, Any]:
    try:
        assert_unchanged()
    except SecurityConfigLockedError as exc:
        log_event(
            "limits_fingerprint_drift",
            peer_ip=(request.client.host if request.client else "anon"),
            path=request.url.path,
            method=request.method,
            status_code=500,
            error=str(exc),
        )
        raise HTTPException(status_code=500, detail="Security limits integrity check failed.") from exc
    return {
        "fingerprint": get_fingerprint(),
        "limits": dict(get_limits_view()),
        "ip_intel": get_ip_intel_stats(),
        "captcha": {"provider": "cloudflare_turnstile", "enabled": turnstile_is_configured()},
        "mutable": False,
        "notice": "This snapshot is read-only. Limits can only change via code + redeploy.",
    }


_AUDIT_API_KEY = os.environ.get("AUDIT_API_KEY", "").strip()


@api_router.get("/security/audit/health")
@limiter.limit("30/minute")
async def security_audit_health(request: Request, window_seconds: int = 3600) -> dict[str, Any]:
    if _AUDIT_API_KEY:
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer ") or auth[len("Bearer "):] != _AUDIT_API_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized.")
    return {"fingerprint": get_fingerprint(), "rollup": rollup(window_seconds=window_seconds)}


@api_router.get("/options")
@limiter.limit(LIMITS.options_rate_limit)
async def options(request: Request) -> dict[str, Any]:
    return {
        "markets": [
            {"code": "Finland", "label": "Suomi / Finland"},
            {"code": "Nordics", "label": "Nordics (Sweden, Denmark, Norway, Iceland)"},
            {"code": "US", "label": "United States (US)"},
            {"code": "EU", "label": "European Union (EU)"},
        ],
        "seniority_levels": [
            "Student/Intern",
            "Early-career",
            "Mid-level",
            "Senior",
            "Lead/Principal",
            "Executive",
        ],
    }


def _audit_context(request: Request) -> dict[str, Any]:
    peer = (request.client.host if request.client else "anon") or "anon"
    client_ip = extract_client_ip(request)
    return {
        "peer_ip": peer,
        "client_ip": client_ip,
        "trusted_peer": is_trusted_proxy(peer),
        "path": request.url.path,
        "method": request.method,
    }


@api_router.post("/review")
@limiter.limit(LIMITS.review_rate_limit)
async def create_review(
    request: Request,
    cv_text: Optional[str] = Form(default=None),
    job_title: Optional[str] = Form(default=None),
    industry: Optional[str] = Form(default=None),
    seniority: Optional[str] = Form(default=None),
    market: Optional[str] = Form(default=None),
    job_description: Optional[str] = Form(default=None),
    specific_concerns: Optional[str] = Form(default=None),
    language: Optional[str] = Form(default="fi"),
    turnstile_token: Optional[str] = Form(default=None),
    file: Optional[UploadFile] = File(default=None),
) -> dict[str, Any]:
    ctx = _audit_context(request)
    language_value = (language or "fi").strip().lower()
    if language_value not in {"fi", "en"}:
        language_value = "fi"

    if turnstile_is_configured():
        verified, reason = await verify_turnstile_token(turnstile_token, remote_ip=ctx["peer_ip"])
        if not verified:
            log_event("captcha_failed", **ctx, status_code=403, reason=reason)
            raise HTTPException(
                status_code=403,
                detail=(
                    "Vahvista ensin ettet ole robotti — napsauta ruutua \"En ole robotti\" ja yritä uudelleen. "
                    "/ Please confirm you're not a robot — tick the \"I'm not a robot\" box and try again."
                ),
            )
        log_event("captcha_passed", **ctx, status_code=200)

    def _reject_oversized(field: str, limit: int, value: str) -> None:
        log_event(
            "oversized_field_rejected",
            **ctx,
            status_code=413,
            field=field,
            length=len(value),
            max_length=limit,
        )

    if cv_text and len(cv_text) > LIMITS.max_cv_text_input:
        _reject_oversized("cv_text", LIMITS.max_cv_text_input, cv_text)
        raise HTTPException(status_code=413, detail=f"CV text is too long. Please trim to under {LIMITS.max_cv_text_input} characters.")
    if job_title and len(job_title) > LIMITS.max_job_title_chars:
        _reject_oversized("job_title", LIMITS.max_job_title_chars, job_title)
        raise HTTPException(status_code=413, detail="Job title is too long.")
    if industry and len(industry) > LIMITS.max_industry_chars:
        _reject_oversized("industry", LIMITS.max_industry_chars, industry)
        raise HTTPException(status_code=413, detail="Industry is too long.")
    if job_description and len(job_description) > LIMITS.max_job_description_chars:
        _reject_oversized("job_description", LIMITS.max_job_description_chars, job_description)
        raise HTTPException(status_code=413, detail=f"Job description is too long. Please trim to under {LIMITS.max_job_description_chars} characters.")
    if specific_concerns and len(specific_concerns) > LIMITS.max_specific_concerns_chars:
        _reject_oversized("specific_concerns", LIMITS.max_specific_concerns_chars, specific_concerns)
        raise HTTPException(status_code=413, detail=f"Specific concerns text is too long. Please trim to under {LIMITS.max_specific_concerns_chars} characters.")

    market_value = (market or "Global").strip() or "Global"
    if market_value not in ALLOWED_MARKETS:
        log_event("invalid_market", **ctx, status_code=400, market=market_value)
        raise HTTPException(status_code=400, detail=f"Unsupported market '{market_value}'.")
    seniority_value = (seniority or "").strip()
    if seniority_value and seniority_value not in ALLOWED_SENIORITY:
        log_event("invalid_seniority", **ctx, status_code=400, seniority=seniority_value)
        raise HTTPException(status_code=400, detail=f"Unsupported seniority '{seniority_value}'.")

    extracted_text = ""
    filename = None
    filetype = None
    if file and file.filename:
        filename = file.filename
        filetype = (Path(file.filename).suffix or "").lower().replace(".", "")
        try:
            extracted_text = await extract_text_from_upload(file)
        except ValueError as exc:
            msg = str(exc)
            if "too large" in msg.lower():
                log_event("oversized_file", **ctx, status_code=400, reason=msg)
            else:
                log_event("invalid_file_type", **ctx, status_code=400, reason=msg)
            raise HTTPException(status_code=400, detail=msg) from exc
        except Exception as exc:
            logger.exception("CV file extraction failed")
            raise HTTPException(status_code=422, detail="We could not extract readable text from this file. If it is a scanned PDF, please paste the CV text instead.") from exc

    pasted_text = (cv_text or "").strip()
    combined_text = (
        f"{extracted_text}\n\nAdditional pasted text:\n{pasted_text}"
        if pasted_text and extracted_text
        else (extracted_text or pasted_text)
    ).strip()

    if len(combined_text) < CV_MIN_CHARS:
        log_event(
            "invalid_payload",
            **ctx,
            status_code=400,
            reason="cv_text_too_short",
            length=len(combined_text),
        )
        raise HTTPException(
            status_code=400,
            detail=(
                f"Lisää CV:hen vähintään {CV_MIN_CHARS} merkkiä tai lataa pidempi tiedosto. "
                f"/ Please provide at least {CV_MIN_CHARS} characters of CV content."
            ),
        )

    was_truncated = len(combined_text) > LIMITS.max_text_chars_for_llm
    text_for_review = combined_text[: LIMITS.max_text_chars_for_llm]
    target = {
        "job_title": (job_title or "").strip(),
        "industry": (industry or "").strip(),
        "seniority": seniority_value,
        "market": market_value,
        "job_description": (job_description or "").strip(),
        "specific_concerns": (specific_concerns or "").strip(),
    }

    review_id = str(uuid.uuid4())
    try:
        ai_review, ai_model_used = await run_cv_review(
            cv_text=text_for_review,
            target=target,
            session_id=f"cv-review-{review_id}",
            language=language_value,
        )
    except RuntimeError as exc:
        logger.exception("AI review failed")
        log_event("review_failed_upstream", **ctx, status_code=503, error_type=type(exc).__name__)
        detail_text = str(exc)
        detail_lower = detail_text.lower()
        if "budget" in detail_lower or "rate" in detail_lower or "overloaded" in detail_lower:
            raise HTTPException(status_code=503, detail="AI-palvelun budjetti on tilapäisesti käytetty. Yritä hetken päästä uudelleen. / The AI service budget is temporarily exhausted. Please try again shortly.") from exc
        if "timeout" in detail_lower or "unavailable" in detail_lower:
            raise HTTPException(status_code=503, detail="AI-palvelu ei ole juuri nyt tavoitettavissa. Yritä hetken päästä uudelleen. / The AI service is not reachable right now. Please try again shortly.") from exc
        raise HTTPException(status_code=502, detail=detail_text) from exc
    except Exception as exc:
        logger.exception("Unexpected AI review error")
        log_event("review_failed_upstream", **ctx, status_code=502, error_type=type(exc).__name__)
        raise HTTPException(status_code=502, detail="AI-arvioija ei voinut viimeistellä analyysiä juuri nyt. Yritä hetken päästä uudelleen. / The AI reviewer could not complete the analysis right now. Please try again shortly.") from exc

    log_event(
        "review_completed",
        **ctx,
        status_code=200,
        model_used=ai_model_used,
        text_length=len(combined_text),
        was_truncated=was_truncated,
    )
    return {
        "id": review_id,
        "created_at": now_iso(),
        "filename": filename,
        "filetype": filetype,
        "job_title": target["job_title"],
        "industry": target["industry"],
        "seniority": target["seniority"],
        "market": target["market"],
        "specific_concerns": target["specific_concerns"],
        "language": language_value,
        "text_length": len(combined_text),
        "was_truncated": was_truncated,
        "model_used": ai_model_used,
        "privacy_mode": "no_server_storage",
        "review": ai_review.model_dump(),
    }


@api_router.get("/reviews")
async def list_reviews_disabled() -> None:
    raise HTTPException(status_code=410, detail="Review history is disabled in privacy-first mode.")


@api_router.get("/reviews/{review_id}")
async def get_review_disabled(review_id: str) -> None:
    raise HTTPException(status_code=410, detail="Review history is disabled in privacy-first mode.")


@api_router.delete("/reviews/{review_id}")
async def delete_review_disabled(review_id: str) -> None:
    raise HTTPException(status_code=410, detail="Review history is disabled in privacy-first mode.")


# ---------------------------------------------------------------------------
# Mock Interview Simulator — Finnish-default AI interviewer
# ---------------------------------------------------------------------------


class InterviewStartRequest(BaseModel):
    language: str = Field(default="fi")
    mode: str = Field(default="chat")  # "chat" | "video"
    consent_video: bool = False
    cv_summary: str = Field(default="", max_length=8000)
    job_title: Optional[str] = Field(default=None, max_length=500)
    industry: Optional[str] = Field(default=None, max_length=500)
    seniority: Optional[str] = Field(default=None, max_length=100)
    market: Optional[str] = Field(default="Finland", max_length=100)
    job_description: Optional[str] = Field(default=None, max_length=5000)
    focus_areas: list[str] = Field(default_factory=list)
    timer_seconds: int = Field(default=INTERVIEW_TIMER_SECONDS_DEFAULT)
    turnstile_token: Optional[str] = None


class InterviewTurnRequest(BaseModel):
    session_id: str
    user_answer: str = Field(default="", max_length=4000)


class InterviewTTSRequest(BaseModel):
    session_id: str
    text: str = Field(min_length=1, max_length=1500)
    voice: str = Field(default="nova")
    speed: float = Field(default=1.0, ge=0.5, le=2.0)


def _require_interview() -> None:
    if not _INTERVIEW_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail=(
                "Haastattelusimulaattori ei ole käytettävissä tässä ympäristössä. "
                "/ Interview simulator is not available in this environment."
            ),
        )


def _map_interview_exception(exc: Exception) -> HTTPException:
    text = str(exc).lower()
    if isinstance(exc, KeyError):
        return HTTPException(status_code=404, detail="Interview session not found or expired.")
    if "budget" in text:
        return HTTPException(
            status_code=503,
            detail=(
                "AI-palvelun budjetti on tilapäisesti käytetty. Yritä hetken päästä uudelleen. "
                "/ The AI service budget is temporarily exhausted. Please try again shortly."
            ),
        )
    if "timeout" in text or "badgateway" in text or "bad gateway" in text:
        return HTTPException(
            status_code=503,
            detail=(
                "AI-palvelu ei ole juuri nyt tavoitettavissa. Yritä hetken päästä uudelleen. "
                "/ The AI service is not reachable right now. Please try again shortly."
            ),
        )
    return HTTPException(status_code=502, detail=f"Interviewer AI error: {exc}")


@api_router.post("/interview/start")
@limiter.limit(LIMITS.review_rate_limit)
async def interview_start(request: Request, payload: InterviewStartRequest) -> dict[str, Any]:
    _require_interview()
    ctx = _audit_context(request)
    language = "fi" if (payload.language or "fi").lower() != "en" else "en"
    mode = payload.mode if payload.mode in {"chat", "video"} else "chat"
    if mode == "video" and not payload.consent_video:
        log_event("interview_consent_missing", **ctx, status_code=400)
        raise HTTPException(
            status_code=400,
            detail=(
                "Kameran käyttö vaatii nimenomaisen suostumuksen. "
                "/ Camera mode requires explicit consent."
            ),
        )

    if turnstile_is_configured():
        verified, reason = await verify_turnstile_token(payload.turnstile_token, remote_ip=ctx["peer_ip"])
        if not verified:
            log_event("captcha_failed", **ctx, status_code=403, reason=reason)
            raise HTTPException(
                status_code=403,
                detail=(
                    "Vahvista ensin ettet ole robotti — napsauta ruutua \"En ole robotti\" ja yritä uudelleen. "
                    "/ Please confirm you're not a robot — tick the \"I'm not a robot\" box and try again."
                ),
            )
        log_event("captcha_passed", **ctx, status_code=200)

    target = InterviewTarget(
        job_title=payload.job_title,
        industry=payload.industry,
        seniority=payload.seniority,
        market=payload.market or "Finland",
        job_description=payload.job_description,
        focus_areas=[f for f in (payload.focus_areas or []) if f][:6],
    )

    try:
        session, first_turn = await interview_start_session(
            language=language,
            mode=mode,
            target=target,
            cv_summary=payload.cv_summary or "",
            consent_video=bool(payload.consent_video),
            timer_seconds=normalize_timer_seconds(payload.timer_seconds),
        )
    except RuntimeError as exc:
        logger.exception("Interview start failed")
        log_event("interview_start_failed", **ctx, status_code=503, error_type=type(exc).__name__)
        raise _map_interview_exception(exc) from exc

    log_event(
        "interview_started",
        **ctx,
        status_code=200,
        mode=mode,
        language=language,
        consent_video=bool(payload.consent_video),
    )
    return {
        "session_id": session.id,
        "language": language,
        "mode": mode,
        "turn": first_turn.model_dump(),
        "timer_seconds": session.timer_seconds,
        "active_sessions": active_session_count(),
        "privacy_mode": "no_server_storage",
    }


@api_router.post("/interview/turn")
@limiter.limit(LIMITS.review_rate_limit)
async def interview_turn(request: Request, payload: InterviewTurnRequest) -> dict[str, Any]:
    _require_interview()
    ctx = _audit_context(request)
    try:
        turn = await interview_answer_turn(payload.session_id, payload.user_answer or "")
    except KeyError as exc:
        log_event("interview_session_missing", **ctx, status_code=404)
        raise HTTPException(status_code=404, detail="Interview session not found or expired.") from exc
    except RuntimeError as exc:
        logger.exception("Interview turn failed")
        log_event("interview_turn_failed", **ctx, status_code=503, error_type=type(exc).__name__)
        raise _map_interview_exception(exc) from exc
    log_event("interview_turn", **ctx, status_code=200, is_final=turn.is_final)
    return {"turn": turn.model_dump()}


@api_router.post("/interview/finish")
@limiter.limit(LIMITS.review_rate_limit)
async def interview_finish(request: Request, payload: InterviewTurnRequest) -> dict[str, Any]:
    _require_interview()
    ctx = _audit_context(request)
    try:
        turn = await interview_finalize_session(payload.session_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Interview session not found or expired.") from exc
    except RuntimeError as exc:
        logger.exception("Interview finalize failed")
        raise _map_interview_exception(exc) from exc
    log_event("interview_finished", **ctx, status_code=200)
    return {"turn": turn.model_dump()}


@api_router.post("/interview/tts")
@limiter.limit(LIMITS.default_rate_limit)
async def interview_tts(request: Request, payload: InterviewTTSRequest) -> dict[str, Any]:
    _require_interview()
    ctx = _audit_context(request)
    if not interview_session_exists(payload.session_id):
        raise HTTPException(status_code=404, detail="Interview session not found or expired.")
    try:
        audio_b64 = await interview_synthesize_speech(
            payload.text,
            voice=payload.voice,
            speed=payload.speed,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("TTS generation failed")
        log_event("interview_tts_failed", **ctx, status_code=503, error_type=type(exc).__name__)
        raise HTTPException(status_code=503, detail=f"TTS temporarily unavailable: {exc}") from exc
    return {
        "audio_base64": audio_b64,
        "format": "mp3",
        "voice": payload.voice,
    }


@api_router.delete("/interview/{session_id}")
@limiter.limit(LIMITS.default_rate_limit)
async def interview_delete(request: Request, session_id: str) -> dict[str, Any]:
    _require_interview()
    existed = interview_end_session(session_id)
    return {"deleted": existed}


@api_router.post("/interview/extract-cv")
@limiter.limit(LIMITS.options_rate_limit)
async def interview_extract_cv(
    request: Request,
    file: UploadFile = File(...),
) -> dict[str, Any]:
    ctx = _audit_context(request)
    try:
        extracted_text = await extract_text_from_upload(file)
    except ValueError as exc:
        msg = str(exc)
        if "too large" in msg.lower():
            log_event("oversized_file", **ctx, status_code=400, reason=msg)
        else:
            log_event("invalid_file_type", **ctx, status_code=400, reason=msg)
        raise HTTPException(status_code=400, detail=msg) from exc
    except Exception as exc:
        logger.exception("Interview CV file extraction failed")
        raise HTTPException(
            status_code=422,
            detail=(
                "Emme pystyneet lukemaan tekstiä tästä tiedostosta. Jos kyseessä on skannattu PDF, "
                "liitä CV-teksti suoraan tekstikenttään. / We could not extract readable text from "
                "this file. If it is a scanned PDF, please paste the CV text instead."
            ),
        ) from exc

    log_event(
        "interview_cv_extracted",
        **ctx,
        status_code=200,
        text_length=len(extracted_text),
        filename=(file.filename or "")[:200],
    )
    return {
        "cv_text": extracted_text[: LIMITS.max_text_chars_for_llm],
        "text_length": len(extracted_text),
        "filename": file.filename,
    }


app.include_router(api_router)
