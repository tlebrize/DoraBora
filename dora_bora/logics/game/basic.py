from dora_bora.logics.exceptions import NotHandled
import time

from .child import ChildLogic


class BasicLogic(ChildLogic):
    def handle_input(self, message):
        if message.startswith("D"):
            return self.send_date()
        raise NotHandled(message)

    def send_date(self):
        date = int(time.time() * 1000) + 3600000 * 2
        # timezone kekw
        self.outputs.put(f"BT{date}")
