import random
import string
import asyncio

from constants import POLICY


class LoginLogic:
    def __init__(self):
        self.outputs = asyncio.Queue()

    async def read(self):
        data = await self.stream.read_until(b"\n")
        cleaned = data.strip(b"\x00").strip().decode()
        print("READ\t-", repr(cleaned))
        return cleaned

    async def run(self, stream):
        self.stream = stream
        await self.outputs.put(POLICY)
        self.key = "".join(random.choices(string.ascii_lowercase, k=32))
        await self.outputs.put("HC" + self.key)
        version = await self.read()
        username = await self.read()
        password = await self.read()
        await asyncio.sleep(0.5)
        login_packets = [
            "Ad" + "pls" + username,
            # "Ad" + self.account.nickname,
            "Ac0",
            # "AH" + self.servers.format_login_list(),
            "AH0;0;110;1|1;1;110;1|2;2;110;1|3;3;110;1|4;4;110;1",
            # "AlK" + self.account.format_is_game_master(),
            "AlK0",
            # "AQ" + self.account.format_security_question(),
            "AQsecurity+Question",
        ]
        await self.outputs.put("\x00".join(login_packets))
        action = await self.read()
        for _ in range(2):
            if action == "Af":
                await self.outputs.put("Af1|1|1|0|1")
            elif action == "Ax":
                raise Exception("Failed successfully !")
            action = await self.read()

        raise Exception("Nope")


"""
for some reason sleeping on line 26 is the issue:
WRITE   - 'HCtpcsloxxrjvhtzkofyuqtpjboqglzacb'
READ    - '1.29.1'
READ    - 'qwe'
READ    - '#17133PO60ZZ10'
READ    - 'Af'
READ    - 'Af'
READ    - 'Af'
WRITE   - 'Adplsqwe\x00Ac0\x00AH0;0;110;1|1;1;110;1|2;2;110;1|3;3;110;1|4;4;110;1\x00AlK0\x00AQsecurity+Question'
WRITE   - 'Af1|1|1|0|1'
WRITE   - 'Af1|1|1|0|1'
-> Nope
"""
