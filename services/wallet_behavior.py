from db.engine import get_db
import time


async def record_event(address: str, chain: str, usd_value: float):
    """
    Record a whale event for behavior scoring.
    """
    db = await get_db()
    await db.execute(
        """
        INSERT INTO wallet_behavior (
            address,
            chain,
            usd_value,
            ts
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            address.lower(),
            chain,
            float(usd_value),
            int(time.time()),
        ),
    )
    await db.commit()


async def behavior_score(address: str) -> dict:
    """
    Simple historical behavior profile.
    """
    db = await get_db()
    cur = await db.execute(
        """
        SELECT
            COUNT(*)            AS events,
            SUM(usd_value)      AS total_usd,
            AVG(usd_value)      AS avg_usd,
            MAX(usd_value)      AS max_usd
        FROM wallet_behavior
        WHERE address = ?
        """,
        (address.lower(),),
    )
    row = await cur.fetchone()
    if not row or row["events"] == 0:
        return {
            "events": 0,
            "total_usd": 0,
            "avg_usd": 0,
            "max_usd": 0,
        }

    return dict(row)
