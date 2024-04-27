from board import Board
from random import shuffle, randint

# ---------------
# Utility
# ---------------

# Board Actions -----------------------


def board_actions_1(board: Board):
    """Returns a generator of column from the left to right."""
    for action in range(board.NB_COLUMNS):
        if not board.is_column_full(action):
            yield action


def board_actions_2(board: Board):
    """Returns a generator of column from center to out."""
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


def board_actions_3(board: Board):
    """Returns the columns in a random order."""
    columns = [i for i in range(board.NB_COLUMNS) if not board.is_column_full(i)]
    shuffle(columns)
    return columns


def board_actions_4(board: Board):
    """Returns the column based on the last move."""
    # get the last action of use the middle column
    middle = board.get_last_move()
    if middle is None:
        middle = board.NB_COLUMNS // 2
    # from the middle to out
    if not board.is_column_full(middle):
        yield middle
    for i in range(1, board.NB_COLUMNS):
        columns = (middle - i, middle + i)
        for column in columns:
            if 0 <= column < board.NB_COLUMNS:
                if not board.is_column_full(column):
                    yield column


def board_actions_5(board: Board):
    """Returns the column based on the last move with a little random."""
    # get the last action of use the middle column
    middle = board.get_last_move()
    if middle is None:
        middle = board.NB_COLUMNS // 2
    # from the middle to out
    if not board.is_column_full(middle):
        yield middle
    for i in range(1, board.NB_COLUMNS):
        columns = [middle - i, middle + i]
        if randint(0, 1) == 1:
            columns.reverse()
        for column in columns:
            if 0 <= column < board.NB_COLUMNS:
                if not board.is_column_full(column):
                    yield column


# End Board Actions -------------------


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


def get_opponent(symbol: str) -> str:
    """Returns the opponent of this symbol."""
    return Board.RED if symbol is Board.YELLOW else Board.YELLOW


def count_win_move(board: Board, symbol: str) -> int:
    """
    Returns the number of winning moves on the board for the symbol.
    """
    res = 0
    for column in board_actions_1(board):
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
    score += evaluate_direction(board, row, col, player, opponent, -1, 0)  # Up

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


# ---------------
# Eval 4
# ---------------


def eval_4(board: Board, symbol: str, depth: int) -> float | int:
    score = 0
    nb_config = 0
    # define symbol
    me = symbol
    opponent = Board.RED if me == Board.YELLOW else Board.YELLOW
    # For each board cell
    for row in range(board.NB_ROWS):
        for col in range(board.NB_COLUMNS):
            # Start count
            directions = (
                (0, 1),  # horizontal (left to right)
                (1, 1),  # diagonal (top left to bottom right)
                (1, 0),  # vertical (top to bottom)
                (1, -1),  # diagonal (top right to bottom left)
            )
            for d_row, d_col in directions:
                my_symbol_count = 0
                opponent_symbol_count = 0
                empty_symbol_count = 0
                config_distance = 0
                is_ok = True
                # count the symbols
                for i in range(4):
                    r = row + i * d_row
                    c = col + i * d_col
                    if not board.is_valid_position(r, c):
                        is_ok = False  # this is a bad config!
                        break
                    # check the symbol in this cell
                    cell_value = board.get_cell_value(r, c)
                    if cell_value == me:
                        my_symbol_count += 1
                    elif cell_value == opponent:
                        opponent_symbol_count += 1
                    else:
                        # the cell is empty! get the distance!
                        empty_symbol_count += 1
                        config_distance += board.get_top_position(c) - r
                # skip if the config is bad
                if not is_ok:
                    continue
                # some checks
                assert config_distance >= 0
                assert (
                               my_symbol_count + opponent_symbol_count + empty_symbol_count
                ) == 4
                # compute my score
                f_score = lambda x, n: (x / (n or 1))
                tmp_score = 0
                tmp_nb_config = 0
                # this is a win move!
                if my_symbol_count == 4:
                    tmp_score += f_score(10000, config_distance)
                    tmp_nb_config += 1
                elif my_symbol_count == 3 and empty_symbol_count == 1:
                    tmp_score += f_score(1000, config_distance)
                    tmp_nb_config += 1
                elif my_symbol_count == 2 and empty_symbol_count == 2:
                    tmp_score += f_score(100, config_distance)
                    tmp_nb_config += 1

                if opponent_symbol_count == 4:
                    tmp_score += f_score(10000, config_distance)
                    tmp_nb_config += 1
                elif opponent_symbol_count == 3 and empty_symbol_count == 1:
                    tmp_score -= f_score(1000, config_distance)
                    tmp_nb_config += 1
                elif opponent_symbol_count == 2 and empty_symbol_count == 2:
                    tmp_score -= f_score(100, config_distance)
                    tmp_nb_config += 1
                # add the score
                if tmp_nb_config != 0:
                    score += tmp_score
                    nb_config += tmp_nb_config
    # the score is ready to use :)
    if nb_config > 0:
        return score / nb_config
    else:
        return 0
