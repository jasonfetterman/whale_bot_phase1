from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from services.typing import typing
from services.stripe_payments import create_checkout_session
from bot.keyboards.main_menu import get_main_menu

router = Router()

SUCCESS_URL = "https://yourdomain.com/success"
CANCEL_URL = "https://yourdomain.com/cancel"


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

    await message.answer(
        "🚀 **Early Access Upgrade**\n\n"
        "Unlock:\n"
        "• Real-time whale alerts\n"
        "• Importance scoring\n"
        "• Entity context\n\n"
        "Choose a plan below 👇",
        reply_markup=build_keyboard(message.from_user.id),
        parse_mode="Markdown",
    )


@router.message(F.text == "⬅ Back to Menu")
async def back_to_menu(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer("⬇️ Main Menu", reply_markup=get_main_menu())
