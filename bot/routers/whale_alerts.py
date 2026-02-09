from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards.main_menu import get_main_menu
from services.typing import typing
from services.alerts import emit

router = Router()


@router.message(F.text == "🚨 Whale Alerts")
async def whale_alerts_status(message: Message):
    await typing(message.bot, message.chat.id)

    # Preview only
    await emit(
        bot=message.bot,
        chat_id=message.chat.id,
        text=(
            "🐋 Whale Alert Preview\n"
            "Amount: 1,234.56 ETH\n"
            "Direction: OUT\n"
            "Counterparty: 0xabc…def\n"
            "Large on-chain transfer detected.\n"
            "TX: PREVIEW_ONLY"
        ),
    )

    await message.answer(
        "🚨 Whale Alerts Status\n\n"
        "✅ Alerts: ACTIVE\n"
        "🌐 Chains monitored automatically.\n\n"
        "Live alerts will appear in this chat.",
        reply_markup=get_main_menu(),
    )
