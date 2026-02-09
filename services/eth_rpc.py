import aiohttp

async def get_block_txs(rpc_url: str, block_hash: str) -> list[dict]:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_getBlockByHash",
        "params": [block_hash, True]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(rpc_url, json=payload, timeout=15) as r:
            data = await r.json()
            return data["result"]["transactions"]