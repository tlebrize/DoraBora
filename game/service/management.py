import httpx

from service.datamodel import (
    Account,
    AccountState,
    ServerList,
    Server,
    CharacterList,
    Character,
    Map,
)


class Management:
    def __init__(self, config):
        self.config = config
        self.client = httpx.AsyncClient(base_url=config.MANAGEMENT_BASE_URL)
        self.server_id = config.SERVER_ID
        self.account = None
        self.character_list = []
        self.current_character = None
        self.current_map = None

    async def login(self, username, password):
        response = await self.client.post(
            "/login/token/",
            json={"username": username, "password": password},
        )
        response.raise_for_status()
        self.token = response.json().get("token")
        if not self.token:
            raise Exception("Login failed.")
        self.client.headers["Authorization"] = f"Token {self.token}"

        return True

    async def get_account(self, force=False):
        if (not self.account) or force:
            response = await self.client.get("/login/account/me/")
            response.raise_for_status()
            self.account = Account(**response.json())
        return self.account

    async def set_account_state(self, state):
        account_id = (await self.get_account()).id
        response = await self.client.patch(f"/login/account/{account_id}/", json={"state": state})
        response.raise_for_status()

    async def get_account_by_id(self, account_id):
        # Insecure
        response = await self.client.get(f"/login/account/{account_id}/")
        response.raise_for_status()
        self.account = Account(**response.json())
        return self.account

    async def list_characters(self, force=False):
        if (not self.character_list) or force:
            account_id = (await self.get_account()).id
            response = await self.client.get(
                f"/character/character/?account_id={account_id}&server_id={self.server_id}"
            )
            response.raise_for_status()
            self.character_list = CharacterList([Character(**data) for data in response.json()])

        return self.character_list

    async def set_current_character(self, character_id, force=False):
        if (not self.character_list) or force:
            await self.list_characters(force=force)

        for character in self.character_list.characters:
            if character.id == character_id:
                self.current_character = character
                break

        return self.current_character

    async def set_current_map(self, map_id):
        response = await self.client.get(f"/map/map/{map_id}/")
        response.raise_for_status()
        self.current_map = Map(**response.json())
        return self.current_map

    async def create_character(self, name, gender, _class, colors):
        data = {
            "server": self.server_id,
            "account": self.account.id,
            "name": name,
            "gender": gender,
            "_class": _class,
            "colors": colors,
        }
        response = await self.client.post(f"/character/character/", json=data)
        response.raise_for_status()
        self.character = Character(**response.json())
        self.character_list = []
