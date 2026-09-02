from typing import Literal

from pydantic import BaseModel


class CompanyExamCreateRequest(BaseModel):
    # Company practice currently has one intentionally fixed-size flow.
    mode: Literal["20"] = "20"


class CompanyAnswerSubmission(BaseModel):
    question_id: int
    answer: str = ""


class CompanyExamSubmitRequest(BaseModel):
    answers: list[CompanyAnswerSubmission]
