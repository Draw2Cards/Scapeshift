import re


def find_types(card):
    return []


class Deck:
    deck_list = []
    types_dict = {}

    def __init__(self, file_path):
        f = open(file_path, "r")
        for row in f:
            m = re.split(r"\s*x?(\d*)\s?(\S.+)", row)
            if len(m) == 4:
                if not m[1]:
                    m[1] = 1
                self.deck_list.append([m[2], int(m[1])])  # [name, quantity]

    def __getitem__(self, item):
        return self.deck_list[item]

    def to_library(self):
        library = []
        for r in self.deck_list:
            library += [r[0]] * r[1]
        return library

    def fill_types_list(self):
        for c in self.deck_list:
            if not c[0] in self.types_dict:
                types = find_types(c[0])
                self.types_dict[c[0]] = types


class TypeFinder:
    pass

