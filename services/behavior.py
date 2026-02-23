# FILE: services/behavior.py
# LOCATION: services/behavior.py
# DROP-IN REPLACEMENT

import time
from collections import defaultdict
from services.plan_guard import can_generate_feature

# Sliding window (seconds)
WINDOW = 60 * 30  # 30 minutes

# Thresholds
ACCUMULATION_TX_COUNT = 5
DISTRIBUTION_TX_COUNT = 5

# address -> [timestamps]
_incoming: dict[str, list[float]] = defaultdict(list)
_outgoing: dict[str, list[float]] = defaultdict(list)


def _prune(now: float):
    cutoff = now - WINDOW
    for store in (_incoming, _outgoing):
        for addr in list(store.keys()):
            store[addr] = [t for t in store[addr] if t >= cutoff]
            if not store[addr]:
                store.pop(addr, None)


async def record_tx(
    user_id: int,
    from_addr: str,
    to_addr: str,
) -> str | None:
    # HARD GATE
    if not await can_generate_feature(user_id, "BEHAVIOR"):
        return None

    now = time.time()
    _prune(now)

    from_addr = from_addr.lower()
    to_addr = to_addr.lower()

    _outgoing[from_addr].append(now)
    _incoming[to_addr].append(now)

    if len(_incoming[to_addr]) >= ACCUMULATION_TX_COUNT:
        return "🟢 Accumulation Pattern Detected"

    if len(_outgoing[from_addr]) >= DISTRIBUTION_TX_COUNT:
        return "🔴 Distribution Pattern Detected"

    return None
