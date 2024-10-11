# Файл app/api/text_chat.py
# Здесь будет храниться обработка текстового чата через WebSocket.

from typing import List

from fastapi import APIRouter, WebSocket

from app.services.websocket_handler import WebSocketHandler

router = APIRouter()

text_clients: List[WebSocket] = []


@router.websocket("/ws/text")
async def websocket_text_chat(websocket: WebSocket):
    await WebSocketHandler.connect(websocket, text_clients)
    try:
        while True:
            data = await websocket.receive_text()
            await WebSocketHandler.broadcast(data, text_clients, websocket)
    except Exception as e:
        await WebSocketHandler.handle_disconnect(websocket, text_clients, e)
