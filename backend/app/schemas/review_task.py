from pydantic import BaseModel, ConfigDict


class ReviewTaskBase(BaseModel):
    hotspot_id: int
    copy_variant_id: int | None = None
    reviewer: str | None = None
    review_notes: str | None = None


class ReviewTaskCreate(ReviewTaskBase):
    pass


class ReviewTaskRead(ReviewTaskBase):
    id: int
    review_status: str

    model_config = ConfigDict(from_attributes=True)
