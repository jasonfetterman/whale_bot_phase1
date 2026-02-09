import json
from pathlib import Path

DATA_FILE = Path("data/users.json")
DATA_FILE.parent.mkdir(exist_ok=True)


def _load():
    if not DATA_FILE.exists():
        return {}
    return json.loads(DATA_FILE.read_text())


def _save(data: dict):
    DATA_FILE.write_text(json.dumps(data, indent=2))


async def get_tier(user_id: int) -> str:
    data = _load()
    return data.get(str(user_id), "free")


async def set_tier(user_id: int, tier: str):
    data = _load()
    data[str(user_id)] = tier
    _save(data)
