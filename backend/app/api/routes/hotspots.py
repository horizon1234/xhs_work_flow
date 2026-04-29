from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.hotspot import Hotspot
from app.models.topic_candidate import TopicCandidate
from app.schemas.hotspot import HotspotCreate, HotspotRead
from app.schemas.topic_candidate import TopicCandidateRead
from app.services.content_pipeline import build_topic_candidates

router = APIRouter()


@router.get("", response_model=list[HotspotRead])
def list_hotspots(db: Session = Depends(get_db)) -> list[HotspotRead]:
    statement = select(Hotspot).order_by(Hotspot.id.desc())
    return list(db.scalars(statement).all())


@router.post("", response_model=HotspotRead, status_code=201)
def create_hotspot(payload: HotspotCreate, db: Session = Depends(get_db)) -> HotspotRead:
    hotspot = Hotspot(
        source_type=payload.source_type,
        source_url=str(payload.source_url) if payload.source_url else None,
        keyword=payload.keyword,
        raw_title=payload.raw_title,
        raw_content=payload.raw_content,
        summary=payload.raw_content[:120],
        status="collected",
    )
    db.add(hotspot)
    db.commit()
    db.refresh(hotspot)
    return hotspot


@router.get("/{hotspot_id}", response_model=HotspotRead)
def get_hotspot(hotspot_id: int, db: Session = Depends(get_db)) -> HotspotRead:
    hotspot = db.get(Hotspot, hotspot_id)
    if hotspot is not None:
        return hotspot
    raise HTTPException(status_code=404, detail="Hotspot not found")


@router.post("/{hotspot_id}/generate-topics", response_model=list[TopicCandidateRead], status_code=201)
def generate_topics(hotspot_id: int, db: Session = Depends(get_db)) -> list[TopicCandidateRead]:
    hotspot = db.get(Hotspot, hotspot_id)
    if hotspot is None:
        raise HTTPException(status_code=404, detail="Hotspot not found")

    existing_topics = list(
        db.scalars(
            select(TopicCandidate).where(TopicCandidate.hotspot_id == hotspot_id).order_by(TopicCandidate.id.asc())
        ).all()
    )
    if existing_topics:
        return existing_topics

    topics = [TopicCandidate(hotspot_id=hotspot.id, **topic_data) for topic_data in build_topic_candidates(hotspot)]
    db.add_all(topics)
    hotspot.status = "topic_generated"
    db.commit()
    for topic in topics:
        db.refresh(topic)
    return topics


@router.get("/{hotspot_id}/topics", response_model=list[TopicCandidateRead])
def list_hotspot_topics(hotspot_id: int, db: Session = Depends(get_db)) -> list[TopicCandidateRead]:
    hotspot = db.get(Hotspot, hotspot_id)
    if hotspot is None:
        raise HTTPException(status_code=404, detail="Hotspot not found")

    statement = select(TopicCandidate).where(TopicCandidate.hotspot_id == hotspot_id).order_by(TopicCandidate.id.asc())
    return list(db.scalars(statement).all())
