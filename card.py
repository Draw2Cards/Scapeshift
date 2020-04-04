from abc import ABC
from zone import ZonesManager


# FLYWEIGHT
class Card:
    def __init__(self, name="", card_types="", cmc=0, card_id=0, fun_play=None):
        self.name = name
        self.card_types = card_types
        self._counters = 0
        self._untapped = True
        self._cmc = cmc
        self._card_id = card_id
        self._fun_play = fun_play

    def _play(self):
        raise NotImplementedError('Not Implemented Error!')

    def remove(self):
        pass

    _facade = None

    @classmethod
    def set_facade(cls, facade):
        cls._facade = facade


class Spell(Card, ABC):
    def _play(self):
        raise NotImplementedError('Not Implemented Error!')

    def _cast(self):
        raise NotImplementedError('Not Implemented Error!')

    def __resolve(self):
        pass


class Land(Card, ABC):
    def play(self):
        pass

    def play_fetch(self):
        self.facade.discard(self)
        land = self.facade.tutor(["Land", "Island"])  # tmp type
        if land:
            self.facede.put_to_play_form_library(land)

    def play_basic(self):
        pass
