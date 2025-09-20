from aiogram import Bot, Dispatcher

from aiogram_bot_template.factory import create_app_config, create_bot, create_dispatcher
from aiogram_bot_template.models.config import AppConfig
from aiogram_bot_template.runners.app import run_polling, run_webhook
from aiogram_bot_template.utils.logging import setup_logger


def main() -> None:
    setup_logger()
    config: AppConfig = create_app_config()
    bot: Bot = create_bot(config=config)
    dispatcher: Dispatcher = create_dispatcher(config=config)
    if config.telegram.use_webhook:
        return run_webhook(dispatcher=dispatcher, bot=bot, config=config)
    return run_polling(dispatcher=dispatcher, bot=bot, config=config)


if __name__ == "__main__":
    main()
