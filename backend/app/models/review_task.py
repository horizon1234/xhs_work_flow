from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ReviewTask(Base):
    __tablename__ = "review_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hotspot_id: Mapped[int] = mapped_column(ForeignKey("hotspots.id"), index=True)
    topic_candidate_id: Mapped[int | None] = mapped_column(ForeignKey("topic_candidates.id"), nullable=True, index=True)
    copy_variant_id: Mapped[int | None] = mapped_column(ForeignKey("copy_variants.id"), nullable=True, index=True)
    reviewer: Mapped[str | None] = mapped_column(String(255), nullable=True)
    review_status: Mapped[str] = mapped_column(String(50), default="pending_review")
    review_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    hotspot = relationship("Hotspot", back_populates="review_tasks")
    topic_candidate = relationship("TopicCandidate", back_populates="review_tasks")
    copy_variant = relationship("CopyVariant", back_populates="review_tasks")