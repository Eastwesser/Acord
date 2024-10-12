# app/core/config.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


def create_app() -> FastAPI:
    app = FastAPI()

    # Загрузка настроек
    settings = Settings()

    # CORS настройки
    setup_cors(app)

    # Настройка статических файлов
    setup_static_files(app)

    return app


def setup_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_static_files(app: FastAPI):
    app.mount("/html", StaticFiles(directory="html"), name="html")
    app.mount("/css", StaticFiles(directory="css"), name="css")
    app.mount("/js", StaticFiles(directory="js"), name="js")
