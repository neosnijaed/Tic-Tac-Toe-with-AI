from enum import Enum, auto


class Status(Enum):
    """Enums for start and exit status."""
    START = auto()
    EXIT = auto()


class Mode(Enum):
    """Enums for Ai difficulty."""
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
