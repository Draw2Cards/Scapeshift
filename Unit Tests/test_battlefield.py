import copy
import unittest

from cards.permanent import Permanent
from zones.Battlefield import Battlefield


class BattlefieldRemoveMonitor(Battlefield):
    def __init__(self):
        Battlefield.__init__(self)
        self.lands_count_decreased = False

    def remove(self, obj):
        old_lands_count = self.lands_count
        Battlefield.remove(self, obj)
        if old_lands_count == self.lands_count + 1:
            self.lands_count_decreased = True


class TestBattlefield(unittest.TestCase):
    def test__append__adding_land__increases_count(self):
        battlefield = Battlefield()
        card = ('Misty Rainforest', 0.0, '', ['Land'])
        battlefield.append(Permanent(card))
        self.assertTrue(battlefield.lands_count, 1)

    def test__remove__removing_land_decreases_count(self):
        battlefield = BattlefieldRemoveMonitor()
        card = ('Misty Rainforest', 0.0, '', ['Land'])
        permanent = Permanent(card)
        battlefield.append(permanent)
        battlefield.remove(permanent)
        self.assertTrue(battlefield.lands_count_decreased)


if __name__ == '__main__':
    unittest.main()
