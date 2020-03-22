import unittest
from collections import Counter

from zone import ZonesFacade
from card import Card
from zone import Zone


class TestFacade(unittest.TestCase):
    # draw
    def test__draw__sufficient_library_card_number__cards_removed_from_library(self):
        library = ["Card1", "Card2"]

        facade = ZonesFacade(library, [], [], [], [])
        facade.draw(2)

        self.assertEqual(facade.library, [])

    def test__draw__sufficient_library_card_number__cards_added_to_hand(self):
        library = ["Card1", "Card2"]

        facade = ZonesFacade(library, [], [], [], [])
        two_first_items_backup = list([library[0], library[1]])
        facade.draw(2)

        result = all(elem in facade.hand for elem in two_first_items_backup)
        self.assertTrue(result)

    def test__draw__insufficient_library_card_number__method_raises_error(self):
        library = ["Card1"]
        facade = ZonesFacade(library, [], [], [], [])
        self.assertRaises(SystemError, facade.draw, 2)

    def test__draw__negative_draw_value__method_raises_error(self):
        facade = ZonesFacade([], [], [], [], [])
        self.assertRaises(ValueError, facade.draw, -1)

    # discard
    def test_discard(self):
        card1 = Card("Card1", [], 0, 0, None)
        card2 = Card("Card2", [], 0, 0, None)
        library = []
        hand = [card1, card2]
        battlefield = []
        graveyard = []
        exile = []

        facade = ZonesFacade(library, hand, battlefield, graveyard, exile)
        facade.discard(card1.name)
        self.assertEqual([card1], facade.graveyard)
        self.assertEqual([card2], facade.hand)

        facade.discard(card1.name)
        self.assertEqual([card1], facade.graveyard)
        self.assertEqual([card2], facade.hand)

    def test_tutor_by_name(self):
        card1 = Card("Card1", [], 0, 0, None)
        card2 = Card("Card2", [], 0, 0, None)
        library = [card1, card2]
        hand = []
        battlefield = []
        graveyard = []
        exile = []

        facade = ZonesFacade(library, hand, battlefield, graveyard, exile)

        facade.tutor_by_name("Card3")
        self.assertEqual([], facade.hand)
        self.assertTrue(Counter([card1, card2]) == Counter(facade.library))

        facade.tutor_by_name("Card1")
        self.assertEqual([card1], facade.hand)
        self.assertEqual([card2], facade.library)

        facade.tutor_by_name("Card1", Zone.HAND, Zone.GRAVEYARD)
        self.assertEqual([], facade.hand)
        self.assertEqual([card2], facade.library)
        self.assertEqual([card1], facade.graveyard)

        self.assertRaises(SystemError, facade.tutor_by_name, "Card1", Zone.HAND, Zone.LIBRARY)

    def test_tutor_by_types(self):
        card1 = Card("Card1", ["Type1"], 0, 0, None)
        card2 = Card("Card2", ["Type1", "Type2"], 0, 0, None)
        library = [card1, card2]
        hand = []
        battlefield = []
        graveyard = []
        exile = []

        facade = ZonesFacade(library, hand, battlefield, graveyard, exile)
        facade.tutor_by_types(["Type1", "Type2"])
        self.assertEqual([card1], facade.library)
        self.assertEqual([card2], facade.hand)

        facade.tutor_by_types(["Type1", "Type2"])
        self.assertEqual([card1], facade.library)
        self.assertEqual([card2], facade.hand)
