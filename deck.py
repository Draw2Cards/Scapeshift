import re


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
            f.find()
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
