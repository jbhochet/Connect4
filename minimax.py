from board import Board
from typing import Any
from math import inf
from random import choice
from eval_tools import terminal_test, board_actions


def minimax(board: Board, symbol: str, depth: int, eval_fx) -> int:
    """
    Run the minimax algorithm on this board using the specified symbol and
    return the column number that provides the best move for that symbol.
    """
    actions = dict()
    for column in board_actions(board):
        board.put_symbol(symbol, column)
        actions[column] = min_value(board, symbol, depth, eval_fx)
        board.undo()
    max_val = max(actions.values())
    return choice([action[0] for action in actions.items() if action[1] == max_val])


def min_value(board: Board, symbol: str, depth: int, eval_fx) -> float:
    """
    Reduce the value of this symbol and return the action with the lower value.
    The returned value is in this format: (column_number, play_value).
    """
    if terminal_test(board, depth):
        return eval_fx(board, symbol, depth)
    opponent = Board.RED if symbol is Board.YELLOW else Board.YELLOW
    v = inf
    for column in board_actions(board):
        board.put_symbol(opponent, column)
        v = min(v, max_value(board, symbol, depth - 1, eval_fx))
        board.undo()
    return v


def max_value(board: Board, symbol: str, depth: int, eval_fx) -> float:
    """
    Maximise the symbol's gain by returning the action with the highest gain.
    The return value should be in the format of (column number, play value).
    """
    if terminal_test(board, depth):
        return eval_fx(board, symbol, depth)
    v = -inf
    for column in board_actions(board):
        board.put_symbol(symbol, column)
        v = max(v, min_value(board, symbol, depth - 1, eval_fx))
        board.undo()
    return v
