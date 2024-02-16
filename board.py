class Board:
    RED = 'R'
    YELLOW = 'Y'
    EMPTY = ' '

    def __init__(self, rows=6, columns=7) -> None:
        self.rows = rows
        self.columns = columns
        self.board = [[self.EMPTY for _ in range(columns)] for _ in range(rows)]

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

    def put_symbol(self, symbol, column) -> bool:
        """
        Puts the symbol on the top of the column.
        Returns True if it's possible, False if the column is full.
        """
        if self.is_column_full(column):
            return False
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][column] == self.EMPTY:
                self.board[row][column] = symbol
                return True

    def is_column_full(self, column) -> bool:
        """
        Returns True if the column is full, False otherwise.
        """
        if not 0 <= column < self.columns:
            return True
        return self.board[0][column] != self.EMPTY

    def is_winner(self, symbol) -> bool:
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
