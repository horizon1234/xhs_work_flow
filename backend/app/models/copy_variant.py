from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CopyVariant(Base):
    __tablename__ = "copy_variants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    topic_candidate_id: Mapped[int] = mapped_column(ForeignKey("topic_candidates.id"), index=True)
    model_name: Mapped[str] = mapped_column(String(100), default="mock-llm")
    prompt_version: Mapped[str] = mapped_column(String(50), default="v1")
    title: Mapped[str] = mapped_column(String(255))
    hook: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    hashtags: Mapped[list[str]] = mapped_column(JSON, default=list)
    cover_text: Mapped[str] = mapped_column(String(255))
    comment_hint: Mapped[str] = mapped_column(String(255))
    risk_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="copy_generated")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    topic_candidate = relationship("TopicCandidate", back_populates="copy_variants")
    review_tasks = relationship("ReviewTask", back_populates="copy_variant")