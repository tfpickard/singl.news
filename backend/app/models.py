from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


JSONType = JSONB().with_variant(JSON(), "sqlite")


class StoryVersion(Base):
    __tablename__ = "story_versions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    full_text: Mapped[str] = mapped_column(Text(), nullable=False)
    summary: Mapped[str] = mapped_column(Text(), nullable=False)
    context_summary: Mapped[str | None] = mapped_column(Text())
    sources_snapshot: Mapped[dict | None] = mapped_column(JSONType)
    token_stats: Mapped[dict | None] = mapped_column(JSONType)

    feed_items: Mapped[list["FeedItem"]] = relationship(
        back_populates="story_version", cascade="all, delete-orphan"
    )


class FeedItem(Base):
    __tablename__ = "feed_items"
    __table_args__ = (UniqueConstraint("hash", name="uq_feed_items_hash"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    feed_url: Mapped[str] = mapped_column(String(512), nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text())
    link: Mapped[str] = mapped_column(String(512), nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    hash: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    raw: Mapped[dict | None] = mapped_column(JSONType)
    story_version_id: Mapped[int | None] = mapped_column(
        ForeignKey("story_versions.id", ondelete="SET NULL"), nullable=True
    )

    story_version: Mapped[StoryVersion | None] = relationship(back_populates="feed_items")
