from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config

from .config import get_settings

BASE_DIR = Path(__file__).resolve().parents[1]


def sync_database_url(database_url: str) -> str:
    """Translate async SQLAlchemy URLs to sync variants for Alembic."""

    if database_url.startswith("postgresql+asyncpg://"):
        return database_url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
    if database_url.startswith("sqlite+aiosqlite://"):
        return database_url.replace("+aiosqlite", "", 1)
    return database_url


def run_migrations() -> None:
    """Apply the latest Alembic migrations using the configured database URL."""

    settings = get_settings()
    config = Config(str(BASE_DIR / "alembic.ini"))
    config.set_main_option("script_location", str(BASE_DIR / "alembic"))
    config.set_main_option("sqlalchemy.url", sync_database_url(settings.database_url))
    command.upgrade(config, "head")
