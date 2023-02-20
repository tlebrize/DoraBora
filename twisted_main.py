import asyncio
from twisted.internet import asyncioreactor

asyncioreactor.install(asyncio.get_event_loop())
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor

from login_logic import LoginLogic
from constants import POLICY, EOM
from database import get_db


class LoginProtocol(Protocol):
    def __init__(self, logic):
        self.logic = logic

    async def connectionMade(self):
        self.logic.db = await get_db("dora_bora")
        self.transport.write(POLICY.encode() + EOM)

    async def dataReceived(self, data):
        print(data)


class LoginFactory(Factory):
    def buildProtocol(self, addr):
        return LoginProtocol(LoginLogic())


def main():
    factory = LoginFactory()
    reactor.listenTCP(4444, factory)
    print("Twisted TCP server running on PORT#4444")
    reactor.run()


if __name__ == "__main__":
    main()
