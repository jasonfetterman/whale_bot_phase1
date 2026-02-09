from pathlib import Path
import sqlite3
import aiosqlite

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "bot.db"

sqlite3.connect(DB_PATH).close()

_db: aiosqlite.Connection | None = None


async def get_db() -> aiosqlite.Connection:
    global _db
    if _db is None:
        _db = await aiosqlite.connect(DB_PATH)
        _db.row_factory = aiosqlite.Row
    return _db


async def init_db():
    db = await get_db()
    await db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY,
            tier TEXT NOT NULL,
            status TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS wallets (
            chat_id INTEGER,
            address TEXT,
            label TEXT,
            PRIMARY KEY (chat_id, address)
        );
        
        CREATE TABLE IF NOT EXISTS wallet_memory (
            address TEXT PRIMARY KEY,
            first_seen INTEGER,
            last_seen INTEGER,
            chain TEXT,
            tag TEXT
        );


        CREATE TABLE IF NOT EXISTS thresholds (
            chain TEXT,
            user_id INTEGER,
            value REAL,
            PRIMARY KEY (chain, user_id)
        );

        CREATE TABLE IF NOT EXISTS alerts_seen (
            alert_key TEXT PRIMARY KEY,
            seen_at INTEGER
        );

        CREATE TABLE IF NOT EXISTS chain_toggles (
            user_id INTEGER,
            chain TEXT,
            enabled INTEGER,
            PRIMARY KEY (user_id, chain)
        );
        
        CREATE TABLE IF NOT EXISTS wallet_identity (
            identity TEXT,
            address TEXT,
            chain TEXT,
            first_seen INTEGER,
            last_seen INTEGER,
            PRIMARY KEY (identity, chain)
        );
        
        CREATE TABLE IF NOT EXISTS wallet_behavior (
            address TEXT,
            chain TEXT,
            usd_value REAL,
            ts INTEGER
        );


        """
    )
    await db.commit()
