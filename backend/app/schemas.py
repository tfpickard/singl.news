from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class StoryVersionBase(BaseModel):
    id: int
    created_at: datetime
    summary: str

    class Config:
        from_attributes = True


class StoryVersionDetail(StoryVersionBase):
    full_text: str
    context_summary: str | None
    sources_snapshot: dict | None


class StoryHistoryItem(StoryVersionBase):
    preview: str


class FeedItemSchema(BaseModel):
    id: int
    feed_url: str
    title: str
    link: str
    summary: str | None
    published_at: datetime | None

    class Config:
        from_attributes = True


class MetaResponse(BaseModel):
    feeds: list[str]
    update_minutes: int
    context_steps: int
    last_update: datetime | None
    story_count: int
