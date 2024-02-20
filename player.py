from typing import Optional, Tuple
from board import Board
from random import choice
from minimax import minimax


class Player:
    def play(self, symbol: str, board: Board) -> int:
        """
        Return the column number to play the player move.
        """


class HumanPlayer(Player):
    def play(self, symbol: str, board: Board) -> int:
        col_x = -1
        while col_x < 0:
            try:
                col_x = int(
                    input(f"Player {symbol}, which column do you want to play in? ")
                )
            except ValueError:
                col_x = -1
        return col_x


class RandomPlayer(Player):
    def play(self, symbol: str, board: Board) -> int:
        pos = []

        for column in range(board.columns):
            if not board.is_column_full(column):
                pos.append(column)

        return choice(pos)

class MMAIPlayer(Player):
    def play(self, symbol: str, board: Board) -> int:
        colx = minimax(board, symbol, 1)
        return colx


class EasyAI(Player):
    def __init__(self, lookahead=1) -> None:
        self.lookahead = lookahead

    def play(self, symbol, board) -> int:
        _, col = self.alphabeta(board, self.lookahead, float('-inf'), float('inf'), True, symbol)
        return col

    def alphabeta(self, board, depth, alpha, beta, maximizing_player, symbol) -> Tuple[float, Optional[int]]:
        if depth == 0 or board.is_winner(Board.RED) or board.is_winner(Board.YELLOW) or board.is_full():
            return self.evaluate(board), None

        if maximizing_player:
            max_eval = float('-inf')
            best_col = None
            for col in range(board.columns):
                if not board.is_column_full(col):
                    board_copy = board.copy()
                    board_copy.put_symbol(symbol, col)
                    evaluation, _ = self.alphabeta(board_copy, depth - 1, alpha, beta, False, symbol)
                    if evaluation > max_eval:
                        max_eval = evaluation
                        best_col = col
                    alpha = max(alpha, evaluation)
                    if beta <= alpha:
                        break
            return max_eval, best_col
        else:
            min_eval = float('inf')
            best_col = None
            for col in range(board.columns):
                if not board.is_column_full(col):
                    board_copy = board.copy()
                    board_copy.put_symbol('R' if symbol == 'Y' else 'Y', col)
                    evaluation, _ = self.alphabeta(board_copy, depth - 1, alpha, beta, True, symbol)
                    if evaluation < min_eval:
                        min_eval = evaluation
                        best_col = col
                    beta = min(beta, evaluation)
                    if beta <= alpha:
                        break
            return min_eval, best_col

    def evaluate(self, board):
        # For Easy AI, return a fixed value
        # since it doesn't perform sophisticated evaluation
        return 0
