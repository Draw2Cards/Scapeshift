from enum import Enum


class Outcome(Enum):
    UNRESOLVED = -1
    WIN = 0
    LOSE = 1


class GameState:
    def __init__(self, first=True):
        self.first = first
        self.turn_counter = 0
        self.outcome = Outcome.UNRESOLVED
