from __future__ import annotations

from typing import Sequence
import os

DEFAULT_CONTEXT_STEPS = int(os.getenv("SINGL_CONTEXT_STEPS", "10"))


def build_context(versions: Sequence, context_steps: int | None = None) -> tuple[str, str]:
    steps = context_steps or DEFAULT_CONTEXT_STEPS
    if not versions:
        return "", ""
    recent = versions[-steps:]
    head = versions[: len(versions) - len(recent)]
    context_summary = "\n".join(getattr(v, "summary", "") for v in head[-5:]) if head else ""
    excerpt = "\n\n".join(getattr(v, "full_text", "") for v in recent)
    return context_summary, excerpt


def build_feed_digest(feed_items: Sequence) -> str:
    if not feed_items:
        return "No new verifiable developments were observed in monitored sources."
    lines = []
    for item in feed_items:
        title = getattr(item, "title", "Untitled")
        feed_url = getattr(item, "feed_url", "")
        summary = getattr(item, "summary", "") or ""
        lines.append(f"- {title} ({feed_url})\n  {summary[:240]}")
    return "\n".join(lines)
