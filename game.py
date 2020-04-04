from enum import Enum


class Outcome(Enum):
    UNRESOLVED = -1
    WIN = 0
    LOSE = 1


class Game:
    def __init__(self, zones):
        self.zones = zones
        self.outcome = Outcome.UNRESOLVED
        self.turn_counter = 0

    def play(self):
        self.prepare()
        while self.outcome is Outcome.UNRESOLVED:
            self.turn()

    def prepare(self):
        pass

    def turn(self):
        self.turn_counter += 0
        self.beginning_phase()
        self.main_phase()
        self.combat_phase()
        self.main_phase()
        self.ending_phase()

    def beginning_phase(self):
        self.untap_step()
        self.upkeep_step()
        self.draw_step()

    def untap_step(self):
        pass

    def upkeep_step(self):
        pass

    def draw_step(self):
        pass
