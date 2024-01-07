import asyncio

from service.service import Service
from service.config import Config


async def create_login(reader, writer):
    service = Service(reader, writer, Config())
    await service.on_connect()


async def run_server():
    print("Starting login server.")
    server = await asyncio.start_server(create_login, "0.0.0.0", 5051)
    async with server:
        await server.serve_forever()


asyncio.run(run_server())
