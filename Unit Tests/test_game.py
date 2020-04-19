import unittest
from abc import ABC
from cards.permanent import Permanent
from game.game import Game
from game.game_state import GameState
from game.phase import PhaseBeginning, Phase, PhasePrecombatMain
from game.step import StepUntap, StepDraw
from game.zone import ZonesManager


class OnlyUntap(Game):
    def __init__(self, zones, game_state):
        self.zones = zones
        self.game_state = game_state

    def turn(self):
        PhaseUntap(self.zones.battlefield, self.game_state).run()


class PhaseUntap(PhaseBeginning):
    def __init__(self, battlefield, game_state):
        self.game_state = game_state
        self.steps = [StepUntap(battlefield)]


class GameWithoutPlayer(Game):
    def __init__(self, zones, game_state):
        self.zones = zones
        self.game_state = game_state
        self.phases = [PhaseDraw(zones, game_state),
                       PhaseSimplePrecombatMain()]


class PhaseDraw(PhaseBeginning, ABC):
    def __init__(self, zones, game_state):
        self.zones = zones
        self.game_state = game_state
        self.steps = [StepDraw(zones, game_state)]


class PhaseSimplePrecombatMain(PhasePrecombatMain, ABC):
    def __init__(self):
        self.is_main_phase_started = False;

    def run(self):
        self.is_main_phase_started = True


class BattlefieldZone(ZonesManager, ABC):
    def __init__(self, battlefield):
        self.battlefield = battlefield


class UntappablePermanent(Permanent):
    def untap(self):
        pass


class DrawZone(ZonesManager, ABC):
    def __init__(self, game_state):
        self.library = []
        self.game_state = game_state


class TestGame(unittest.TestCase):
    def test__untap_step__all_card_tapped__no_tapped_cards(self):
        permanent = Permanent("Card1")
        permanent.untapped = False
        zones = BattlefieldZone([permanent])
        game = OnlyUntap(zones, GameState())
        game.turn()
        self.assertTrue(permanent.untapped)

    def test__untap_step__card_that_never_untaps__card_stay_untapped(self):
        permanent = UntappablePermanent("Card1")
        permanent.untapped = False
        zones = BattlefieldZone([permanent])
        game = OnlyUntap(zones, GameState())
        game.turn()
        self.assertFalse(permanent.untapped)

    def test__draw_step__empty_library__game_ends_in_the_end_of_draw_step(self):
        game_state = GameState(False)
        zones = DrawZone(game_state)
        game = GameWithoutPlayer(zones, game_state)
        game.turn()
        self.assertFalse(game.phases[1].is_main_phase_started)
