import random
from typing import Any
from math import inf
from board import Board
from eval_tools import terminal_test


def board_actions(board: Board):
    middle = board.NB_COLUMNS // 2

    if board.NB_COLUMNS % 2 != 0 and not board.is_column_full(middle):
        yield middle

    for i in range(middle):
        i += 1
        column = [middle - i, middle + i]
        if random.randint(0, 1) == 1:
            column.reverse()
        for column in column:
            if not board.is_column_full(column):
                yield column


def max_value(
    board: Board, symbol: str, depth: int, alpha: float, beta: float, eval_func
) -> tuple[int, None] | tuple[float, int | None]:
    if terminal_test(board, depth):
        return eval_func(board, symbol, depth), None

    best_column = None
    v = -inf
    for column in board_actions(board):
        board.put_symbol(symbol, column)
        utility, _ = min_value(board, symbol, depth - 1, alpha, beta, eval_func)
        board.undo()
        if v < utility:
            v = utility
            best_column = column

        if v >= beta:
            return v, best_column

        alpha = max(alpha, v)

    return v, best_column


def min_value(
    board: Board, symbol: str, depth: int, alpha: float, beta: float, eval_func
) -> tuple[int, None] | tuple[float | Any, int | None]:
    opponent = Board.RED if symbol is Board.YELLOW else Board.YELLOW
    if terminal_test(board, depth):
        return -eval_func(board, opponent, depth), None
    
    best_column = None
    v = inf
    for column in board_actions(board):
        board.put_symbol(opponent, column)
        utility, _ = max_value(board, symbol, depth - 1, alpha, beta, eval_func)
        board.undo()
        if v > utility:
            v = utility
            best_column = column

        if v <= alpha:
            return v, best_column

        beta = min(beta, v)

    return v, best_column


def alphabeta(board: Board, symbol: str, depth: int, eval_func) -> int:
    _, best_column = max_value(board, symbol, depth, -inf, inf, eval_func)
    return best_column
