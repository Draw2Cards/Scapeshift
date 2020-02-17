from abc import ABC


class Card:
    def __init__(self, name, card_types, cmc, card_id, zone):
        self._name = name
        self._card_types = card_types
        self._counters = 0
        self._untapped = True
        self._cmc = cmc
        self._card_id = card_id
        self._zone = zone

    def _play(self):
        raise NotImplementedError('Not Implemented Error!')

    def remove(self):
        pass


class Spell(Card, ABC):
    def _play(self):
        raise NotImplementedError('Not Implemented Error!')

    def _cast(self):
        raise NotImplementedError('Not Implemented Error!')

    def __resolve(self):
        pass


class Permanent(Spell, ABC):
    def play(self):
        pass


class NonPermanent(Spell, ABC):
    def play(self):
        pass


class Land(Card, ABC):
    def play(self):
        pass
