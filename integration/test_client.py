import asyncio
import pytest
import pytest_asyncio
import os
import httpx
import redis.asyncio as redis


from dataclasses import dataclass

from crypt import crypt_password


@dataclass
class Config:
    LOGIN_PORT: int = int(os.environ.get("LOGIN_PORT"))
    GAME_PORT: int = int(os.environ.get("GAME_PORT"))
    MANAGEMENT_BASE_URL: str = os.environ.get("MANAGEMENT_BASE_URL")
    REDIS_URL: str = os.environ.get("REDIS_URL")


@pytest.fixture
def config():
    return Config()


@dataclass
class Client:
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

    async def read(self):
        return (await self.reader.readuntil(b"\0")).decode().strip("\0")

    async def write(self, message):
        self.writer.write(message.encode() + b"\0\n")
        await self.writer.drain()

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()


@pytest_asyncio.fixture
def login_client_factory(config):
    async def factory():
        reader, writer = await asyncio.open_connection("login", config.LOGIN_PORT)
        return Client(reader=reader, writer=writer)

    return factory


@pytest_asyncio.fixture
def game_client_factory(config):
    async def factory():
        reader, writer = await asyncio.open_connection("game", config.GAME_PORT)
        return Client(reader=reader, writer=writer)

    return factory


@pytest_asyncio.fixture
async def management_client(config):
    client = httpx.AsyncClient(base_url=config.MANAGEMENT_BASE_URL)
    response = (
        await client.request(
            "post",
            "/login/token/",
            json={"username": "test", "password": "test"},
        )
    ).json()
    client.headers["Authorization"] = "Token " + response.get("token")
    return client


@pytest_asyncio.fixture
async def exchange_client(config):
    class Client:
        redis = redis.from_url(config.REDIS_URL)
        pubsub = redis.pubsub()

    return Client()


async def quick_login_connect(login_client):
    # check policy
    msg = await login_client.read()
    assert len(msg) == 271

    # get key
    msg = await login_client.read()
    key = msg[2:]
    assert msg[:2] == "HC"
    assert len(key) == 32

    # send version
    await login_client.write("1.39.8e")
    return key


@pytest.mark.asyncio
async def test_login(login_client_factory, game_client_factory, management_client, exchange_client):
    login_client = await login_client_factory()

    # connect to login
    key = await quick_login_connect(login_client)

    # send username/password
    await login_client.write("test")
    await login_client.write(crypt_password("test", key))

    # account infos
    assert await login_client.read() == "Adtest"
    assert await login_client.read() == "Ac0"
    assert await login_client.read() == "AH1;1;110;0"
    assert await login_client.read() == "AlK0"
    assert await login_client.read() == "AQtest"

    await login_client.write("Ap5051")  # unhandled
    await login_client.write("Aioooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    await login_client.write("Ax")

    # read servers/characters (should be empty)
    package = await login_client.read()
    assert package.startswith("AxK")
    assert package.endswith("|1,0"), "Most likely test character still exists."

    # connect to server
    await login_client.write("AX1")
    assert await login_client.read() == "AYKlocalhost:5052;3"

    assert (await management_client.get("/login/account/3/")).json()["state"] == "in_login"
    await login_client.close()

    # connected to server
    game_client = await game_client_factory()
    assert await game_client.read() == "HG"
    await game_client.write("AT3")

    assert await game_client.read() == "ATK0"
    await game_client.write("Ak0")

    await game_client.write("AV")
    assert await game_client.read() == "AV0"

    await game_client.write("Agfr")

    # list characters
    await game_client.write("AL")
    package = await game_client.read()
    assert package.startswith("ALK")
    assert package.endswith("|0|")

    await game_client.write("Af")
    assert await game_client.read() == "Af1|1|1|1|1"

    # create new characters
    await game_client.write("AATest|1|0|0|0|16777215")
    assert await game_client.read() == "AAK"

    response = await management_client.get("/character/character/", params={"account_id": 3, "server_id": 1})
    character = response.json()[0]
    expected = {"account": 3, "server": 1, "_class": 1, "name": "Test"}
    for key, value in expected.items():
        assert character[key] == value
    character_id = character["id"]
    map_id = character["map"]

    # list charcaters
    package = await game_client.read()
    assert package.startswith("ALK")
    assert package.endswith(f"|1|{character_id};Test;1;10;0;0;ffffff;,,,,;0;1;0")

    # connect to game
    await game_client.write(f"AS{character_id}")
    assert await game_client.read() == "Rx0"
    assert await game_client.read() == f"ASK|{character_id}|Test|1|1|0|100|0|ffffff|"
    assert await game_client.read() == "ILS2000"
    assert await game_client.read() == "ZS-1"
    assert await game_client.read() == "cC+i*"
    assert await game_client.read() == "al|"
    assert await game_client.read() == "eL0|0"
    assert await game_client.read() == "AR6bk"
    assert await game_client.read() == "Ow0|999"
    assert (await game_client.read()).startswith("GDM|")
    assert await game_client.read() == "fC0"
    assert await game_client.read() == "FO-"
    assert await game_client.read() == "SL1~1~1;2~1~2;3~2~4;"
    assert await game_client.read() == "Im189"
    assert await game_client.read() == "Im0153;127.0.0.1"

    # character is on map
    assert await exchange_client.redis.sismember(f"server.1.map.{map_id}", character_id)

    # switch character
    await game_client.write(f"HS")
    # get switch token
    token = (await game_client.read())[2:]
    assert token
    await game_client.close()

    # reconnect to login
    login_client = await login_client_factory()
    key = await quick_login_connect(login_client)

    # login with token
    await login_client.write("#S")
    await login_client.write(token)
    assert await login_client.read() == "Adtest"

    # read extra infos
    await login_client.read()
    await login_client.read()
    await login_client.read()
    await login_client.read()

    await login_client.write("AX1")
    assert await login_client.read() == f"AYKlocalhost:5052;3"
    assert (await management_client.get("/login/account/3/")).json()["state"] == "in_login"
    await login_client.close()

    # reconnect to game
    game_client = await game_client_factory()
    assert await game_client.read() == "HG"
    await game_client.write("AT3")
    assert await game_client.read() == "ATK0"

    # Delete character
    await game_client.write(f"AD{character_id}|")
    package = await game_client.read()
    assert package.startswith("ALK")
    assert package.endswith("|0|")

    assert (await management_client.get("/login/account/3/")).json()["state"] == "in_game"
    response = await management_client.get("/character/character/", params={"account_id": 3, "server_id": 1})
    assert len(response.json()) == 0
