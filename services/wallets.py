from db.engine import get_db
from services.user_tiers import get_tier
import re


TIER_LIMITS = {
    "free": 1,
    "pro": 5,
    "elite": 20,
    "super_elite": 100,
}

ALL_CHAINS = ["eth", "bsc", "polygon", "arbitrum", "base"]
_ADDRESS_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")


async def _ensure_columns():
    db = await get_db()
    try:
        await db.execute("ALTER TABLE wallets ADD COLUMN enabled INTEGER DEFAULT 1")
    except Exception:
        pass
    try:
        await db.execute("ALTER TABLE wallets ADD COLUMN chains TEXT")
    except Exception:
        pass
    await db.commit()


def _normalize_address(address: str) -> str:
    return address.strip().lower()


def _validate_address(address: str):
    if not _ADDRESS_RE.match(address):
        raise RuntimeError("INVALID_ADDRESS")


async def _get_wallet_limit(chat_id: int) -> int:
    tier = await get_tier(chat_id)
    return TIER_LIMITS.get(tier, 1)


async def _wallet_exists(chat_id: int, address: str) -> bool:
    db = await get_db()
    cur = await db.execute(
        "SELECT 1 FROM wallets WHERE chat_id = ? AND address = ? LIMIT 1",
        (chat_id, address),
    )
    return await cur.fetchone() is not None


async def count_wallets(chat_id: int) -> int:
    await _ensure_columns()
    db = await get_db()
    cur = await db.execute(
        "SELECT COUNT(*) as cnt FROM wallets WHERE chat_id = ?",
        (chat_id,),
    )
    row = await cur.fetchone()
    return row["cnt"] if row else 0


async def add_wallet(chat_id: int, address: str, label: str | None = None):
    await _ensure_columns()
    address = _normalize_address(address)
    _validate_address(address)

    if await _wallet_exists(chat_id, address):
        raise RuntimeError("DUPLICATE_WALLET")

    current = await count_wallets(chat_id)
    limit = await _get_wallet_limit(chat_id)
    if current >= limit:
        raise RuntimeError("WALLET_LIMIT_REACHED")

    db = await get_db()
    await db.execute(
        """
        INSERT INTO wallets (chat_id, address, label, enabled, chains)
        VALUES (?, ?, ?, 1, ?)
        """,
        (chat_id, address, label, ",".join(ALL_CHAINS)),
    )
    await db.commit()


async def remove_wallet(chat_id: int, address: str):
    await _ensure_columns()
    address = _normalize_address(address)
    db = await get_db()
    await db.execute(
        "DELETE FROM wallets WHERE chat_id = ? AND address = ?",
        (chat_id, address),
    )
    await db.commit()


async def set_wallet_enabled(chat_id: int, address: str, enabled: bool):
    await _ensure_columns()
    address = _normalize_address(address)
    db = await get_db()
    await db.execute(
        "UPDATE wallets SET enabled = ? WHERE chat_id = ? AND address = ?",
        (1 if enabled else 0, chat_id, address),
    )
    await db.commit()


async def set_wallet_chains(chat_id: int, address: str, chains: list[str]):
    await _ensure_columns()
    address = _normalize_address(address)

    clean = [c for c in chains if c in ALL_CHAINS]
    if not clean:
        raise RuntimeError("EMPTY_CHAIN_SET")

    db = await get_db()
    await db.execute(
        "UPDATE wallets SET chains = ? WHERE chat_id = ? AND address = ?",
        (",".join(clean), chat_id, address),
    )
    await db.commit()


async def update_wallet_label(chat_id: int, address: str, label: str | None):
    await _ensure_columns()
    address = _normalize_address(address)
    db = await get_db()
    await db.execute(
        "UPDATE wallets SET label = ? WHERE chat_id = ? AND address = ?",
        (label, chat_id, address),
    )
    await db.commit()


async def get_wallets(chat_id: int) -> list[dict]:
    await _ensure_columns()
    db = await get_db()
    cur = await db.execute(
        "SELECT address, label, enabled, chains FROM wallets WHERE chat_id = ?",
        (chat_id,),
    )
    rows = await cur.fetchall()

    out = []
    for r in rows:
        chains = r["chains"].split(",") if r["chains"] else ALL_CHAINS
        out.append(
            {
                "address": r["address"],
                "label": r["label"],
                "enabled": bool(r["enabled"]),
                "chains": chains,
            }
        )
    return out


async def is_tracked(address: str, chain: str | None = None) -> bool:
    await _ensure_columns()
    address = _normalize_address(address)
    db = await get_db()

    if chain:
        cur = await db.execute(
            """
            SELECT 1 FROM wallets
            WHERE address = ? AND enabled = 1
              AND (chains IS NULL OR instr(chains, ?) > 0)
            LIMIT 1
            """,
            (address, chain),
        )
    else:
        cur = await db.execute(
            "SELECT 1 FROM wallets WHERE address = ? AND enabled = 1 LIMIT 1",
            (address,),
        )

    return await cur.fetchone() is not None
