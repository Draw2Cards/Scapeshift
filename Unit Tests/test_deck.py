import unittest
import os
from deck import Deck


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

    def test_to_library(self):
        file_path = "test_deck"
        f = open(file_path, "w")
        f.write(
            """2 Snow-Covered Forest
        Flooded Grove
    x2 Valakut, the Molten Pinnacle""")
        f.close()
        deck = Deck(file_path)
        library = deck.make_library()
        self.assertEqual(library[0], "Snow-Covered Forest")
        self.assertEqual(library[1], "Snow-Covered Forest")
        self.assertEqual(library[2], "Flooded Grove")
        self.assertEqual(library[3], "Valakut, the Molten Pinnacle")
        self.assertEqual(library[4], "Valakut, the Molten Pinnacle")
        os.remove(file_path)

    def test_fill_types_list(self):
        file_path = "test_deck"
        f = open(file_path, "w")
        f.write(
            """2 Snow-Covered Forest
        Flooded Grove
    x4 Sakura-Tribe Elder""")
        f.close()
        deck = Deck(file_path)
        deck.fill_types_list()
        self.assertEqual(deck.types_dict["Snow-Covered Forest"], ["Basic", "Snow", "Land", "Forest"])
        self.assertEqual(deck.types_dict["Flooded Grove"], ["Land"])
        self.assertEqual(deck.types_dict["Sakura-Tribe Elder"], ["Creature", "Snake", "Shaman"])
        self.assertEqual(len(deck.types_dict), 3)
        os.remove(file_path)
