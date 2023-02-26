import string
import random

from dora_bora.constants import POLICY
from dora_bora.non_blocking_queue import NonBlockingQueue
from dora_bora.database_accessor import DatabaseAccessor
from dora_bora.datamodel import AccountState

from .exceptions import AccountNotFound, InvalidVersion, ServerNotFound


class LoginLogic:
    def __init__(self):
        self.inputs = NonBlockingQueue()
        self.outputs = NonBlockingQueue()
        self.db = DatabaseAccessor()
        self.step = 0

    def start(self):
        self.send_policy()
        self.generate_key()
        self.send_key()

    def handle_input(self):
        if self.step == 0:
            self.read_version()
            self.validate_version()
            self.step += 1
        elif self.step == 1:
            self.read_login()
            self.validate_login()
            self.send_login_info()
            self.step += 1
        else:
            self.handle_server_input()

    def send_policy(self):
        self.outputs.put(POLICY)

    def generate_key(self):
        self.key = "".join(random.choices(string.ascii_lowercase, k=32))

    def send_key(self):
        self.outputs.put("HC" + self.key)

    def read_version(self):
        self.version = self.inputs.get()

    def validate_version(self):
        if self.version != "1.29.1":
            raise InvalidVersion(self.version)

    def read_login(self):
        self.username, password_hash = self.inputs.get().split()
        # check #1
        self.password_hash = password_hash[2:]

    def validate_login(self):
        self.account = self.db.accounts.get_by("username", self.username)
        if not self.account:
            raise AccountNotFound(self.username)

    def send_login_info(self):
        servers = self.db.servers.list()
        login_packets = [
            "Ad" + self.account.nickname,
            "Ac" + str(self.account.community),
            "AH" + servers.format_login_list(),
            "AlK" + self.account.format_is_game_master(),
            "AQ" + self.account.format_security_question(),
        ]
        self.outputs.put("\0".join(login_packets))

    def handle_server_input(self):
        msg = self.inputs.get()
        if msg == "Af":
            self.outputs.put("Af0|0|0|1|-1")
            # login queue is disabled.
        elif msg == "Ax":
            self.send_server_list()
        elif msg[:2] == "AX":
            self.send_server_connection(int(msg[2:]))
        # if msg == "AF":
        #     pass
        #     # Friend list
        else:
            print("not handled", msg)

    def send_server_list(self):
        if self.account.subscribed_seconds:
            subscribed = str(self.account.subscribed_milliseconds()) + "|"
        else:
            subscribed = ""

        server_characters = "|".join(
            [
                f"{server_id},{count}"
                for (server_id, count) in self.db.servers.count_characters(
                    self.account.id
                )
            ]
        )

        self.outputs.put("AxK" + subscribed + server_characters)

    def send_server_connection(self, id_):
        server = self.db.servers.get(id_)
        if not server:
            raise ServerNotFound(id_)
        self.outputs.put("AYK" + server.format_connection())
        self.db.accounts.set(self.account.id, "state", AccountState.InLogin)
