# PR: Remove vibe-coding shortcuts

Centralized CV limits and interview timer config in `shared/app_config.json`, made Finnish-only behavior explicit, added configurable 60/90/120 second timers, improved error recovery actions, normalized CTA/card density, and fixed focus chip accessibility/touch targets.

## Changed files

- `shared/app_config.json` — single source of truth for CV minimum length, language mode, and timer options.
- `backend/app_config.py`, `api/app_config.py` — backend/API readers for shared config.
- `backend/server.py`, `api/server.py` — `/api/app-config`, shared CV limit validation, timer validation/echo.
- `backend/interview_models.py`, `api/interview_models.py` — timer normalization helper.
- `backend/interview_service.py`, `api/interview_service.py` — session timer stored consistently.
- `frontend/craco.config.js` — allows importing the shared config JSON.
- `frontend/src/App.js` — shared CV limit, Finnish-only notice, consistent CTA classes, actionable errors.
- `frontend/src/pages/InterviewPage.js` — timer selector, Finnish-only notice, actionable errors, accessible 44px focus chips.
- `frontend/src/components/interview/InterviewChat.js` — configurable timer selector and display.
- `frontend/src/i18n.js` — removed hidden language storage state and added concise recovery/timer copy.
- `backend/tests/test_vibe_cleanup_contract.py` — config sync, Finnish-only, timer edge, error UI, and chip accessibility checks.

## Verification

- `yarn build` passed.
- Focused Python lint passed for modified backend/API files.
- `pytest -q backend/tests/test_vibe_cleanup_contract.py backend/tests/test_interview.py backend/tests/test_interview_rotation_logic.py backend/tests/test_cv_fallback_logic.py` passed.
- Manual browser check confirmed Finnish notice, timer selector, 44px focus chip, aria-label, and no mobile overflow.

## Migration notes

- Product limits now live in `shared/app_config.json`; update that file instead of editing frontend/backend separately.
- Interview timer values are limited to the configured options; invalid values fall back to the configured default.

## Release note

Cleaned up hidden config, timer behavior, error recovery, and accessibility polish.