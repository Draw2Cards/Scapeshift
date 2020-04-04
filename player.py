import random
from zone import ZonesManager


class Player:
    def __init__(self, zone):
        self.hand_keep = True
        self.card_limit = 7
        self.zones = ZonesManager(zone)

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
            self.zones.hand.romove(to_delete)
