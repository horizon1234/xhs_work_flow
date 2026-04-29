from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.copy_variant import CopyVariant
from app.models.hotspot import Hotspot
from app.models.topic_candidate import TopicCandidate
from app.schemas.copy_variant import CopyVariantRead
from app.services.content_pipeline import build_copy_variants

router = APIRouter()


@router.post("/{topic_id}/generate-copy", response_model=list[CopyVariantRead], status_code=201)
def generate_copy(topic_id: int, db: Session = Depends(get_db)) -> list[CopyVariantRead]:
    topic = db.get(TopicCandidate, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")

    existing_variants = list(
        db.scalars(
            select(CopyVariant).where(CopyVariant.topic_candidate_id == topic_id).order_by(CopyVariant.id.asc())
        ).all()
    )
    if existing_variants:
        return existing_variants

    hotspot = db.get(Hotspot, topic.hotspot_id)
    if hotspot is None:
        raise HTTPException(status_code=404, detail="Hotspot not found")

    copy_variants = [
        CopyVariant(topic_candidate_id=topic.id, **copy_data) for copy_data in build_copy_variants(topic, hotspot)
    ]
    db.add_all(copy_variants)
    topic.status = "copy_generated"
    hotspot.status = "copy_generated"
    db.commit()
    for copy_variant in copy_variants:
        db.refresh(copy_variant)
    return copy_variants


@router.get("/{topic_id}/copy-variants", response_model=list[CopyVariantRead])
def list_copy_variants(topic_id: int, db: Session = Depends(get_db)) -> list[CopyVariantRead]:
    topic = db.get(TopicCandidate, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")

    statement = select(CopyVariant).where(CopyVariant.topic_candidate_id == topic_id).order_by(CopyVariant.id.asc())
    return list(db.scalars(statement).all())