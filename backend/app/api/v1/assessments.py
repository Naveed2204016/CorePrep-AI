import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.roadmap import (
    Assessment,
    AssessmentQuestion,
    Roadmap,
    RoadmapTopic,
    UserAnswer,
    UserAssessmentAttempt,
)
from app.schemas.roadmap import AssessmentCreateRequest, AssessmentSubmitRequest
from app.services.assessment_service import get_assessment_service
from app.services.curriculum_registry import CURRICULA

router = APIRouter(prefix="/api/v1/assessments", tags=["assessments"])
logger = logging.getLogger(__name__)


def _assessment_subject(roadmap: Roadmap, topic: RoadmapTopic) -> str:
    if topic.curriculum_subject:
        return topic.curriculum_subject
    if not roadmap.subject.startswith("Job description:"):
        return roadmap.subject
    matches = [
        subject for subject, curriculum in CURRICULA.items()
        if any(item.title == topic.topic_name for item in curriculum)
    ]
    if not matches:
        raise ValueError(f"No curriculum subject found for {topic.topic_name}")
    return matches[0]


def _owned_assessment(
    db: Session, assessment_id: int, user_id: int
) -> tuple[Assessment, Roadmap, RoadmapTopic]:
    row = (
        db.query(Assessment, Roadmap, RoadmapTopic)
        .join(Roadmap, Roadmap.id == Assessment.roadmap_id)
        .join(RoadmapTopic, RoadmapTopic.id == Assessment.topic_id)
        .filter(Assessment.id == assessment_id, Roadmap.user_id == user_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return row


def _stored_attempt_result(
    db: Session,
    attempt: UserAssessmentAttempt,
    topic: RoadmapTopic,
) -> dict[str, Any]:
    rows = (
        db.query(UserAnswer, AssessmentQuestion)
        .join(AssessmentQuestion, AssessmentQuestion.id == UserAnswer.question_id)
        .filter(UserAnswer.attempt_id == attempt.id)
        .order_by(AssessmentQuestion.id)
        .all()
    )
    items = [
        {
            "questionId": question.id,
            "type": question.question_type,
            "question": question.question_text,
            "userAnswer": answer.user_answer or "",
            "correctAnswer": question.correct_answer,
            "explanation": answer.explanation,
            "correct": bool(answer.is_correct),
            "revisionArea": topic.topic_name,
        }
        for answer, question in rows
    ]
    score = round(attempt.score or 0)
    revision_areas = [topic.topic_name] if any(not item["correct"] for item in items) else []
    return {
        "topicId": topic.id,
        "score": score,
        "correctCount": sum(1 for item in items if item["correct"]),
        "totalQuestions": len(items),
        "passed": score >= 70,
        "evaluationSource": "stored",
        "revisionAreas": revision_areas,
        "items": items,
    }


@router.post("/generate")
async def generate_assessment(
    request: AssessmentCreateRequest,
    db: Session = Depends(get_db),
    current_user: dict[str, Any] = Depends(get_current_user),
):
    roadmap = (
        db.query(Roadmap)
        .filter(Roadmap.id == request.roadmap_id, Roadmap.user_id == current_user["id"])
        .first()
    )
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    topic = (
        db.query(RoadmapTopic)
        .filter(
            RoadmapTopic.id == request.topic_id,
            RoadmapTopic.roadmap_id == roadmap.id,
        )
        .first()
    )
    if not topic:
        raise HTTPException(status_code=404, detail="Roadmap topic not found")

    try:
        generated = await get_assessment_service().generate_questions(
            topic=topic.topic_name,
            subject=_assessment_subject(roadmap, topic),
            num_mcq=request.num_mcq,
            num_short=request.num_short,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="The AI could not generate a grounded assessment. Please try again.",
        ) from exc

    assessment = Assessment(
        roadmap_id=roadmap.id,
        topic_id=topic.id,
        num_mcq=request.num_mcq,
        num_short=request.num_short,
        duration_minutes=request.duration_minutes,
    )
    for item in generated.mcq:
        assessment.questions.append(AssessmentQuestion(
            question_text=item.question,
            question_type="mcq",
            options=item.options,
            correct_answer=item.correct_answer,
        ))
    for item in generated.short:
        assessment.questions.append(AssessmentQuestion(
            question_text=item.question,
            question_type="short",
            options=None,
            correct_answer=item.reference_answer,
        ))
    try:
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
    except Exception:
        db.rollback()
        raise

    questions = sorted(assessment.questions, key=lambda question: question.id)
    return {
        "assessmentId": assessment.id,
        "generationSource": "groq-rag",
        "topicId": topic.id,
        "durationMinutes": assessment.duration_minutes,
        "questions": [
            {
                "id": question.id,
                "type": question.question_type,
                "question": question.question_text,
                "options": question.options if question.question_type == "mcq" else None,
            }
            for question in questions
        ],
    }


@router.post("/{assessment_id}/submit")
async def submit_assessment(
    assessment_id: int,
    request: AssessmentSubmitRequest,
    db: Session = Depends(get_db),
    current_user: dict[str, Any] = Depends(get_current_user),
):
    assessment, roadmap, topic = _owned_assessment(
        db, assessment_id, current_user["id"]
    )
    existing_attempt = (
        db.query(UserAssessmentAttempt)
        .filter(
            UserAssessmentAttempt.assessment_id == assessment.id,
            UserAssessmentAttempt.user_id == current_user["id"],
            UserAssessmentAttempt.submitted_at.isnot(None),
        )
        .order_by(UserAssessmentAttempt.id.desc())
        .first()
    )
    if existing_attempt:
        logger.info("Returning stored result for assessment %s", assessment.id)
        return _stored_attempt_result(db, existing_attempt, topic)
    questions = (
        db.query(AssessmentQuestion)
        .filter(AssessmentQuestion.assessment_id == assessment.id)
        .order_by(AssessmentQuestion.id)
        .all()
    )
    submitted = {item.question_id: item.answer for item in request.answers}
    grading_input = [
        {
            "question_id": question.id,
            "question_type": question.question_type,
            "question": question.question_text,
            "options": question.options,
            "correct_answer": question.correct_answer,
            "user_answer": submitted.get(question.id, ""),
        }
        for question in questions
    ]
    evaluations, evaluation_source = await get_assessment_service().evaluate_answers(
        topic=topic.topic_name,
        subject=_assessment_subject(roadmap, topic),
        questions=grading_input,
    )
    # A retry can arrive while the first request is being evaluated. Recheck before
    # writing so the same generated assessment is not recorded twice.
    existing_attempt = (
        db.query(UserAssessmentAttempt)
        .filter(
            UserAssessmentAttempt.assessment_id == assessment.id,
            UserAssessmentAttempt.user_id == current_user["id"],
            UserAssessmentAttempt.submitted_at.isnot(None),
        )
        .order_by(UserAssessmentAttempt.id.desc())
        .first()
    )
    if existing_attempt:
        return _stored_attempt_result(db, existing_attempt, topic)
    evaluation_by_id = {item.question_id: item for item in evaluations}
    logger.info(
        "Assessment %s evaluation source: %s", assessment.id, evaluation_source
    )

    attempt = UserAssessmentAttempt(
        user_id=current_user["id"],
        assessment_id=assessment.id,
        score=0,
    )
    db.add(attempt)
    db.flush()

    items = []
    total_marks = 0.0
    for question in questions:
        evaluation = evaluation_by_id[question.id]
        user_answer = submitted.get(question.id, "")
        total_marks += evaluation.marks
        db.add(UserAnswer(
            attempt_id=attempt.id,
            question_id=question.id,
            user_answer=user_answer,
            is_correct=evaluation.is_correct,
            explanation=evaluation.explanation,
            marks_obtained=evaluation.marks,
        ))
        items.append({
            "questionId": question.id,
            "type": question.question_type,
            "question": question.question_text,
            "userAnswer": user_answer,
            "correctAnswer": question.correct_answer,
            "explanation": evaluation.explanation,
            "correct": evaluation.is_correct,
            "revisionArea": evaluation.revision_area,
        })

    score = round((total_marks / max(1, len(questions))) * 100)
    passed = score >= 70
    attempt.score = score
    from datetime import datetime
    attempt.submitted_at = datetime.utcnow()
    if passed:
        topic.completed = True
        topic.completion_score = score
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    revision_areas = list(dict.fromkeys(
        item["revisionArea"] for item in items if not item["correct"]
    ))
    return {
        "topicId": topic.id,
        "score": score,
        "correctCount": sum(1 for item in items if item["correct"]),
        "totalQuestions": len(items),
        "passed": passed,
        "evaluationSource": evaluation_source,
        "revisionAreas": revision_areas,
        "items": items,
    }
