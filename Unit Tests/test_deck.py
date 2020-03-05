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

    def test_add_types(self):
        pass
