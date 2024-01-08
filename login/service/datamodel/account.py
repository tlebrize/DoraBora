from dataclasses import dataclass
from enum import Enum


class AccountState(str, Enum):
    OFFLINE = "offline"
    IN_LOGIN = "in_login"
    IN_GAME = "in_game"
    BANNED = "banned"


@dataclass
class Account:
    id: int
    username: str
    nickname: str
    state: AccountState
    subscribed_seconds: int
    is_game_master: bool
    security_question: str
    community: str
    switch_token: str

    def format_is_game_master(self):
        return str(int(self.is_game_master))

    def format_security_question(self):
        return self.security_question.replace(" ", "+")

    def subscribed_milliseconds(self):
        return self.subscribed_seconds * 1000


@dataclass
class AccountList:
    accounts: [Account]
