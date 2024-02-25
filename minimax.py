from board import Board
from typing import Any
from math import inf
from random import choice


def board_actions(board: Board):
    for column in range(board.columns):
        if not board.is_column_full(column):
            yield column


def minimax(board: Board, symbol: str, depth: int) -> int:
    """
    Run the minimax algorithm on this board using the specified symbol and
    return the column number that provides the best move for that symbol.
    """
    actions = dict()
    for column in board_actions(board):
        board_cpy = board.copy()
        board_cpy.put_symbol(symbol, column)
        actions[column] = min_value(board_cpy, symbol, depth)
    max_val = max(actions.values())
    return choice([action[0] for action in actions.items() if action[1] == max_val])


def terminal_test(board: Board, depth: int) -> bool:
    if depth == 0:
        return True
    if board.is_winner(Board.RED):
        return True
    if board.is_winner(Board.YELLOW):
        return True
    if board.is_full():
        return True
    return False


def min_value(board: Board, symbol: str, depth: int) -> float:
    """
    Reduce the value of this symbol and return the action with the lower value.
    The returned value is in this format: (column_number, play_value).
    """
    if terminal_test(board, depth):
        return eval_board(board, symbol, depth)
    opponent = Board.RED if symbol is Board.YELLOW else Board.YELLOW
    v = inf
    for column in board_actions(board):
        board_cpy = board.copy()
        board_cpy.put_symbol(opponent, column)
        v = min(v, max_value(board_cpy, symbol, depth - 1))
    return v


def max_value(board: Board, symbol: str, depth: int) -> int | float | Any:
    """
    Maximise the symbol's gain by returning the action with the highest gain.
    The return value should be in the format of (column number, play value).
    """
    if terminal_test(board, depth):
        return eval_board(board, symbol, depth)
    v = -inf
    for column in board_actions(board):
        board_cpy = board.copy()
        board_cpy.put_symbol(symbol, column)
        v = max(v, min_value(board_cpy, symbol, depth - 1))
    return v


def count_win_move(board: Board, symbol: str) -> int:
    """
    Returns the number of winning moves on the board for the symbol.
    """
    res = 0
    for column in range(board.columns):
        board_cpy = board.copy()
        board_cpy.put_symbol(symbol, column)
        if board_cpy.is_winner(symbol):
            res += 1
    return res


def eval_board(board: Board, symbol: str, depth) -> int:
    """
    Return the value of the current board for the symbol.
    The value returned will be
    -1000 if this symbol wins,
    -1000 if the opponent wins,
    and 1 if nothing special happens.
    This will be improved later.
    """
    me = symbol
    opponent = Board.RED if me == Board.YELLOW else Board.YELLOW

    if board.is_winner(me):
        return (depth + 1) * 1000
    elif board.is_winner(opponent):
        return -(depth + 1) * 1000
    elif board.is_full():
        return 0
    else:
        # Check the player's winning moves on the board
        return count_win_move(board, symbol) - count_win_move(board, opponent)
