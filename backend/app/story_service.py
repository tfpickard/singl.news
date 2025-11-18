from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import get_settings
from .models import FeedItem, StoryVersion
from .openai_client import model_client
from .ws import broadcast_story
from .narrative import build_context, build_feed_digest

logger = logging.getLogger(__name__)
settings = get_settings()


def build_context(versions: Sequence[StoryVersion]) -> tuple[str, str]:
    if not versions:
        return "", ""
    recent = versions[-settings.singl_context_steps :]
    head = versions[: len(versions) - len(recent)]
    context_summary = "\n".join(v.summary for v in head[-5:]) if head else ""
    excerpt = "\n\n".join(v.full_text for v in recent)
    return context_summary, excerpt


def build_feed_digest(feed_items: Sequence[FeedItem]) -> str:
    if not feed_items:
        return "No new verifiable developments were observed in monitored sources."
    lines = []
    for item in feed_items:
        summary = item.summary or ""
        lines.append(f"- {item.title} ({item.feed_url})\n  {summary[:240]}")
    return "\n".join(lines)


async def generate_next_story_version(session: AsyncSession) -> StoryVersion | None:
    result = await session.execute(
        select(StoryVersion).order_by(StoryVersion.created_at.desc()).limit(50)
    )
    versions = list(reversed(result.scalars().all()))
    context_summary, excerpt = build_context(versions, settings.singl_context_steps)

    feed_stmt = select(FeedItem).where(FeedItem.story_version_id.is_(None)).order_by(
        FeedItem.published_at.desc()
    )
    feed_items = (await session.execute(feed_stmt)).scalars().all()

    if not feed_items and versions:
        latest = versions[-1]
        if latest.created_at >= datetime.now(timezone.utc) - timedelta(
            minutes=settings.singl_minimum_update_minutes
        ):
            logger.info("Skipping story generation; no new feeds and within quiet window")
            return None

    logger.info("Generating next story version using %s feed items", len(feed_items))
    feed_digest = build_feed_digest(feed_items)

    base_prompt = (
        "You are the global continuity desk for Singl News. Maintain a single story, "
        "never restarting. Fold new reports into the existing narrative with a "
        "serious news tone."
    )
    user_prompt = f"Context summary:\n{context_summary}\n\nRecent chapters:\n{excerpt}\n\nNew source briefings:\n{feed_digest}\n\nWrite the next chapter of the single global story, labeled 'Story:'"

    messages = [
        {"role": "system", "content": base_prompt},
        {"role": "user", "content": user_prompt},
    ]

    full_text, summary, token_stats = await model_client.generate_story(messages)
    if not full_text:
        logger.warning("Model returned empty story; aborting")
        return None

    created_at = datetime.now(timezone.utc)
    story = StoryVersion(
        created_at=created_at,
        full_text=full_text.strip(),
        summary=summary.strip() or full_text[:200],
        context_summary=context_summary or None,
        sources_snapshot={"feed_count": len(feed_items)},
        token_stats=token_stats,
    )
    session.add(story)
    await session.flush()

    for item in feed_items:
        item.story_version_id = story.id

    await session.commit()
    await broadcast_story(story)
    logger.info("Created story version %s", story.id)
    return story
