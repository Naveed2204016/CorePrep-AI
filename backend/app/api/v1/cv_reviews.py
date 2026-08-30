import logging
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.security import get_current_user
from app.schemas.cv_review import CVReviewResponse
from app.services.cv_review_service import CVReviewError, get_cv_review_service


router = APIRouter(prefix="/api/v1/cv-reviews", tags=["CV reviews"])
logger = logging.getLogger(__name__)


@router.post("/analyze", response_model=CVReviewResponse)
async def analyze_cv(
    file: UploadFile = File(...),
    current_user: dict[str, Any] = Depends(get_current_user),
) -> CVReviewResponse:
    del current_user
    try:
        return await get_cv_review_service().review(file)
    except CVReviewError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("CV review failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI could not review this CV. Please try again.",
        ) from exc

