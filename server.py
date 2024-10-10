from typing import List

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/html", StaticFiles(directory="html"), name="html")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")

# Списки для хранения активных клиентов текстового и голосового чатов
text_clients: List[WebSocket] = []
voice_clients: List[WebSocket] = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")


# WebSocket для текстового чата
@app.websocket("/ws/text")
async def websocket_text_chat(websocket: WebSocket):
    await websocket.accept()
    text_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in text_clients:
                if client != websocket:
                    await client.send_text(f"Кто-то написал: {data}")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        text_clients.remove(websocket)


# WebSocket для голосового чата
@app.websocket("/ws/voice")
async def websocket_voice_chat(websocket: WebSocket):
    await websocket.accept()
    voice_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # Можно заменить на .receive_json()
            # Обработка сообщений для WebRTC
            for client in voice_clients:
                if client != websocket:
                    await client.send_text(data)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        voice_clients.remove(websocket)
