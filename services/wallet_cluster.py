import time
from collections import defaultdict

# Window where related wallets are considered linked
WINDOW = 60 * 30  # 30 minutes

# entity_id -> {address}
_entities: dict[int, set[str]] = defaultdict(set)

# address -> (entity_id, timestamp)
_index: dict[str, tuple[int, float]] = {}

_next_entity_id = 1


def _prune(now: float):
    cutoff = now - WINDOW
    for addr, (eid, ts) in list(_index.items()):
        if ts < cutoff:
            _index.pop(addr, None)
            _entities[eid].discard(addr)
            if not _entities[eid]:
                _entities.pop(eid, None)


def observe(address: str) -> str | None:
    """
    Observe wallet activity and cluster wallets likely
    controlled by the same entity.
    """
    global _next_entity_id

    now = time.time()
    address = address.lower()
    _prune(now)

    if address in _index:
        eid, _ = _index[address]
        _index[address] = (eid, now)
        return None

    # Try to attach to existing entity via timing proximity
    for eid, wallets in _entities.items():
        for w in wallets:
            _, ts = _index.get(w, (None, 0))
            if now - ts <= WINDOW:
                wallets.add(address)
                _index[address] = (eid, now)
                return f"🧩 Wallet Cluster: Entity #{eid}"

    # Create new entity
    eid = _next_entity_id
    _next_entity_id += 1

    _entities[eid].add(address)
    _index[address] = (eid, now)
    return None
