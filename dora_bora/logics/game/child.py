class ChildLogic:
    def __init__(self, root):
        self.server_id = root.server_id
        self.inputs = root.inputs
        self.outputs = root.outputs
        self.db = root.db
        self.root = root
