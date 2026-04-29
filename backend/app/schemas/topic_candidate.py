from pydantic import BaseModel, ConfigDict


class TopicCandidateRead(BaseModel):
    id: int
    hotspot_id: int
    angle_type: str
    title_hint: str
    description: str
    audience: str
    relevance_score: float
    risk_score: float
    status: str

    model_config = ConfigDict(from_attributes=True)