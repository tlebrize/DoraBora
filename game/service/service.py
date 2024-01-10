import asyncio
from service.management import Management
from service.handlers import (
    account_handler,
    chat_handler,
    basic_handler,
    game_handler,
    conquest_handler,
)
from service.handlers.miscellaneous import disconnect
from service.exchange import create_exchange_task
import redis.asyncio as redis


class Service:
    def __init__(self, reader, writer, config):
        self.reader = reader
        self.writer = writer
        self.config = config
        self.management = Management(config)
        self.redis = redis.from_url(config.REDIS_URL)
        self.server_id = config.SERVER_ID
        self.server_exchange_task = None

    async def write(self, message: str, drain: bool = False):
        print(">", message)
        self.writer.write(message.encode() + b"\0")
        if drain:
            await self.writer.drain()

    async def readline(self) -> str:
        line = (await self.reader.readline()).decode().strip("\x00\n")
        if "ù" in line:
            print("? ignored ù")
            line = line.split("ù")[2]

        print("<", repr(line))
        return line

    async def create_server_exchange(self):
        self.server_exchange_task = await create_exchange_task(
            service=self,
            channel_name="server",
            key=self.server_id,
        )

    async def stop_server_exhange(self):
        self.server_exchange_task.cancel()

    def exchange_message(self, exchange_name, exchange_key, message):
        print(f"+{exchange_name}#{exchange_key} : {message}")

    async def broadcast(self, channel, message):
        await self.redis.publish(channel, message)

    async def on_connect(self):
        await self.write("HG")

        while True:
            command = await self.readline()
            if not command:
                break

            match command:
                case "HS":
                    await disconnect(self)
                    break

            match command[0]:
                case "A":
                    await account_handler(self, command[1:])
                case "c":
                    await chat_handler(self, command[1:])
                case "B":
                    await basic_handler(self, command[1:])
                case "G":
                    await game_handler(self, command[1:])
                case "C":
                    await conquest_handler(self, command[1:])
