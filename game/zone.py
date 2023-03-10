from random import shuffle
from enum import Enum
from cards.permanent import Permanent
from game.game_state import Outcome
from logger import Logger

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
            return self.hand.cards
        elif enum == Zone.BATTLEFIELD:
            return self.battlefield.get_cards()
        elif enum == Zone.GRAVEYARD:
            return self.graveyard
        else:
            return self.exile

    def draw(self, count=1):
        result = []
        if count < 1:
            raise ValueError('Only positive values allowed!')
        for x in range(count):
            if len(self.library) == 0:
                self.game_state.outcome = Outcome.LOSE
                break
            self.hand.cards += self.library[:1]
            result += self.library[:1]
            del self.library[:1]
        Logger.draw_step(result)
        return result

    def discard(self, card):
        for c in self.hand.cards:
            if card == c:
                self.graveyard.append(card)
                self.hand.cards.remove(card)
                break

    def move_card(self, card, enum_from=Zone.LIBRARY, enum_to=Zone.HAND):
        list_from = self._set_zone(enum_from)
        if enum_to == Zone.LIBRARY:
            raise SystemError('Using this method to add card to the library is blocked! Use ''library_add'' ')
        list_to = self._set_zone(enum_to)

        for c in list_from:
            if card[0] == c[0]:
                if enum_to == Zone.BATTLEFIELD:  # TODO IF enum_to is Zone.BATTLEFIELD convert to Permanent
                    self.battlefield.permanents.append(Permanent(card))
                else:
                    list_to.append(card)
                if enum_from == Zone.BATTLEFIELD:  # TODO IF enum_to is Zone.BATTLEFIELD convert to Card
                    self.battlefield.remove(card)
                else:
                    list_from.remove(card)
                break
        if enum_from == Zone.LIBRARY:
            self.shuffle_library()

    # TODO OUTDATED
    def tutor_by_name(self, name, enum_from=Zone.LIBRARY, enum_to=Zone.HAND):
        result = None
        list_from = self._set_zone(enum_from)
        if enum_to == Zone.LIBRARY:
            raise SystemError('Using this method to add card to the library is blocked! Use ''library_add'' ')
        list_to = self._set_zone(enum_to)

        for card in list_from:
            if name == card[0]:
                if enum_to == Zone.BATTLEFIELD:  # TODO IF enum_to is Zone.BATTLEFIELD convert to Permanent
                    self.battlefield.permanents.append(Permanent(card))
                else:
                    list_to.append(card)
                if enum_from == Zone.BATTLEFIELD: # TODO IF enum_to is Zone.BATTLEFIELD convert to Card
                    self.battlefield.remove(card)
                else:
                    list_from.remove(card)
                result = card
                break
        if enum_from == Zone.LIBRARY:
            self.shuffle_library()

        return result

    def play_land(self, land):
        if land:
            self.move_card(land, Zone.HAND, Zone.BATTLEFIELD)
            self.game_state.land_played = True

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

    def find_spells_in_hand_ready_to_cast(self):
        spells = []
        for card in self.hand.find_spells_with_cmc_leq(self.battlefield.count_open_mana()):
            if self.battlefield.can_cast(card):
                spells.append(card)
        return spells

    def tap_lands(self, cost):
        self.battlefield.tap_lands(cost)
