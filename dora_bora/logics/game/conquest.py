from .child import ChildLogic
from dora_bora.logics.exceptions import InvalidWorldInfo, NotHandled


class ConquestLogic(ChildLogic):
    def handle_input(self, message):
        if message.startswith("W"):
            return self.send_world_info(message[1:])
        raise NotHandled(message)

    def send_world_info(self, data):
        if data == "J" or data == "V":
            CW = "CW|0|10"  # PrismesGeoposition
            self.outputs.put(CW)  # Bontarians
            self.outputs.put(CW)  # Brakmarians
            return
        raise InvalidWorldInfo(data)
