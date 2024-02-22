import random
from typing import Optional, Tuple, List
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
        column = minimax(board, symbol, 1)
        return column


class EasyAI(Player):
    def __init__(self, lookahead: int = 1) -> None:
        self.lookahead = lookahead

    def play(self, symbol: str, board: Board) -> int:
        _, col = self.alphabeta(board, self.lookahead, float('-inf'), float('inf'), True, symbol)
        return col

    def alphabeta(self, board: Board, depth: int, alpha: float, beta: float, maximizing_player: bool, symbol: str)\
            -> Tuple[float, Optional[int]]:
        if depth == 0 or board.is_winner(Board.RED) or board.is_winner(Board.YELLOW) or board.is_full():
            return self.evaluate(board, symbol), None

        if maximizing_player:
            max_eval = float('-inf')
            best_col = None
            for col in self.get_ordered_columns(board):
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
            for col in self.get_ordered_columns(board):
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

    def evaluate(self, board: Board, symbol: str) -> int:
        me = symbol
        opponent = Board.RED if me == Board.YELLOW else Board.YELLOW
        score = 0

        # Evaluate the board based on the current player's symbol
        for row in range(board.rows):
            for col in range(board.columns):
                if board.get_cell_value(row, col) == me:
                    score += self.evaluate_position(board, row, col, me, opponent)
                elif board.get_cell_value(row, col) == opponent:
                    score -= self.evaluate_position(board, row, col, opponent, me)

        return score

    def evaluate_position(self, board: Board, row: int, col: int, player: str, opponent: str) -> int:
        """
        Evaluate the position on the board for the given player.
        """
        score = 0

        # Check horizontal
        for c in range(board.columns - 3):
            window = [board.get_cell_value(row, c + i) for i in range(4)]
            score += self.evaluate_window(window, player, opponent)

        # Check vertical
        for r in range(board.rows - 3):
            window = [board.get_cell_value(r + i, col) for i in range(4)]
            score += self.evaluate_window(window, player, opponent)

        # Check positive slope diagonal (/)
        for r in range(board.rows - 3):
            for c in range(board.columns - 3):
                window = [board.get_cell_value(r + i, c + i) for i in range(4)]
                score += self.evaluate_window(window, player, opponent)

        # Check negative slope diagonal (\)
        for r in range(3, board.rows):
            for c in range(board.columns - 3):
                window = [board.get_cell_value(r - i, c + i) for i in range(4)]
                score += self.evaluate_window(window, player, opponent)

        return score

    @staticmethod
    def evaluate_window(window: List[str], player: str, opponent: str) -> int:
        """
        Evaluate a window of 4 cells.
        """
        score = 0
        count_player = window.count(player)
        count_opponent = window.count(opponent)
        count_empty = window.count(Board.EMPTY)

        if count_player == 4:
            score += 100
        elif count_player == 3 and count_empty == 1:
            score += 5
        elif count_player == 2 and count_empty == 2:
            score += 2

        if count_opponent == 3 and count_empty == 1:
            score -= 4

        return score

    @staticmethod
    def get_ordered_columns(board: Board):
        """
        Return a list of columns ordered by preference (from center to sides).
        """
        center_col = board.columns // 2
        columns = list(range(board.columns))
        random.shuffle(columns)  # Shuffle to add randomness
        columns.sort(key=lambda x: abs(x - center_col))  # Sort by distance from center
        return columns
