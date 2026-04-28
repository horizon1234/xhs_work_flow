from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas.hotspot import HotspotCreate, HotspotRead

router = APIRouter()

_hotspots: List[HotspotRead] = []


@router.get("", response_model=list[HotspotRead])
def list_hotspots() -> list[HotspotRead]:
    return _hotspots


@router.post("", response_model=HotspotRead, status_code=201)
def create_hotspot(payload: HotspotCreate) -> HotspotRead:
    hotspot = HotspotRead(
        id=len(_hotspots) + 1,
        source_type=payload.source_type,
        source_url=payload.source_url,
        keyword=payload.keyword,
        raw_title=payload.raw_title,
        raw_content=payload.raw_content,
        status="collected",
    )
    _hotspots.append(hotspot)
    return hotspot


@router.get("/{hotspot_id}", response_model=HotspotRead)
def get_hotspot(hotspot_id: int) -> HotspotRead:
    for hotspot in _hotspots:
        if hotspot.id == hotspot_id:
            return hotspot
    raise HTTPException(status_code=404, detail="Hotspot not found")
