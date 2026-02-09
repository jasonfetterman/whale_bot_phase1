from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("restart"))
async def restart_cmd(message: Message):
    await message.answer("Bot is running.")
