from abc import ABC
import requests


class Finder:
    def find(self):
        raise NotImplementedError('Not Implemented Error!')


class DbFinder(Finder, ABC):
    def __init__(self, dictionary, to_find, db_manager):
        self.dictionary = dictionary
        self.to_find = to_find
        self.db_manager = db_manager

    def find(self):
        for c in self.to_find:
            if c[0] not in self.dictionary:
                row = self.db_manager.find(c[0])
                if row:
                    self.dictionary[row[0]] = tuple((row[1:]))
                    self.to_find.remove(c)
            else:
                self.to_find.remove(c)


class ScryfallFinder(Finder, ABC):
    def __init__(self, dictionary, to_find, db_manager):
        self.dictionary = dictionary
        self.to_find = to_find
        self.db_manager = db_manager
        self.url = 'https://api.scryfall.com/cards/named'
        self.errors_details = set()

    def find(self):
        for c in self.to_find:
            if c[0] not in self.dictionary:
                data = self.find(c[0])
                obj = data["object"]
                if obj == "card":
                    self.db_manager.insert(data)
                    self.add_to_dict(c)
                    self.to_find.remove(c)
                elif obj == "error":
                    self.errors_details.add(data["details"])
                else:
                    assert False
            else:
                self.to_find.remove(c)

    def find(self, name):
        params = dict(
            fuzzy=name
        )
        resp = requests.get(url=self.url, params=params)
        return resp.json()