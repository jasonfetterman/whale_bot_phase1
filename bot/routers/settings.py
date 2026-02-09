from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from config.settings import settings
from bot.keyboards.main_menu import get_main_menu
from services.typing import typing
from services.thresholds import get_for_user, set_for_user

router = Router()


def settings_keyboard(is_owner: bool) -> ReplyKeyboardMarkup:
    rows = []
    if is_owner:
        rows.extend([
            [KeyboardButton(text="➕ ETH Threshold")],
            [KeyboardButton(text="➖ ETH Threshold")],
        ])
    rows.append([KeyboardButton(text="⬅ Back to Menu")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


@router.message(F.text == "⚙ Settings")
async def settings_menu(message: Message):
    await typing(message.bot, message.chat.id)

    user_id = message.from_user.id
    is_owner = user_id == settings.OWNER_CHAT_ID
    eth = await get_for_user("eth", user_id, settings.ETH_WHALE_THRESHOLD)

    await message.answer(
        "⚙ Settings\n\n"
        f"• ETH whale threshold: {eth} ETH\n\n"
        "Use buttons below to adjust.",
        reply_markup=settings_keyboard(is_owner),
    )


@router.message(F.text == "➕ ETH Threshold")
async def eth_up(message: Message):
    if message.from_user.id != settings.OWNER_CHAT_ID:
        return
    current = await get_for_user("eth", message.from_user.id, settings.ETH_WHALE_THRESHOLD)
    await set_for_user("eth", message.from_user.id, current + 10)
    await settings_menu(message)


@router.message(F.text == "➖ ETH Threshold")
async def eth_down(message: Message):
    if message.from_user.id != settings.OWNER_CHAT_ID:
        return
    current = await get_for_user("eth", message.from_user.id, settings.ETH_WHALE_THRESHOLD)
    await set_for_user("eth", message.from_user.id, max(10, current - 10))
    await settings_menu(message)


@router.message(F.text == "⬅ Back to Menu")
async def back_to_menu(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer("⬇️ Main Menu", reply_markup=get_main_menu())
