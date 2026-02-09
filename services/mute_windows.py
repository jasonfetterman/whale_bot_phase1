from datetime import datetime, time
from typing import Optional

# structure: {user_id: (start_hour, end_hour)}
# hours are 0–23, local server time for now
_MUTE_WINDOWS: dict[int, tuple[int, int]] = {}


def set_mute_window(user_id: int, start_hour: int, end_hour: int):
    """
    Mute alerts between start_hour → end_hour.
    Example: 22 → 7 (10pm to 7am)
    """
    _MUTE_WINDOWS[user_id] = (start_hour % 24, end_hour % 24)


def clear_mute_window(user_id: int):
    _MUTE_WINDOWS.pop(user_id, None)


def is_muted(user_id: int, now: Optional[datetime] = None) -> bool:
    """
    Returns True if user is currently muted.
    """
    window = _MUTE_WINDOWS.get(user_id)
    if not window:
        return False

    start, end = window
    now = now or datetime.now()
    hour = now.hour

    # overnight window (e.g. 22 → 7)
    if start > end:
        return hour >= start or hour < end

    # same-day window
    return start <= hour < end
