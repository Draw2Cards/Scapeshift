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

    def can_cast(self, card):
        available_mana = []
        for p in self.permanents:
            if "Land" in p.card[3]:
                if p.untapped:
                    if p.card[0] == 'Breeding Pool':
                        available_mana.append(["U", "G"])
                    elif p.card[0] == 'Snow-Covered Island':
                        available_mana.append("U")
                    elif p.card[0] == 'Snow-Covered Forest':
                        available_mana.append("G")
                    elif p.card[0] == 'Mystic Sanctuary':
                        available_mana.append("U")
                    elif p.card[0] == 'Steam Vents':
                        available_mana.append(["U", "R"])
                    elif p.card[0] == 'Stomping Ground':
                        available_mana.append(["G", "R"])
                    elif p.card[0] == 'Snow-Covered Mountain':
                        available_mana.append("R")
                    elif p.card[0] == 'Valakut, the Molten Pinnacle':
                        available_mana.append("R")
                    else:
                        raise NotImplementedError(p.card[0] + ': Not Implemented!')

    def get_fetches(self):
        fetches = []
        for p in self.permanents:
            if "Land" in p.card[3]:
                if p.card[0] == 'Flooded Strand':
                    fetches.append(p.card)
                elif p.card[0] == 'Polluted Delta':
                    fetches.append(p.card)
                elif p.card[0] == 'Bloodstained Mire':
                    fetches.append(p.card)
                elif p.card[0] == 'Wooded Foothills':
                    fetches.append(p.card)
                elif p.card[0] == 'Wooded Foothills':
                    fetches.append(p.card)
                elif p.card[0] == 'Marsh Flats':
                    fetches.append(p.card)
                elif p.card[0] == 'Scalding Tarn':
                    fetches.append(p.card)
                elif p.card[0] == 'Verdant Catacombs':
                    fetches.append(p.card)
                elif p.card[0] == 'Arid Mesa':
                    fetches.append(p.card)
                elif p.card[0] == 'Misty Rainforest':
                    fetches.append(p.card)
        return fetches

    def get_cards(self):
        result = []
        for p in self.permanents:
            result.append(p.card)
        return result

    def remove(self, card):
        for p in self.permanents:
            if p.card == card:
                self.permanents.remove(p)
