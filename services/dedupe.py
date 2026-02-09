from db.repo import alert_seen, mark_alert_seen


async def should_send_alert(alert_key: str) -> bool:
    if await alert_seen(alert_key):
        return False
    await mark_alert_seen(alert_key)
    return True
