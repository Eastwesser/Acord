# Файл app/services/websocket_handler.py
# Этот модуль будет общим для обработки WebSocket соединений.

from typing import List

from fastapi import WebSocket


class WebSocketHandler:

    @staticmethod
    async def connect(websocket: WebSocket, clients: List[WebSocket]):
        await websocket.accept()
        clients.append(websocket)
        print(f"Client {websocket} connected.")

    @staticmethod
    async def broadcast(message: str, clients: List[WebSocket], sender: WebSocket):
        for client in clients:
            if client != sender:
                await client.send_text(f"Кто-то написал: {message}")

    @staticmethod
    async def handle_disconnect(websocket: WebSocket, clients: List[WebSocket]):
        clients.remove(websocket)
        print(f"Client {websocket} disconnected.")
