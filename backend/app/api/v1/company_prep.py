from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.company_prep import (
    CompanyExam,
    CompanyExamAnswer,
    CompanyExamAttempt,
    CompanyExamQuestion,
)
from app.schemas.company_prep import CompanyExamCreateRequest, CompanyExamSubmitRequest
from app.services.company_evaluation_service import get_company_evaluation_service
from app.services.company_prep_service import (
    COMPANIES_BY_SLUG,
    CompanyQuestionSourceError,
    get_company_prep_service,
)


router = APIRouter(prefix="/api/v1/company-prep", tags=["company preparation"])


@router.get("/companies")
async def list_companies(
    _current_user: dict[str, Any] = Depends(get_current_user),
):
    return {"companies": get_company_prep_service().companies()}


@router.get("/companies/{company_slug}")
async def get_company(
    company_slug: str,
    _current_user: dict[str, Any] = Depends(get_current_user),
):
    company = COMPANIES_BY_SLUG.get(company_slug)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    try:
        questions = await get_company_prep_service().questions(company_slug)
    except CompanyQuestionSourceError as exc:
        raise HTTPException(
            status_code=502,
            detail="The company question bank is temporarily unavailable. Please try again.",
        ) from exc
    return {
        "name": company.name,
        "slug": company.slug,
        "shortName": company.short_name,
        "questionCount": len(questions),
        "examQuestionCount": 20,
    }


@router.post("/companies/{company_slug}/exams")
async def create_company_exam(
    company_slug: str,
    request: CompanyExamCreateRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    company = COMPANIES_BY_SLUG.get(company_slug)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    try:
        available = await get_company_prep_service().questions(company_slug)
        generated_questions = await get_company_prep_service().create_exam(company_slug)
    except CompanyQuestionSourceError as exc:
        raise HTTPException(
            status_code=502,
            detail="The company question bank is temporarily unavailable. Please try again.",
        ) from exc
    exam = CompanyExam(
        user_id=current_user["id"],
        company_slug=company.slug,
        company_name=company.name,
    )
    for position, item in enumerate(generated_questions, start=1):
        exam.questions.append(CompanyExamQuestion(
            question_text=item["question"],
            reference_answer=item.get("answer") or None,
            position=position,
        ))
    try:
        db.add(exam)
        db.commit()
        db.refresh(exam)
    except Exception:
        db.rollback()
        raise
    stored_questions = sorted(exam.questions, key=lambda item: item.position)
    return {
        "examId": exam.id,
        "company": {
            "name": company.name,
            "slug": company.slug,
            "shortName": company.short_name,
        },
        "mode": "20",
        "availableQuestionCount": len(available),
        "questionCount": len(stored_questions),
        "questions": [
            {
                "id": item.id,
                "question": item.question_text,
            }
            for item in stored_questions
        ],
    }


def _stored_result(db: Session, attempt: CompanyExamAttempt) -> dict[str, Any]:
    rows = (
        db.query(CompanyExamAnswer, CompanyExamQuestion)
        .join(CompanyExamQuestion, CompanyExamQuestion.id == CompanyExamAnswer.question_id)
        .filter(CompanyExamAnswer.attempt_id == attempt.id)
        .order_by(CompanyExamQuestion.position)
        .all()
    )
    items = [
        {
            "questionId": question.id,
            "question": question.question_text,
            "userAnswer": answer.user_answer,
            "score": round(answer.score, 1),
            "status": answer.status,
            "feedback": answer.feedback,
            "suggestedAnswer": answer.suggested_answer,
            "referenceAnswer": question.reference_answer,
        }
        for answer, question in rows
    ]
    return {
        "examId": attempt.exam_id,
        "attemptId": attempt.id,
        "score": round(attempt.score),
        "correctCount": sum(item["status"] == "correct" for item in items),
        "partialCount": sum(item["status"] == "partially_correct" for item in items),
        "totalQuestions": len(items),
        "evaluationSource": "ai",
        "items": items,
    }


@router.post("/exams/{exam_id}/submit")
async def submit_company_exam(
    exam_id: int,
    request: CompanyExamSubmitRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    exam = (
        db.query(CompanyExam)
        .filter(CompanyExam.id == exam_id, CompanyExam.user_id == current_user["id"])
        .first()
    )
    if exam is None:
        raise HTTPException(status_code=404, detail="Company exam not found")
    previous = (
        db.query(CompanyExamAttempt)
        .filter(
            CompanyExamAttempt.exam_id == exam.id,
            CompanyExamAttempt.user_id == current_user["id"],
        )
        .order_by(CompanyExamAttempt.id.desc())
        .first()
    )
    if previous:
        return _stored_result(db, previous)

    questions = (
        db.query(CompanyExamQuestion)
        .filter(CompanyExamQuestion.exam_id == exam.id)
        .order_by(CompanyExamQuestion.position)
        .all()
    )
    submitted = {item.question_id: item.answer.strip() for item in request.answers}
    if len(submitted) != len(request.answers):
        raise HTTPException(status_code=400, detail="Each question may be answered only once")
    valid_ids = {item.id for item in questions}
    if any(question_id not in valid_ids for question_id in submitted):
        raise HTTPException(status_code=400, detail="An answer contains an invalid question ID")
    evaluation_input = [
        {
            "question_id": question.id,
            "question": question.question_text,
            "reference_answer": question.reference_answer,
            "user_answer": submitted.get(question.id, ""),
        }
        for question in questions
    ]
    try:
        evaluations = await get_company_evaluation_service().evaluate(
            company_name=exam.company_name,
            questions=evaluation_input,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="The AI could not evaluate this attempt. Your answers are saved in the browser; please try again.",
        ) from exc

    # Prevent two simultaneous submissions from creating duplicate attempts.
    previous = (
        db.query(CompanyExamAttempt)
        .filter(
            CompanyExamAttempt.exam_id == exam.id,
            CompanyExamAttempt.user_id == current_user["id"],
        )
        .first()
    )
    if previous:
        return _stored_result(db, previous)

    average = sum(item.score for item in evaluations) / max(1, len(evaluations))
    attempt = CompanyExamAttempt(
        exam_id=exam.id,
        user_id=current_user["id"],
        score=average * 10,
    )
    try:
        db.add(attempt)
        db.flush()
        by_id = {item.question_id: item for item in evaluations}
        for question in questions:
            evaluation = by_id[question.id]
            db.add(CompanyExamAnswer(
                attempt_id=attempt.id,
                question_id=question.id,
                user_answer=submitted.get(question.id, ""),
                score=evaluation.score,
                status=evaluation.status,
                feedback=evaluation.feedback,
                suggested_answer=evaluation.suggested_answer,
                is_correct=evaluation.status == "correct",
            ))
        db.commit()
        db.refresh(attempt)
    except IntegrityError:
        # The database constraint is the final guard when two requests finish
        # evaluation at the same time. Return the transaction that won the race.
        db.rollback()
        previous = (
            db.query(CompanyExamAttempt)
            .filter(
                CompanyExamAttempt.exam_id == exam.id,
                CompanyExamAttempt.user_id == current_user["id"],
            )
            .first()
        )
        if previous is None:
            raise
        return _stored_result(db, previous)
    except Exception:
        db.rollback()
        raise
    return _stored_result(db, attempt)
