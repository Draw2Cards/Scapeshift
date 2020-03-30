import re
import sqlite3
from abc import ABC
from database_manager import DatabaseManager


class Deck:
    deck_list = []
    cards_dict = {}
    gameplay_fields = []
    not_found_cards = []

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

    def __init__(self, dictionary, to_find, db_path=""):
        self.dictionary = dictionary
        self.to_find = to_find
        self.table = "cards"
        self.conn = None
        self.cursor = None
        if not db_path:
            self.db_path = "cards.db"
        else:
            self.db_path = db_path

    def prepare(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        if not self.is_table_exists(self.table):
            self.create_table(self.table)

    def is_table_exists(self, table):
        is_exists = False
        self.cursor("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=':table'", {'table', table})
        if self.cursor.fetchone()[0] == 1:
            is_exists = True
        return is_exists

    def create_table(self, table):
        self.cursor.execute("""CREATE TABLE ':table' (
                    name text,
                    cmc integer,
                    mana_cost text,
                    type_line text,
                    import_date text
                    )""", {'table', table})
        self.conn.commit()

    def proceed(self):
        for c in self.to_find:
            if c[0] not in self.dictionary:
                x = self.db_find(c[0])
                if x:
                    self.add_to_dict(c)
                    self.to_find.remove(c)
            else:
                self.to_find.remove(c)

    def db_find(self, name):
        self.cursor.execute("SELECT * FROM cards WHERE name=':name'", {'name': name})
        card = self.cursor.fetchone()
        return card

    def add_to_dict(self, card):
        pass

    def finish(self):
        self.conn.close()


class ScryfallFinder(Finder, ABC):

    def __init__(self, dictionary, to_find):
        self.dictionary = dictionary
        self.to_find = to_find

    def prepare(self):
        pass

    def proceed(self):
        for c in self.to_find:
            if c[0] not in self.dictionary:
                x = self.db_find(c[0])
                if x:
                    self.add_to_dict(c)
                    self.to_find.remove(c)
            else:
                self.to_find.remove(c)

    def finish(self):
        pass
