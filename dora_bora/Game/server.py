from DoraBora.server import BaseServer

from Game import procedures
from Login.models import Server


class GameServer(BaseServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server = None

    async def run(self, server_name):
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
