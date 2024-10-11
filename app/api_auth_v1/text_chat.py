# app/api_auth_v1/text_chat.py

import json
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))


manager = ConnectionManager()


@router.websocket("/ws/text")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received data: {data}")  # Логируем входящие данные

            if not data:
                await websocket.send_text(json.dumps({"error": "Empty message"}))
                continue

            # Проверка, является ли data валидным JSON
            try:
                message_data = json.loads(data)  # Парсим JSON
            except json.JSONDecodeError:
                # Если это не JSON, создаем сообщение в формате JSON
                message_data = {"text": data}  # Создаем JSON-объект с текстом

            text_message = message_data.get("text")  # Получаем текст из сообщения

            if text_message:
                await manager.broadcast({"text": text_message})  # Отправляем сообщение всем клиентам
            else:
                await websocket.send_text(json.dumps({"error": "Invalid message format"}))  # Отправляем ошибку

    except WebSocketDisconnect:
        manager.disconnect(websocket)
