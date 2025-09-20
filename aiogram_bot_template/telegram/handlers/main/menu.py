from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import TelegramObject
from aiogram_i18n import I18nContext

from aiogram_bot_template.telegram.keyboards.callback_data.menu import CDDeposit, CDMenu
from aiogram_bot_template.telegram.keyboards.common import back_keyboard
from aiogram_bot_template.telegram.keyboards.menu import deposit_keyboard

if TYPE_CHECKING:
    from aiogram_bot_template.models.dto.user import UserDto
    from aiogram_bot_template.telegram.helpers import MessageHelper

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
@router.callback_query(CDMenu.filter())
async def greeting(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
    user: UserDto,
) -> Any:
    return await helper.answer(
        text=i18n.messages.greeting(name=user.mention),
        reply_markup=deposit_keyboard(i18n=i18n),
    )


@router.callback_query(CDDeposit.filter())
async def answer_deposit(
    _: TelegramObject,
    helper: MessageHelper,
    i18n: I18nContext,
) -> Any:
    return await helper.answer(
        text=i18n.messages.deposit(),
        reply_markup=back_keyboard(i18n=i18n),
    )
