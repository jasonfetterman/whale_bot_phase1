# FILE: services/metrics.py
# LOCATION: services/metrics.py
# DROP-IN REPLACEMENT

import time
from collections import deque

_NOW = lambda: int(time.time())
_DAY = 60 * 60 * 24
_WEEK = _DAY * 7

# ---- base counters (lifetime) ----
_METRICS = {
    "users": 0,
    "alerts": 0,
    "latency": 0.0,
    "reconnects": 0,
    "wallet_adds": 0,
    "upgrade_clicks": 0,
    "starts": 0,
}

# ---- rolling event logs (timestamps only) ----
_EVENTS = {
    "starts": deque(),
    "wallet_adds": deque(),
    "upgrade_clicks": deque(),
    "alerts": deque(),
}


def _trim(event: str):
    now = _NOW()
    dq = _EVENTS[event]
    while dq and now - dq[0] > _WEEK:
        dq.popleft()


def _record(event: str):
    _EVENTS[event].append(_NOW())
    _trim(event)


# ---- incrementors ----

def inc_users(count: int):
    _METRICS["users"] = count


def inc_alerts():
    _METRICS["alerts"] += 1
    _record("alerts")


def inc_wallet_adds():
    _METRICS["wallet_adds"] += 1
    _record("wallet_adds")


def inc_upgrade_clicks():
    _METRICS["upgrade_clicks"] += 1
    _record("upgrade_clicks")


def inc_starts():
    _METRICS["starts"] += 1
    _record("starts")


def set_latency(value: float):
    _METRICS["latency"] = round(value, 2)


def inc_reconnects():
    _METRICS["reconnects"] += 1


# ---- helpers ----

def _count_since(event: str, seconds: int) -> int:
    now = _NOW()
    return sum(1 for ts in _EVENTS[event] if now - ts <= seconds)


async def get_metrics() -> dict:
    return {
        **_METRICS,
        "windows": {
            "24h": {
                "starts": _count_since("starts", _DAY),
                "wallet_adds": _count_since("wallet_adds", _DAY),
                "upgrade_clicks": _count_since("upgrade_clicks", _DAY),
                "alerts": _count_since("alerts", _DAY),
            },
            "7d": {
                "starts": _count_since("starts", _WEEK),
                "wallet_adds": _count_since("wallet_adds", _WEEK),
                "upgrade_clicks": _count_since("upgrade_clicks", _WEEK),
                "alerts": _count_since("alerts", _WEEK),
            },
        },
    }
