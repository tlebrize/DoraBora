from django.core.management.base import BaseCommand
import asyncio
from Login.server import LoginServer
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        asyncio.run(self.start_server())

    async def server_entrypoint(self, reader, writer):
        server = LoginServer(reader, writer)
        await server.run()

    async def start_server(self):
        print("Starting login server.")
        server = await asyncio.start_server(
            self.server_entrypoint,
            settings.LOGIN_HOST,
            settings.LOGIN_PORT,
        )
        async with server:
            await server.serve_forever()
