import re


class Deck:
    def __init__(self, deck_path):
        self.not_found_cards = []
        self.gameplay_fields = []
        self.deck_list = []
        self.cards_dict = {}
        self.count = 0
        file = open(deck_path)
        for line in file:
            self.add(line)

    def __getitem__(self, item):
        return self.deck_list[item]

    def __len__(self):
        return len(self.deck_list)

    def add(self, line):
        m = re.split(r"\s*x?(\d*)\s?(\S.+)", line)
        if len(m) == 4:
            if not m[1]:
                m[1] = 1
            quantity = int(m[1])
            self.deck_list.append([m[2], quantity])  # [name, quantity]
            self.count += quantity

    def fill_dict(self, finders_list):
        to_find = self.deck_list.copy()
        for f in finders_list:
            self.cards_dict.update(f.find(to_find))
            to_find = self.update_to_find(to_find)
            if not to_find:
                break
        if len(to_find) > 0:
            self.not_found_cards = to_find

    def update_to_find(self, to_find):
        updated = [x for x in to_find if x[0] not in self.cards_dict]
        return updated

    def to_library(self):
        library = []
        for r in self.deck_list:
            x = self.cards_dict[r[0]]
            if x:
                library += [x] * r[1]
        return library
