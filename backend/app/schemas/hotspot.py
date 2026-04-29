from pydantic import BaseModel, ConfigDict, HttpUrl


class HotspotBase(BaseModel):
    source_type: str
    source_url: HttpUrl | None = None
    keyword: str
    raw_title: str
    raw_content: str


class HotspotCreate(HotspotBase):
    pass


class HotspotRead(HotspotBase):
    id: int
    summary: str | None = None
    status: str

    model_config = ConfigDict(from_attributes=True)
