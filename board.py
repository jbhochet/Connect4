from copy import deepcopy
from typing import Optional


class Board:
    RED = "R"
    YELLOW = "Y"
    EMPTY = " "

    NB_COLUMNS = 7
    NB_ROWS = 6

    def __init__(self) -> None:
        # The board
        self.board = [
            [self.EMPTY for _ in range(self.NB_COLUMNS)] for _ in range(self.NB_ROWS)
        ]
        # The move history
        self.history = []
        # The list of the free position in each column
        self.column_top_positions = [self.NB_ROWS - 1 for _ in range(self.NB_COLUMNS)]
        # Store the winner
        self.__winner = None

    def __str__(self) -> str:
        """
        Returns a string representation of the board.
        """
        result = ""
        for row in self.board:
            result += "| " + " | ".join(row) + " |\n"
        result += "|---" * self.NB_COLUMNS + "|\n"
        result += "| " + " | ".join(str(i) for i in range(self.NB_COLUMNS))
        return result

    def copy(self):
        """
        Creates and returns a deep copy of the board.
        """
        return deepcopy(self)

    def __compute_winner(self):
        last_column = self.history[-1]
        last_row = self.column_top_positions[last_column] + 1
        symbol = self.board[last_row][last_column]

        # Check horizontal
        for i in range(4):
            bmin = last_column - i
            bmax = bmin + 3
            if bmin < 0 or bmax >= self.NB_COLUMNS:
                continue
            if all(self.board[last_row][c] == symbol for c in range(bmin, bmax + 1)):
                self.__winner = symbol
                return

        # Check vertically
        for i in range(4):
            bmin = last_row - i
            bmax = bmin + 3
            if bmin < 0 or bmax >= self.NB_ROWS:
                continue
            if all(self.board[r][last_column] == symbol for r in range(bmin, bmax + 1)):
                self.__winner = symbol
                return

        # Check diagonal
        for i in range(4):
            brmin = last_row - i
            brmax = brmin + 3
            bcmin = last_column - i
            bcmax = bcmin + 3

            if brmin < 0 or brmax >= self.NB_ROWS:
                continue
            if bcmin < 0 or bcmax >= self.NB_COLUMNS:
                continue

            if all(self.board[brmin + j][bcmin + j] == symbol for j in range(4)):
                self.__winner = symbol
                return

        # Check diagonal (neg)
        for i in range(4):
            brmin = last_row - i
            brmax = brmin + 3
            bcmax = last_column + i
            bcmin = bcmax - 3

            if brmin < 0 or brmax >= self.NB_ROWS:
                continue
            if bcmin < 0 or bcmax >= self.NB_COLUMNS:
                continue

            if all(self.board[brmin + j][bcmax - j] == symbol for j in range(4)):
                self.__winner = symbol
                return

    def put_symbol(self, symbol: str, column: int):
        """
        Puts the symbol on the top of the column.
        Returns True if it's possible, False if the column is full.
        """
        assert not self.is_column_full(column), "The column is full!"
        # Get the free position on this column
        top_pos = self.column_top_positions[column]
        # Put the symbol and update history and free space for the column
        self.board[top_pos][column] = symbol
        self.history.append(column)
        self.column_top_positions[column] -= 1
        # Compute the actual winner
        self.__compute_winner()
    
    def get_last_move(self) -> Optional[int]:
        """Returns the last played move."""
        if len(self.history) > 0:
            return self.history[-1]
        else:
            return None

    def undo(self):
        """
        Undo the last move.
        """
        assert len(self.history) > 0, "Empty history!"
        # Get the last played column
        last_column = self.history.pop()
        # Decrements the last free space in the last played column
        self.column_top_positions[last_column] += 1
        # Put the empty symbol
        top_pos = self.column_top_positions[last_column]
        self.board[top_pos][last_column] = Board.EMPTY
        # Reset winner
        self.__winner = None

    def get_cell_value(self, row: int, column: int) -> str:
        """
        Returns the value of the cell at the given row and column.
        """
        return self.board[row][column]
    
    def get_top_position(self, column: int) -> int:
        """Returns the top position (where put the next move) of the column."""
        return self.column_top_positions[column]

    def is_valid_position(self, row: int, column: int) -> bool:
        """
        Checks if the given position (row, col) is valid on the board.
        Returns True if the position is valid, False otherwise.
        """
        return 0 <= row < self.NB_ROWS and 0 <= column < self.NB_COLUMNS

    def is_column_full(self, column: int) -> bool:
        """
        Returns True if the column is full, False otherwise.
        """
        assert 0 <= column < self.NB_COLUMNS
        return self.column_top_positions[column] < 0

    def is_winner(self, symbol: str) -> bool:
        return self.__winner == symbol

    def is_full(self) -> bool:
        """
        Returns True if the board is full, False otherwise.
        """
        return len(self.history) == (self.NB_COLUMNS * self.NB_ROWS)
