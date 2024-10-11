from app.api_auth_v1 import text_chat, voice_chat
from app.core.config import create_app

app = create_app()

# Подключение маршрутов
app.include_router(text_chat.router)
app.include_router(voice_chat.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
