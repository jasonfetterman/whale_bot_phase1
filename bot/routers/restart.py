from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config.settings import settings
from services.user_tiers import get_tier

router = Router()


@router.message(Command("restart"))
async def restart_cmd(message: Message):
    user_id = message.from_user.id
    tier = await get_tier(user_id)

    # OWNER: full control (message only here; actual restart handled elsewhere)
    if user_id == settings.OWNER_CHAT_ID:
        await message.answer("🔄 Restart acknowledged (owner).")
        return

    # SUPER ELITE: allowed, non-destructive
    if tier == "super_elite":
        await message.answer("ℹ️ Bot is running normally.")
        return

    # OTHERS: blocked
    return
