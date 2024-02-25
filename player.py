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
    def play(self, symbol: str, board: Board) -> int:
        pos = []

        for column in range(board.columns):
            if not board.is_column_full(column):
                pos.append(column)

        return choice(pos)


class MMAIPlayer(Player):
    def play(self, symbol: str, board: Board) -> int:
        column = minimax(board, symbol, 1)
        return column


class AlphaBetaPlayer(Player):
    def __init__(self, lookahead: int = 1) -> None:
        self.lookahead = lookahead

    def play(self, symbol: str, board: Board) -> int:
        _, col = alphabeta(board, self.lookahead, float('-inf'), float('inf'), True, symbol)
        return col
