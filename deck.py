import re
import sqlite3


def db_find(name, db_path=""):
    if not db_path:
        db_path = "cards.db"
    card = []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM cards WHERE name=':name'", {'name': name})
    card = c.fetchone()
    conn.close()
    return card


def scryfall_find(name):
    card = []
    return card


def db_add(card):
    pass


class Deck:
    deck_list = []
    cards_dict = {}
    gameplay_fields = []

    def __init__(self, file_path):
        f = open(file_path, "r")
        for row in f:
            m = re.split(r"\s*x?(\d*)\s?(\S.+)", row)
            if len(m) == 4:
                if not m[1]:
                    m[1] = 1
                self.deck_list.append([m[2], int(m[1])])  # [name, quantity]
        f.close()

    def __getitem__(self, item):
        return self.deck_list[item]

    def add_card(self, name, quantity=1):
        card = self.cards_dict[name]
        if not card:
            card = self.get_card(name)
        return [card] * quantity

    def get_card(self, name):
        card = db_find(name)
        if not card:
            card = scryfall_find(name)
            db_add(card)
        self.dict_add(name, card)
        return card

    def dict_add(self, name, card):
        self.cards_dict[name] = card

    def to_library(self):
        library = []
        for r in self.deck_list:
            library += self.add_card(r)
            # library += [r[0]] * r[1]
        return library
