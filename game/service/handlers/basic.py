import time


async def basic_handler(service, command):
    match command[0]:
        case "D":
            await service.write(f"BT{int(time.time() * 1000) + 3600000 * 2}")
