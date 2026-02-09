CREATE TABLE IF NOT EXISTS pnl_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chain TEXT NOT NULL,
    wallet TEXT NOT NULL,
    amount REAL NOT NULL,
    usd_price REAL NOT NULL,
    direction TEXT CHECK(direction IN ('in','out')) NOT NULL,
    ts INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_pnl_wallet
ON pnl_ledger (chain, wallet);
