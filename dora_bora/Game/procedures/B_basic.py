import time


async def basic_handler(s, command):
    match command[0]:
        case "D":
            await s.write(f"BT{int(time.time() * 1000) + 3600000 * 2}")
