import enum

class MemoryCellState(enum.Enum):
    NEVER_USED = enum.auto()
    STALE = enum.auto()
    SELECTED = enum.auto()
