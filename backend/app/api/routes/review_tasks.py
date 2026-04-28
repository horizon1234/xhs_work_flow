from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas.review_task import ReviewTaskCreate, ReviewTaskRead

router = APIRouter()

_review_tasks: List[ReviewTaskRead] = []


@router.get("", response_model=list[ReviewTaskRead])
def list_review_tasks() -> list[ReviewTaskRead]:
    return _review_tasks


@router.post("", response_model=ReviewTaskRead, status_code=201)
def create_review_task(payload: ReviewTaskCreate) -> ReviewTaskRead:
    review_task = ReviewTaskRead(
        id=len(_review_tasks) + 1,
        hotspot_id=payload.hotspot_id,
        copy_variant_id=payload.copy_variant_id,
        review_status="pending_review",
        reviewer=payload.reviewer,
        review_notes=payload.review_notes,
    )
    _review_tasks.append(review_task)
    return review_task


@router.get("/{review_task_id}", response_model=ReviewTaskRead)
def get_review_task(review_task_id: int) -> ReviewTaskRead:
    for review_task in _review_tasks:
        if review_task.id == review_task_id:
            return review_task
    raise HTTPException(status_code=404, detail="Review task not found")
