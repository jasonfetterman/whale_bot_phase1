from pathlib import Path
import json

DATA_FILE = Path("data/entities.json")

# Default seed (used if file does not exist)
DEFAULT_ENTITIES = {
    "binance": {
        "label": "Binance",
        "addresses": []
    },
    "coinbase": {
        "label": "Coinbase",
        "addresses": []
    },
    "kraken": {
        "label": "Kraken",
        "addresses": []
    },
    "bridge": {
        "label": "Bridge",
        "addresses": []
    }
}


def _load_entities() -> dict:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text(json.dumps(DEFAULT_ENTITIES, indent=2))
        return DEFAULT_ENTITIES

    try:
        return json.loads(DATA_FILE.read_text())
    except Exception:
        return DEFAULT_ENTITIES


def resolve_entity(address: str | None) -> str | None:
    if not address:
        return None

    address = address.lower()
    entities = _load_entities()

    for data in entities.values():
        for a in data.get("addresses", []):
            if a.lower() == address:
                return data.get("label")

    return None
