import unittest
from collections import Counter

from zone import ZonesFacade
from card import Card
from zone import Zone


class TestFacade(unittest.TestCase):

    def test_draw(self):
        card1 = "Card1"
        card2 = "Card2"
        card3 = "Card3"
        library = [card1, card2, card3]
        hand = []
        battlefield = []
        graveyard = []
        exile = []

        facade = ZonesFacade(library, hand, battlefield, graveyard, exile)
        facade.draw()
        self.assertEqual([card1], facade.hand)
        self.assertEqual([card2, card3], facade.library)

        facade.draw(2)
        self.assertEqual([card1, card2, card3], facade.hand)
        self.assertEqual([], facade.library)

        self.assertRaises(ValueError, facade.draw, -1)
        self.assertRaises(SystemError, facade.draw, 1)

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
