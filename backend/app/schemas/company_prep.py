from typing import Literal

from pydantic import BaseModel


class CompanyExamCreateRequest(BaseModel):
    mode: Literal["20", "40", "all"]


class CompanyAnswerSubmission(BaseModel):
    question_id: int
    answer: str = ""


class CompanyExamSubmitRequest(BaseModel):
    answers: list[CompanyAnswerSubmission]
