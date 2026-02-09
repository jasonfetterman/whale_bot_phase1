from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.keyboards.main_menu import get_main_menu
from services.typing import typing
from services.user_tiers import get_tier, set_tier

router = Router()


async def show_main_menu(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer(
        "🐋 Whaler X is live\n\nChoose an option below 👇",
        reply_markup=get_main_menu(),
    )


@router.message(Command("start"))
async def start_cmd(message: Message):
    user_id = message.from_user.id
    tier = await get_tier(user_id)
    if tier == "free":
        await set_tier(user_id, "free")

        await message.answer(
            "👋 Welcome to Whaler X\n\n"
            "You’ll receive whale alerts when large transactions hit the chain.\n\n"
            "Alerts are enabled automatically."
        )

    await show_main_menu(message)


@router.message(F.text == "⬅ Back to Menu")
async def back_to_menu(message: Message):
    await show_main_menu(message)
