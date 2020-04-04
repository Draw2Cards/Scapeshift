class Player:
    def __init__(self):
        self.hand_keep = True

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
