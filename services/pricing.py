import aiohttp, asyncio

PRICES = {
    "ethereum": "ethereum",
    "bsc": "binancecoin",
    "polygon": "matic-network",
}

_cache = {}
_last = 0

async def get_price(chain: str) -> float:
    global _last
    if asyncio.get_event_loop().time() - _last < 60 and chain in _cache:
        return _cache[chain]

    ids = ",".join(PRICES.values())
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    async with aiohttp.ClientSession() as s:
        async with s.get(url, timeout=10) as r:
            data = await r.json()
            for k,v in PRICES.items():
                _cache[k] = float(data[v]["usd"])
            _last = asyncio.get_event_loop().time()
            return _cache[chain]