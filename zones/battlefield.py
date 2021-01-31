class Battlefield:
    lands_count = 0

    def __init__(self):
        self.permanents = []

    def count_open_mana(self):
        result = 0
        for p in self.permanents:
            if "Land" in p.card[3]:
                if p.untapped:
                    result += 1
        return result
