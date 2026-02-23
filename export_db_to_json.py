# FILE: export_db_to_json.py
# LOCATION: project root (whale_bot_phase1/export_db_to_json.py)

import json
import sqlite3
from pathlib import Path
from datetime import datetime

# --- Paths ---
ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "bot.db"
OUTPUT_PATH = ROOT / "data" / "data.json"

def export_db_to_json():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Pull wallets only (web-safe)
    cur.execute(
        """
        SELECT address, label
        FROM wallets
        ORDER BY address
        """
    )
    rows = cur.fetchall()
    conn.close()

    wallets = [
        {
            "address": row["address"],
            "label": row["label"],
        }
        for row in rows
    ]

    payload = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "wallets": wallets,
        "count": len(wallets),
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

if __name__ == "__main__":
    export_db_to_json()
    print(f"Export complete → {OUTPUT_PATH}")
