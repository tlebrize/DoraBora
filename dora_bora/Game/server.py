from DoraBora.server import BaseServer

from Game import procedures
from Login.models import Server


class GameServer(BaseServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = None
        self.exchange = None
        self.server = None
        self.account = None
        self.character = None
        self.map = None

    async def run(self, server_name, exchange):
        self.exchange = exchange
        self.client_id = await self.exchange.get_next_client_id()
        self.server = await Server.objects.aget(name=server_name)

        await self.write("HG")

        while True:
            command = await self.readline()
            if not command:
                await procedures.disconnect(self)
                break

            match command:
                case "HS":
                    await procedures.disconnect_switch(self)
                    break

            match command[0]:
                case "A":
                    await procedures.account_handler(self, command[1:])
                case "c":
                    await procedures.chat_handler(self, command[1:])
                case "B":
                    await procedures.basic_handler(self, command[1:])
                case "G":
                    await procedures.game_handler(self, command[1:])
                case "C":
                    await procedures.conquest_handler(self, command[1:])
