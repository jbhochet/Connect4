from board import Board
from random import choice
from minimax import minimax
from alpha_beta import alphabeta
import eval_tools


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

        for column in range(board.NB_COLUMNS):
            if not board.is_column_full(column):
                pos.append(column)

        return choice(pos)
    
class EvalPlayer(Player):
    def __init__(self, eval_func, depth: int) -> None:
        self.eval_func = eval_func
        self.depth = depth

    def play(self, symbol: str, board: Board) -> int:
        return alphabeta(board, symbol, self.depth, self.eval_func)

class EasyPlayer(Player):
    def __str__(self) -> str:
        return "Easy Player"

    def play(self, symbol: str, board: Board) -> int:
        return alphabeta(board, symbol, 1, eval_tools.eval_easy)


class MediumPlayer(Player):
    def __str__(self) -> str:
        return "Medium Player"

    def play(self, symbol: str, board: Board) -> int:
        return alphabeta(board, symbol, 5, eval_tools.eval_medium)


class HardPlayer(Player):
    def __str__(self) -> str:
        return "Hard Player"

    def play(self, symbol: str, board: Board) -> int:
        return alphabeta(board, symbol, 5, eval_tools.eval_hard)


# Unused --------------------

class MMAIPlayer(Player):
    def __init__(self, depth=1) -> None:
        self.depth = depth

    def __str__(self) -> str:
        return f"MiniMax Player (depth: {self.depth})"

    def play(self, symbol: str, board: Board) -> int:
        column = minimax(board, symbol, self.depth)
        return column
