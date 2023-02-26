from .base import BaseDatabase

from dora_bora.datamodel import Character, CharacterList


class CharactersDatabase(BaseDatabase):
    table = "characters"
    model = Character
    list_model = CharacterList

    def list_for_account(self, account_id):
        return self.list_model(
            [
                self.model(**row)
                for row in self.execute(
                    "SELECT * FROM characters WHERE account_id = %s;",
                    [account_id],
                )
            ]
        )
