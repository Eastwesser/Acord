# app/api_v1/text_chat.py

from fastapi import APIRouter, WebSocketDisconnect
from starlette.websockets import WebSocket

from app.services.websocket_handler import WebSocketHandler

router = APIRouter()
clients = []


@router.websocket("/ws/text")
async def websocket_text_chat(websocket: WebSocket):
    await WebSocketHandler.connect(websocket, clients)
    try:
        while True:
            data = await websocket.receive_text()
            await WebSocketHandler.broadcast(data, clients, websocket)
    except WebSocketDisconnect:
        await WebSocketHandler.handle_disconnect(websocket, clients)
