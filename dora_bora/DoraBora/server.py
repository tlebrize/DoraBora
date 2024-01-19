class BaseServer:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def run(self):
        raise NotImplementedError()

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
