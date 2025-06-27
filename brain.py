import numpy as np, array
import random as rd
from game_settings import *


class Player:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol


class AIPlayer:
    def __init__(self, unallowed_names, unallowed_symbols):
        self.name = self.get_random(AI_NAMES, unwanted=unallowed_names)
        self.symbol = self.get_random(AI_SYMBOLS, unwanted=unallowed_symbols)

    def get_random(self, l: list, unwanted: list) -> str:
        if unwanted in l:
            l = self.remove_from_list(l=l, items=unwanted)
        return rd.choice(l)

    @staticmethod
    def remove_from_list(l: list, items: list) -> list:
        for item in items:
            l.pop(item)
        return l

    @staticmethod
    def get_move(cols: int, rows: int) -> str:
        """Returns a tic-tac-toe coordinate as pseudo input."""
        selected_col = rd.randint(1, cols)
        selected_row = rd.randint(1, rows)
        return f"{selected_row} {selected_col}"


class TableDisplay:
    def __init__(self, padding=TABLE_PADDING):
        self.table = self.create_table()
        self.padding = padding

    @staticmethod
    def create_table():
        table = np.array([["X" for _ in range(TABLE_SIZE)] for _ in range(TABLE_SIZE)])
        return table

    def display_table(self) -> str:
        """Display the table for front-end tic-tac-toe display."""
        fmtd = []

        for ind, row in enumerate(self.table):
            new_row = self.row_display(row)
            fmtd.append(new_row)
            if not ind == len(self.table) - 1:  # if not the last row
                fmtd.append(self.get_row_border(length=ROW_BORDER_LENGTH))
        return self.combine_rows(fmtd)

    @staticmethod
    def get_row_border(length) -> str:
        return "-" * length

    def row_display(self, row: array) -> str:

        fmtd = []

        for i in range(len(row)):
            column = self.pad(row[i], self.padding)
            if not i == len(row) - 1:
                column = column + "|"
            fmtd.append(column)
        fmtd_string = "".join(fmtd)
        return fmtd_string

    def combine_rows(self, rows: list[str]) -> str:
        for ind, row in enumerate(rows):
            rows[ind] = row + "\n"
        return "".join(rows)

    @staticmethod
    def pad(s: str, pd: int) -> str:
        padding = " " * pd
        padded = padding + s + padding
        return padded


class Brain(TableDisplay):
    def __init__(self, players: list[Player]):
        super().__init__()
        self.players = players
        self.current_turn = 0  # current player's turn by 'players' list index
        self.current_player = self.players[self.current_turn]
        self.moves_made = []

    def log_move(self, move: tuple):  # tuple of column and row
        self.moves_made.append(move)

    def next_player(self):
        if self.current_turn == len(self.players) - 1:
            self.current_turn = 0
        else:
            self.current_turn += 1
        self.update_current_player(indx_n=self.current_turn)

    def update_current_player(self, indx_n):
        self.current_player = self.players[indx_n]

    def commence_turn(self):
        """Commences the turn process. After current player turn, it will check if they have won. If the player
        has won, then it will commence the winning function."""
        turn_made = False

        while not turn_made:
            if self.is_ai_player():
                turn_inp = self.current_player.get_move(
                    rows=3, cols=3
                )  # gets random coordinates for turn input
                print("The computer is making its move...")
            else:
                turn_inp = input("Please enter your turn here: ")

            try:
                loc: tuple = self.parse_turn(turn_inp)  # parsing to account for 0 index
            except ValueError:
                print("Did you put in the correct format?")
                continue

            if not self.spot_taken(loc):
                self.log_move(loc)  # record the move
                turn_made = True
            else:
                print("Spot already taken.")

        self.mark_area(row=loc[0], col=loc[1])

    def is_ai_player(self):
        return type(self.current_player) == AIPlayer

    def spot_taken(self, turn_info: tuple) -> bool:
        return turn_info in self.moves_made

    def parse_turn(self, turn_input: str) -> tuple[str] | bool:
        col, row = turn_input.split(" ")
        try:
            col, row = (
                int(col) - 1,
                int(row) - 1,
            )  # subtract one to account for indexing
        except ValueError:
            return False
        else:
            return (col, row)

    def mark_area(self, col: int, row: int) -> None:
        self.table[row, col] = self.current_player.symbol

    def has_won(self) -> Player | bool:
        if self.is_diagnol() or self.is_horizontal() or self.is_vertical():
            return self.current_player
        return False

    def is_horizontal(self) -> bool:
        for row in self.table:
            row_report = [value == self.current_player.symbol for value in row]
            if self.enough_in_a_row(row_report, threshold=THRESHOLD):
                return True
        return False

    def is_vertical(self) -> bool:

        for i in range(len(self.table)):
            column = [
                self.table[j, i] for j in range(len(self.table))
            ]  # retrieves vertical column
            column_report = [value == self.current_player.symbol for value in column]
            if self.enough_in_a_row(
                column_report, threshold=THRESHOLD
            ):  # checking if symbols of list are in a row. if there is, then they have won
                return True
        return False  # if there are no scoring in a row

    @staticmethod
    def enough_in_a_row(l: list[bool], threshold: int) -> bool:
        """Checks the list of bools for a specificed amount in a row. Returns 'True' if the list equals the
        threshold of 'True's in a row."""
        score = 0

        for v in l:
            if v:
                score += 1
                if score >= threshold:
                    return True
            else:
                score = 0

        return False

    def is_diagnol(self) -> bool:
        routes = self.get_diagnol_routes()

        for route in routes:
            symbols = self.get_bool_by_locations(route)
            if self.enough_in_a_row(symbols, threshold=THRESHOLD):
                return True
        return False

    def get_bool_by_locations(self, locations: tuple[tuple[int]]) -> list[bool]:
        """Returns 'True' in place of the location in a list if it equals the current
        player's symbol. If it's anything else, it will be listed as 'False'."""
        report = [
            self.table[loc[0], loc[1]] == self.current_player.symbol
            for loc in locations
        ]
        return report

    def get_bool_by_symbol(self, l: list):
        """Parses list of symbols. It returns a boolean in the place of the given list of whether
        the symbol is equal to the current player's or not."""
        return [v == self.current_player.symbol for v in l]

    def get_diagnol_routes(self) -> list[list[tuple]]:
        routes = []
        starting_row = 0

        for starting_col in range(len(self.table)):  # format (row, col)
            se_diagnol_route = [  # generated diagnol routes going \
                (starting_row + ind, starting_col + ind)
                for ind in range(len(self.table[0]) - starting_col)
            ]

            sw_diagnol_route = [  # all routes going /
                (starting_row + ind, starting_col - ind)
                for ind in range(starting_col + 1)
            ]

            routes.append(sw_diagnol_route)
            routes.append(se_diagnol_route)
        return routes
