from dataclasses import dataclass
from enum import Enum


class ServerState(str, Enum):
    OFFLINE = "offline"
    ONLINE = "online"
    MAINTENANCE = "maintenance"


@dataclass
class Server:
    id: int
    name: str
    host: str
    port: int
    state: ServerState
    subscriber_only: bool
    character_count: int

    def format_state(self):
        if self.state == ServerState.OFFLINE:
            return "0"
        elif self.state == ServerState.ONLINE:
            return "1"
        elif self.state == ServerState.MAINTENANCE:
            return "2"
        else:
            raise Exception(f"Invalid state for {self.id} : {self.state}.")

    def format_connection(self):
        return f"{self.host}:{self.port};{self.format_state()}"


@dataclass
class ServerList:
    servers: [Server]

    def format_login_list(self):
        return "|".join([f"{s.id};{s.format_state()};110;1" for s in self.servers])
