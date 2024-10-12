# app/api_v1/voice_chat.py

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
        await WebRTCHandler.handle_disconnect(websocket, voice_clients)
