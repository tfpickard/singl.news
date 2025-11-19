from __future__ import annotations

import pytest

from app.openai_client import StoryModelClient


@pytest.mark.asyncio
async def test_generate_story_falls_back_without_api_key(monkeypatch) -> None:
    init_called = False

    class _SentinelAsyncOpenAI:  # pragma: no cover - sanity guard
        def __init__(self, *args, **kwargs):
            nonlocal init_called
            init_called = True

    monkeypatch.setattr("app.openai_client.AsyncOpenAI", _SentinelAsyncOpenAI)

    client = StoryModelClient()
    assert init_called is False

    text, summary, stats = await client.generate_story(
        [
            {
                "role": "user",
                "content": "Story: The newsroom is waiting for an update.",
            }
        ]
    )

    assert "newsroom" in text
    assert summary
    assert stats == {"mode": "fallback"}
