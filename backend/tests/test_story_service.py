from __future__ import annotations

from datetime import datetime, timezone

from app.narrative import build_feed_digest, build_context


class Dummy:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def make_story(idx: int):
    return Dummy(
        id=idx,
        created_at=datetime.now(timezone.utc),
        full_text=f"Story body {idx}",
        summary=f"Summary {idx}",
    )


def test_build_context_truncates_history():
    versions = [make_story(i) for i in range(15)]
    context, excerpt = build_context(versions)
    assert "Summary 0" in context
    assert "Story body 14" in excerpt


def test_feed_digest_handles_empty():
    digest = build_feed_digest([])
    assert "No new verifiable" in digest


def test_feed_digest_formats_items():
    items = [
        Dummy(
            id=1,
            feed_url="http://example.com",
            title="Headline",
            summary="Details",
        )
    ]
    digest = build_feed_digest(items)
    assert "Headline" in digest
