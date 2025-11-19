from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router as api_router
from .config import get_settings
from .database import Base, engine
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


async def init_db() -> None:
    """Ensure the database schema exists before the app starts serving."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()
    # Run one scheduler cycle so a freshly started stack has an initial story
    # and feed ingest before serving traffic. This prevents 404s on
    # /api/story/current while waiting for the interval job to fire.
    await bootstrap_once()
    start_scheduler()
