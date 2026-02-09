from aiogram import Router, F
from aiogram.types import Message

from config.settings import settings
from services.typing import typing
from services.metrics import get_metrics

router = Router()


def _is_owner(message: Message) -> bool:
    return message.from_user.id == settings.OWNER_CHAT_ID


@router.message(F.text == "📊 Admin")
async def admin_panel(message: Message):
    if not _is_owner(message):
        return

    await typing(message.bot, message.chat.id)
    metrics = await get_metrics()

    await message.answer(
        "📊 Admin Dashboard\n\n"
        f"👥 Active users: {metrics['users']}\n"
        f"🚨 Alerts sent: {metrics['alerts']}\n"
        f"⏱ Avg latency: {metrics['latency']}s\n"
        f"🔌 WS reconnects: {metrics['reconnects']}\n"
    )
