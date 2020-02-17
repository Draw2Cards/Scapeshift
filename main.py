import copy
import random
from itertools import count
from typing import Type


class Card:
    def __init__(self, name, card_types, cmc, card_id):
        self.name = name
        self.card_types = card_types
        self.counters = 0
        self.untapped = True
        self.cmc = cmc
        self.card_id = card_id


class RoundStatus:
    def __init__(self):
        self.land_was_played = False
        self.turn = 0


def print_cards(deck):
    cards_count = 0
    for x in deck:
        cards_count += 1
        print("%s. %s - %s" % (cards_count, x.name, x.card_types))
    print()


def draw_card(to, deck, cards_count=1):
    to += deck[:cards_count]
    del deck[:cards_count]


def play_land(hand, bf, library, gy):
    x = search_for(hand, Card("", ["Land", "Fetch"], "", 0))
    if x:
        y = search_for(library, Card("", ["Land", "Forest"], "", 0))
        random.shuffle(library)
        if y:
            gy.append(x)
            bf.append(y)
            hand.remove(x)
            library.remove(y)
        else:
            y = search_for(library, Card("", ["Land", "Island"], "", 0))
            if y:
                gy.append(x)
                bf.append(y)
                hand.remove(x)
                library.remove(y)
            else:
                y = search_for(library, Card("", ["Land", "Mountain"], "", 0))
                if y:
                    gy.append(x)
                    bf.append(y)
                    hand.remove(x)
                    library.remove(y)
        return True
    else:
        x = search_for(hand, Card("", ["Land"], "", 0))
        if x:
            bf.append(x)
            hand.remove(x)
            return True
        else:
            return False


def check_deck(hand, deck, bf, gy, ex, tmp_zone=[]):
    if (len(hand) + len(deck) + len(bf) + len(gy) + len(ex) + len(tmp_zone)) == 60:
        return True
    return False


def get_untapped_lands_count(bf):
    lands_count = 0
    for x in bf:
        if "Land" in x.card_types:
            if x.untapped:
                lands_count += 1
    return lands_count


def tap_lands(bf, lands_count):
    for x in bf:
        if "Land" in x.card_types:
            if x.untapped:
                x.untapped = False
                lands_count -= 1
                if lands_count == 0:
                    break


def cast_growth_spiral(hand, deck, bf, gv):
    for x in hand:
        if x.name == "Growth Spiral":
            if get_untapped_lands_count(bf) >= 2:
                tap_lands(bf, 2)
                gv.append(x)
                hand.remove(x)
                draw_card(hand, deck)
                play_land(hand, bf, deck, gv)
                return True
            break
    return False


def untap_bf(bf):
    for x in bf:
        if not x.untapped:
            x.untapped = True


def count_cards(field, card):
    card_count = 0
    if card.name:
        for x in field:
            if card.name == x.name:
                card_count += 1
    else:
        for x in field:
            if all(elem in x.card_types for elem in card.card_types):
                card_count += 1
    return card_count


def cast_scapeshift(hand, deck, bf, gv, rs):
    for x in hand:
        if x.name == "Scapeshift":
            if get_untapped_lands_count(bf) >= 7:
                if count_cards(bf, Card("", ["Land"], "", 0)) >= 7:
                    tap_lands(bf, 7)
                    gv.append(x)
                    hand.remove(x)
                    # sacrifice lands
                    # search lands
                    # put land onto the bf
                    return True
            break
    return False


def search_for(from_list, card):
    if card.name:
        for x in from_list:
            if card.name == x.name:
                return x
    else:
        for x in from_list:
            if all(elem in x.card_types for elem in card.card_types):
                return x


def cast_search_for_tomorrow(hand, deck, bf, gv):
    for x in hand:
        if x.name == "Search for Tomorrow":
            if get_untapped_lands_count(bf) >= 3:
                tap_lands(bf, 3)
                gv.append(x)
                hand.remove(x)
                y = search_for(deck, Card("", ["Land", "Basic"], "", 0))
                random.shuffle(deck)
                if y:
                    bf.append(y)
                    deck.remove(y)
                return True
            break
    return False


def susped_search_for_tomorrow(hand, exile, bf):
    for x in hand:
        if x.name == "Search for Tomorrow":
            if get_untapped_lands_count(bf) >= 1:
                tap_lands(bf, 1)
                exile.append(x)
                hand.remove(x)
                x.counters = 2


def cast_sakura_tribe_elder(hand, deck, bf, gy):
    for x in hand:
        if x.name == "Sakura-Tribe Elder":
            if get_untapped_lands_count(bf) >= 2:
                tap_lands(bf, 2)
                gy.append(x)
                hand.remove(x)
                y = search_for(deck, Card("", ["Land", "Basic"], "", 0))
                random.shuffle(deck)
                if y:
                    bf.append(y)
                    deck.remove(y)
                    y.untapped = False
                return True
            break
    return False


