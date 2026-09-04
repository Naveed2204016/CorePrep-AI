from typing import Literal

from pydantic import BaseModel, Field


class SubjectPerformance(BaseModel):
    subject: str
    answered: int = Field(ge=0)
    correct: int = Field(ge=0)
    incorrect: int = Field(ge=0)
    accuracy: int = Field(ge=0, le=100)
    weakness_score: int = Field(ge=0, le=100)
    status: Literal["weak", "needs_attention", "strong", "not_enough_data"]


class PerformanceSummary(BaseModel):
    total_answered: int = Field(ge=0)
    overall_accuracy: int = Field(ge=0, le=100)
    weak_subjects: list[str]
    subjects: list[SubjectPerformance]

