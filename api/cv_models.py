from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


DIMENSIONS = [
    "Formatting and Structure",
    "Content Relevance",
    "Language and Style",
    "Cultural and Market Fit",
    "Strategic Positioning",
]


class DimensionFeedback(BaseModel):
    dimension: str
    score: int = Field(ge=0, le=10)
    strengths: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)
    observations: str = ""


class KeyStrength(BaseModel):
    title: str
    explanation: str


class PriorityRecommendation(BaseModel):
    rank: int = Field(ge=1)
    title: str
    impact: str
    rationale: str
    example: Optional[str] = None


class RevisedExcerpt(BaseModel):
    section: str
    original: Optional[str] = None
    revised: str
    why_it_works: str


class CVReview(BaseModel):
    overall_score: int = Field(ge=0, le=10)
    overall_assessment: str
    key_strength: KeyStrength
    dimensions: List[DimensionFeedback]
    priority_recommendations: List[PriorityRecommendation]
    revised_excerpts: List[RevisedExcerpt] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    market_notes: List[str] = Field(default_factory=list)
