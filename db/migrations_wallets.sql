CREATE TABLE IF NOT EXISTS wallets (
    chat_id INTEGER NOT NULL,
    address TEXT NOT NULL,
    label TEXT,
    created_at INTEGER NOT NULL,
    PRIMARY KEY (chat_id, address)
);

