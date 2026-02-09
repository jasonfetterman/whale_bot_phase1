from db.engine import get_db
import time
import hashlib


def _identity_key(address: str) -> str:
    """
    Deterministic cross-chain identity key.
    """
    return hashlib.sha256(address.lower().encode()).hexdigest()


async def link_wallet(address: str, chain: str):
    """
    Link wallet to a global identity across chains.
    """
    identity = _identity_key(address)
    now = int(time.time())

    db = await get_db()
    await db.execute(
        """
        INSERT OR IGNORE INTO wallet_identity (
            identity,
            address,
            chain,
            first_seen,
            last_seen
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (identity, address.lower(), chain, now, now),
    )
    await db.commit()


async def touch_identity(address: str):
    """
    Update last_seen across all chains.
    """
    identity = _identity_key(address)
    db = await get_db()
    await db.execute(
        """
        UPDATE wallet_identity
        SET last_seen = ?
        WHERE identity = ?
        """,
        (int(time.time()), identity),
    )
    await db.commit()


async def get_identity(address: str) -> dict | None:
    """
    Fetch cross-chain identity profile.
    """
    identity = _identity_key(address)
    db = await get_db()
    cur = await db.execute(
        """
        SELECT identity,
               COUNT(DISTINCT chain) AS chains,
               MIN(first_seen) AS first_seen,
               MAX(last_seen) AS last_seen
        FROM wallet_identity
        WHERE identity = ?
        GROUP BY identity
        """,
        (identity,),
    )
    row = await cur.fetchone()
    return dict(row) if row else None
