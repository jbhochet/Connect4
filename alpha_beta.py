from typing import Tuple
from math import inf
from board import Board
from eval_tools import terminal_test, board_actions, get_opponent


def alphabeta(board: Board, symbol: str, depth: int, eval_fx) -> int:
    """Returns the best column to play the next move."""
    u, best_action = max_value(board, symbol, depth, -inf, +inf, eval_fx)
    return best_action


def max_value(
    board: Board, symbol: str, depth: int, alpha: int, beta: int, eval_fx
) -> Tuple[float, int]:
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
        v_bis, _ = min_value(board, symbol, depth - 1, alpha, beta, eval_fx)
        # undo the action
        board.undo()
        # update best move if the utility is better
        if v_bis > v:
            v = v_bis
            best_action = action
        # alpha beta cut off
        if v > beta:
            break
        alpha = max(alpha, v)
    # return the best action
    return v, best_action


def min_value(
    board: Board, symbol: str, depth: int, alpha: int, beta: int, eval_fx
) -> Tuple[float, int]:
    # "symbol" here is still the maximizing player.
    # If this config is terminal, we need to evaluate it for this player,
    # *but* knowing that if there is a next move then it is the opponent's move.
    # We can approximate this without adding a second parameter to eval
    # by evaluating the config from the opponent's point of view
    # and then taking the negative value of that (assuming eval symmetric).

    opponent = get_opponent(symbol)

    # check the terminal test
    if terminal_test(board, depth):
        return -eval_fx(board, opponent, depth), 0
    # init
    v = +inf
    best_action = None
    for action in board_actions(board):
        # play the action
        board.put_symbol(opponent, action)
        # compute the utility score of this action
        v_bis, _ = max_value(board, symbol, depth - 1, alpha, beta, eval_fx)
        # undo the action
        board.undo()
        # update best move if the utility is better
        if v_bis < v:
            v = v_bis
            best_action = action
        # alpha beta cut off
        if v < alpha:
            break
        beta = min(beta, v)
    # return the best action
    return v, best_action
