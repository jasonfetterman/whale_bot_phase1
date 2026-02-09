import asyncio
import json
import websockets

from services.metrics import inc_reconnects


class AlchemyWS:
    def __init__(self, ws_url: str):
        self.ws_url = ws_url
        self._running = True

    async def stop(self):
        self._running = False

    async def run(self, handler):
        while self._running:
            try:
                async with websockets.connect(
                    self.ws_url,
                    ping_interval=20,
                    ping_timeout=20,
                    close_timeout=5,
                ) as ws:
                    await ws.send(json.dumps({
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "eth_subscribe",
                        "params": ["newHeads"],
                    }))
                    print("[alchemy] subscribed")

                    async for msg in ws:
                        if not self._running:
                            return
                        data = json.loads(msg)
                        if "params" in data:
                            await handler(data["params"]["result"])

            except asyncio.CancelledError:
                return
            except Exception as e:
                inc_reconnects()
                print(f"[alchemy] reconnecting ({e})")
                await asyncio.sleep(5)
