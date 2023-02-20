import tornado
import asyncio
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.netutil import bind_sockets

from login_logic_v2 import LoginLogic
from constants import EOM


class LoginServer(TCPServer):
    async def handle_stream(self, stream, address):
        print(stream, address)
        self.stream = stream
        self.address = address
        self.logic = LoginLogic()
        await asyncio.gather(
            self.write_forever(),
            self.logic.run(self.stream),
        )

    async def write_forever(self):
        print("Ready to write.")
        while True:
            message = await self.logic.outputs.get()
            print("WRITE\t-", repr(message))
            await self.stream.write(message.encode() + EOM)


sockets = bind_sockets(4444)
tornado.process.fork_processes(0)


async def post_fork_main():
    server = LoginServer()
    server.add_sockets(sockets)
    await asyncio.Event().wait()


asyncio.run(post_fork_main())
