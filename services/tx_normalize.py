def normalize_pending(ev: dict) -> dict:
    tx = ev.get("result", {})
    return {
        "hash": tx.get("hash"),
        "value": int(tx.get("value", "0"), 16) if isinstance(tx.get("value"), str) else int(tx.get("value", 0)),
        "chain": "ethereum",
    }