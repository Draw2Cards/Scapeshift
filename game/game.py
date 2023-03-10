from game.game_state import Outcome
from game.phase import PhaseBeginning, PhaseEnding, PhasePrecombatMain, PhasePostcombatMain, PhaseCombat
from logger import Logger

class Game:
    def __init__(self, zones, game_state, player):
        self.game_state = game_state
        self.zones = zones
        self.player = player

        self.phases = [PhaseBeginning(zones, game_state, player),
                       PhasePrecombatMain(zones, game_state, player),
                       PhaseCombat(zones, game_state, player),
                       PhasePostcombatMain(zones, game_state, player),
                       PhaseEnding(zones, game_state, player)]

    def play(self):
        self.preparation()
        while self.game_state.outcome is Outcome.UNRESOLVED:
            self.turn()

    def preparation(self):
        self.zones.shuffle_library()
        starting_hand = self.zones.draw(7)
        Logger.hand(starting_hand)
        self.game_state.turn_counter = 0
        while not self.player.hand_keep:
            self.zones.mulligan()

    def turn(self):
        self.game_state.land_played = False
        self.game_state.turn_counter += 1
        Logger.turn_start(self.game_state.turn_counter)
        Logger.hand(self.zones.hand.cards)
        for p in self.phases:
            p.run()
            if self.game_state.outcome != Outcome.UNRESOLVED:
                break
