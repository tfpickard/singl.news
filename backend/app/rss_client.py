from __future__ import annotations

import hashlib
import logging
from datetime import datetime, timezone
from typing import Any

import feedparser

logger = logging.getLogger(__name__)


def _hash_entry(entry: Any) -> str:
    payload = "|".join(
        [
            getattr(entry, "id", ""),
            getattr(entry, "guid", ""),
            getattr(entry, "link", ""),
            getattr(entry, "title", ""),
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def normalize_entry(feed_url: str, entry: Any) -> dict[str, Any]:
    published_parsed = getattr(entry, "published_parsed", None)
    published_at = (
        datetime(*published_parsed[:6], tzinfo=timezone.utc)
        if published_parsed
        else None
    )
    return {
        "feed_url": feed_url,
        "title": getattr(entry, "title", "Untitled"),
        "summary": getattr(entry, "summary", None),
        "link": getattr(entry, "link", ""),
        "published_at": published_at,
        "hash": _hash_entry(entry),
        "raw": {k: getattr(entry, k) for k in entry.keys()},
    }


def fetch_feed(feed_url: str) -> list[dict[str, Any]]:
    logger.debug("Fetching feed %s", feed_url)
    feed = feedparser.parse(feed_url)
    if feed.bozo:
        logger.warning("Feed %s raised parsing error: %s", feed_url, feed.bozo_exception)
        return []
    normalized = [normalize_entry(feed_url, entry) for entry in feed.entries]
    logger.info("Fetched %s entries from %s", len(normalized), feed_url)
    return normalized


def fetch_all(feeds: list[str]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for feed_url in feeds:
        try:
            items.extend(fetch_feed(feed_url))
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.exception("Failed to fetch feed %s: %s", feed_url, exc)
    return items
