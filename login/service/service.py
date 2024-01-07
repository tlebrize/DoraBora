import asyncio, random, string
from service.password import decrypt
from service.management import Management

POLICY = """
<?xml version="1.0" encoding="UTF-8"?>
<cross-domain-policy>
<site-control permitted-cross-domain-policies="all"/>
<allow-access-from domain="*" to-ports="*" secure="false"/>
<allow-http-request-headers-from domain="*" headers="*" secure="false"/>
</cross-domain-policy>"
""".strip()


class Service:
    def __init__(self, reader, writer, config):
        self.reader = reader
        self.writer = writer
        self.config = config
        self.management = Management(self.config)
        self.step = 0

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
        while True:
            if self.step == 0:
                print("connecting")
                await self.write(POLICY)
                self.key = "".join(random.choices(string.ascii_lowercase, k=32))
                await self.write(f"HC{self.key}", drain=True)
                self.step = 1

            if self.step == 1:
                print("checking version")
                version = await self.readline()
                self.check_version(version)
                self.step = 2

            if self.step == 2:
                print("authenticating")
                self.username = await self.readline()
                password = await self.readline()
                await self.login(password)
                self.step = 3

            if self.step == 3:
                print("sending login infos")
                await self.send_logged_in_info()
                self.step = 4

            if self.step == 4:
                print("handling server info")
                await self.handle_server_input()

    def check_version(self, version):
        if not "1.39.8e" in version:
            raise Exception(f"Invalid Version : {version}")

    async def login(self, password_hash):
        check, password_hash = password_hash.split("#1")
        if check:
            raise Exception("Invalid password format")

        decrypted_password = decrypt(password_hash, self.key)

        if not (await self.management.login(self.username, decrypted_password)):
            raise Exception("Invalid login.")

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
        # if msg == "AF": Friend list
        # if msg == "Ap": ???
        else:
            print("not handled", repr(msg))
            if not msg:
                self.writer.close()
                exit(0)

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
            raise Exception(f"server not found {id_}")

        await asyncio.gather(
            self.write("AYK" + server.format_connection()),
            self.management.set_account_in_login(),
        )
