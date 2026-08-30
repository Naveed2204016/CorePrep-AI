from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class RoadmapGenerateRequest(BaseModel):
    subject: str
    timeline: Literal[4, 6, 8, 10]


class RoadmapSuggestEditRequest(BaseModel):
    suggestion: str = Field(min_length=3, max_length=1000)

    @field_validator("suggestion")
    @classmethod
    def suggestion_is_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Suggestion cannot be blank")
        return value.strip()


class ResourceSchema(BaseModel):
    id: int | None = None
    title: str
    url: str
    type: Literal["Blog", "YouTube"]


class RoadmapTopicSchema(BaseModel):
    id: int
    title: str
    dayRange: str
    description: str
    resources: list[ResourceSchema]
    completed: bool = False


class RoadmapResponse(BaseModel):
    id: int
    title: str
    mode: Literal["topic"] = "topic"
    weeks: int
    sourceLabel: str
    topics: list[RoadmapTopicSchema]
    confirmed: bool
    createdAt: datetime | None = None


class RoadmapSummary(BaseModel):
    id: int
    title: str
    weeks: int
    sourceLabel: str
    topicCount: int
    createdAt: datetime


class AssessmentCreateRequest(BaseModel):
    roadmap_id: int
    topic_id: int
    num_mcq: int = Field(ge=0, le=10)
    num_short: int = Field(ge=0, le=10)
    duration_minutes: int = Field(ge=1, le=120)

    @model_validator(mode="after")
    def contains_at_least_one_question(self) -> "AssessmentCreateRequest":
        if self.num_mcq + self.num_short < 1:
            raise ValueError("Select at least one question")
        return self


class AssessmentAnswerRequest(BaseModel):
    question_id: int
    answer: str = Field(default="", max_length=5000)


class AssessmentSubmitRequest(BaseModel):
    answers: list[AssessmentAnswerRequest] = Field(max_length=20)
