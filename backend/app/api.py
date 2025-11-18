from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import get_settings
from .database import get_session
from .models import StoryVersion
from .schemas import MetaResponse, StoryHistoryItem, StoryVersionDetail

router = APIRouter(prefix="/api", tags=["story"])
settings = get_settings()


@router.get("/story/current", response_model=StoryVersionDetail)
async def get_current_story(session: AsyncSession = Depends(get_session)) -> StoryVersion:
    result = await session.execute(
        select(StoryVersion).order_by(StoryVersion.created_at.desc()).limit(1)
    )
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=404, detail="No story available")
    return story


@router.get("/story/history", response_model=list[StoryHistoryItem])
async def get_history(
    limit: int = 20,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
) -> list[StoryHistoryItem]:
    stmt = (
        select(StoryVersion)
        .order_by(StoryVersion.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    stories = (await session.execute(stmt)).scalars().all()
    return [
        StoryHistoryItem(
            id=story.id,
            created_at=story.created_at,
            summary=story.summary,
            full_text=story.full_text,
            preview=story.full_text[:200],
        )
        for story in stories
    ]


@router.get("/story/{story_id}", response_model=StoryVersionDetail)
async def get_story(story_id: int, session: AsyncSession = Depends(get_session)) -> StoryVersion:
    story = await session.get(StoryVersion, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.get("/meta", response_model=MetaResponse)
async def get_meta(session: AsyncSession = Depends(get_session)) -> MetaResponse:
    last_story = await session.execute(
        select(StoryVersion).order_by(StoryVersion.created_at.desc()).limit(1)
    )
    last = last_story.scalar_one_or_none()
    count = await session.execute(select(func.count()).select_from(StoryVersion))
    total = count.scalar() or 0
    return MetaResponse(
        feeds=settings.feeds,
        update_minutes=settings.singl_update_minutes,
        context_steps=settings.singl_context_steps,
        last_update=last.created_at if last else None,
        story_count=total,
    )


@router.get("/health")
async def health(session: AsyncSession = Depends(get_session)) -> dict[str, str | int]:
    result = await session.execute(
        select(func.count()).select_from(StoryVersion)
    )
    count = result.scalar() or 0
    return {"status": "ok", "stories": count}
