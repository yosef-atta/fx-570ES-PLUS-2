"""Calculator action definitions independent of Qt."""
from dataclasses import dataclass
from enum import Enum, auto

class Kind(Enum):
    INSERT = auto()
    COMMAND = auto()
    DEFERRED = auto()

@dataclass(frozen=True)
class Action:
    name: str
    kind: Kind
    text: str = ""

    @classmethod
    def insert(cls, value: str) -> "Action":
        return cls("insert", Kind.INSERT, value)

    @classmethod
    def command(cls, name: str) -> "Action":
        return cls(name, Kind.COMMAND)

    @classmethod
    def deferred(cls, name: str) -> "Action":
        return cls(name, Kind.DEFERRED)
