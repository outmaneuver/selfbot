import asyncio
import time

class RateLimiter:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.retry_after = 0

    async def wait(self):
        async with self.lock:
            if self.retry_after > time.time():
                await asyncio.sleep(self.retry_after - time.time())

    def update_rate_limit(self, retry_after):
        self.retry_after = time.time() + retry_after
