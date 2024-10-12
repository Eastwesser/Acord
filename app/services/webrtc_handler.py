# app/services/webrtc_handler.py

from typing import List

from fastapi import WebSocket

from app.services.websocket_handler import WebSocketHandler


class WebRTCHandler:

    @staticmethod
    async def connect(websocket: WebSocket, clients: List[WebSocket]):
        await WebSocketHandler.connect(websocket, clients)

    @staticmethod
    async def handle_message(data: str, websocket: WebSocket, clients: List[WebSocket]):
        # Используем переданные данные напрямую.
        message = data
        for client in clients:
            if client != websocket:
                await client.send_json(message)

    @staticmethod
    async def handle_disconnect(websocket: WebSocket, clients: List[WebSocket]):
        await WebSocketHandler.handle_disconnect(websocket, clients)
