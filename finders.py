from abc import ABC
import requests


class Finder:
    def find(self):
        raise NotImplementedError('Not Implemented Error!')


class DbFinder(Finder, ABC):
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def find(self, to_find):
        cards_dict = {}
        for c in to_find:
            row = self.db_manager.find(c[0])
            if row:
                cards_dict[row[0]] = tuple((row[1:]))
        return cards_dict


class ScryfallFinder(Finder, ABC):
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.url = 'https://api.scryfall.com/cards/named'
        self.errors_details = set()

    def find(self, to_find):
        cards_dict = {}
        for c in self.to_find:
            data = self.find_card(c[0])
            obj = data["object"]
            if obj == "card":
                cards_dict = [data["name"]] = (data["cmc"], data["mana_cost"], data["type_line"])
            elif obj == "error":
                self.errors_details.add(data["details"])
            else:
                assert False
        return cards_dict

    def find_card(self, name):
        params = dict(
            exact=name
        )
        resp = requests.get(url=self.url, params=params)
        return resp.json()
