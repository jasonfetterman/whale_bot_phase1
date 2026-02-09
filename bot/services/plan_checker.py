import os
import json
import aiohttp

OWNER_TG_ID = int(os.getenv("OWNER_TG_ID", "0"))
WEB_APP_BASE_URL = os.getenv("WEB_APP_BASE_URL", "http://localhost:3000")

LINK_FILE = "telegram_links.json"


def load_links():
    if not os.path.exists(LINK_FILE):
        return {}
    with open(LINK_FILE, "r") as f:
        return json.load(f)


async def get_user_plan(telegram_id: int) -> str:
    # 👑 Owner override
    if telegram_id == OWNER_TG_ID:
        return "super_elite"

    links = load_links()
    link = links.get(str(telegram_id))

    if not link:
        return "free"

    clerk_user_id = link.get("clerk_user_id")
    if not clerk_user_id:
        return "free"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{WEB_APP_BASE_URL}/api/telegram/plan",
                json={"clerk_user_id": clerk_user_id},
                timeout=5,
            ) as resp:
                if resp.status != 200:
                    return "free"
                data = await resp.json()
                return data.get("plan", "free")
    except Exception:
        return "free"


async def can_track_wallets(telegram_id: int, current_count: int) -> bool:
    plan = await get_user_plan(telegram_id)

    if plan == "super_elite":
        return True

    if plan == "elite":
        return current_count < 50

    if plan == "pro":
        return current_count < 10

    return current_count < 1
