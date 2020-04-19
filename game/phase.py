from game.game_state import Outcome
from game.step import StepCleanup, StepCombatBeginning, StepCombatDamage, StepCombatEnd, StepDeclareAttackers, \
    StepDeclareBlockers, StepDraw, StepEnd, StepUntap, StepUpkeep


class Phase:
    def __init__(self, zones, game_state, player):
        self.zones = zones
        self.game_state = game_state
        self.player = player

    def run(self):
        raise NotImplementedError('Not Implemented Error!')


class PhaseBeginning(Phase):
    def __int__(self, zones, game_state, player):
        super().__init__(zones, game_state, player)
        self.steps = [StepUntap(zones), StepUpkeep(), StepDraw()]

    def run(self):
        for s in self.steps:
            s.run()
            if self.game_state.outcome != Outcome.UNRESOLVED:
                break


class PhasePrecombatMain(Phase):
    def run(self):
        self.player.precombat_main_phase()


class PhaseCombat(Phase):
    def __int__(self, zones, game_state, player):
        super().__init__(zones, game_state, player)
        self.steps = [StepCombatBeginning(),
                      StepDeclareAttackers(),
                      StepDeclareBlockers(),
                      StepCombatDamage(),
                      StepCombatEnd()]

    def run(self):
        for s in self.steps:
            s.run()
            if self.game_state.outcome != Outcome.UNRESOLVED:
                break


class PhasePostcombatMain(Phase):
    def run(self):
        self.player.postcombat_main_phase()


class PhaseEnding(Phase):
    def __int__(self, zones, game_state, player):
        super().__init__(zones, game_state, player)
        self.steps = [StepEnd(), StepCleanup()]

    def run(self):
        for s in self.steps:
            s.run()
            if self.game_state.outcome != Outcome.UNRESOLVED:
                break
