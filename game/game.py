from game.game_state import GameState, Outcome


class Game:
    def __init__(self, zones, game_state, player):
        self.game_state = game_state
        self.zones = zones
        self.player = player

    def play(self):
        self.preparation()
        while self.game_state.outcome is Outcome.UNRESOLVED:
            self.turn()

    def preparation(self):
        self.zones.shuffle_library()
        self.zones.draw(7)
        while not self.player.hand_keep:
            self.zones.mulligan()

    def turn(self):
        self.game_state.turn_counter += 1
        self.beginning_phase()
        self.precombat_main_phase()
        self.combat_phase()
        self.postcombat_main_phase()
        self.ending_phase()

    def beginning_phase(self):
        self.untap_step()
        self.upkeep_step()
        self.draw_step()

    def untap_step(self):
        for c in self.zones.battlefield:
            c.untap()

    def upkeep_step(self):
        for c in self.zones.battlefield:
            c.upkeep()

    def draw_step(self):
        if self.game_state.turn_counter is 1:
            if self.game_state.first:
                return
        self.zones.draw()

    def precombat_main_phase(self):
        self.player.precombat_main_phase()

    def combat_phase(self):
        self.beginning_of_combat_step()
        if self.declare_attackers_step() > 0:
            self.declare_blockers_step()
            self.combat_damage_step()
            self.end_of_combat_step()

    def beginning_of_combat_step(self):
        self.player.beginning_of_combat_step()

    def declare_attackers_step(self):
        # returns number of attacking creatures
        return self.player.declare_attackers_step()

    def declare_blockers_step(self):
        self.player.declare_blockers_step()

    def combat_damage_step(self):
        self.player.combat_damage_step()

    def end_of_combat_step(self):
        self.player.end_of_combat_step()

    def postcombat_main_phase(self):
        self.player.postcombat_main_phase()

    def ending_phase(self):
        self.end_step()
        self.cleanup_step()

    def end_step(self):
        self.player.end_step()

    def cleanup_step(self):
        self.player.cleanup_step()
