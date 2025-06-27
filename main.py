from brain import *
from game_settings import *  # constants

YES = "y"
NO = "n"


def main():

    game = initialize_game()
    game_is_on = True

    while game_is_on:
        game.next_player()
        game.commence_turn()
        if player := game.has_won():
            game_is_on = False
        print(game.display_table())

    print(f"{player.name} won!")


def initialize_game() -> Brain:
    player1 = fetch_player(player_n=1)
    if wants_ai_player():
        player2 = AIPlayer(
            unallowed_names=player1.name, unallowed_symbols=player1.symbol
        )  # generates own name
    else:
        player2 = fetch_player(
            player_n=2, taken_names=player1.name, taken_symbols=player1.symbol
        )
    return Brain(players=[player1, player2])


def fetch_player(player_n: int, taken_symbols=None, taken_names=None):
    name = fetch_inp(player_n=player_n, unallowed=taken_names, request="name")
    symbol = fetch_inp(player_n=player_n, unallowed=taken_symbols, request="symbol")
    return Player(name, symbol)


def fetch_inp(player_n, unallowed=None, request="name", as_type=str) -> str:
    while True:
        try:
            inp = as_type(input(f"What's P{player_n}'s {request}? : ")).title()
        except ValueError:
            pass

        if unallowed:
            if inp in unallowed:
                print(f"Whoops! That {request} is already taken!")
                continue
        return inp


def wants_ai_player() -> bool:
    while True:
        inp = input(f"Do you want an AI player? {YES}/{NO}").lower()
        if inp == YES:
            return True
        elif inp == NO:
            return False
        else:
            print("Did you put the right input?")


if __name__ == "__main__":
    main()
