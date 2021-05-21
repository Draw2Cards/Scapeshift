import unittest
from abc import ABC
from game.zone import ZonesManager, Zone
from cards.card import Card
from game.game_state import GameState, Outcome
from zones.hand import Hand

class FakeShufflingZonesManager(ZonesManager, ABC):
    def __init__(self, library, hand, battlefield, graveyard, exile):
        self.library = library
        self.hand = hand
        self.battlefield = battlefield
        self.graveyard = graveyard
        self.exile = exile
        self.library_shuffled = False

    def shuffle_library(self):
        self.library_shuffled = True
        pass


class SimpleZoneDraw(ZonesManager, ABC):
    def __init__(self, library, hand, game_state):
        self.library = library
        self.hand = hand
        self.game_state = game_state


class SimpleZoneDiscard(ZonesManager, ABC):
    def __init__(self, graveyard, hand):
        self.graveyard = graveyard
        self.hand = hand


class SimpleZoneTutor(ZonesManager, ABC):
    def __init__(self, library, hand, battlefield, graveyard, exile,):
        self.library = library
        self.hand = hand
        self.battlefield = battlefield
        self.graveyard = graveyard
        self.exile = exile


class TestFacade(unittest.TestCase):
    # draw
    def test__draw__sufficient_library_card_number__cards_removed_from_library(self):
        library = ["Card1", "Card2"]
        facade = SimpleZoneDraw(library, Hand(), None)
        facade.draw(2)
        self.assertEqual(facade.library, [])

    def test__draw__sufficient_library_card_number__cards_added_to_hand(self):
        facade = SimpleZoneDraw([("Card1",), ("Card2",)], Hand(), None)
        facade.draw(2)
        self.assertEqual(facade.hand.cards, [("Card1",), ("Card2",)])

    def test__draw__insufficient_library_card_number__outcome_changed_to_lose(self):
        game_state = GameState()
        facade = SimpleZoneDraw([("Card1",)], Hand(), game_state)
        facade.draw(2)
        self.assertEqual(game_state.outcome, Outcome.LOSE)

    def test__draw__negative_draw_value__method_raises_error(self):
        facade = SimpleZoneDraw([], [], None)
        self.assertRaises(ValueError, facade.draw, -1)

    # discard
    def test__discard__card_in_hand__removed_from_hand(self):
        hand = Hand()
        card1 = Card("Card1")
        facade = SimpleZoneDiscard([], hand)
        facade.discard(card1)
        self.assertEqual(facade.hand.cards, [])

    def test__discard__card_in_hand__moved_to_graveyard(self):
        hand = Hand()
        card1 = Card("Card1")
        hand.cards.append(card1)
        facade = SimpleZoneDiscard([], hand)
        facade.discard(card1)
        self.assertEqual(facade.graveyard, [card1])

    # tutor_by_name
    def test__tutor__card_in_library__moved_to_hand(self):
        card1 = ("Card1",)
        facade = SimpleZoneTutor([card1], Hand(), [], [], [])
        facade.tutor_by_name(card1[0])
        self.assertEqual(facade.hand.cards, [card1])

    def test__tutor__card_in_library__removed_from_library(self):
        card1 = ("Card1",)
        facade = SimpleZoneTutor([card1], Hand(), [], [], [])
        facade.tutor_by_name(card1[0])
        self.assertEqual(facade.library, [])

    def test__tutor_by_name__using_method_to_add_to_library__rises_error(self):
        facade = SimpleZoneTutor([], [], [], [], [])
        self.assertRaises(SystemError, facade.tutor_by_name, "Card1", Zone.GRAVEYARD, Zone.LIBRARY)

    def test__tutor_by_name__card_in_library__shuffled_library(self):
        card1 = ("Card1",)
        facade = FakeShufflingZonesManager([card1], Hand(), [], [], [])
        facade.tutor_by_name(card1[0])
        self.assertTrue(facade.library_shuffled)

    def test__tutor_by_name__card_not_in_library__shuffled_library(self):
        card1_name = "Card1"
        facade = FakeShufflingZonesManager([], Hand(), [], [], [])
        facade.tutor_by_name(card1_name)
        self.assertTrue(facade.library_shuffled)

    def test__tutor_by_name__looking_in_graveyard__no_shuffling(self):
        card1_name = "Card1"
        facade = FakeShufflingZonesManager([], Hand(), [], [], [])
        facade.tutor_by_name(card1_name, Zone.GRAVEYARD, Zone.HAND)
        self.assertFalse(facade.library_shuffled)

    # tutor_by_type
    def test__tutor_by_type__card_in_library__moved_to_hand(self):
        card1_types = ["type1", "type2"]
        card1 = Card("", card1_types)
        facade = SimpleZoneTutor([card1], [], [], [], [])
        facade.tutor_by_types(["type1", "type2"])
        self.assertEqual(facade.hand, [card1])

    def test__tutor_by_type__card_in_library__removed_from_library(self):
        card1_types = ["type1", "type2"]
        card1 = Card("", card1_types)
        facade = SimpleZoneTutor([card1], [], [], [], [])
        facade.tutor_by_types(["type1", "type2"])
        self.assertEqual(facade.library, [])

    def test__tutor_by_type__card_in_library__shuffled_library(self):
        card1_types = ["type1", "type2"]
        card1 = Card("", card1_types)
        facade = FakeShufflingZonesManager([card1], [], [], [], [])
        facade.tutor_by_types(["type1", "type2"])
        self.assertTrue(facade.library_shuffled)

    def test__tutor_by_type__card_not_in_library__shuffled_library(self):
        card1_types = ["type1", "type2"]
        card1 = Card("", card1_types)
        facade = FakeShufflingZonesManager([], [], [], [], [])
        facade.tutor_by_types(["type1", "type2"])
        self.assertTrue(facade.library_shuffled)