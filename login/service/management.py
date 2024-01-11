import httpx

from service.datamodel import Account, AccountState, ServerList, Server
from service.helpers import api_error_logger


class Management:
    def __init__(self, config):
        self.config = config
        self.client = httpx.AsyncClient(base_url=config.MANAGEMENT_BASE_URL)
        self.account = None
        self.servers = []

    async def request(self, method, path, json=None):
        if json:
            print(f"$ {method}:{path}  {json}")
            response = await getattr(self.client, method)(path, json=json)
        else:
            print(f"$ {method}:{path}")
            response = await getattr(self.client, method)(path)

        response.raise_for_status()
        return response.json()

    @api_error_logger
    async def password_login(self, username, password):
        response = await self.request("post", "/login/token/", json={"username": username, "password": password})
        self.token = response.get("token")
        if not self.token:
            raise Exception("Login failed.")
        self.client.headers["Authorization"] = f"Token {self.token}"

        return True

    @api_error_logger
    async def switch_login(self, switch_token):
        response = await self.request("post", "/login/switch/", json={"switch_token": switch_token})
        self.token = response.get("token")
        if not self.token:
            raise Exception("Login failed.")
        self.client.headers["Authorization"] = f"Token {self.token}"

        return True

    @api_error_logger
    async def get_account(self, force=False):
        if (not self.account) or force:
            response = await self.request("get", "/login/account/me/")
            self.account = Account(**response)
        return self.account

    @api_error_logger
    async def list_servers(self, force=False):
        if (not self.servers) or force:
            response = await self.request("get", "/login/server/")
            self.servers = ServerList(
                [Server(**data) for data in response],
            )
        return self.servers

    @api_error_logger
    async def set_account_in_login(self):
        account_id = (await self.get_account()).id
        await self.request(
            "patch",
            f"/login/account/{account_id}/",
            json={"state": AccountState.IN_LOGIN.value},
        )

    @api_error_logger
    async def set_account_switch_token(self, token):
        account_id = (await self.get_account()).id
        await self.request(
            "patch",
            f"/login/account/{account_id}/",
            json={"switch_token": token},
        )
