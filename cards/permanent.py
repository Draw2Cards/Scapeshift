class Permanent:
    def __init__(self, card, untapped=True):
        self.card = card
        self.untapped = untapped

    def untap(self):
        self.untapped = True

    def upkeep(self):
        pass
