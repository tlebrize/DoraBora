from django.core.management.base import BaseCommand
import asyncio, random, string

POLICY = """
<?xml version="1.0" encoding="UTF-8"?>
<cross-domain-policy>
<site-control permitted-cross-domain-policies="all"/>
<allow-access-from domain="*" to-ports="*" secure="false"/>
<allow-http-request-headers-from domain="*" headers="*" secure="false"/>
</cross-domain-policy>"
""".strip()


class Command(BaseCommand):
    def handle(self, *args, **options):
        asyncio.run(self.run_server())

    async def run_server(self):
        print("Starting login server.")
        server = await asyncio.start_server(self.create_login, "0.0.0.0", 5051)
        async with server:
            await server.serve_forever()

    async def create_login(self, reader, writer):
        self.reader = reader
        self.writer = writer

        await self.write(POLICY)
        self.key = "".join(random.choices(string.ascii_lowercase, k=32))
        await self.write(f"HC{self.key}", drain=True)
        version = await self.readline()
        print(version)

    async def write(self, message: str, drain: bool = False):
        print(">", message)
        self.writer.write(message.encode() + b"\0")
        if drain:
            await self.writer.drain()

    async def readline(self) -> str:
        line = (await self.reader.readline()).decode().strip("\x00\n")
        if "ù" in line:
            print("? ignored ù")
            line = line.split("ù")[2]

        print("<", repr(line))
        return line
