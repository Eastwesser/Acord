from typing import List

from fastapi import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.api_v1 import text_chat, voice_chat
from app.core.config import create_app

app = create_app()

# Подключение CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Позволить всем источникам
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(text_chat.router)
app.include_router(voice_chat.router)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        if len(self.active_connections) >= 3:
            await websocket.close()  # Закрыть соединение, если превышен лимит
            return
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_audio(self, data: bytes):
        for connection in self.active_connections:
            await connection.send_bytes(data)


manager = ConnectionManager()


@app.websocket("/ws/voice")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            audio_data = await websocket.receive_bytes()  # Получаем аудио в виде байтов
            await manager.broadcast_audio(audio_data)  # Пересылаем всем клиентам
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
