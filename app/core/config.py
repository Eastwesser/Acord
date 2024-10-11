# app/core/config.py
# Этот файл будет содержать настройки для приложения, такие как CORS-политики,
# настройки статических файлов и другие глобальные конфигурации.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


def create_app() -> FastAPI:
    app = FastAPI()

    # CORS настройки
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Настройка статических файлов
    app.mount("/html", StaticFiles(directory="html"), name="html")
    app.mount("/css", StaticFiles(directory="css"), name="css")
    app.mount("/js", StaticFiles(directory="js"), name="js")

    return app
