from __future__ import annotations

import logging

import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router as api_router
from .config import get_settings
from .migration_utils import run_migrations
from .scheduler import bootstrap_once, start_scheduler
from .ws import router as ws_router

settings = get_settings()
logging.basicConfig(level=getattr(logging, settings.singl_log_level.upper(), "INFO"))

app = FastAPI(title="Singl News API", version="0.1.0")

origins = ["*"]
if settings.singl_ws_origin:
    origins = [settings.singl_ws_origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(ws_router)


async def apply_migrations() -> None:
    """Run Alembic migrations in a worker thread before serving traffic."""

    await asyncio.to_thread(run_migrations)


@app.on_event("startup")
async def on_startup() -> None:
    await apply_migrations()
    # Run one scheduler cycle so a freshly started stack has an initial story
    # and feed ingest before serving traffic. This prevents 404s on
    # /api/story/current while waiting for the interval job to fire.
    await bootstrap_once()
    start_scheduler()
