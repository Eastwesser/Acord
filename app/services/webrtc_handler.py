# Файл app/services/webrtc_handler.py
# Здесь будет храниться логика для обработки WebRTC сообщений и кандидатов ICE.

from typing import List

from fastapi import WebSocket


class WebRTCHandler:

    @staticmethod
    async def connect(websocket: WebSocket, clients: List[WebSocket]):
        await websocket.accept()
        clients.append(websocket)
        print(f"Client {websocket} connected to voice chat.")

    @staticmethod
    async def handle_message(data: str, websocket: WebSocket, clients: List[WebSocket]):
        message = await websocket.receive_json()

        if message["type"] == "offer" or message["type"] == "answer":
            # Отправляем оффер или ответ всем остальным клиентам
            for client in clients:
                if client != websocket:
                    await client.send_json(message)
        elif message["type"] == "ice-candidate":
            # Отправляем кандидата ICE всем остальным клиентам
            for client in clients:
                if client != websocket:
                    await client.send_json(message)

    @staticmethod
    async def handle_disconnect(websocket: WebSocket, clients: List[WebSocket], error: Exception):
        clients.remove(websocket)
        print(f"Client {websocket} disconnected from voice chat. Error: {error}")
