from fastapi import WebSocket, WebSocketDisconnect

from app.api_auth_v1 import text_chat, voice_chat
from app.core.config import create_app

# Используем create_app для создания приложения
app = create_app()

# Подключение маршрутов
app.include_router(text_chat.router)
app.include_router(voice_chat.router)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        if len(self.active_connections) >= 10:
            await websocket.close()  # Закрыть соединение, если превышен лимит
            return
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# WebSocket endpoint
@app.websocket("/ws/{chat_type}")
async def websocket_endpoint(websocket: WebSocket, chat_type: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{chat_type} chat: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
