import httpx

from service.datamodel import Account, AccountState, ServerList, Server


class Management:
    def __init__(self, config):
        self.config = config
        self.client = httpx.AsyncClient(base_url=config.MANAGEMENT_BASE_URL)
        self.account = None
        self.servers = []

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

    async def list_servers(self, force=False):
        if (not self.servers) or force:
            response = await self.client.get("/login/server/")
            response.raise_for_status()
            self.servers = ServerList(
                [Server(**data) for data in response.json()],
            )
        return self.servers

    async def set_account_in_login(self):
        account_id = (await self.get_account()).id
        response = await self.client.patch(f"/login/account/{account_id}/", json={"state": AccountState.IN_LOGIN})
        response.raise_for_status()
