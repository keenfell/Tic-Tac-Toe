import numpy as np, array
from statistics import median


class Player:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol


class TableDisplay:
    def __init__(self, padding=2):
        self.table = self.create_table()
        self.padding = padding

    @staticmethod
    def create_table():
        table = np.array([["X", "X", "X"], ["X", "X", "X"], ["X", "X", "X"]])
        return table

    def display_table(self) -> str:
        """Display the table for front-end tic-tac-toe display."""
        fmtd = []

        for ind, row in enumerate(self.table):
            new_row = self.row_display(row)
            fmtd.append(new_row)
            if not ind == len(self.table) - 1:  # if not the last row
                fmtd.append(self.get_row_border(length=17))
        return self.combine_rows(fmtd)

    @staticmethod
    def get_row_border(length: int) -> str:
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

        turn_inp = input("Please enter your turn here: ")
        c, r = self.parse_turn(turn_inp)
        self.mark_area(column=c, row=r)

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

    def mark_area(self, row: int, column: int) -> None:
        self.table[row, column] = self.current_player.symbol

    def has_won(self) -> bool:
        return self.is_horizontal() or self.is_vertical()

    def is_horizontal(self) -> bool:
        for row in self.table:
            if all(value == self.current_player.symbol for value in row):
                return True

    def is_vertical(self) -> bool:
        for i in range(len(self.table)):
            column = [self.table[j, i] for j in range(0, len(self.table))]
            if all(value == self.current_player.symbol for value in column):
                return True

    def is_diagnol(self) -> bool: ...
