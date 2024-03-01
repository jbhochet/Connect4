from board import Board
from random import choice
from minimax import minimax
from alpha_beta import alphabeta


class Player:
    def play(self, symbol: str, board: Board) -> int:
        """
        Return the column number to play the player move.
        """


class HumanPlayer(Player):
    def __str__(self) -> str:
        return "Human Player"
    
    def play(self, symbol: str, board: Board) -> int:
        column = -1
        while column < 0:
            try:
                column = int(
                    input(f"Player {symbol}, which column do you want to play in? ")
                )
            except ValueError:
                column = -1
        return column


class RandomPlayer(Player):
    def __str__(self) -> str:
        return "Random Player"
    
    def play(self, symbol: str, board: Board) -> int:
        pos = []

        for column in range(board.columns):
            if not board.is_column_full(column):
                pos.append(column)

        return choice(pos)


class MMAIPlayer(Player):
    def __init__(self, depth = 1) -> None:
        self.depth = depth
    
    def __str__(self) -> str:
        return f"MiniMax Player (depth: {self.depth})"

    def play(self, symbol: str, board: Board) -> int:
        column = minimax(board, symbol, self.depth)
        return column


class AlphaBetaPlayer(Player):
    def __init__(self, depth: int = 1) -> None:
        self.depth = depth
    
    def __str__(self) -> str:
        return f"Alpha Beta Player (depth: {self.depth})"

    def play(self, symbol: str, board: Board) -> int:
        col = alphabeta(board, symbol, self.depth)
        return col
