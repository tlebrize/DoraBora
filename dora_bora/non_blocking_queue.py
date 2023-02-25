from queue import Queue, Empty


class NonBlockingQueue(Queue):
    def get(self):
        try:
            return super().get(block=False)
        except Empty:
            return None

    def put(self, msg):
        return super().put(msg, block=False)
