class Battlefield:

    def __init__(self):
        self.permanents = []

    def count_open_mana(self):
        result = 0
        for p in self.permanents:
            if "Land" in p.card[3]:
                if p.untapped:
                    result += 1
        return result

    def count_lands(self):
        result = 0
        for p in self.permanents:
            if "Land" in p.card[3]:
                result += 1
        return result

    def tap_lands(self, cost):
        result = 0
        for p in self.permanents:
            if "Land" in p.card[3]:
                if p.untapped:
                    p.untapped = False
                    result += 1
        return result

    def tap(self, card):
        for p in self.permanents:
            if p.card is card:
                p.untapped = False
