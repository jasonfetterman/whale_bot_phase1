from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.keyboards.main_menu import get_main_menu
from services.typing import typing
from services.user_tiers import get_tier, set_tier
from services.metrics import inc_starts
from services.referrals import get_or_create_code, apply_referral

router = Router()


async def show_main_menu(message: Message):
    await typing(message.bot, message.chat.id)
    await message.answer(
        "🐋 Whaler X\n\nChoose an option below 👇",
        reply_markup=get_main_menu(),
    )


@router.message(Command("start"))
async def start_cmd(message: Message):
    inc_starts()

    user_id = message.from_user.id
    tier = await get_tier(user_id)

    parts = message.text.split()
    if len(parts) == 2:
        await apply_referral(user_id, parts[1])

    if tier == "free":
        await set_tier(user_id, "free")
        await message.answer(
            "👋 Welcome to Whaler X\n\n"
            "1) Add at least one wallet\n"
            "2) Alerts are ON by default\n"
            "3) Upgrade anytime\n"
        )

    code = await get_or_create_code(user_id)
    await message.answer(
        f"🎁 Referral link:\nhttps://t.me/{message.bot.username}?start={code}"
    )

    await show_main_menu(message)


# ===== BUTTON HANDLING (REPLY KEYBOARD FIX) =====

@router.message(F.text.in_({
    "🚨 Whale Alerts",
    "👛 Wallets",
    "📊 My Plan",
    "⚙ Settings",
    "🚀 Upgrade",
    "❓ Help",
}))
async def menu_buttons_work(message: Message):
    await message.answer(f"✅ Button received: {message.text}")
