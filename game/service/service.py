import asyncio
from service.management import Management
from service.handlers import (
    account_handler,
    chat_handler,
    basic_handler,
    game_handler,
    conquest_handler,
)


class Service:
    def __init__(self, reader, writer, config):
        self.reader = reader
        self.writer = writer
        self.config = config
        self.management = Management(self.config)

    async def write(self, message: str, drain: bool = False):
        print(">", message)
        self.writer.write(message.encode() + b"\0")
        if drain:
            await self.writer.drain()

    async def readline(self) -> str:
        line = (await self.reader.readline()).decode().strip("\x00\n")
        print("<", repr(line))
        return line

    async def on_connect(self):
        await self.write("HG")

        while True:
            command = await self.readline()
            if not command:
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
