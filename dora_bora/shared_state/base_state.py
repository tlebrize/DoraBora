from dataclasses import dataclass


@dataclass
class BaseState:
    root: ...

    def __getattr__(self, name):
        if name.isupper():
            return getattr(self.root, name.lower())
        else:
            super().__getattribute__(name)
