from pydantic import BaseModel, ConfigDict, model_validator


class ReviewTaskBase(BaseModel):
    hotspot_id: int | None = None
    topic_candidate_id: int | None = None
    copy_variant_id: int | None = None
    reviewer: str | None = None
    review_notes: str | None = None


class ReviewTaskCreate(ReviewTaskBase):
    @model_validator(mode="after")
    def validate_reference(self) -> "ReviewTaskCreate":
        if self.hotspot_id is None and self.topic_candidate_id is None and self.copy_variant_id is None:
            raise ValueError("hotspot_id, topic_candidate_id, copy_variant_id 至少传一个")
        return self


class ReviewTaskRead(ReviewTaskBase):
    id: int
    review_status: str

    model_config = ConfigDict(from_attributes=True)


class ReviewTaskAction(BaseModel):
    reviewer: str | None = None
    review_notes: str | None = None
