import time

_METRICS = {
    "users": 0,
    "alerts": 0,
    "latency": 0.0,
    "reconnects": 0,
}

_START = time.time()


def inc_users(count: int):
    _METRICS["users"] = count


def inc_alerts():
    _METRICS["alerts"] += 1


def set_latency(value: float):
    _METRICS["latency"] = round(value, 2)


def inc_reconnects():
    _METRICS["reconnects"] += 1


async def get_metrics() -> dict:
    return dict(_METRICS)
