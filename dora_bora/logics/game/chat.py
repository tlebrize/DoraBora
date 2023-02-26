from dora_bora.logics.exceptions import NotHandled
from .child import ChildLogic


class ChatLogic(ChildLogic):
    def handle_input(self, message):
        if message.startswith("C"):
            data = message[1:]
            if data == "NaN":
                return
            elif data[0] == "+":
                return self.add_channel(data[1:])
            elif data[0] == "-":
                return self.remove_channel(data[1:])
        raise NotHandled(message)

    def add_channel(self, channel):
        pass

    def remove_channel(self, channel):
        pass
