class ZonesFacade:
    def __init__(self, library, hand, battlefield, graveyard, exile):  # also stack and command (and ante)
        self.__library = library
        self.__hand = hand
        self.__battlefield = battlefield
        self.__graveyard = graveyard
        self.__exile = exile

    def draw(self, count=1):
        self.__hand += self.__library[:count]
        del self.__library[:count]


class Zone:
    def __init__(self, cards):
        self._cards = cards


class Library(Zone):
    pass
