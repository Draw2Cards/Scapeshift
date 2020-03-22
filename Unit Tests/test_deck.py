import unittest
import os
from deck import Deck
import deck
import sqlite3
from datetime import date


class TestDeck(unittest.TestCase):
    def test_import(self):
        file_path = "test_deck"
        f = open(file_path, "w")
        f.write(
            """2 Snow-Covered Forest
        Flooded Grove
    x2 Valakut, the Molten Pinnacle""")
        f.close()
        deck = Deck(file_path)
        self.assertEqual(deck[0], ["Snow-Covered Forest", 2])
        self.assertEqual(deck[1], ["Flooded Grove", 1])
        self.assertEqual(deck[2], ["Valakut, the Molten Pinnacle", 2])
        os.remove(file_path)

    def test_db_find(self):
        db_path = "test.db"
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute("""CREATE TABLE cards (
                    name text,
                    cmc integer,
                    mana_cost text,
                    type_line text,
                    import_date text
                    )""")
        c.execute("INSERT INTO cards VALUES ('Snow-Covered Forest', 0, '', 'Basic Snow Land — Forest', '2020-03-14')")
        conn.commit()
        conn.close()

        card = deck.db_find("Snow-Covered Forest", "test.db")
        self.assertEqual(card, [6, "4WW", "Basic Snow Land — Forest""])"])  # TODO types to table

        os.remove(db_path)

    def test_add_card(self):  # TODO check/use assertSame
        library = []
        deck = Deck()
        library += deck.add_card(["Snow-Covered Forest", 2])
        self.assertEqual(library[0].name, "Snow-Covered Forest")
        self.assertEqual(library[1].name, "Snow-Covered Forest")
        self.assertEqual(deck.cards_dict["Snow-Covered Forest"], [6, "4WW", ["Basic", "Snow", "Land", "Forest"]])

    def test_to_library(self):  # add_card in loop
        file_path = "test_deck"
        f = open(file_path, "w")
        f.write(
            """2 Snow-Covered Forest
        Flooded Grove
    x2 Valakut, the Molten Pinnacle""")
        f.close()
        deck = Deck(file_path)
        library = deck.to_library()
        self.assertEqual(library[0], "Snow-Covered Forest")
        self.assertEqual(library[1], "Snow-Covered Forest")
        self.assertEqual(library[2], "Flooded Grove")
        self.assertEqual(library[3], "Valakut, the Molten Pinnacle")
        self.assertEqual(library[4], "Valakut, the Molten Pinnacle")
        os.remove(file_path)

    def test_get_cards_gameplay_fields(self):
        file_path = "test_deck"
        f = open(file_path, "w")
        f.write(
            """2 Snow-Covered Forest
        Flooded Grove
    x4 Sakura-Tribe Elder""")
        f.close()
        deck = Deck(file_path)
        deck.get_cards_gameplay_fields()
        self.assertEqual(deck.types_dict["Snow-Covered Forest"], ["Basic", "Snow", "Land", "Forest"])
        self.assertEqual(deck.types_dict["Flooded Grove"], ["Land"])
        self.assertEqual(deck.types_dict["Sakura-Tribe Elder"], ["Creature", "Snake", "Shaman"])
        self.assertEqual(len(deck.types_dict), 3)
        os.remove(file_path)
