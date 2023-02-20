from dataclasses import dataclass
from enum import Enum


class ServerState(str, Enum):
    Offline = "offline"
    Online = "online"
    Maintenance = "maintenance"


@dataclass
class Server:
    id: int
    name: str
    host: str
    port: int
    state: ServerState
    subscriber_only: bool

    def format_state(self):
        if self.state == ServerState.Offline:
            return "0"
        elif self.state == ServerState.Online:
            return "1"
        elif self.state == ServerState.Maintenance:
            return "2"
        else:
            raise Exception(f"Invalid state for {self.id} : {self.state}.")


@dataclass
class ServerList:
    servers: [Server]

    def format_login_list(self):
        return "|".join([f"{s.id};{s.format_state()};110;1" for s in self.servers])


class AccountState(str, Enum):
    Offline = "offline"
    InLogin = "in_login"
    InGame = "in_game"
    Banned = "banned"


@dataclass
class Account:
    id: int
    username: str
    nickname: str
    password: str
    state: AccountState
    subscribed_seconds: int
    is_game_master: bool
    security_question: str

    def format_is_game_master(self):
        return str(int(self.is_game_master))

    def format_security_question(self):
        return self.security_question.replace(" ", "+")


class Character:
    id: int
    server_id: int
    server: Server
    account_id: int
    account: Account
