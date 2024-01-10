import asyncio


class Exchange:
    def __init__(self, service, channel, name, key):
        self.service = service
        self.channel = channel
        self.name = name
        self.key = key

    async def run(self):
        await self.channel.subscribe(f"{self.name}.{self.key}")
        while True:
            message = await self.channel.get_message(ignore_subscribe_messages=True)
            if message is not None:
                self.service.exchange_message(self.name, self.key, message)
            await asyncio.sleep(1)


async def create_exchange_task(service, channel_name, key):
    async with service.redis.pubsub() as channel:
        exchange = Exchange(service, channel, channel_name, key)
        return asyncio.create_task(exchange.run())  # keep a ref to this
