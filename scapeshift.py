from deck import Deck
from finders import DbFinder, ScryfallFinder
from database_manager import DatabaseManager
from zone import ZonesManager


def main():
    db_manager = DatabaseManager()
    deck = Deck("D:\\scapeshift_02-04-2020.txt")
    if deck.count == 60:
        print('Deck size: OK.')
        print('Collecting cards data...')
        db_manager.init()
        db_finder = DbFinder(db_manager)
        sf_finder = ScryfallFinder(db_manager)
        deck.fill_dict([db_finder, sf_finder])
        if not deck.not_found_cards:
            print('Card data: OK.')
            library = deck.to_library()
            hand = []
            battlefield = []
            graveyard = []
            exile = []
            zones = ZonesManager(library, hand, battlefield, graveyard, exile)

        else:
            print('Card data:ERROR.')
            print('Card not found:')
            for card in deck.not_found_cards:
                print(card)
        db_manager.close()
    else:
        print('Deck size: ERROR({}).'.format(deck.count))


if __name__ == "__main__":
    main()
