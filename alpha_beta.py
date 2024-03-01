import random
from typing import Tuple, List
from math import inf
from board import Board
from minimax import terminal_test


def board_actions(board: Board):
    middle = board.columns // 2

    if board.columns % 2 != 0 and not board.is_column_full(middle):
        yield middle

    for i in range(middle):
        i += 1
        colums = [middle - i, middle + i]
        if random.randint(0, 1) == 1:
            colums.reverse()
        for column in colums:
            if not board.is_column_full(column):
                yield column


def max_value(board: Board, symbol: str, depth: int, alpha: float, beta: float) -> Tuple[float, int]:
    if terminal_test(board, depth):
        return evaluate(board, symbol), None

    best_column = None
    v = -inf
    for column in board_actions(board):
        board.put_symbol(symbol, column)
        utility, _ = min_value(board, symbol, depth - 1, alpha, beta)
        board.undo()
        if v < utility:
            v = utility
            best_column = column

        if v >= beta:
            return v, best_column

        alpha = max(alpha, v)

    return v, best_column


def min_value(board: Board, symbol: str, depth: int, alpha: float, beta: float) -> Tuple[float, int]:
    if terminal_test(board, depth):
        return evaluate(board, symbol), None

    opponent = Board.RED if symbol is Board.YELLOW else Board.YELLOW
    best_column = None
    v = inf
    for column in board_actions(board):
        board.put_symbol(opponent, column)
        utility, _ = max_value(board, symbol, depth - 1, alpha, beta)
        board.undo()
        if v > utility:
            v = utility
            best_column = column

        if v <= alpha:
            return v, best_column

        beta = min(beta, v)

    return v, best_column


def alphabeta(board: Board, symbol: str, depth: int) -> int:
    _, best_column = max_value(board, symbol, depth, -inf, inf)
    return best_column


def evaluate(board: Board, symbol: str) -> int:
    me = symbol
    opponent = Board.RED if me == Board.YELLOW else Board.YELLOW
    score = 0

    # Evaluate the board based on the current player's symbol
    for row in range(board.rows):
        for col in range(board.columns):
            if board.get_cell_value(row, col) == me:
                score += evaluate_position(board, row, col, me, opponent)
            elif board.get_cell_value(row, col) == opponent:
                score -= evaluate_position(board, row, col, opponent, me)

    return score


def evaluate_position(board: Board, row: int, col: int, player: str, opponent: str) -> int:
    """
    Evaluate the position on the board for the given player.
    """
    score = 0

    # Check horizontal
    for c in range(board.columns - 3):
        window = [board.get_cell_value(row, c + i) for i in range(4)]
        score += evaluate_window(window, player, opponent)

    # Check vertical
    for r in range(board.rows - 3):
        window = [board.get_cell_value(r + i, col) for i in range(4)]
        score += evaluate_window(window, player, opponent)

    # Check positive slope diagonal (/)
    for r in range(board.rows - 3):
        for c in range(board.columns - 3):
            window = [board.get_cell_value(r + i, c + i) for i in range(4)]
            score += evaluate_window(window, player, opponent)

    # Check negative slope diagonal (\)
    for r in range(3, board.rows):
        for c in range(board.columns - 3):
            window = [board.get_cell_value(r - i, c + i) for i in range(4)]
            score += evaluate_window(window, player, opponent)

    return score


def evaluate_window(window: List[str], player: str, opponent: str) -> int:
    """
    Evaluate a window of four cells.
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
