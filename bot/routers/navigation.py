from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards.main_menu import get_main_menu
from services.typing import typing

router = Router()


@router.message(F.text == "⬅ Back to Menu")
async def back_to_menu(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer(
        "⬇️ Main Menu",
        reply_markup=get_main_menu(),
    )
