from aiogram_bot_template.errors.base import AppError


class BotError(AppError):
    pass


class UnknownMessageError(BotError):
    pass
