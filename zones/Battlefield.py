class Battlefield:
    lands_count = 0

    def __init__(self):
        self.permanents = []

    def append(self, obj):
        self.permanents.append(obj)
        if "Land" in obj.card[3]:
            Battlefield.lands_count += 1

    def remove(self, obj):
        self.permanents.remove(obj)
        if "Land" in obj.card[3]:
            Battlefield.lands_count -= 1
