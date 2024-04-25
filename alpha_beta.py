import random
from typing import Any, Tuple
from math import inf
from board import Board
from eval_tools import terminal_test


def board_actions(board: Board):
    """Return a generator of column from center to out."""
    actions = []
    middle = board.NB_COLUMNS // 2

    if board.NB_COLUMNS % 2 != 0 and not board.is_column_full(middle):
        actions.append(middle)

    for i in range(middle):
        i += 1
        column = [middle - i, middle + i]
        for column in column:
            if not board.is_column_full(column):
                actions.append(column)
    
    return actions


def get_opponent(symbol: str) -> str:
    """Returns the opponent of this symbol."""
    return Board.RED if symbol is Board.YELLOW else Board.YELLOW

# board: Board, symbol: str, depth: int

def alphabeta(board: Board, symbol: str, depth: int, eval_fx) -> int:
    """Returns the best column to play the next move."""
    u, best_action = max_value(board, symbol, depth, -inf, +inf, eval_fx)
    print("{} : v = {} | action = {}".format(symbol, u, best_action))
    return best_action

def max_value(board: Board, symbol: str, depth: int, alpha: int, beta: int, eval_fx) -> Tuple[float, int]:
    # check the terminal test
    if terminal_test(board, depth):
        return eval_fx(board, symbol, depth), 0
    # init
    v = -inf
    best_action = None
    for action in board_actions(board):
        # play the action
        board.put_symbol(symbol, action)
        # compute the utility score of this action
        v_bis, _ = min_value(board, symbol, depth-1, alpha, beta, eval_fx)
        # undo the action
        board.undo()
        # update best move if the utility is better
        if v_bis > v:
            v = v_bis
            best_action = action
        # alpha beta cut off
        if v >= beta:
            return v, best_action
        alpha = max(alpha, v)
    # return the best action
    return v, best_action

def min_value(board: Board, symbol: str, depth: int, alpha: int, beta: int, eval_fx) -> Tuple[float, int]:
    # check the terminal test
    if terminal_test(board, depth):
        return eval_fx(board, symbol, depth), 0
    # init
    v = +inf
    best_action = None
    for action in board_actions(board):
        # play the action
        board.put_symbol(symbol, action)
        # compute the utility score of this action
        v_bis, _ = max_value(board, symbol, depth-1, alpha, beta, eval_fx)
        # undo the action
        board.undo()
        # update best move if the utility is better
        if v_bis < v:
            v = v_bis
            best_action = action
        # alpha beta cut off
        if v <= alpha:
            return v, best_action
        beta = min(beta, v)
    # return the best action
    return v, best_action
