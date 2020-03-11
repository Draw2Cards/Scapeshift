from random import shuffle
from enum import Enum


class Zone(Enum):
    LIBRARY = 0
    HAND = 1
    BATTLEFIELD = 2
    GRAVEYARD = 3
    EXILE = 4


class ZonesFacade:
    def __init__(self, library, hand, battlefield, graveyard, exile):  # also stack and command (and ante)
        self.library = library
        self.hand = hand
        self.battlefield = battlefield
        self.graveyard = graveyard
        self.exile = exile

    def _set_zone(self, enum):
        if enum == Zone.LIBRARY:
            return self.library
        elif enum == Zone.HAND:
            return self.hand
        elif enum == Zone.BATTLEFIELD:
            return self.battlefield
        elif enum == Zone.GRAVEYARD:
            return self.graveyard
        else:
            return self.exile

    def draw(self, count=1):
        if count < 1:
            raise ValueError('Only positive values allowed!')
        for x in range(count):
            if len(self.library) == 0:
                raise SystemError('Attempt of drawing a card from the library with no cards! You lose the game!')
            self.hand += self.library[:1]
            del self.library[:1]

    def discard(self, name):
        for card in self.hand:
            if card.name == name:
                self.graveyard.append(card)
                self.hand.remove(card)
                break

    def tutor_by_name(self, name, enum_from=Zone.LIBRARY, enum_to=Zone.HAND):
        list_from = self._set_zone(enum_from)
        if enum_to == Zone.LIBRARY:
            raise SystemError('Using this method to add card to the library is blocked! Use ''library_add'' ')
        list_to = self._set_zone(enum_to)

        for card in list_from:
            if name == card.name:
                list_to.append(card)
                list_from.remove(card)
                break
        if enum_from == Zone.LIBRARY:
            shuffle(self.library)

    def tutor_by_types(self, types):
        for card in self.library:
            if all(elem in card.card_types for elem in types):
                self.hand.append(card)
                self.library.remove(card)
        shuffle(self.library)

    def library_add(self):
        raise NotImplementedError('Not Implemented Error!')
