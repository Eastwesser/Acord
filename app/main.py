import logging
from datetime import (
    datetime,
    timedelta,
)
from typing import (
    List,
    Optional,
)

import jwt
from fastapi import (
    WebSocket,
    WebSocketDisconnect,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from starlette.responses import RedirectResponse

from app.api_v1 import (
    text_chat,
    voice_chat,
)
from app.core.config import (
    create_app,
    Settings,
)
from app.services.webrtc_handler import WebRTCHandler

app = create_app()
settings = Settings()  # Загружаем настройки

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация JWT
SECRET_KEY = settings.secret_key  # Используем секретный ключ из настроек
ALGORITHM = settings.algorithm  # Используем алгоритм из настроек
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes  # Используем время истечения токена из настроек

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"Клиент подключен: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"Клиент отключен: {websocket.client}")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения клиенту {connection.client}: {e}")


manager = ConnectionManager()


@app.websocket("/ws/text")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} отключился.")
    except Exception as e:
        logger.error(f"Ошибка при обработке текста от {username}: {e}")


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "user" and form_data.password == "password":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


app.include_router(text_chat.router)
app.include_router(voice_chat.router)


@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/html/index.html")


clients = []


@app.websocket("/ws/voice")
async def websocket_voice_endpoint(websocket: WebSocket, token: str = Depends(oauth2_scheme)):
    username = verify_token(token)

    await WebRTCHandler.connect(websocket, clients)

    try:
        while True:
            data = await websocket.receive_json()
            await WebRTCHandler.handle_message(data, websocket, clients)
    except WebSocketDisconnect:
        await WebRTCHandler.handle_disconnect(websocket, clients)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
