import random
from typing import Any
from math import inf
from board import Board
from minimax import terminal_test


def board_actions(board: Board):
    middle = board.columns // 2

    if board.columns % 2 != 0 and not board.is_column_full(middle):
        yield middle

    for i in range(middle):
        i += 1
        column = [middle - i, middle + i]
        if random.randint(0, 1) == 1:
            column.reverse()
        for column in column:
            if not board.is_column_full(column):
                yield column


def max_value(board: Board, symbol: str, depth: int, alpha: float, beta: float) \
        -> tuple[int, None] | tuple[float, int | None]:
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


def min_value(board: Board, symbol: str, depth: int, alpha: float, beta: float) \
        -> tuple[int, None] | tuple[float | Any, int | None]:
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
    score += evaluate_direction(board, row, col, player, opponent, 0, 1)  # Right
    score += evaluate_direction(board, row, col, player, opponent, 0, -1)  # Left

    # Check vertical
    score += evaluate_direction(board, row, col, player, opponent, 1, 0)  # Down

    # Check positive slope diagonal (/)
    score += evaluate_direction(board, row, col, player, opponent, 1, 1)  # Down-right
    score += evaluate_direction(board, row, col, player, opponent, -1, -1)  # Up-left

    # Check negative slope diagonal (\)
    score += evaluate_direction(board, row, col, player, opponent, 1, -1)  # Down-left
    score += evaluate_direction(board, row, col, player, opponent, -1, 1)  # Up-right

    return score


def evaluate_direction(board: Board, row: int, col: int, player: str, opponent: str, d_row: int, d_col: int) -> int:
    """
    Evaluate a specific direction (horizontal, vertical, diagonal) for the given player.
    """
    score = 0
    num_player_tokens = 0
    num_empty_spaces = 0

    # Count consecutive player tokens and empty spaces in the specified direction
    for i in range(1, 4):
        r = row + i * d_row
        c = col + i * d_col
        if board.is_valid_position(r, c):
            cell_value = board.get_cell_value(r, c)
            if cell_value == player:
                num_player_tokens += 1
            elif cell_value == opponent:
                break  # Stop counting if opponent's token encountered
            else:
                num_empty_spaces += 1

    # Evaluate based on the count of player tokens and empty spaces
    if num_player_tokens == 3 and num_empty_spaces == 0:
        score += 100  # Four in a row
    elif num_player_tokens == 2 and num_empty_spaces == 1:
        score += 5  # Three in a row with one empty space
    elif num_player_tokens == 1 and num_empty_spaces == 2:
        score += 2  # Two in a row with two empty spaces

    return score
