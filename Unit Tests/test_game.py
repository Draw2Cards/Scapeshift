import unittest
from abc import ABC

from cards.permanent import Permanent
from game.game import Game
from game.zone import ZonesManager


class GameOnlyZones(Game):
    def __init__(self, zones):
        self.zones = zones


class BattlefieldZone(ZonesManager, ABC):
    def __init__(self, battlefield):
        self.battlefield = battlefield


class NeverUntapPermanent(Permanent):
    def untap(self):
        pass


class TestGame(unittest.TestCase):
    def test__untap_step__all_card_tapped__no_tapped_cards(self):
        permanent = Permanent("Card1")
        permanent.init(False)
        zones = BattlefieldZone([permanent])
        game = GameOnlyZones(zones)
        game.untap_step()
        self.assertTrue(permanent.untapped)

    def test__untap_step__card_that_never_untaps__card_stay_untapped(self):
        permanent = Permanent("Card1")
        permanent.init(False)
        zones = BattlefieldZone([permanent])
        game = GameOnlyZones(zones)
        game.untap_step()
        self.assertTrue(permanent.untapped)

    def test__draw_step__empty_library__game_ends_before_precombat_main_phase(self):
        pass
