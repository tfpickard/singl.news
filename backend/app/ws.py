from __future__ import annotations

import json
import logging
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from .database import AsyncSessionMaker
from .models import StoryVersion

logger = logging.getLogger(__name__)
router = APIRouter()


class ConnectionManager:
    def __init__(self) -> None:
        self.active: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active.add(websocket)
        logger.info("WebSocket connected; %s clients", len(self.active))

    def disconnect(self, websocket: WebSocket) -> None:
        self.active.discard(websocket)
        logger.info("WebSocket disconnected; %s clients", len(self.active))

    async def broadcast(self, message: dict[str, Any]) -> None:
        payload = json.dumps(message, default=str)
        for connection in list(self.active):
            try:
                await connection.send_text(payload)
            except Exception:
                self.disconnect(connection)


manager = ConnectionManager()


@router.websocket("/ws/story")
async def story_socket(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    async with AsyncSessionMaker() as session:
        result = await session.execute(
            select(StoryVersion).order_by(StoryVersion.created_at.desc()).limit(1)
        )
        story = result.scalar_one_or_none()
        if story:
            await websocket.send_json(
                {
                    "type": "initial",
                    "story": {
                        "id": story.id,
                        "created_at": story.created_at.isoformat(),
                        "full_text": story.full_text,
                        "summary": story.summary,
                    },
                }
            )
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def broadcast_story(story: StoryVersion) -> None:
    await manager.broadcast(
        {
            "type": "update",
            "story": {
                "id": story.id,
                "created_at": story.created_at.isoformat(),
                "full_text": story.full_text,
                "summary": story.summary,
            },
        }
    )
