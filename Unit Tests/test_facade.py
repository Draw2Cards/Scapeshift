import unittest
from abc import ABC
from zone import ZonesFacade
from card import Card
from zone import Zone


class FakeShufflingZonesFacade(ZonesFacade, ABC):
    def __init__(self, library, hand, battlefield, graveyard, exile):
        super().__init__(library, hand, battlefield, graveyard, exile)
        self.library_shuffled = False

    def shuffle_library(self):
        self.library_shuffled = True
        pass


class TestFacade(unittest.TestCase):
    # draw
    def test__draw__sufficient_library_card_number__cards_removed_from_library(self):
        library = ["Card1", "Card2"]
        facade = ZonesFacade(library, [], [], [], [])
        facade.draw(2)
        self.assertEqual(facade.library, [])

    def test__draw__sufficient_library_card_number__cards_added_to_hand(self):
        facade = ZonesFacade(["Card1", "Card2"], [], [], [], [])
        facade.draw(2)
        self.assertEqual(facade.hand, ["Card1", "Card2"])

    def test__draw__insufficient_library_card_number__method_raises_error(self):
        library = ["Card1"]
        facade = ZonesFacade(library, [], [], [], [])
        self.assertRaises(SystemError, facade.draw, 2)

    def test__draw__negative_draw_value__method_raises_error(self):
        facade = ZonesFacade([], [], [], [], [])
        self.assertRaises(ValueError, facade.draw, -1)

    # discard
    def test__discard__card_in_hand__removed_from_hand(self):
        card_name = "Card1"
        facade = ZonesFacade([], [Card(card_name)], [], [], [])
        facade.discard(card_name)
        self.assertEqual(facade.hand, [])

    def test__discard__card_in_hand__moved_to_graveyard(self):
        card1_name = "Card1"
        card1 = Card(card1_name)
        facade = ZonesFacade([], [card1], [], [], [])
        facade.discard(card1_name)
        self.assertEqual(facade.graveyard, [card1])

    # tutor_by_name
    def test__tutor__card_in_library__moved_to_hand(self):
        card1_name = "Card1"
        card1 = Card(card1_name)
        facade = ZonesFacade([card1], [], [], [], [])
        facade.tutor_by_name(card1_name)
        self.assertEqual(facade.hand, [card1])

    def test__tutor__card_in_library__removed_from_library(self):
        card1_name = "Card1"
        card1 = Card(card1_name)
        facade = ZonesFacade([card1], [], [], [], [])
        facade.tutor_by_name(card1_name)
        self.assertEqual(facade.library, [])

    def test__tutor_by_name__using_method_to_add_to_library__rises_error(self):
        facade = ZonesFacade([], [], [], [], [])
        self.assertRaises(SystemError, facade.tutor_by_name, "Card1", Zone.GRAVEYARD, Zone.LIBRARY)

    def test__tutor__card_in_library__shuffled_library(self):
        card1_name = "Card1"
        card1 = Card(card1_name)
        facade = FakeShufflingZonesFacade([card1], [], [], [], [])
        facade.tutor_by_name(card1_name)
        self.assertTrue(facade.library_shuffled)

    def test__tutor__card_not_in_library__shuffled_library(self):
        card1_name = "Card1"
        card1 = Card(card1_name)
        facade = FakeShufflingZonesFacade([], [], [], [], [])
        facade.tutor_by_name(card1_name)
        self.assertTrue(facade.library_shuffled)

    def test__tutor__looking_in_graveyard__no_shuffling(self):
        card1_name = "Card1"
        card1 = Card(card1_name)
        facade = FakeShufflingZonesFacade([], [], [], [], [])
        facade.tutor_by_name(card1_name, Zone.GRAVEYARD, Zone.HAND)
        self.assertFalse(facade.library_shuffled)

    # tutor_by_type
    def test__tutor_by_type__card_in_library__moved_to_hand(self):
        card1_types = ["type1", "type2"]
        card1 = Card("", card1_types)
        facade = ZonesFacade([card1], [], [], [], [])
        facade.tutor_by_types(["type1", "type2"])
        self.assertEqual(facade.hand, [card1])

    def test__tutor_by_type__card_in_library__removed_from_library(self):
        card1_types = ["type1", "type2"]
        card1 = Card("", card1_types)
        facade = ZonesFacade([card1], [], [], [], [])
        facade.tutor_by_types(["type1", "type2"])
        self.assertEqual(facade.library, [])

    def test__tutor_by_type__card_in_library__shuffled_library(self):
        card1_types = ["type1", "type2"]
        card1 = Card("", card1_types)
        facade = FakeShufflingZonesFacade([card1], [], [], [], [])
        facade.tutor_by_types(["type1", "type2"])
        self.assertTrue(facade.library_shuffled)

    def test__tutor_by_type__card_not_in_library__shuffled_library(self):
        card1_types = ["type1", "type2"]
        card1 = Card("", card1_types)
        facade = FakeShufflingZonesFacade([], [], [], [], [])
        facade.tutor_by_types(["type1", "type2"])
        self.assertTrue(facade.library_shuffled)
