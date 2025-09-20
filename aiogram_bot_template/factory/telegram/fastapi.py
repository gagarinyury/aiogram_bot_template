from aiogram import Bot, Dispatcher
from fastapi import FastAPI

from aiogram_bot_template.endpoints import healthcheck


def setup_fastapi(app: FastAPI, dispatcher: Dispatcher, bot: Bot) -> FastAPI:
    app.include_router(healthcheck.router)
    for key, value in dispatcher.workflow_data.items():
        setattr(app.state, key, value)
    app.state.dispatcher = dispatcher
    app.state.bot = bot
    app.state.shutdown_completed = False
    return app
