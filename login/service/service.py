import asyncio, random, string
from service.password import decrypt
from service.management import Management
from enum import Enum

POLICY = """
<?xml version="1.0" encoding="UTF-8"?>
<cross-domain-policy>
<site-control permitted-cross-domain-policies="all"/>
<allow-access-from domain="*" to-ports="*" secure="false"/>
<allow-http-request-headers-from domain="*" headers="*" secure="false"/>
</cross-domain-policy>"
""".strip()


class LoginStep(int, Enum):
    QUIT = 0
    START = 1
    VERSION_CHECK = 2
    CONNECTION = 3
    PASSWORD = 4
    SWITCH = 5
    SEND_INFO = 6
    HANDLE_INPUTS = 7


class Service:
    def __init__(self, reader, writer, config):
        self.reader = reader
        self.writer = writer
        self.config = config
        self.management = Management(self.config)
        self.step = LoginStep.START

    async def write(self, message: str, drain: bool = False):
        print(">", message)
        self.writer.write(message.encode() + b"\0")
        if drain:
            await self.writer.drain()

    async def readline(self) -> str:
        line = (await self.reader.readline()).decode().strip("\0\n")
        print("<", repr(line))
        return line

    async def on_connect(self):
        while self.step != LoginStep.QUIT:
            if self.step == LoginStep.START:
                await self.write(POLICY)
                self.key = "".join(random.choices(string.ascii_lowercase, k=32))
                await self.write(f"HC{self.key}", drain=True)
                self.step = LoginStep.VERSION_CHECK

            if self.step == LoginStep.VERSION_CHECK:
                version = await self.readline()
                self.check_version(version)
                self.step = LoginStep.CONNECTION

            if self.step == LoginStep.CONNECTION:
                packet = await self.readline()
                if packet == "#S":
                    self.step = LoginStep.SWITCH
                else:
                    self.username = packet
                    self.step = LoginStep.PASSWORD

            if self.step == LoginStep.PASSWORD:
                password = await self.readline()
                await self.password_login(password)
                self.step = LoginStep.SEND_INFO

            if self.step == LoginStep.SWITCH:
                switch_token = await self.readline()
                await self.switch_login(switch_token)
                self.step = LoginStep.SEND_INFO

            if self.step == LoginStep.SEND_INFO:
                await self.send_logged_in_info()
                self.step = LoginStep.HANDLE_INPUTS

            if self.step == LoginStep.HANDLE_INPUTS:
                self.step = await self.handle_server_input()

    def check_version(self, version):
        if not "1.39.8e" in version:
            raise Exception(f"Invalid Version : {version}")

    async def password_login(self, password_hash):
        check, password_hash = password_hash.split("#1")
        if check:
            raise Exception("Invalid password format")

        decrypted_password = decrypt(password_hash, self.key)

        if not (await self.management.password_login(self.username, decrypted_password)):
            raise Exception("Invalid password")

    async def switch_login(self, switch_token):
        if not (await self.management.switch_login(switch_token[:196])):
            raise Exception("Invalid switch_token")

    async def send_logged_in_info(self):
        account, server_list = await asyncio.gather(
            self.management.get_account(),
            self.management.list_servers(),
        )
        login_packets = [
            f"Ad{account.nickname}",
            f"Ac{account.community}",
            f"AH{server_list.format_login_list()}",
            f"AlK{account.format_is_game_master()}",
            f"AQ{account.format_security_question()}",
        ]
        await self.write("\0".join(login_packets))

    async def handle_server_input(self):
        msg = await self.readline()
        if msg == "Af":
            await self.write("Af0|0|0|1|-1")
            # login queue is disabled.
        elif msg == "Ax":
            await self.send_server_list()
        elif msg[:2] == "AX":
            await self.handle_server_connection(int(msg[2:]))
        elif msg[:2] == "Ai":
            await self.handle_switch_token(msg[2:])  # maybe ?
        # if msg == "AF": Friend list
        # if msg == "Ap": ???
        else:
            if not msg:
                self.writer.close()
                return LoginStep.QUIT
            else:
                print("! not handled")

        return LoginStep.HANDLE_INPUTS

    async def send_server_list(self):
        account, server_list = await asyncio.gather(
            self.management.get_account(),
            self.management.list_servers(),
        )

        if account.subscribed_seconds:
            subscribed = str(account.subscribed_milliseconds()) + "|"
        else:
            subscribed = ""

        server_characters = "|".join(
            [f"{s.id},{s.character_count}" for s in server_list.servers],
        )

        await self.write("AxK" + subscribed + server_characters)

    async def handle_server_connection(self, server_id):
        server_list = await self.management.list_servers()

        try:
            server = next(filter(lambda s: s.id == server_id, server_list.servers))
        except StopIteration:
            raise Exception(f"server not found {server_id}")

        await asyncio.gather(
            self.write("AYK" + server.format_connection()),
            self.management.set_account_in_login(),
        )

    async def handle_switch_token(self, token):
        # unsure about what this really does.
        await self.management.set_account_switch_token(token[:196])
