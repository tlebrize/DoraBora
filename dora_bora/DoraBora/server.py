from unidecode import unidecode


class BaseServer:
    def __init__(self, reader, writer):
        self.client_id = None
        self.reader = reader
        self.writer = writer

    async def run(self):
        self.client_id = None
        raise NotImplementedError()

    def get_client_id_prefix(self):
        if self.client_id:
            return f"[{self.client_id}]"
        else:
            return ""

    async def write(self, message: str, drain: bool = False):
        print(self.get_client_id_prefix(), ">", message)
        self.writer.write(message.encode() + b"\0")
        if drain:
            await self.writer.drain()

    async def readline(self) -> str:
        line = (await self.reader.readline()).decode().strip("\x00\n")
        if "ù" in line:
            print(self.get_client_id_prefix(), "? ignored ù")
            line = line.split("ù")[2]

        line = unidecode(line)

        print(self.get_client_id_prefix(), "<", repr(line))
        return line
