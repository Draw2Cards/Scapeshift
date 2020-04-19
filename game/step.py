from abc import ABC


class Step:
    def __int__(self, zones, game_state, player):
        self.zones = zones
        self.game_state = game_state
        self.player = player

    def run(self):
        raise NotImplementedError('Not Implemented Error!')


class StepUntap(Step):
    def __init__(self, battlefield):
        self.battlefield = battlefield

    def run(self):
        for c in self.battlefield:
            c.untap()


class StepUpkeep(Step):
    def __init__(self, battlefield):
        self.battlefield = battlefield

    def run(self):
        for c in self.battlefield:
            c.upkeep()


class StepDraw(Step):
    def __init__(self, zones, game_state):
        self.zones = zones
        self.game_state = game_state

    def run(self):
        if self.game_state.turn_counter is 1:
            if self.game_state.first:
                return
        self.zones.draw()


class StepCombat(Step):
    def __init__(self, player):
        self.player = player

    def run(self):
        raise NotImplementedError('Not Implemented Error!')


class StepCombatBeginning(StepCombat):
    def run(self):
        self.player.beginning_of_combat_step()


class StepDeclareAttackers(StepCombat):
    def run(self):
        # returns number of attacking creatures
        return self.player.declare_attackers_step()


class StepDeclareBlockers(StepCombat):
    def run(self):
        self.player.declare_blockers_step()


class StepCombatDamage(StepCombat):
    def run(self):
        self.player.combat_damage_step()


class StepCombatEnd(StepCombat):
    def run(self):
        self.player.end_of_combat_step()


class StepEnd(Step):
    def __init__(self, player):
        self.player = player

    def run(self):
        self.player.end_step()


class StepCleanup(Step):
    def __init__(self, player):
        self.player = player

    def run(self):
        self.player.cleanup_step()
