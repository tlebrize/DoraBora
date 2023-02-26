from dora_bora.logics.exceptions import InvalidAccountState
from dora_bora.datamodel import Gender, Class, AccountState


class AccountLogic:
    def __init__(self, parent):
        self.server_id = parent.server_id
        self.inputs = parent.inputs
        self.outputs = parent.outputs
        self.db = parent.db

    def handle_input(self, message):
        if message.startswith("T"):
            self.account = self.db.accounts.get(int(message[1:]))
            if self.account.state != AccountState.InLogin:
                raise InvalidAccountState(self.account.state)
            self.outputs.put("ATK0")
            self.db.accounts.set(self.account.id, "state", AccountState.InGame)

        elif message.startswith("k"):
            pass  # setKeyIndex ?
        elif message.startswith("V"):
            self.outputs.put("AV0")  # RegionalVersion ?
        elif message.startswith("g"):
            self._language = message[1:]
            # then getGifts ?
        elif message.startswith("i"):
            self._identity = message[1:]
        elif message.startswith("L"):
            self.send_characters_list()
        elif message.startswith("f"):
            self.send_queue_position()
        elif message.startswith("A"):
            self.handle_add_character(message[1:])
        elif message.startswith("D"):
            self.handle_delete_character(message[1:])
        else:
            exit(0)

    def send_characters_list(self):
        characters = self.db.characters.list_for_account(self.account.id)

        self.outputs.put(
            "ALK"
            + "|".join(
                map(
                    str,
                    [
                        self.account.subscribed_milliseconds(),
                        characters.count(),
                        characters.format_alk(),
                    ],
                )
            )
        )

    def send_queue_position(self):
        self.outputs.put(f"Af1|1|1|1|{self.server_id}")
        # position|totalAbo|totalNonAbo|button?
        # unused ?

    def handle_add_character(self, data):
        name, class_, gender, c1, c2, c3 = data.split("|")
        # check name
        self.db.characters.create(
            {
                "server_id": self.server_id,
                "account_id": self.account.id,
                "name": name,
                "gender": Gender(int(gender)),
                "class_": Class(int(class_)),
                "colors": [int(c1), int(c2), int(c3)],
                "kamas": 0,
                "spell_points": 0,
                "stat_points": 0,
                "energy": 0,
                "level": 1,
                "xp": 0,
            }
        )
        self.outputs.put("AAK")  # create perso ok
        self.send_characters_list()

    def handle_delete_character(self, data):
        id_, answer = data.split("|")
        if self.db.characters.where(
            "id = %(id)s AND account_id = %(account_id)s",
            {"id": id_, "account_id": self.account.id},
        ).count():
            # check question before delete
            self.db.characters.delete(id_)
            self.send_characters_list()
        else:
            self.outputs.put("ADE")
