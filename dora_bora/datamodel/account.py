from dataclasses import dataclass
from enum import Enum


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
    community: int

    def format_is_game_master(self):
        return str(int(self.is_game_master))

    def format_security_question(self):
        return self.security_question.replace(" ", "+")

    def subscribed_milliseconds(self):
        return self.subscribed_seconds * 1000


@dataclass
class AccountList:
    accounts: [Account]
