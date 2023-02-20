import asyncio
import windyquery
from datamodel import (
    ServerState,
    Server,
    ServerList,
    AccountState,
    Account,
    Character,
)


async def get_db(name):
    db = windyquery.DB()
    await db.connect(
        name,
        {
            "host": "localhost",
            "port": "5432",
            "database": name,
            "username": "postgres",
            "password": "password",
        },
        default=True,
    )
    return db


async def get_account(db, username=None):
    base = db.table("accounts").select()
    if username:
        data = await base.where("username", username)
    else:
        return None
    return Account(**data[0])


async def list_servers(db):
    return ServerList(
        servers=[Server(**row) for row in await db.table("servers").select()]
    )
