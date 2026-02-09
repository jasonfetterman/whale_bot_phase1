from db.engine import get_db
import time


async def remember_wallet(address: str, chain: str, tag: str | None = None):
    """
    Persistently remember a wallet across chains.
    """
    db = await get_db()
    await db.execute(
        """
        INSERT OR IGNORE INTO wallet_memory (
            address,
            first_seen,
            last_seen,
            chain,
            tag
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            address.lower(),
            int(time.time()),
            int(time.time()),
            chain,
            tag,
        ),
    )
    await db.commit()


async def touch_wallet(address: str):
    """
    Update last_seen timestamp.
    """
    db = await get_db()
    await db.execute(
        """
        UPDATE wallet_memory
        SET last_seen = ?
        WHERE address = ?
        """,
        (int(time.time()), address.lower()),
    )
    await db.commit()


async def get_wallet_profile(address: str) -> dict | None:
    """
    Return wallet profile if known.
    """
    db = await get_db()
    cur = await db.execute(
        """
        SELECT *
        FROM wallet_memory
        WHERE address = ?
        """,
        (address.lower(),),
    )
    row = await cur.fetchone()
    return dict(row) if row else None
