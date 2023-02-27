from dora_bora.logics.exceptions import InvalidAccountState, NotHandled
from dora_bora.datamodel import Gender, Class, AccountState
from dora_bora.shared_state import get_shared_state

from .child import ChildLogic


class AccountLogic(ChildLogic):
    def handle_input(self, message):
        if message.startswith("T"):
            return self.handle_connect(message[1:])
        elif message.startswith("k"):
            return  # setKeyIndex ?
        elif message.startswith("V"):
            return self.outputs.put("AV0")  # RegionalVersion ?
        elif message.startswith("g"):
            self._language = message[1:]
            return
            # then getGifts ?
        elif message.startswith("i"):
            self._identity = message[1:]
            return
        elif message.startswith("L"):
            return self.send_characters_list()
        elif message.startswith("f"):
            return self.send_queue_position()
        elif message.startswith("A"):
            return self.handle_add_character(message[1:])
        elif message.startswith("D"):
            return self.handle_delete_character(message[1:])
        elif message.startswith("S"):
            return self.handle_join_game(message[1:])
        raise NotHandled(message)

    def handle_connect(self, data):
        self.root.account = self.db.accounts.get(int(data))
        if self.root.account.state != AccountState.InLogin:
            raise InvalidAccountState(self.root.account.state)
        self.outputs.put("ATK0")
        self.db.accounts.set(self.root.account.id, "state", AccountState.InGame)

    def send_characters_list(self):
        characters = self.db.characters.list_for_account(self.root.account.id)

        self.outputs.put(
            "ALK"
            + "|".join(
                map(
                    str,
                    [
                        self.root.account.subscribed_milliseconds(),
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
                "account_id": self.root.account.id,
                "name": name,
                "gender": Gender(int(gender)),
                "class_": Class(int(class_)),
                "colors": [int(c1), int(c2), int(c3)],
                "kamas": 0,
                "spell_points": 0,
                "stat_points": 0,
                "energy": 0,
                "level": 1,
                "experience": 0,
            }
        )
        self.outputs.put("AAK")  # create perso ok
        self.send_characters_list()

    def handle_delete_character(self, data):
        id_, answer = data.split("|")
        if self.db.characters.where(
            "id = %(id)s AND account_id = %(account_id)s",
            {"id": id_, "account_id": self.root.account.id},
        ).count():
            # check question before delete
            self.db.characters.delete(id_)
            self.send_characters_list()
        else:
            self.outputs.put("ADE")

    def handle_join_game(self, data):
        id_ = int(data)
        self.root.character = self.db.characters.get(id_)
        c = self.root.character
        # check seller ?
        # check mount
        self.outputs.put("Rx0")  # mount exp
        self.outputs.put(
            f"ASK|{c.id}|{c.name}|{c.level}|{c.class_}|{c.gender}|"
            f"{c.get_gfxid()}" + "|".join(map(str, c.get_colors())) + "|"
            # Items
        )
        # check fight
        self.outputs.put("ILS2000")  # No fight
        # check jobs
        self.outputs.put("ZS-1")  # Alignment neutral
        self.outputs.put("cC+i*")  # chats enabled
        # check guild
        self.outputs.put("al|")  # Zone alignment
        self.outputs.put("eL0|0")  # Emotes
        self.outputs.put("AR6bk")  # Restrictions
        self.outputs.put(c.format_pods())  # used_pods|max_pods
        self.root.map = self.db.maps.get(c.map_id)
        self.outputs.put(self.root.map.format_map_data())
        self.shared.characters.move_to_map(c.id, self.root.map.id)
        self.shared.characters.move_to_cell(c.id, 210)
        self.outputs.put("fC0")  # fight counts
        self.outputs.put("FO-")  # - = don't see friend connection / +
        self.outputs.put("SL1~1~1;2~1~2;3~2~4;")  # Spell list id~level~placement;
        self.outputs.put("Im189")  # Welcome message, non-existant
        self.outputs.put("Im0153;127.0.0.1")  # IP msg
