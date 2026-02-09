from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db.engine import get_db

router = Router()


@router.message(Command("confirm"))
async def confirm_command(message: Message):
    """
    REAL confirmation command.
    Usage: /confirm <wallet_address>
    """

    parts = message.text.strip().split()

    if len(parts) != 2:
        await message.answer(
            "❌ Usage:\n"
            "/confirm <wallet_address>\n\n"
            "Example:\n"
            "/confirm 0xabc123..."
        )
        return

    wallet_address = parts[1].lower()
    chat_id = message.chat.id

    # Basic ETH address sanity check
    if not wallet_address.startswith("0x") or len(wallet_address) != 42:
        await message.answer("❌ Invalid wallet address format.")
        return

    db = await get_db()

    # Check if wallet already exists
    cur = await db.execute(
        """
        SELECT 1 FROM wallets
        WHERE chat_id = ? AND address = ?
        """,
        (chat_id, wallet_address),
    )
    exists = await cur.fetchone()

    if exists:
        await message.answer(
            "⚠️ *Wallet already added*\n\n"
            f"`{wallet_address}`",
            parse_mode="Markdown",
        )
        return

    # Insert new wallet
    await db.execute(
        """
        INSERT INTO wallets (chat_id, address, label)
        VALUES (?, ?, ?)
        """,
        (chat_id, wallet_address, "manual"),
    )
    await db.commit()

    await message.answer(
        "✅ *Wallet confirmed and saved. Ready for alerts!*\n\n"
        f"`{wallet_address}`",
        parse_mode="Markdown",
    )
