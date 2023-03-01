from dora_bora.non_blocking_queue import NonBlockingQueue
from dora_bora.database_accessor import DatabaseAccessor


class BaseLogic:
    def __init__(self):
        self.inputs = NonBlockingQueue()
        self.outputs = NonBlockingQueue()
        self.db = DatabaseAccessor()

    def end(self):
        pass

    def start(self):
        pass

    def register(self, protocol):
        self._protocol = protocol

    def flush(self):
        self._protocol.send_all()
