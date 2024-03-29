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


def eval_position(board: Board, symbol: str, row: int, col: int):
    score = 0
    temp_score = 0

    me = symbol
    opponent = Board.RED if me == Board.YELLOW else Board.YELLOW

    results = []

    # Check horizontal
    if col + 3 < board.NB_COLUMNS:
        for i in range(1, 4):
            cell_val = board.get_cell_value(row, col + i)
            if cell_val == me:
                temp_score += 1
            elif cell_val == opponent:
                temp_score = 0
                break

    results.append(temp_score)

    # Check horizontal
    if row + 3 < board.NB_ROWS:
        for i in range(1, 4):
            cell_val = board.get_cell_value(row + i, col)
            if cell_val == me:
                temp_score += 1
            elif cell_val == opponent:
                temp_score = 0
                break

    results.append(temp_score)

    # Check vertical positive
    if row + 3 < board.NB_ROWS and col + 3 < board.NB_COLUMNS:
        for i in range(1, 4):
            cell_val = board.get_cell_value(row + i, col + i)
            if cell_val == me:
                temp_score += 1
            elif cell_val == opponent:
                temp_score = 0
                break

    results.append(temp_score)

    # Check vertical negative
    if row + 3 < board.NB_ROWS and col - 3 >= 0:
        for i in range(1, 4):
            cell_val = board.get_cell_value(row + i, col - i)
            if cell_val == me:
                temp_score += 1
            elif cell_val == opponent:
                temp_score = 0
                break

    results.append(temp_score)

    for result in results:
        if result == 1:
            score += 5
        elif result == 2:
            score += 10
        elif result == 3:
            score += 100

    return score


# ---------------
# Easy
# ---------------


def eval_easy(board: Board, symbol: str, depth: int):
    me = symbol
    opponent = Board.RED if me == Board.YELLOW else Board.YELLOW

    if board.is_winner(me):
        return (depth + 1) * 1000
    elif board.is_winner(opponent):
        return -(depth + 1) * 1000
    else:
        return 0


# ---------------
# Medium
# ---------------


def eval_medium(board: Board, symbol: str, depth: int):
    me = symbol
    opponent = Board.RED if me == Board.YELLOW else Board.YELLOW

    result = eval_easy(board, symbol, depth)
    if result != 0:
        return result

    return count_win_move(board, symbol) - count_win_move(board, opponent)


# ---------------
# Hard
# ---------------

def eval_hard(board: Board, symbol: str, depth: int) -> int:
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


def evaluate_position(
    board: Board, row: int, col: int, player: str, opponent: str
) -> int:
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


def evaluate_direction(
    board: Board, row: int, col: int, player: str, opponent: str, d_row: int, d_col: int
) -> int:
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