def cast_snapcaster_mage(hand, bf, gy, exile, library):
    scm_target = None
    for x in hand:
        if x.name == "Snapcaster Mage":
            if get_untapped_lands_count(bf) >= 2:
                if get_untapped_lands_count(bf) >= 2 + 3:
                    for y in gy:
                        if y.name == "Search for Tomorrow":
                            scm_target = y
                            break
                        elif y.name == "Growth Spiral":
                            scm_target = y
                    break
                elif get_untapped_lands_count(bf) >= 2 + 2:
                    for y in gy:
                        if y.name == "Growth Spiral":
                            scm_target = y
                            break
                break
        break

    if scm_target:
        tap_lands(bf, 2)
        bf.append(x)
        hand.remove(x)
        if scm_target.name == "Search for Tomorrow":
            cast_search_for_tomorrow(gy, library, bf, exile)
            return True
        elif scm_target.name == "Growth Spiral":
            cast_growth_spiral(gy, library, bf, exile)
            return True
    return False


def prepare_line(win_turn, card1, card2, hand_cpy, deck_cpy, bf_cpy, gy_cpy, rs_cpy):
    untapped_lands = get_untapped_lands_count(bf_cpy)
    land = count_cards(bf_cpy, Card("", ["Land"], "", 0))
    scapeshift_hand = count_cards(hand_cpy, Card("Scapeshift", "", "", 0))
    scapeshift_libary = count_cards(deck_cpy, Card("Scapeshift", [], "", 0))
    scapeshift_gy = count_cards(gy_cpy, Card("Scapeshift", [], "", 0))

    growth_spiral_hand = count_cards(hand_cpy, Card("Growth Spiral", [], "", 0))
    growth_spiral_libary = count_cards(deck_cpy, Card("Growth Spiral", [], "", 0))
    growth_spiral_gy = count_cards(gy_cpy, Card("Growth Spiral", [], "", 0))

    s_f_t_hand = count_cards(hand_cpy, Card("Search for Tomorrow", [], "", 0))
    s_f_t_libary = count_cards(deck_cpy, Card("Search for Tomorrow", [], "", 0))
    s_f_t_gy = count_cards(gy_cpy, Card("Search for Tomorrow", [], "", 0))

    s_t_e_hand = count_cards(hand_cpy, Card("Sakura-Tribe Elder", [], "", 0))
    s_t_e_libary = count_cards(deck_cpy, Card("Sakura-Tribe Elder", [], "", 0))

    s_m_hand = count_cards(hand_cpy, Card("Snapcaster Mage", [], "", 0))
    s_m_libary = count_cards(deck_cpy, Card("Snapcaster Mage", [], "", 0))

    d_f_d_hand = count_cards(hand_cpy, Card("Drawn from Dreams", [], "", 0))
    d_f_d_libary = count_cards(deck_cpy, Card("Drawn from Dreams", [], "", 0))
    d_f_d_gy = count_cards(gy_cpy, Card("Drawn from Dreams", [], "", 0))

    return "%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % (
    win_turn, card1.card_id, card2.card_id, int(rs_cpy.land_was_played), land, untapped_lands, scapeshift_hand,
    scapeshift_libary, scapeshift_gy, growth_spiral_hand, growth_spiral_libary, growth_spiral_gy, s_f_t_hand,
    s_f_t_libary, s_f_t_gy, s_t_e_hand, s_t_e_libary, s_m_hand, s_m_libary, d_f_d_hand, d_f_d_libary, d_f_d_gy)


def add_game_to_csv(win_turn, card1, card2, hand_cpy, deck_cpy, bf_cpy, gy_cpy, rs_cpy):
    file_name = "test.csv"
    line = prepare_line(win_turn, card1, card2, hand_cpy, deck_cpy, bf_cpy, gy_cpy, rs_cpy)
    f = open(file_name, "a+")
    f.write(line + "\n")
    f.close()


def start_game(hand, deck, bf, gy, exile, rs, gd, new_game):
    check_deck(hand, deck, bf, gy, exile)
    casted_spells = []
    new_win = False
    while not new_win:

        if new_game:
            rs.land_was_played = False
            rs.turn += 1
            untap_bf(bf)
            manage_suspended_cards(exile, deck, bf, gy)
            draw_card(hand, deck)

        if not rs.land_was_played:
            if play_land(hand, bf, deck, gy):
                RS.land_was_played = True
        check_deck(hand, deck, bf, gy, exile)
        casted_spells = cast_spells(hand, deck, bf, exile, gy, rs, gd)

        if not rs.land_was_played:
            if play_land(hand, bf, deck, gy):
                rs.land_was_played = True
        new_win = check_win(casted_spells)

        new_game = True
    return rs.turn


