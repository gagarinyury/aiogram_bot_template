from __future__ import annotations

import asyncio
import signal
from functools import partial
from typing import TYPE_CHECKING, Any

import uvicorn
from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from uvicorn import server

from aiogram_bot_template.endpoints.telegram import TelegramRequestHandler
from aiogram_bot_template.factory.telegram import setup_fastapi
from aiogram_bot_template.runners.lifespan import emit_aiogram_shutdown
from aiogram_bot_template.runners.polling import polling_lifespan, polling_startup
from aiogram_bot_template.runners.webhook import webhook_shutdown, webhook_startup

if TYPE_CHECKING:
    from aiogram_bot_template.models.config import AppConfig


# noinspection PyProtectedMember
def handle_sigterm(*_: Any, app: FastAPI) -> None:
    if app.state.is_polling:
        app.state.dispatcher._signal_stop_polling(sig=signal.SIGTERM)
        app.state.shutdown_completed = True
    else:
        asyncio.create_task(emit_aiogram_shutdown(app=app))


def run_app(app: FastAPI, config: AppConfig) -> None:
    server.HANDLED_SIGNALS = (signal.SIGINT,)  # type: ignore
    signal.signal(signal.SIGTERM, partial(handle_sigterm, app=app))
    return uvicorn.run(
        app=app,
        host=config.server.host,
        port=config.server.port,
        access_log=False,
    )


def run_polling(dispatcher: Dispatcher, bot: Bot, config: AppConfig) -> None:
    dispatcher.workflow_data.update(is_polling=True)
    app: FastAPI = FastAPI(lifespan=polling_lifespan)
    setup_fastapi(app=app, bot=bot, dispatcher=dispatcher)
    dispatcher.startup.register(polling_startup)
    return run_app(app=app, config=config)


def run_webhook(dispatcher: Dispatcher, bot: Bot, config: AppConfig) -> None:
    dispatcher.workflow_data.update(is_polling=False)
    app: FastAPI = FastAPI()
    setup_fastapi(app=app, bot=bot, dispatcher=dispatcher)
    handler: TelegramRequestHandler = TelegramRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        path=config.telegram.webhook_path,
        secret_token=config.telegram.webhook_secret.get_secret_value(),
    )
    app.state.tg_webhook_handler = handler
    app.include_router(handler.router)
    dispatcher.startup.register(webhook_startup)
    dispatcher.shutdown.register(webhook_shutdown)
    dispatcher.workflow_data.update(app=app)
    return run_app(app=app, config=config)
