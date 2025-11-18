from __future__ import annotations

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(
        default="sqlite+aiosqlite:///./singl.db", alias="DATABASE_URL"
    )
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    singl_model_name: str = Field(default="gpt-4o-mini", alias="SINGL_MODEL_NAME")
    singl_update_minutes: int = Field(default=30, alias="SINGL_UPDATE_MINUTES")
    singl_context_steps: int = Field(default=10, alias="SINGL_CONTEXT_STEPS")
    singl_feeds: str = Field(
        default=(
            "https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best"
            ",https://feeds.npr.org/1001/rss.xml,https://www.aljazeera.com/xml/rss/all.xml"
        ),
        alias="SINGL_FEEDS",
    )
    singl_log_level: str = Field(default="INFO", alias="SINGL_LOG_LEVEL")
    singl_ws_origin: str | None = Field(default=None, alias="SINGL_WS_ORIGIN")
    singl_minimum_update_minutes: int = Field(
        default=120, alias="SINGL_MINIMUM_UPDATE_MINUTES"
    )

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def feeds(self) -> list[str]:
        return [feed.strip() for feed in self.singl_feeds.split(",") if feed.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
