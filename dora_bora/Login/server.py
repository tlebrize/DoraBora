from DoraBora.server import BaseServer
from Login import procedures
from Login.models import Account


class LoginServer(BaseServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key: str = procedures.make_key()
        self.quit: bool = False
        self.username: str = None
        self.account: Account = None

    async def run(self):
        await self.connection_steps()

        while not self.quit:
            await self.account_handler()

    async def connection_steps(self):
        await procedures.send_policy(self)
        await procedures.send_key(self)
        await procedures.check_version(self)

        # choose connection type
        packet = await self.readline()
        if packet == "#S":
            await procedures.switch_login(self)
        else:
            self.username = packet
            await procedures.password_login(self)

        await procedures.send_connected_infos(self)

    async def account_handler(self):
        msg = await self.readline()
        if not msg:
            self.quit = True
        elif msg == "Af":
            await self.write("Af0|0|0|1|-1")
            # login queue is disabled.
        elif msg == "Ax":
            await procedures.send_server_list(self)
        elif msg[:2] == "AX":
            await procedures.handle_server_connection(self, int(msg[2:]))
        elif msg[:2] == "Ai":
            await procedures.handle_switch_token(self, msg[2:])  # maybe ?
