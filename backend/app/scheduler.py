from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from .config import get_settings
from .database import AsyncSessionMaker
from .models import FeedItem, StoryVersion
from .rss_client import fetch_all
from .story_service import generate_next_story_version

logger = logging.getLogger(__name__)
settings = get_settings()


async def ingest_feeds() -> None:
    items = fetch_all(settings.feeds)
    if not items:
        logger.info("No items fetched from RSS")
        return
    async with AsyncSessionMaker() as session:
        for item in items:
            exists = await session.execute(
                select(FeedItem).where(FeedItem.hash == item["hash"])
            )
            if exists.scalar_one_or_none():
                continue
            session.add(FeedItem(**item))
        await session.commit()
    logger.info("Ingested %s new feed items", len(items))


async def maybe_generate_story() -> None:
    async with AsyncSessionMaker() as session:
        result = await session.execute(
            select(StoryVersion).order_by(StoryVersion.created_at.desc()).limit(1)
        )
        latest = result.scalar_one_or_none()
        if latest:
            logger.info("Latest story version %s at %s", latest.id, latest.created_at)
    async with AsyncSessionMaker() as session:
        await generate_next_story_version(session)


async def scheduled_job() -> None:
    logger.info("Scheduler tick at %s", datetime.now(timezone.utc))
    await ingest_feeds()
    await maybe_generate_story()


def start_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduled_job, "interval", minutes=settings.singl_update_minutes)
    scheduler.start()
    logger.info("Scheduler started with %s minute interval", settings.singl_update_minutes)
    return scheduler


async def bootstrap_once() -> None:
    await scheduled_job()
