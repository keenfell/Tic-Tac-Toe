import numpy as np, array
from brain import *


def main():

    game = initialize_game()
    game_is_on = True

    while True:
        print(game.display_table())
        if game.has_won():
            print("Someone won!")
        game.next_player()
        game.commence_turn()
        if game.has_won():
            print("Someone won!")
        print(game.display_table())


def initialize_game() -> Brain:
    player1 = fetch_player(player_n=1)
    player2 = fetch_player(player_n=2)
    return Brain(players=[player1, player2])


def fetch_player(player_n: int):
    name = input(f"What's P{player_n}'s name? : ")
    symbol = input(f"What's P{player_n}'s symbol? : ")
    return Player(name, symbol)


# TODO: Find a way to make the tic-tac-toe generate diagnol paths heading south-west

if __name__ == "__main__":
    main()
