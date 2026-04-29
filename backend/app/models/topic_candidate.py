from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TopicCandidate(Base):
    __tablename__ = "topic_candidates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hotspot_id: Mapped[int] = mapped_column(ForeignKey("hotspots.id"), index=True)
    angle_type: Mapped[str] = mapped_column(String(50))
    title_hint: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    audience: Mapped[str] = mapped_column(String(255))
    relevance_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="topic_generated")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    hotspot = relationship("Hotspot", back_populates="topic_candidates")
    copy_variants = relationship("CopyVariant", back_populates="topic_candidate", cascade="all, delete-orphan")
    review_tasks = relationship("ReviewTask", back_populates="topic_candidate")