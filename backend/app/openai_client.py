from __future__ import annotations

import logging
from typing import Any

from openai import OpenAI

from .config import get_settings

logger = logging.getLogger(__name__)


class StoryModelClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = OpenAI(api_key=self.settings.openai_api_key)

    async def generate_story(self, messages: list[dict[str, str]]) -> tuple[str, str, dict[str, Any]]:
        if not self.settings.openai_api_key:
            logger.warning("OPENAI_API_KEY not provided; using fallback narrative")
            fallback_text = "\n".join(
                [
                    m["content"]
                    for m in messages
                    if m["role"] == "user" and "story:" in m["content"].lower()
                ]
            )
            text = fallback_text or "The global desk acknowledges a quiet interval."  # fallback
            summary = text[:200]
            return text, summary, {"mode": "fallback"}

        response = await self.client.chat.completions.create(  # type: ignore[call-arg]
            model=self.settings.singl_model_name,
            messages=messages,
            temperature=0.7,
        )
        choice = response.choices[0]
        text = choice.message.content or ""
        summary_response = await self.client.chat.completions.create(  # type: ignore[call-arg]
            model=self.settings.singl_model_name,
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the following story in two sentences.",
                },
                {"role": "user", "content": text},
            ],
            temperature=0.3,
        )
        summary = summary_response.choices[0].message.content or ""
        usage = getattr(response, "usage", None)
        return text, summary, usage.model_dump() if hasattr(usage, "model_dump") else {}


model_client = StoryModelClient()
