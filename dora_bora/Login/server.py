from DoraBora.server import BaseServer

from Login import procedures as procs
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
            await self.handle_server_input()

    async def connection_steps(self):
        await procs.send_policy(self)
        await procs.send_key(s)
        await procs.check_version(version)

        # choose connection type
        packet = await self.readline()
        if packet == "#S":
            await procs.switch_login(self)
        else:
            self.username = packet
            await procs.password_login(self)

        await procs.send_connected_infos(self)
