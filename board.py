from copy import deepcopy


class Board:
    RED = 'R'
    YELLOW = 'Y'
    EMPTY = ' '

    def __init__(self, rows: int = 6, columns: int = 7) -> None:
        self.rows = rows
        self.columns = columns
        self.board = [[self.EMPTY for _ in range(columns)] for _ in range(rows)]
        self.history = []

    def __str__(self) -> str:
        """
        Returns a string representation of the board.
        """
        result = ''
        for row in self.board:
            result += '| ' + ' | '.join(row) + ' |\n'
        result += '|---' * self.columns + '|\n'
        result += '| ' + ' | '.join(str(i) for i in range(self.columns)) + ' |\n'
        return result

    def copy(self):
        """
        Creates and returns a deep copy of the board.
        """
        return deepcopy(self)

    def put_symbol(self, symbol: str, column: int):
        """
        Puts the symbol on the top of the column.
        Returns True if it's possible, False if the column is full.
        """
        assert not self.is_column_full(column), "The column is full!"
        added = False
        i = self.rows - 1
        while i >= 0 and not added:
            if self.board[i][column] == self.EMPTY:
                self.board[i][column] = symbol
                self.history.append(column)
                added = True
            i -= 1
        assert added, "Symbol not added!"
    
    def undo(self):
        assert (len(self.history) > 0), "Empty history!"
        last = self.history.pop()
        i = 0
        reverted = False
        while i < self.rows and not reverted:
            if self.board[i][last] != Board.EMPTY:
                self.board[i][last] = Board.EMPTY
                reverted = True
            i += 1
        assert reverted, "Can't undo last move!"

    def get_cell_value(self, row: int, column: int) -> str:
        """
        Returns the value of the cell at the given row and column.
        """
        return self.board[row][column]

    def is_valid_position(self, row: int, column: int) -> bool:
        """
        Checks if the given position (row, col) is valid on the board.
        Returns True if the position is valid, False otherwise.
        """
        return 0 <= row < self.rows and 0 <= column < self.columns

    def is_column_full(self, column: int) -> bool:
        """
        Returns True if the column is full, False otherwise.
        """
        if not 0 <= column < self.columns:
            return True
        return self.board[0][column] != self.EMPTY

    def is_winner(self, symbol: str) -> bool:
        """
        Returns True if the symbol is the winner, False otherwise.
        """
        # Check horizontally
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if all(self.board[row][col + i] == symbol for i in range(4)):
                    return True

        # Check vertically
        for row in range(self.rows - 3):
            for col in range(self.columns):
                if all(self.board[row + i][col] == symbol for i in range(4)):
                    return True

        # Check diagonally (positive slope)
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if all(self.board[row + i][col + i] == symbol for i in range(4)):
                    return True

        # Check diagonally (negative slope)
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if all(self.board[row - i][col + i] == symbol for i in range(4)):
                    return True

        return False

    def is_full(self) -> bool:
        """
        Returns True if the board is full, False otherwise.
        """
        return all(self.board[0][col] != self.EMPTY for col in range(self.columns))
