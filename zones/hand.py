class Hand:

    def __init__(self):
        self.cards = []

    def countType(self, typeName):
        result = 0
        for c in self.cards:
            if typeName in c[3]:
                result += 1
        return result

    def find(self, namesList):
        result = False
        for c in self.cards:
            if c[0] in namesList:
                result = True
                break
        return result

    def find_spells_with_cmc_leq(self, cmc):
        result = []
        for c in self.cards:
            if c[1] <= cmc:
                if "Land" not in c[3]:
                    result.append(c)
        return result
