from collections import defaultdict
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.roadmap import (
    Assessment,
    Roadmap,
    RoadmapTopic,
    UserAnswer,
    UserAssessmentAttempt,
)
from app.schemas.profile import PerformanceSummary, SubjectPerformance


router = APIRouter(prefix="/api/v1/profile", tags=["Profile"])
MIN_ANSWERS_FOR_CLASSIFICATION = 3


def _status(answered: int, weakness_score: int) -> str:
    if answered < MIN_ANSWERS_FOR_CLASSIFICATION:
        return "not_enough_data"
    if weakness_score >= 50:
        return "weak"
    if weakness_score >= 30:
        return "needs_attention"
    return "strong"


@router.get("/performance", response_model=PerformanceSummary)
def get_performance(
    db: Session = Depends(get_db),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> PerformanceSummary:
    rows = (
        db.query(Roadmap.subject, RoadmapTopic.curriculum_subject, UserAnswer.is_correct)
        .join(Assessment, Assessment.roadmap_id == Roadmap.id)
        .join(RoadmapTopic, RoadmapTopic.id == Assessment.topic_id)
        .join(
            UserAssessmentAttempt,
            UserAssessmentAttempt.assessment_id == Assessment.id,
        )
        .join(UserAnswer, UserAnswer.attempt_id == UserAssessmentAttempt.id)
        .filter(
            UserAssessmentAttempt.user_id == current_user["id"],
            UserAssessmentAttempt.submitted_at.isnot(None),
            UserAnswer.is_correct.isnot(None),
        )
        .all()
    )

    totals: dict[str, dict[str, int]] = defaultdict(lambda: {"answered": 0, "correct": 0})
    for roadmap_subject, curriculum_subject, is_correct in rows:
        subject = curriculum_subject or roadmap_subject or "Other"
        totals[subject]["answered"] += 1
        totals[subject]["correct"] += int(bool(is_correct))

    subjects: list[SubjectPerformance] = []
    for subject, counts in totals.items():
        answered = counts["answered"]
        correct = counts["correct"]
        incorrect = answered - correct
        accuracy = round(correct / answered * 100) if answered else 0
        weakness_score = 100 - accuracy
        subjects.append(SubjectPerformance(
            subject=subject,
            answered=answered,
            correct=correct,
            incorrect=incorrect,
            accuracy=accuracy,
            weakness_score=weakness_score,
            status=_status(answered, weakness_score),
        ))

    subjects.sort(key=lambda item: (-item.weakness_score, -item.answered, item.subject))
    total_answered = sum(item.answered for item in subjects)
    total_correct = sum(item.correct for item in subjects)
    return PerformanceSummary(
        total_answered=total_answered,
        overall_accuracy=round(total_correct / total_answered * 100) if total_answered else 0,
        weak_subjects=[item.subject for item in subjects if item.status == "weak"],
        subjects=subjects,
    )

