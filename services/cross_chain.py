import time
from collections import defaultdict

# Correlation window
WINDOW = 60 * 20  # 20 minutes

# address -> [(chain, timestamp)]
_seen: dict[str, list[tuple[str, float]]] = defaultdict(list)


def _prune(now: float):
    cutoff = now - WINDOW
    for addr in list(_seen.keys()):
        _seen[addr] = [(c, t) for c, t in _seen[addr] if t >= cutoff]
        if not _seen[addr]:
            _seen.pop(addr, None)


def record(chain: str, address: str) -> str | None:
    """
    Track wallet activity across chains.
    Returns correlation label if detected.
    """
    now = time.time()
    _prune(now)

    address = address.lower()
    _seen[address].append((chain, now))

    chains = {c for c, _ in _seen[address]}

    if len(chains) >= 2:
        chain_list = ", ".join(sorted(chains))
        return f"🌐 Cross-Chain Activity: {chain_list}"

    return None
