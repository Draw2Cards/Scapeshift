from random import shuffle
from enum import Enum
from cards.permanent import Permanent
from game.game_state import Outcome


class Zone(Enum):
    LIBRARY = 0
    HAND = 1
    BATTLEFIELD = 2
    GRAVEYARD = 3
    EXILE = 4


class ZonesManager:
    def __init__(self, library, hand, battlefield, graveyard, exile, stack, game_state):  # also command (and ante)
        self.library = library
        self.hand = hand
        self.battlefield = battlefield
        self.graveyard = graveyard
        self.exile = exile
        self.stack = stack
        self.game_state = game_state

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
                self.game_state.outcome = Outcome.LOSE
                break
            self.hand += self.library[:1]
            del self.library[:1]

    def discard(self, card):
        for c in self.hand:
            if card == c:
                self.graveyard.append(card)
                self.hand.remove(card)
                break

    # TODO OUTDATED
    def tutor_by_name(self, name, enum_from=Zone.LIBRARY, enum_to=Zone.HAND):
        list_from = self._set_zone(enum_from)
        if enum_to == Zone.LIBRARY:
            raise SystemError('Using this method to add card to the library is blocked! Use ''library_add'' ')
        list_to = self._set_zone(enum_to)

        for card in list_from:
            if name == card.name:
                if enum_to == Zone.BATTLEFIELD:  # TODO IF enum_to is Zone.BATTLEFIELD convert to Permanent
                    list_to.append(Permanent(card))
                else:
                    list_to.append(card)
                if enum_from == Zone.BATTLEFIELD: # TODO IF enum_to is Zone.BATTLEFIELD convert to Card
                    list_to.append(card.card)
                else:
                    list_from.remove(card)
                break
        if enum_from == Zone.LIBRARY:
            self.shuffle_library()

    def play_land(self, land_name):
        if land_name:
            self.tutor_by_name(land_name, Zone.HAND, Zone.BATTLEFIELD)

    # TODO OUTDATED
    def tutor_by_types(self, types):
        for card in self.library:
            if all(elem in card.card_types for elem in types):
                self.hand.append(card)
                self.library.remove(card)
        self.shuffle_library()

    def shuffle_library(self):
        shuffle(self.library)

    def library_add(self):
        raise NotImplementedError('Not Implemented Error!')

    def mulligan(self):
        # TODO
        pass