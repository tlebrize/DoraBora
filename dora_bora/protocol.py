from twisted.protocols.basic import LineReceiver


class BaseProtocol(LineReceiver):
    delimiter = b"\n\0"

    def __init__(self, logic):
        self.logic = logic

    def write(self, message):
        print(f"SEND > [{self.logic.__class__.__name__}]\t{repr(message)}")
        self.transport.write(message.encode() + b"\0")

    def send_all(self):
        while message := self.logic.outputs.get():
            self.write(message)

    def connectionMade(self):
        self.logic.start()
        self.send_all()

    def lineReceived(self, message):
        print(f"< READ [{self.logic.__class__.__name__}]\t{repr(message.decode())}")
        self.logic.inputs.put(message.decode())
        while not self.logic.inputs.empty():
            self.logic.handle_input()
        self.send_all()
