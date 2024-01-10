import asyncio, httpx

from service.service import Service
from service.config import Config
from service.datamodel.server import ServerState


async def set_server_state(state):
    c = Config()
    async with httpx.AsyncClient(
        base_url=c.MANAGEMENT_BASE_URL,
        headers={"Authorization": f"Token {c.SERVER_TOKEN}"},
    ) as client:
        response = await client.patch(f"/login/server/{c.SERVER_ID}/", json={"state": state})
        response.raise_for_status()
        print("Set state :", state)


async def create_service(reader, writer):
    service = Service(reader, writer, Config())
    await service.on_connect()


async def run_server():
    print("Starting game server.")
    await set_server_state(ServerState.ONLINE)
    try:
        server = await asyncio.start_server(create_service, "0.0.0.0", Config().SERVER_PORT)
        async with server:
            await server.serve_forever()
    finally:
        await set_server_state(ServerState.OFFLINE)  # this does not work


asyncio.run(run_server(), debug=True)
