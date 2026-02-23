from aiogram import Router
from aiogram.types import Message

from config.settings import settings
from services.user_tiers import get_tier

router = Router()


@router.message()
async def debug_all(message: Message):
    user_id = message.from_user.id
    tier = await get_tier(user_id)

    if user_id != settings.OWNER_CHAT_ID and tier != "super_elite":
        return

    print("📥 DEBUG MESSAGE:", repr(message.text))
