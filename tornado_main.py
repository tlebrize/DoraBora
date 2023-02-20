import tornado
import asyncio

from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.netutil import bind_sockets
from login_logic import LoginLogic, ActionModes

from constants import EOM
import database as db


class LoginServer(TCPServer):
    async def handle_stream(self, stream, address):
        database = await db.get_db("dora_bora")
        logic = LoginLogic(database)

        while logic.running:
            if logic.mode == ActionModes.SEND:
                for message in await logic.send():
                    print("<", repr(message))
                    await stream.write(message.encode() + EOM)

            elif logic.mode == ActionModes.READ:
                data = await stream.read_until(b"\n")
                cleaned = data.strip(b"\x00").strip().decode()
                print(">", repr(cleaned))
                await logic.read(cleaned)

            else:
                print("Logic exited.")
                break


sockets = bind_sockets(4444)
tornado.process.fork_processes(0)


async def post_fork_main():
    server = LoginServer()
    server.add_sockets(sockets)
    await asyncio.Event().wait()


asyncio.run(post_fork_main())
