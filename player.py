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
                    input(f"Player {symbol}, which column do you want to play in ? ")
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
    def __init__(self, name: str, eval_func, depth: int, use_minimax = False) -> None:
        self.__name = name
        self.__eval_func = eval_func
        self.__depth = depth
        self.__use_minimax = use_minimax

    def __str__(self) -> str:
        algo = "AB" if not self.__use_minimax else "MM"
        return f"{self.__name} (depth: {self.__depth} | {algo})"

    def play(self, symbol: str, board: Board) -> int:
        if self.__use_minimax:
            algo = minimax
        else:
            algo = alphabeta
        return algo(board, symbol, self.__depth, self.__eval_func)


class EasyPlayer(EvalPlayer):
    def __init__(self) -> None:
        super().__init__("Easy", eval_tools.eval_1, 4)


class MediumPlayer(EvalPlayer):
    def __init__(self) -> None:
        super().__init__("Medium", eval_tools.eval_2, 4)


class HardPlayer(EvalPlayer):
    def __init__(self) -> None:
        super().__init__("Hard", eval_tools.eval_3, 6)


# Unused --------------------

class MMAIPlayer(Player):
    def __init__(self, depth=1) -> None:
        self.depth = depth

    def __str__(self) -> str:
        return f"MiniMax Player (depth: {self.depth})"

    def play(self, symbol: str, board: Board) -> int:
        column = minimax(board, symbol, self.depth)
        return column
