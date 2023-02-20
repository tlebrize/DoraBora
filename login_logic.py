import asyncio
import string
import random

from constants import POLICY
import database as db

database = {
    "servers": {
        "DoraBora": {"qwe": ["foo"]},
    },
    "users": {
        "qwe": 1000000,
    },
}


class LogicException(BaseException()):
    ...


class ActionModes:
    READ = "READ"
    SEND = "SEND"
    EXIT = "EXIT"


class LoginLogic(object):
    def __init__(self):
        self.tree = {
            "send_policy": "send_key",
            "send_key": "read_version",
            "read_version": "read_username",
            "read_username": "read_password",
            "read_password": "send_login",
            "send_login": "read_server_commands",
            "read_server_commands": "read_server_commands",
            "command_queue_info": "send_login",
            "command_friends": "read_server_commands",
            "command_character_server_map": "read_server_commands",
            "command_send_server_info": "exit",
            "exit": "exit",
        }
        self.next_step = "send_policy"
        self.mode = ActionModes.SEND
        self.running = True
        self.client = {}
        self.af_count = 0

    def _get_step(self):
        print("performing:", self.next_step)
        step = getattr(self, self.next_step)
        self.next_step = self.tree[self.next_step]
        return step

    async def send(self):
        step = self._get_step()
        return await step()

    async def read(self, message):
        step = self._get_step()
        return await step(message)

    async def exit(self, message):
        print("Exiting on:", message)
        exit(0)

    async def send_policy(self):
        self.mode = ActionModes().SEND
        return [POLICY]

    async def send_key(self):
        key = "".join(random.choices(string.ascii_lowercase, k=32))
        self.client["key"] = key
        self.mode = ActionModes().READ
        return [f"HC{key}"]

    async def read_version(self, version):
        self.mode = ActionModes().READ

    async def read_username(self, username):
        self.username = username
        # self.account = await db.get_account(self.db, username=self.username)
        # print("INFO\t- Logging account: ", self.account.__dict__)
        self.mode = ActionModes().READ

    async def read_password(self, password):
        if password.startswith("#1"):
            password = password[2:]
        self.password = password

        # assume password is valid
        self.mode = ActionModes().SEND

    async def send_login(self):
        # self.servers = await db.list_servers(self.db)
        packets = "\x00".join(
            [
                "Ad" + "pls" + self.username,
                # "Ad" + self.account.nickname,
                "Ac0",
                # "AH" + self.servers.format_login_list(),
                "AH0;0;110;1|1;1;110;1|2;2;110;1|3;3;110;1|4;4;110;1",
                # "AlK" + self.account.format_is_game_master(),
                "AlK0",
                # "AQ" + self.account.format_security_question(),
                "AQsecurity+Question",
            ]
        )
        self.mode = ActionModes().READ
        return [packets]

    async def read_server_commands(self, command):
        print("server_command:", command)
        if command == "Af":
            self.af_count += 1
            if self.af_count > 3:
                exit(0)
            self.next_step = "command_queue_info"
            self.mode = ActionModes().SEND
        elif command == "Ax":
            self.next_step = "command_character_server_map"
            self.mode = ActionModes().SEND
        elif command.startswith("AX"):
            self.selected_server_id = int(command[2:])
            self.next_step = "command_send_server_info"
            self.mode = ActionModes().SEND
        if command == "AF":
            self.next_step = "command_friends"
            self.mode = ActionModes().SEND
        else:
            print(command)

    async def command_friends(self):
        self.mode = ActionModes().READ
        return ["AF0,1"]

    async def command_queue_info(self):
        self.mode = ActionModes().SEND
        return ["Af1|1|1|0|1"]

    async def command_character_server_map(self):
        subscribed_remaining = database["users"].get(self.username, 0)
        server_list = [str(subscribed_remaining)]

        for index, (server, users) in enumerate(database["servers"].items()):
            if self.username in users.keys():
                character_count = len(users[self.username])
                server_list.append(f"{index},{character_count}")

        self.mode = ActionModes().READ
        return ["AxK" + "|".join(server_list)]

    async def command_send_server_info(self):
        print(self.selected_server_id)
        self.running = False
        self.mode = ActionModes().EXIT
        return [f"AYK127.0.0.1:4445;1"]
