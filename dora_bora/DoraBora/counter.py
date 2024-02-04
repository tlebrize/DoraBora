import asyncio


class AsyncCounter:
    def __init__(self, maximum=None):
        self.maximum = maximum
        self.value = 0
        self.lock = asyncio.Lock()

    async def __call__(self):
        async with self.lock:
            self.value += 1

            if self.maximum and self.value > self.maximum:
                self.value = self.value % self.maximum

            value = self.value

        return value
