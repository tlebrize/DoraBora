from dora_bora.shared_state import get_shared_state


class ChildLogic:
    def __init__(self, root):
        self.server_id = root.server_id
        self.inputs = root.inputs
        self.outputs = root.outputs
        self.db = root.db
        self.root = root
        self.shared = get_shared_state()
