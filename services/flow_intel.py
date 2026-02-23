# FILE: services/flow_intel.py
# LOCATION: services/flow_intel.py
# DROP-IN REPLACEMENT

from services.plan_guard import can_generate_feature


async def record_flow(user_id: int, tx: dict) -> str | None:
    # HARD GATE
    if not await can_generate_feature(user_id, "FLOW"):
        return None

    # Placeholder for future flow logic
    return None
