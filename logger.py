def get_cards_names(cards_list):
    result = []
    for c in cards_list:
        result.append(c[0])
    return "; ".join(result)


class Logger:

    @staticmethod
    def hand(cards_list):
        print("  Hand: " + get_cards_names(cards_list))

    @staticmethod
    def draw_step(card):
        if card:
            print("   Draw step: " + get_cards_names(card))
        else:
            print("   Draw step: -")

    @staticmethod
    def turn_start(turn):
        print("  Turn: ", turn)

    @staticmethod
    def card_played(card):
        print("   Card played: ", card[0])
