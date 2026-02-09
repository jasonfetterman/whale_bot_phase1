from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def debug_all(message: Message):
    print("📥 DEBUG MESSAGE:", repr(message.text))
