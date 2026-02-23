# FILE: bot/routers/upgrade.py
# LOCATION: bot/routers/upgrade.py
# DROP-IN REPLACEMENT

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import os

from services.typing import typing
from services.stripe_payments import create_checkout_session
from services.user_tiers import get_tier
from services.metrics import inc_upgrade_clicks
from bot.keyboards.main_menu import get_main_menu

router = Router()

SUCCESS_URL = os.getenv("STRIPE_SUCCESS_URL")
CANCEL_URL = os.getenv("STRIPE_CANCEL_URL")

if not SUCCESS_URL or not CANCEL_URL:
    raise RuntimeError("STRIPE_SUCCESS_URL and STRIPE_CANCEL_URL must be set in .env")


def build_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Pro",
                    url=create_checkout_session(
                        tier="pro",
                        success_url=SUCCESS_URL,
                        cancel_url=CANCEL_URL,
                        telegram_id=user_id,
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔥 Elite",
                    url=create_checkout_session(
                        tier="elite",
                        success_url=SUCCESS_URL,
                        cancel_url=CANCEL_URL,
                        telegram_id=user_id,
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text="👑 Super Elite",
                    url=create_checkout_session(
                        tier="super_elite",
                        success_url=SUCCESS_URL,
                        cancel_url=CANCEL_URL,
                        telegram_id=user_id,
                    ),
                )
            ],
        ]
    )


@router.message(Command("upgrade"))
@router.message(F.text == "🚀 Upgrade")
async def upgrade(message: Message):
    await typing(message.bot, message.chat.id)

    tier = await get_tier(message.from_user.id)

    if tier == "super_elite":
        await message.answer(
            "👑 **Super Elite**\n\n"
            "You’re already on the highest plan.",
            reply_markup=get_main_menu(),
            parse_mode="Markdown",
        )
        return

    inc_upgrade_clicks()  # 📊 metric

    await message.answer(
        "🚀 **Upgrade**\n\nChoose a plan 👇",
        reply_markup=build_keyboard(message.from_user.id),
        parse_mode="Markdown",
    )


@router.message(F.text == "⬅ Back to Menu")
async def back_to_menu(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer("⬇️ Main Menu", reply_markup=get_main_menu())
