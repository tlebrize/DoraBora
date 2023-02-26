import os
from dotenv import load_dotenv
from twisted.internet.protocol import Factory
from twisted.internet import reactor

from dora_bora.logics import LoginLogic, GameLogic
from dora_bora.protocol import BaseProtocol
from dora_bora.database import ServersDatabase
from dora_bora.datamodel import ServerState


class LoginFactory(Factory):
    def buildProtocol(self, addr):
        return BaseProtocol(LoginLogic())


class GameFactory(Factory):
    def __init__(self, server_id):
        self.server_id = server_id
        self.servers_db = ServersDatabase()
        self.servers_db.set(self.server_id, "state", ServerState.Online)

    def __del__(self):
        self.servers_db.set(self.server_id, "state", ServerState.Offline)

    def buildProtocol(self, addr):
        return BaseProtocol(GameLogic(self.server_id))


def main():
    login_port = int(os.getenv("LOGIN_PORT"))
    game_port = int(os.getenv("GAME_PORT"))
    print("Starting login on port", login_port)
    reactor.listenTCP(login_port, LoginFactory())
    print("Starting game #1 on port", game_port)
    reactor.listenTCP(game_port, GameFactory(1))
    reactor.run()


if __name__ == "__main__":
    load_dotenv()
    main()
