import numpy as np, array
from statistics import median

THRESHOLD = 3


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
            turn_inp = input("Please enter your turn here: ")
            loc: tuple = self.parse_turn(turn_inp)
            if not self.spot_taken(loc):  # checking if the selected spot is taken
                self.log_move(loc)  # record the move
                turn_made = True
            else:
                print("Spot already taken.")
        self.mark_area(row=loc[0], col=loc[1])

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

    def has_won(self) -> bool:
        return self.is_diagnol()

    def is_horizontal(self) -> bool:
        for row in self.table:
            row_report = [value == self.current_player.symbol for value in row]
            print(row_report)
            print(self.enough_in_a_row(row_report, threshold=THRESHOLD), "Aaa")
            if self.enough_in_a_row(row_report, threshold=THRESHOLD):
                return True
        return False

    def is_vertical(self) -> bool:

        for i in range(len(self.table)):
            column = [
                self.table[j, i] for j in range(len(self.table))
            ]  # retrieves vertical column
            print(column)
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
            if self.enough_in_a_row(
                symbols, threshold=THRESHOLD
            ):
                return True
        return False

    def get_bool_by_locations(self, locations: tuple[tuple[int]]) -> list[bool]:
        """Returns 'True' in place of the location in a list if it equals the current
        player's symbol. If it's anything else, it will be listed as 'False'."""
        report = [self.table[loc[0], loc[1]] == self.current_player.symbol for loc in locations]
        return report
    
    def get_bool_by_symbol(self, l: list):
        """Parses list of symbols. It returns a boolean in the place of the given list of whether
        the symbol is equal to the current player's or not."""
        return [v == self.current_player.symbol for v in l]

    def get_diagnol_routes(self) -> list[list[tuple]]:
        routes = []
        starting_row = 0


        for starting_col in range(len(self.table)):  # format (row, col)
            se_diagnol_route = [ # generated diagnol routes going south east
                (starting_row + ind, starting_col + ind)
                for ind in range(len(self.table[0]) - starting_col)
            ]

            sw_diagnol_route = [
                (starting_row + ind, starting_col - ind)
                for ind in range(starting_col + 1)
            ]

            routes.append(sw_diagnol_route)
            routes.append(se_diagnol_route)
        return routes
