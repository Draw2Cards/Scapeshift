import sys
import unittest
from abc import ABC
import os
from deck import Deck, Finder, DBFinder, ScryfallFinder
import sqlite3
from datetime import date
from database_manager import DatabaseManager
import requests


class FakeDeck_FilledDeckListAndCardsDict(Deck, ABC):
    def __init__(self):
        self.deck_list = [["Card", 4]]
        self.cards_dict = {"Card": [0, "", ["Type1", "Type2"]]}


class FakeDeck_FilledDeckList(Deck, ABC):
    def __init__(self):
        self.deck_list = [["Card", 4]]


class NeverFinder(Finder, ABC):
    def prepare(self):
        pass

    def proceed(self):
        pass

    def finish(self):
        pass


class AlwaysFinder(Finder, ABC):
    def __init__(self, to_find):
        self.to_find = to_find

    def prepare(self):
        pass

    def proceed(self):
        self.to_find.clear()

    def finish(self):
        pass


class TestDeck(unittest.TestCase):
    def test__add__acceptable_input__name_extracted(self):
        tests = ["Card", "1 Card", "x1 Card", " Card"]
        for test in tests:
            with self.subTest(test=test):
                new_deck = Deck()
                new_deck.add(test)
                self.assertEqual(new_deck[0][0], "Card")

    def test__add__acceptable_input__quantity_extracted(self):
        tests = ["Card", "1 Card", "x1 Card", " Card"]
        for test in tests:
            with self.subTest(test=test):
                new_deck = Deck()
                new_deck.add(test)
                self.assertEqual(new_deck[0][1], 1)

    def test__add__empty_lines__unchanged_deck_size(self):
        tests = ["", " "]
        for test in tests:
            with self.subTest(test=test):
                new_deck = Deck()
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

        new_deck.fill_dict(to_find, [fake_finder])
        self.assertEqual(new_deck.not_found_cards, [['Card', 4]])

    def test__fill_dict__existing_card__empty_not_found_list(self):
        new_deck = FakeDeck_FilledDeckList()
        to_find = new_deck.deck_list.copy()
        fake_finder = AlwaysFinder(to_find)

        new_deck.fill_dict(to_find, [fake_finder])
        self.assertEqual(new_deck.not_found_cards, [])

    def test_requests(self):
        # https://api.scryfall.com/cards/named?fuzzy=Valakut,%20the%20Molten%20Pinnacle
        url = 'https://api.scryfall.com/cards/named'

        params = dict(
            fuzzy='Valakut, the Molten Pinnacle'
        )
        resp = requests.get(url=url, params=params)
        data = resp.json()  # Check the JSON Response Content documentation below
        self.assertTrue(True)

    def test_database_manager(self):
        db_manager = DatabaseManager()
        db_manager.init()

        url = 'https://api.scryfall.com/cards/named'

        params = dict(
            fuzzy='Valakut, the Molten Pinnacle'
        )
        resp = requests.get(url=url, params=params)
        data = resp.json()

        db_manager.insert(data)

        row = db_manager.find(data["name"])
        set = {row}

        params = dict(
            fuzzy='Scapeshift'
        )
        resp = requests.get(url=url, params=params)
        data = resp.json()

        db_manager.insert(data)

        row = db_manager.find(data["name"])
        set.add(row)

        for x in set:
            print(x[4])

        db_manager.close()