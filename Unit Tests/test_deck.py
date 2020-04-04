import unittest
from abc import ABC
from deck import Deck
from finders import Finder


class FakeDeck_EmptyInit(Deck, ABC):
    def __init__(self):
        self.not_found_cards = []
        self.gameplay_fields = []
        self.deck_list = []
        self.cards_dict = {}
        self.count = 0


class FakeDeck_FilledDeckListAndCardsDict(Deck, ABC):
    def __init__(self):
        self.not_found_cards = []
        self.gameplay_fields = []
        self.count = 0
        self.deck_list = [["Card", 4]]
        self.cards_dict = {"Card": [0, "", ["Type1", "Type2"]]}


class FakeDeck_FilledDeckList(Deck, ABC):
    def __init__(self):
        self.not_found_cards = []
        self.gameplay_fields = []
        self.cards_dict = {}
        self.count = 0
        self.deck_list = [["Card", 4]]


class NeverFinder(Finder, ABC):
    def find(self, to_find):
        return {}


class AlwaysFinder(Finder, ABC):
    def find(self, to_find):
        dic = {}
        for c in to_find:
            dic[c[0]] = None
        return dic


class TestDeck(unittest.TestCase):
    def test__add__acceptable_input__name_extracted(self):
        tests = ["Card", "1 Card", "x1 Card", " Card"]
        for test in tests:
            with self.subTest(test=test):
                new_deck = FakeDeck_EmptyInit()
                new_deck.add(test)
                self.assertEqual(new_deck[0][0], "Card")

    def test__add__acceptable_input__quantity_extracted(self):
        tests = ["Card", "1 Card", "x1 Card", " Card"]
        for test in tests:
            with self.subTest(test=test):
                new_deck = FakeDeck_EmptyInit()
                new_deck.add(test)
                self.assertEqual(new_deck[0][1], 1)

    def test__add__empty_lines__unchanged_deck_size(self):
        tests = ["", " "]
        for test in tests:
            with self.subTest(test=test):
                new_deck = FakeDeck_EmptyInit()
                new_deck.add("")
                self.assertEqual(len(new_deck), 0)

    def test__to_library__full_set_in_deck__correct_amount_in_library(self):
        new_deck = FakeDeck_FilledDeckListAndCardsDict()
        library = new_deck.to_library()
        self.assertEqual(len(library), 4)

    def test__to_library__full_set_in_deck__correct_cards_in_library(self):
        new_deck = FakeDeck_FilledDeckListAndCardsDict()
        library = new_deck.to_library()
        card = new_deck.cards_dict["Card"]
        for i in range(4):
            with self.subTest(i=i):
                self.assertIs(library[i], card)

    def test__fill_dict__not_existing_card__card_returned_in_not_found_items(self):
        new_deck = FakeDeck_FilledDeckList()
        to_find = new_deck.deck_list.copy()
        fake_finder = NeverFinder()

        new_deck.fill_dict([fake_finder])
        self.assertEqual(new_deck.not_found_cards, [['Card', 4]])

    def test__fill_dict__existing_card__empty_not_found_list(self):
        new_deck = FakeDeck_FilledDeckList()
        fake_finder = AlwaysFinder()

        new_deck.fill_dict([fake_finder])
        self.assertEqual(new_deck.not_found_cards, [])

    def test__update_to_find__card_in_dict_card__deleted_from_list(self):
        new_deck = FakeDeck_FilledDeckListAndCardsDict()
        to_find = new_deck.deck_list.copy()
        to_find = new_deck.update_to_find(to_find)
        self.assertEqual(to_find, [])

    def test__update_to_find__card_not_in_dict__no_changes(self):
        new_deck = FakeDeck_EmptyInit()
        to_find = new_deck.deck_list.copy()
        updated = new_deck.update_to_find(to_find)
        self.assertEqual(updated, to_find)

    def test__update_to_find__partly_cards_in_dict__removed_duplicates(self):
        card_to_find = [["Card2", 4]]
        new_deck = FakeDeck_FilledDeckListAndCardsDict()
        to_find = new_deck.deck_list.copy()
        to_find += card_to_find
        updated = new_deck.update_to_find(to_find)
        self.assertEqual(updated, card_to_find)
