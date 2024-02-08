class Board:
    RED = 'R'
    YELLOW = 'Y'
    EMPTY = ' '

    def __init__(self) -> None:
        self.board = None
    
    def __str__(self) -> str:
        pass

    def put_symbol(self, symbol: str, column: int) -> bool:
        """
        Put the symbol on the top of the column.
        Return True if it's possible, False if the column is full.
        """

    def is_column_full(self, column: int) -> bool:
        """
        Return True if the column is full, False otherwise.
        """

    def is_winner(self, symbol: str) -> bool:
        """
        Return True is the symbol is the winner, False otherwise.
        """

    def is_full(self) -> bool:
        """
        Return True is the board is full, False otherwise.
        """
