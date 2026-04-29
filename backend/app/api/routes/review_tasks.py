from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.copy_variant import CopyVariant
from app.models.hotspot import Hotspot
from app.models.review_task import ReviewTask
from app.models.topic_candidate import TopicCandidate
from app.schemas.review_task import ReviewTaskAction, ReviewTaskCreate, ReviewTaskRead

router = APIRouter()


def _apply_review_status(review_task: ReviewTask, status: str, payload: ReviewTaskAction, db: Session) -> ReviewTask:
    if review_task.review_status == status:
        raise HTTPException(status_code=409, detail=f"Review task already {status}")
    if review_task.review_status not in {"pending_review", "rejected", "approved"}:
        raise HTTPException(status_code=400, detail="Review task status transition is not allowed")

    review_task.review_status = status
    review_task.reviewer = payload.reviewer or review_task.reviewer
    review_task.review_notes = payload.review_notes

    hotspot = db.get(Hotspot, review_task.hotspot_id)
    topic_candidate = (
        db.get(TopicCandidate, review_task.topic_candidate_id)
        if review_task.topic_candidate_id is not None
        else None
    )
    copy_variant = db.get(CopyVariant, review_task.copy_variant_id) if review_task.copy_variant_id is not None else None

    if hotspot is not None:
        hotspot.status = status
    if topic_candidate is not None:
        topic_candidate.status = status
    if copy_variant is not None:
        copy_variant.status = status

    db.commit()
    db.refresh(review_task)
    return review_task


@router.get("", response_model=list[ReviewTaskRead])
def list_review_tasks(db: Session = Depends(get_db)) -> list[ReviewTaskRead]:
    statement = select(ReviewTask).order_by(ReviewTask.id.desc())
    return list(db.scalars(statement).all())


@router.post("", response_model=ReviewTaskRead, status_code=201)
def create_review_task(payload: ReviewTaskCreate, db: Session = Depends(get_db)) -> ReviewTaskRead:
    hotspot: Hotspot | None = None
    topic_candidate: TopicCandidate | None = None
    copy_variant: CopyVariant | None = None

    resolved_hotspot_id = payload.hotspot_id
    resolved_topic_candidate_id = payload.topic_candidate_id

    if payload.copy_variant_id is not None:
        copy_variant = db.get(CopyVariant, payload.copy_variant_id)
        if copy_variant is None:
            raise HTTPException(status_code=404, detail="Copy variant not found")
        resolved_topic_candidate_id = copy_variant.topic_candidate_id

    if resolved_topic_candidate_id is not None:
        topic_candidate = db.get(TopicCandidate, resolved_topic_candidate_id)
        if topic_candidate is None:
            raise HTTPException(status_code=404, detail="Topic candidate not found")
        resolved_hotspot_id = topic_candidate.hotspot_id

    if resolved_hotspot_id is None:
        raise HTTPException(status_code=400, detail="Unable to resolve hotspot for review task")

    hotspot = db.get(Hotspot, resolved_hotspot_id)
    if hotspot is None:
        raise HTTPException(status_code=404, detail="Hotspot not found")

    review_task = ReviewTask(
        hotspot_id=resolved_hotspot_id,
        topic_candidate_id=resolved_topic_candidate_id,
        copy_variant_id=payload.copy_variant_id,
        review_status="pending_review",
        reviewer=payload.reviewer,
        review_notes=payload.review_notes,
    )
    db.add(review_task)

    hotspot.status = "pending_review"
    if topic_candidate is not None:
        topic_candidate.status = "pending_review"
    if copy_variant is not None:
        copy_variant.status = "pending_review"

    db.commit()
    db.refresh(review_task)
    return review_task


@router.get("/{review_task_id}", response_model=ReviewTaskRead)
def get_review_task(review_task_id: int, db: Session = Depends(get_db)) -> ReviewTaskRead:
    review_task = db.get(ReviewTask, review_task_id)
    if review_task is not None:
        return review_task
    raise HTTPException(status_code=404, detail="Review task not found")


@router.post("/{review_task_id}/approve", response_model=ReviewTaskRead)
def approve_review_task(
    review_task_id: int, payload: ReviewTaskAction, db: Session = Depends(get_db)
) -> ReviewTaskRead:
    review_task = db.get(ReviewTask, review_task_id)
    if review_task is None:
        raise HTTPException(status_code=404, detail="Review task not found")
    return _apply_review_status(review_task, "approved", payload, db)


@router.post("/{review_task_id}/reject", response_model=ReviewTaskRead)
def reject_review_task(
    review_task_id: int, payload: ReviewTaskAction, db: Session = Depends(get_db)
) -> ReviewTaskRead:
    review_task = db.get(ReviewTask, review_task_id)
    if review_task is None:
        raise HTTPException(status_code=404, detail="Review task not found")
    return _apply_review_status(review_task, "rejected", payload, db)
