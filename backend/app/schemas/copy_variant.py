from pydantic import BaseModel, ConfigDict


class CopyVariantRead(BaseModel):
    id: int
    topic_candidate_id: int
    model_name: str
    prompt_version: str
    title: str
    hook: str
    body: str
    hashtags: list[str]
    cover_text: str
    comment_hint: str
    risk_notes: str | None = None
    status: str

    model_config = ConfigDict(from_attributes=True)