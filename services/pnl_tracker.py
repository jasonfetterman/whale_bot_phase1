# Wallet P&L + cost basis tracker
# Conservative, spot-transfer based (no leverage assumptions)

from db.engine import get_db
import time

async def record_transfer(
    chain: str,
    wallet: str,
    amount: float,
    usd_price: float,
    direction: str,  # "in" | "out"
):
    db = await get_db()
    await db.execute(
        """
        INSERT INTO pnl_ledger (chain, wallet, amount, usd_price, direction, ts)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (chain, wallet.lower(), amount, usd_price, direction, int(time.time())),
    )
    await db.commit()


async def get_pnl(chain: str, wallet: str) -> dict:
    db = await get_db()
    cur = await db.execute(
        """
        SELECT amount, usd_price, direction
        FROM pnl_ledger
        WHERE chain = ? AND wallet = ?
        """,
        (chain, wallet.lower()),
    )
    rows = await cur.fetchall()

    cost = 0.0
    proceeds = 0.0
    net_amount = 0.0

    for r in rows:
        if r["direction"] == "in":
            cost += r["amount"] * r["usd_price"]
            net_amount += r["amount"]
        else:
            proceeds += r["amount"] * r["usd_price"]
            net_amount -= r["amount"]

    realized = proceeds - cost
    return {
        "net_amount": net_amount,
        "cost": cost,
        "proceeds": proceeds,
        "realized_pnl": realized,
    }
