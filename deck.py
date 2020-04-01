import re
import sqlite3
from abc import ABC
from database_manager import DatabaseManager
import requests

class Deck:
    def __init__(self):
        self.cards_dict = {}
        self.deck_list = []
        self.gameplay_fields = []
        self.not_found_cards = []

    def __getitem__(self, item):
        return self.deck_list[item]

    def __len__(self):
        return len(self.deck_list)

    def add(self, line):
        m = re.split(r"\s*x?(\d*)\s?(\S.+)", line)
        if len(m) == 4:
            if not m[1]:
                m[1] = 1
            self.deck_list.append([m[2], int(m[1])])  # [name, quantity]

    def fill_dict(self, to_find, finders_list):
        for f in finders_list:
            f.prepare()
            f.proceed()
            f.finish()
            if len(to_find) is 0:
                break
        if len(to_find) > 0:
            self.not_found_cards = to_find

    def to_library(self):
        library = []
        for r in self.deck_list:
            x = self.cards_dict[r[0]]
            if x:
                library += [x] * r[1]
        return library


class Finder:
    def prepare(self):
        raise NotImplementedError('Not Implemented Error!')

    def proceed(self):
        raise NotImplementedError('Not Implemented Error!')

    def finish(self):
        raise NotImplementedError('Not Implemented Error!')


class DBFinder(Finder, ABC):

    def __init__(self, dictionary, to_find, db_manager):
        self.dictionary = dictionary
        self.to_find = to_find
        self.db_manager = db_manager

    def prepare(self):
        pass

    def proceed(self):
        for c in self.to_find:
            if c[0] not in self.dictionary:
                row = self.db_manager.find(c[0])
                if row:
                    self.dictionary[row[0]] = tuple((row[1:]))
                    self.to_find.remove(c)
            else:
                self.to_find.remove(c)

    def finish(self):
        pass


class ScryfallFinder(Finder, ABC):

    def __init__(self, dictionary, to_find, db_manager):
        self.dictionary = dictionary
        self.to_find = to_find
        self.db_manager = db_manager
        self.url = 'https://api.scryfall.com/cards/named'

    def prepare(self):
        pass

    def proceed(self):
        for c in self.to_find:
            if c[0] not in self.dictionary:
                data = self.find(c[0])
                if data:
                    self.db_manager.insert(data)
                    self.add_to_dict(c)
                    self.to_find.remove(c)
            else:
                self.to_find.remove(c)

    def find(self, name):
        params = dict(
            fuzzy=name
        )
        resp = requests.get(url=self.url, params=params)
        return resp.json()

    def finish(self):
        pass
