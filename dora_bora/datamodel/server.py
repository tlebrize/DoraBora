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

    def format_connection(self):
        return f"{self.host}:{self.port};{self.format_state()}"


@dataclass
class ServerList:
    servers: [Server]

    def format_login_list(self):
        return "|".join([f"{s.id};{s.format_state()};110;0" for s in self.servers])
