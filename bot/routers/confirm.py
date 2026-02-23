from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from db.engine import get_db
from services.user_tiers import get_tier
from services.plan_checker import can_track_wallets

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
    user_id = message.from_user.id

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

    # COUNT wallets
    cur = await db.execute(
        "SELECT COUNT(*) FROM wallets WHERE chat_id = ?",
        (chat_id,),
    )
    row = await cur.fetchone()
    wallet_count = row[0]

    tier = await get_tier(user_id)

    # ENFORCE LIMIT (Super Elite bypasses)
    if tier != "super_elite":
        allowed = await can_track_wallets(user_id, wallet_count)
        if not allowed:
            await message.answer(
                "🚫 Wallet limit reached.\n\nUpgrade to unlock more wallets."
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
