import random
from enum import Enum

from game.zone import Zone
from logger import Logger


class Player:
    def __init__(self, zone, game_state):
        self.hand_keep = True
        self.card_limit = 7
        self.zones = zone
        self.game_state = game_state

    def precombat_main_phase(self):
        pass

    def beginning_of_combat_step(self):
        pass

    def declare_attackers_step(self):
        # returns number of attacking creatures
        return 0

    def declare_blockers_step(self):
        pass

    def combat_damage_step(self):
        pass

    def end_of_combat_step(self):
        pass

    def postcombat_main_phase(self):
        pass

    def end_step(self):
        pass

    def cleanup_step(self):
        while len(self.zones.hand.cards) > self.card_limit:
            to_delete = random.choice(self.zones.hand.cards)
            self.zones.discard(to_delete)


class Strategy(Enum):
    RAMP = 0
    DIG_RAMP = 1
    DIG_SS = 2
    CAST_SS = 3


class RugPlayer(Player):
    def __init__(self, zone, game_state):
        Player.__init__(self, zone, game_state)
        self.strategy = Strategy.RAMP

    def precombat_main_phase(self):
        self.set_strategy()
        Logger.selected_strategy(self.strategy)
        while True:
            if not self.game_state.land_played:
                self.play_land()
            casted_spells_count = self.cast_spells()
            if casted_spells_count == 0:
                break

    def play_land(self):
        land = self.pick_land()
        if land:
            self.zones.play_land(land)
            Logger.card_played(land)

    def pick_land(self):
        priority = {
            "Misty Rainforest": 1,
            "Breeding Pool": 2,
            "Snow-Covered Island": 3,
            "Snow-Covered Forest": 4,
            "Mystic Sanctuary": 5,
            "Steam Vents": 6,
            "Stomping Ground": 7,
            "Snow-Covered Mountain": 8,
            "Valakut, the Molten Pinnacle": 9
        }

        top_card = ["", 99]
        for c in self.zones.hand.cards:
            x = priority.get(c[0])
            if x:
                if x < top_card[1]:
                    top_card = [c, x]

        return top_card[0]

    def cast_spells(self):
        result = 0
        spells_rdy_cast = self.zones.find_spells_ready_to_cast()
        if spells_rdy_cast:
            if self.strategy == Strategy.RAMP:
                result = self.cast_ramp_spell(spells_rdy_cast)
            elif self.strategy == Strategy.DIG_RAMP or self.strategy == Strategy.DIG_SS:
                result = self.cast_dig_spell(spells_rdy_cast)
            else:
                result = self.cast_ss(spells_rdy_cast)
        return result

    def set_strategy(self):
        lands_on_bf = self.zones.battlefield.count_lands()
        if lands_on_bf >= 7:
            if "Scapeshift" in self.zones.hand.cards:
                self.strategy = Strategy.CAST_SS
            else:
                self.strategy = Strategy.DIG_SS
        else:
            potencial_lands = lands_on_bf + self.zones.hand.countType("Land")
            if potencial_lands >= 7:
                if "Scapeshift" in self.zones.hand.cards:
                    self.strategy = Strategy.RAMP
                else:
                    self.strategy = Strategy.DIG_SS
            else:
                if self.ramp_in_hand():
                    self.strategy = Strategy.RAMP
                else:
                    if "Scapeshift" in self.zones.hand.cards:
                        self.strategy = Strategy.DIG_RAMP
                    else:
                        self.strategy = Strategy.DIG_SS

    def ramp_in_hand(self):
        ramp_spells = {
            'Sakura-Tribe Elder',
            'Search for Tomorrow',
            'Growth Spiral',
            "Uro, Titan of Nature's Wrath"
        }
        return self.zones.hand.find(ramp_spells)

    def cast_ramp_spell(self, spells_rdy_cast):

        result = 0;
        priority = {
            "Uro, Titan of Nature's Wrath": 0,
            "Search for Tomorrow": 1,
            "Sakura-Tribe Elder": 2,
            "Growth Spiral": 3,
        }

        top_card = ["", 99]
        for c in spells_rdy_cast:
            x = priority.get(c[0])
            if x:
                if x < top_card[1]:
                    top_card = [c, x]

        if top_card[0]:
            self.cast(top_card[0])
            result = 1

        return result

    def cast_dig_spell(self, spells_rdy_cast):
        return 0

    def cast_ss(self, spells_rdy_cast):
        return 0

    def cast(self, card):
        Logger.card_played(card)
        self.zones.tap_lands(card[1])
        if card[0] == 'Uro, Titan of Nature\'s Wrath':
            self.zones.draw()
            self.play_land()
        elif card[0] == 'Search for Tomorrow':
            card = self.zones.tutor_by_name("Snow-Covered Forest", Zone.LIBRARY, Zone.BATTLEFIELD)
            if not card:
                card = self.zones.tutor_by_name("Snow-Covered Island", Zone.LIBRARY, Zone.BATTLEFIELD)
            if not card:
                card = self.zones.tutor_by_name("Snow-Covered Mountain", Zone.LIBRARY, Zone.BATTLEFIELD)
            if card:
                Logger.card_played(card)
        elif card[0] == 'Sakura-Tribe Elder':
            card = self.zones.tutor_by_name("Snow-Covered Forest", Zone.LIBRARY, Zone.BATTLEFIELD)
            if not card:
                card = self.zones.tutor_by_name("Snow-Covered Island", Zone.LIBRARY, Zone.BATTLEFIELD)
            if not card:
                card = self.zones.tutor_by_name("Snow-Covered Mountain", Zone.LIBRARY, Zone.BATTLEFIELD)
            if card:
                Logger.card_played(card)
                self.zones.battlefield.tap(card)
        elif card[0] == 'Growth Spiral':
            self.zones.draw()
            self.play_land()
