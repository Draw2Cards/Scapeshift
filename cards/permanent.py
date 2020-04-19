class Permanent:
    def __init__(self, card):
        self.card = card
        self.untapped = True

    def init(self, untapped=True):
        self.untapped = untapped

    def untap(self):
        self.untapped = True

    def upkeep(self):
        pass
