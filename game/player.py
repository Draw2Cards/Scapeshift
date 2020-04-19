import random

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
        while len(self.zones.hand) > self.card_limit:
            to_delete = random.choice(self.zones.hand)
            self.zones.discard(to_delete)


class RugPlayer(Player):
    def precombat_main_phase(self):
        if not self.game_state.land_played:
            self.play_land()

    def play_land(self):
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
        for c in self.zones.hand:
            x = priority.get(c[0])
            if x:
                if x < top_card[1]:
                    top_card = [c[0], x]

        return top_card[0]
