import numpy as np, array
from brain import *


def main():

    game = initialize_game()
    game_is_on = True

    while True:
        print(game.display_table())
        game.commence_turn()
        game.next_player()
        print(game.display_table())


def initialize_game() -> Brain:
    player1 = fetch_player(player_n=1)
    player2 = fetch_player(player_n=2)
    return Brain(players=[player1, player2])


def fetch_player(player_n: int):
    name = input(f"What's P{player_n}'s name? : ")
    symbol = input(f"What's P{player_n}'s symbol? : ")
    return Player(name, symbol)


# TODO: Movie this tic-tac-toe display stuff into a class

if __name__ == "__main__":
    main()