def prepare_all_combinations(tmp_zone):
    cards_combinations = []
    for x in tmp_zone:
        for y in tmp_zone:
            if x != y:
                rest = []
                for b in tmp_zone:
                    if b != x and b != y:
                        rest.append(b)
                cards_combinations.append([x, y, rest])

    for z in cards_combinations:
        card1 = z[0]
        card2 = z[1]
        for a in cards_combinations:
            if not z == a:
                if card1.name == a[0].name:
                    if card2.name == a[1].name:
                        cards_combinations.remove(a)
                elif card1.name == a[1].name:
                    if card2.name == a[0].name:
                        cards_combinations.remove(a)

    return cards_combinations


def cast_drawn_from_dreams(hand, deck, bf, gy, exile, rs, gd):
    for x in hand:
        if x.name == "Drawn from Dreams":
            if get_untapped_lands_count(bf) >= 4:
                check_deck(hand, deck, bf, gy, exile)
                tap_lands(bf, 4)
                gy.append(x)
                hand.remove(x)

                tmp_zone = []
                draw_card(tmp_zone, deck, 7)

                hand_cpy = hand.copy()
                deck_cpy = deck.copy()
                bf_cpy = bf.copy()
                gy_cpy = gy.copy()
                exile_cpy = exile.copy()
                rs_copy = copy.copy(rs)

                combinations = prepare_all_combinations(tmp_zone)
                counter = 0
                for y in combinations:
                    counter = counter + 1
                    hand_cpy.append(y[0])
                    hand_cpy.append(y[1])
                    deck_cpy.extend(y[2])

                    print("Start INGame: %s" % counter)
                    in_win = start_game(hand_cpy, deck_cpy, bf_cpy, gy_cpy, exile_cpy, rs_copy, gd, False)
                    print("End INGame: %s" % counter)
                    add_game_to_csv(in_win, y[0], y[1], hand, deck, bf, gy, rs)

                    hand_cpy = hand.copy()
                    deck_cpy = deck.copy()
                    bf_cpy = bf.copy()
                    gy_cpy = gy.copy()
                    exile_cpy = exile.copy()

                    rs_copy = copy.copy(rs)
                    check_deck(hand, deck, bf, gy, exile, tmp_zone)
                return True
    return False


def cast_spells(hand, deck, bf, exile, gy, rs, gd):
    check_deck(hand, deck, bf, gy, exile)
    casted_spells = []
    casted_spells_count = 0
    while True:
        if cast_scapeshift(hand, deck, bf, gy, rs):
            casted_spells.append(Card("Scapeshift", "Sorcery", "2GG", 0))
        if cast_drawn_from_dreams(hand, deck, bf, gy, exile, rs, gd):
            casted_spells.append(Card("Scapeshift", "Sorcery", "2GG", 0))
        if cast_snapcaster_mage(hand, bf, gy, exile, deck):
            casted_spells.append(Card("Snapcaster Mage", "Creature", "1U", 0))
        if cast_search_for_tomorrow(hand, deck, bf, gy):
            casted_spells.append(Card("Search for Tomorrow", "Sorcery", "2G", 0))
        if cast_sakura_tribe_elder(hand, deck, bf, gy):
            casted_spells.append(Card("Sakura-Tribe Elder", "Creature", "1G", 0))
        if cast_growth_spiral(hand, deck, bf, gy):
            casted_spells.append(Card("Growth Spiral", "Instant", "GU", 0))
        susped_search_for_tomorrow(hand, exile, bf)

        x = search_for(casted_spells, Card("Scapeshift", "Sorcery", "2GG", 0))
        if x:
            return casted_spells

        if len(casted_spells) == casted_spells_count:
            break
        else:
            casted_spells_count = len(casted_spells)

    return casted_spells


def check_win(casted_spells):
    for x in casted_spells:
        if x.name == "Scapeshift":
            return True
    return False


def manage_suspended_cards(exile, library, bf, gy):
    for x in Exile:
        if x.name == "Search for Tomorrow":
            x.counters -= 1
            if x.counters == 0:
                gy.append(x)
                exile.remove(x)
                y = search_for(library, Card("", ["Land", "Basic"], "", 0))
                random.shuffle(library)
                if y:
                    bf.append(y)
                    library.remove(y)


GenerateData = True
RS = RoundStatus()
main_loop = 0
number_of_tests = 1
wins = []

