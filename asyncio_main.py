import asyncio
import random
import string
from constants import POLICY, EOM

class TestProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        self.transport.write(POLICY.encode() + EOM)
        self.transport.write("".join(random.choices(string.ascii_lowercase, k=32)).encode() + EOM)

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Close the client socket')
        self.transport.close()


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 4444)

    print('serving on 4444')
    async with server:
        await server.serve_forever()


asyncio.run(main())