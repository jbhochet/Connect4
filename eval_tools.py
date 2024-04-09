from board import Board
from functools import lru_cache

# ---------------
# Utility
# ---------------


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


def board_actions(board: Board):
    for column in range(board.NB_COLUMNS):
        if not board.is_column_full(column):
            yield column


def count_win_move(board: Board, symbol: str) -> int:
    """
    Returns the number of winning moves on the board for the symbol.
    """
    res = 0
    for column in board_actions(board):
        board.put_symbol(symbol, column)
        if board.is_winner(symbol):
            res += 1
        board.undo()
    return res


# ---------------
# Eval 1
# ---------------


def eval_1(board: Board, symbol: str, depth: int):
    me = symbol
    opponent = Board.RED if me == Board.YELLOW else Board.YELLOW

    if board.is_winner(me):
        return (depth + 1) * 1000
    elif board.is_winner(opponent):
        return -(depth + 1) * 1000
    else:
        return 0


# ---------------
# Eval 2
# ---------------


def eval_2(board: Board, symbol: str, depth: int):
    me = symbol
    opponent = Board.RED if me == Board.YELLOW else Board.YELLOW

    result = eval_1(board, symbol, depth)
    if result != 0:
        return result

    return count_win_move(board, symbol) - count_win_move(board, opponent)


# ---------------
# Eval 3
# ---------------


def eval_3(board: Board, symbol: str, depth: int) -> int:
    me = symbol
    opponent = Board.RED if me == Board.YELLOW else Board.YELLOW
    score = 0

    # Evaluate the board based on the current player's symbol
    for row in range(board.NB_ROWS):
        for col in range(board.NB_COLUMNS):
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
    score += evaluate_direction(board, row, col, player, opponent, -1, 0)  # Up

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
    num_opponent_tokens = 0

    # Count consecutive player tokens, opponent tokens, and empty spaces in the specified direction
    for i in range(1, 4):
        r = row + i * d_row
        c = col + i * d_col
        if board.is_valid_position(r, c):
            cell_value = board.get_cell_value(r, c)
            if cell_value == player:
                num_player_tokens += 1
            elif cell_value == opponent:
                num_opponent_tokens += 1
                break  # Stop counting if opponent's token encountered
            else:
                num_empty_spaces += 1

    # Evaluate based on the count of player tokens, opponent tokens, and empty spaces
    if num_player_tokens == 3 and num_empty_spaces == 0:
        score += 100  # Four in a row
    elif num_player_tokens == 2 and num_empty_spaces == 1:
        score += 20  # Three in a row with one empty space
    elif num_player_tokens == 1 and num_empty_spaces == 2:
        score += 10  # Two in a row with two empty spaces

    if num_opponent_tokens == 3 and num_empty_spaces == 0:
        score -= 100  # Opponent has four in a row
    elif num_opponent_tokens == 2 and num_empty_spaces == 1:
        score -= 20  # Opponent has three in a row with one empty space
    elif num_opponent_tokens == 1 and num_empty_spaces == 2:
        score -= 10  # Opponent has two in a row with two empty spaces

    return score
