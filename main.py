from game.game_state import GameState
from setup.deck import Deck
from setup.finders import DbFinder, ScryfallFinder
from setup.database_manager import DatabaseManager
from game.game import Game
from game.player import Player, RugPlayer
from game.zone import ZonesManager
from zones.battlefield import Battlefield
from zones.hand import Hand

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
            game_state = GameState()
            bf = Battlefield()
            hand = Hand()
            zones = ZonesManager(library, hand, bf, [], [], [], game_state)
            # player = Player(zones, game_state)
            player = RugPlayer(zones, game_state)
            game = Game(zones, game_state, player)
            print(" Game: START")
            game.play()
            print(" Game: END")
            print("Outcome: {}".format(game_state.outcome.name))
            print("Turn: {}".format(game_state.turn_counter))
        else:
            print('Card data: ERROR.')
            print('Card not found:')
            for card in deck.not_found_cards:
                print(card)
        db_manager.close()
    else:
        print('Deck size: ERROR({}).'.format(deck.count))


if __name__ == "__main__":
    main()
