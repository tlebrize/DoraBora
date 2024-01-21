import asyncio

from django.core.management.base import BaseCommand

from Game.server import GameServer
from Game.exchange import Exchange
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        asyncio.run(self.start_server())

    async def server_entrypoint(self, reader, writer):
        server = GameServer(reader, writer)
        await server.run(settings.GAME_SERVER_NAME, self.exchange)

    async def start_server(self):
        print("Starting game server.")

        self.exchange = Exchange()

        server = await asyncio.start_server(
            self.server_entrypoint,
            settings.GAME_HOST,
            settings.GAME_PORT,
        )
        async with server:
            await server.serve_forever()
