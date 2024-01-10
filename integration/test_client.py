import asyncio
import pytest
import pytest_asyncio
import os

from dataclasses import dataclass


@dataclass
class Config:
    LOGIN_PORT: str = os.environ.get("LOGIN_PORT")


@dataclass
class Client:
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

    async def read(self):
        return (await self.reader.readuntil(b"\0")).decode()

    async def write(self, message):
        await self.writer.write(message.encode() + b"\0\n")


@pytest_asyncio.fixture
async def login_client():
    config = Config()
    reader, writer = await asyncio.open_connection("login", config.LOGIN_PORT)
    return Client(reader, writer)


@pytest.mark.asyncio
async def test_login(login_client):
    # check policy
    msg = await login_client.read()
    assert len(msg) == 272

    # get key
    msg = await login_client.read()
    key = msg[2:]
    assert msg[:2] == "HC"
    assert len(key) == 33

    # send version
    await login_client.write("1.39.8e")

    # send username/password
    await login_client.write("test")
    await login_client.write("#1" + encode_password(key, "test"))
