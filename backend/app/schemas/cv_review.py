from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CVImprovement(BaseModel):
    model_config = ConfigDict(extra="forbid")

    priority: Literal["high", "medium", "low"]
    title: str = Field(min_length=3, max_length=120)
    detail: str = Field(min_length=10, max_length=700)
    rewrite_tip: str = Field(min_length=10, max_length=500)


class CVReviewResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score: int = Field(ge=0, le=100)
    summary: str = Field(min_length=20, max_length=1000)
    strengths: list[str] = Field(min_length=2, max_length=6)
    improvements: list[CVImprovement] = Field(min_length=2, max_length=6)
    missing_sections: list[str] = Field(max_length=8)
    keywords_found: list[str] = Field(max_length=15)


class CVReviewResponse(CVReviewResult):
    file_name: str
    page_count: int = Field(ge=1)

