# Файл app/api/voice_chat.py
# Здесь будет обработка голосового чата через WebSocket,
# а WebRTC логика будет вынесена в отдельный модуль.

from fastapi import APIRouter, WebSocket

from app.services.webrtc_handler import WebRTCHandler

router = APIRouter()

voice_clients = []


@router.websocket("/ws/voice")
async def websocket_voice_chat(websocket: WebSocket):
    await WebRTCHandler.connect(websocket, voice_clients)
    try:
        while True:
            data = await websocket.receive_text()
            await WebRTCHandler.handle_message(data, websocket, voice_clients)
    except Exception as e:
        await WebRTCHandler.handle_disconnect(websocket, voice_clients, e)
