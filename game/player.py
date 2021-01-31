import random
from enum import Enum

from game.zone import Zone


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
            to_delete = random.choice(self.zones.hand)
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
        while True:
            if not self.game_state.land_played:
                self.play_land()
            casted_spells_count = self.cast_spells()
            if casted_spells_count == 0:
                break

    def play_land(self):
        land = self.pick_land()
        if land:
            self.zones.play_land(self.pick_land())

    def pick_land(self):
        priority = {
            "Misty Rainforest": 0,
            "Breeding Pool": 1,
            "Snow-Covered Island": 2,
            "Snow-Covered Forest": 3,
            "Mystic Sanctuary": 4,
            "Steam Vents": 5,
            "Stomping Ground": 6,
            "Snow-Covered Mountain": 7,
            "Valakut, the Molten Pinnacle": 8
        }

        top_card = ["", 99]
        for c in self.zones.hand.cards:
            x = priority.get(c[0])
            if x:
                if x < top_card[1]:
                    top_card = [c[0], x]

        return top_card[0]

    def cast_spells(self):
        result = 0
        spells_cast = self.zones.find_spells_ready_to_cast()
        return result

    def set_strategy(self):
        lands_on_bf = self.zones.battlefield.lands_count
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