while main_loop < number_of_tests:
    main_loop += 1

    DeckList = [
        Card("Snow-Covered Forest", ["Land", "Basic", "Forest"], "", 1),
        Card("Snow-Covered Forest", ["Land", "Basic", "Forest"], "", 1),
        Card("Snow-Covered Island", ["Land", "Basic", "Island"], "", 2),
        Card("Snow-Covered Island", ["Land", "Basic", "Island"], "", 2),
        Card("Snow-Covered Island", ["Land", "Basic", "Island"], "", 2),
        Card("Snow-Covered Mountain", ["Land", "Basic", "Mountain"], "", 3),
        Card("Snow-Covered Mountain", ["Land", "Basic", "Mountain"], "", 3),
        Card("Breeding Pool", ["Land", "Forest", "Island"], "", 4),
        Card("Breeding Pool", ["Land", "Forest", "Island"], "", 4),
        Card("Steam Vents", ["Land", "Mountain", "Island"], "", 5),
        Card("Steam Vents", ["Land", "Mountain", "Island"], "", 5),
        Card("Steam Vents", ["Land", "Mountain", "Island"], "", 5),
        Card("Steam Vents", ["Land", "Mountain", "Island"], "", 5),
        Card("Stomping Ground", ["Land", "Mountain", "Forest"], "", 6),
        Card("Stomping Ground", ["Land", "Mountain", "Forest"], "", 6),
        Card("Stomping Ground", ["Land", "Mountain", "Forest"], "", 6),
        Card("Stomping Ground", ["Land", "Mountain", "Forest"], "", 6),
        Card("Valakut, the Molten Pinnacle", ["Land", "Tapped"], "", 7),
        Card("Valakut, the Molten Pinnacle", ["Land", "Tapped"], "", 7),
        Card("Flooded Grove", "Land", "", 8),
        Card("Misty Rainforest", ["Land", "Fetch"], "", 9),
        Card("Misty Rainforest", ["Land", "Fetch"], "", 9),
        Card("Misty Rainforest", ["Land", "Fetch"], "", 9),
        Card("Misty Rainforest", ["Land", "Fetch"], "", 9),

        Card("Scapeshift", "Sorcery", "2GG", 10),
        Card("Scapeshift", "Sorcery", "2GG", 10),
        Card("Scapeshift", "Sorcery", "2GG", 10),
        Card("Scapeshift", "Sorcery", "2GG", 10),

        Card("Growth Spiral", "Instant", "GU", 11),
        Card("Growth Spiral", "Instant", "GU", 11),
        Card("Growth Spiral", "Instant", "GU", 11),
        Card("Growth Spiral", "Instant", "GU", 11),

        Card("Search for Tomorrow", "Sorcery", ["2G", "G"], 12),
        Card("Search for Tomorrow", "Sorcery", ["2G", "G"], 12),
        Card("Search for Tomorrow", "Sorcery", ["2G", "G"], 12),
        Card("Search for Tomorrow", "Sorcery", ["2G", "G"], 12),

        Card("Sakura-Tribe Elder", "Creature", "1G", 13),
        Card("Sakura-Tribe Elder", "Creature", "1G", 13),
        Card("Sakura-Tribe Elder", "Creature", "1G", 13),
        Card("Sakura-Tribe Elder", "Creature", "1G", 13),

        Card("Snapcaster Mage", "Creature", "1U", 14),
        Card("Snapcaster Mage", "Creature", "1U", 14),
        Card("Snapcaster Mage", "Creature", "1U", 14),
        Card("Snapcaster Mage", "Creature", "1U", 14),

        Card("Drawn from Dreams", "Sorcery", "2UU", 15),
        Card("Drawn from Dreams", "Sorcery", "2UU", 15),
        Card("Drawn from Dreams", "Sorcery", "2UU", 15),
        Card("Drawn from Dreams", "Sorcery", "2UU", 15),
        Card("TODO", "TODO", "", 0),
        Card("TODO", "TODO", "", 0),
        Card("TODO", "TODO", "", 0),
        Card("TODO", "TODO", "", 0),
        Card("TODO", "TODO", "", 0),
        Card("TODO", "TODO", "", 0),
        Card("TODO", "TODO", "", 0),
        Card("TODO", "TODO", "", 0),
        Card("TODO", "TODO", "", 0),
        Card("TODO", "TODO", "", 0),
        Card("TODO", "TODO", "", 0),
        Card("TODO", "TODO", "", 0)
    ]

    random.shuffle(DeckList)
    win = False
    RS.turn = 0

    Hand = DeckList[:7]
    del DeckList[:7]

    Battlefield = []
    Graveyard = []
    Exile = []
    print("Start Game: %s" % main_loop)
    win = start_game(Hand, DeckList, Battlefield, Graveyard, Exile, RS, GenerateData, True)
    print("End Game: %s" % main_loop)
    print("Win at: %s" % win)
