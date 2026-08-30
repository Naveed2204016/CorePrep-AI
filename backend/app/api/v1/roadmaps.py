from io import BytesIO

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile, status
from pypdf import PdfReader
from sqlalchemy.orm import Session, selectinload

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.roadmap import Roadmap, RoadmapTopic, TopicResource
from app.schemas.roadmap import RoadmapGenerateRequest, RoadmapSuggestEditRequest
from app.services.roadmap_service import get_roadmap_service

router = APIRouter(prefix="/api/v1/roadmaps", tags=["roadmaps"])


def _owned_roadmap(db: Session, roadmap_id: int, user_id: int) -> Roadmap:
    roadmap = (
        db.query(Roadmap)
        .options(selectinload(Roadmap.topics).selectinload(RoadmapTopic.resources))
        .filter(Roadmap.id == roadmap_id, Roadmap.user_id == user_id)
        .first()
    )
    if not roadmap:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return roadmap


def _serialize(roadmap: Roadmap, generation_source: str | None = None) -> dict:
    topics = sorted(roadmap.topics, key=lambda item: item.order)
    result = {
        "id": roadmap.id,
        "title": roadmap.title,
        "mode": "job" if roadmap.subject.startswith("Job description:") else "topic",
        "weeks": roadmap.timeline,
        "sourceLabel": roadmap.subject,
        "confirmed": roadmap.status == "active",
        "createdAt": roadmap.created_at,
        "topics": [
            {
                "id": topic.id,
                "title": topic.topic_name,
                "dayRange": f"Day {topic.start_day}-{topic.end_day}",
                "description": topic.description or "",
                "completed": bool(topic.completed),
                "resources": [
                    {
                        "id": resource.id,
                        "title": resource.title,
                        "url": resource.url,
                        "type": resource.resource_type,
                    }
                    for resource in topic.resources
                ],
            }
            for topic in topics
        ],
    }
    if generation_source:
        result["generationSource"] = generation_source
    return result


def _replace_topics(roadmap: Roadmap, generated_topics: list[dict]) -> None:
    roadmap.topics.clear()
    for order, item in enumerate(generated_topics):
        topic = RoadmapTopic(
            order=order,
            topic_name=item["title"],
            curriculum_subject=item.get("subject"),
            start_day=item["start_day"],
            end_day=item["end_day"],
            duration_weeks=max(1, round((item["end_day"] - item["start_day"] + 1) / 7)),
            description=item["description"],
        )
        topic.resources = [
            TopicResource(
                resource_type=resource["type"],
                title=resource["title"],
                url=resource["url"],
            )
            for resource in item["resources"]
        ]
        roadmap.topics.append(topic)


@router.post("/generate")
async def generate_roadmap(
    request: RoadmapGenerateRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        generated = await get_roadmap_service().generate_roadmap(
            request.subject, request.timeline
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    roadmap = Roadmap(
        user_id=current_user["id"],
        title=generated["title"],
        subject=request.subject,
        timeline=request.timeline,
        status="draft",
    )
    _replace_topics(roadmap, generated["topics"])
    try:
        db.add(roadmap)
        db.commit()
        db.refresh(roadmap)
    except Exception:
        db.rollback()
        raise
    return _serialize(
        _owned_roadmap(db, roadmap.id, current_user["id"]),
        generated.get("generation_source"),
    )


@router.post("/generate-from-job")
async def generate_roadmap_from_job(
    timeline: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if file.content_type != "application/pdf" or not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Please upload a PDF file")
    contents = await file.read(5 * 1024 * 1024 + 1)
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="PDF must be 5 MB or smaller")
    try:
        reader = PdfReader(BytesIO(contents))
        if len(reader.pages) != 1:
            raise HTTPException(status_code=422, detail="Job description PDF must contain exactly one page")
        text = reader.pages[0].extract_text() or ""
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=422, detail="The uploaded PDF could not be read") from exc
    if not text.strip():
        raise HTTPException(status_code=422, detail="The PDF contains no extractable text")

    service = get_roadmap_service()
    subjects = service.detect_job_subjects(text)
    if not subjects:
        raise HTTPException(status_code=422, detail="No CS fundamentals were found in job description")
    try:
        generated = await service.generate_job_roadmap(subjects, timeline)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    source_label = "Job description: " + ", ".join(generated["subjects"])
    roadmap = Roadmap(
        user_id=current_user["id"], title=generated["title"], subject=source_label,
        timeline=timeline, status="draft",
    )
    _replace_topics(roadmap, generated["topics"])
    try:
        db.add(roadmap)
        db.commit()
        db.refresh(roadmap)
    except Exception:
        db.rollback()
        raise
    return _serialize(
        _owned_roadmap(db, roadmap.id, current_user["id"]),
        generated.get("generation_source"),
    )


@router.get("")
def get_user_roadmaps(
    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    roadmaps = (
        db.query(Roadmap)
        .options(selectinload(Roadmap.topics).selectinload(RoadmapTopic.resources))
        .filter(Roadmap.user_id == current_user["id"], Roadmap.status == "active")
        .order_by(Roadmap.created_at.desc())
        .all()
    )
    return [_serialize(roadmap) for roadmap in roadmaps]


@router.get("/{roadmap_id}")
def get_roadmap(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return _serialize(_owned_roadmap(db, roadmap_id, current_user["id"]))


@router.delete("/{roadmap_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_roadmap(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> Response:
    roadmap = _owned_roadmap(db, roadmap_id, current_user["id"])
    try:
        db.delete(roadmap)
        db.commit()
    except Exception:
        db.rollback()
        raise
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{roadmap_id}/suggest-edit")
async def suggest_edit(
    roadmap_id: int,
    request: RoadmapSuggestEditRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    roadmap = _owned_roadmap(db, roadmap_id, current_user["id"])
    if roadmap.status == "active":
        raise HTTPException(status_code=409, detail="A confirmed roadmap cannot be edited")
    if roadmap.subject.startswith("Job description:"):
        raise HTTPException(
            status_code=409,
            detail="Mixed job-description roadmaps cannot be revised after generation",
        )
    current = {
        "title": roadmap.title,
        "topics": [
            {
                "title": topic.topic_name,
                "days": topic.end_day - topic.start_day + 1,
                "description": topic.description,
            }
            for topic in sorted(roadmap.topics, key=lambda item: item.order)
        ],
    }
    try:
        generated = await get_roadmap_service().suggest_edit(
            current, request.suggestion, roadmap.timeline, roadmap.subject
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    roadmap.title = generated["title"]
    _replace_topics(roadmap, generated["topics"])
    db.commit()
    return _serialize(
        _owned_roadmap(db, roadmap.id, current_user["id"]),
        generated.get("generation_source"),
    )


@router.post("/{roadmap_id}/confirm")
def confirm_roadmap(
    roadmap_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    roadmap = _owned_roadmap(db, roadmap_id, current_user["id"])
    roadmap.status = "active"
    db.commit()
    return _serialize(roadmap)
