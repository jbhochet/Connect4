# Run all stats in one command!
# Take a coffe ;)

from multiprocessing import Pool
import subprocess
import os
import time

# Configuration -----------------------
EVALS = range(1, 4 + 1)
BOARD_ACTIONS = range(1, 5 + 1)
ALGOS = ("AB", "MM")
DEPTHS = (2, 4, 6)
NB_GAMES = 10
OUT_DIR = "stats/"

# Others constants
EVAL_PREFIX = "eval_"
BOARD_ACTIONS_PREFIX = "board_actions_"
PYTHON_BIN = "python3"
STATS_PY = "main_stats.py"

# Utilities ---------------------------


def player_config_to_str(config):
    """Returns in that format: eval_4:board_actions_4:2"""
    eval, board_action, algo, depth = config
    res = f"{EVAL_PREFIX}{eval}:{BOARD_ACTIONS_PREFIX}{board_action}:{depth}"
    if algo == "MM":
        res += ":m"
    return res


def settings_player_generator():
    for eval in EVALS:
        for board_action in BOARD_ACTIONS:
            for algo in ALGOS:
                for depth in DEPTHS:
                    config = (eval, board_action, algo, depth)
                    yield player_config_to_str(config)


def settings_players_generator():
    for player1 in settings_player_generator():
        for player2 in settings_player_generator():
            yield player1, player2


def run_stats(players):
    player1, player2 = players
    output_file = OUT_DIR + player1 + "_" + player2
    before = time.time()
    p = subprocess.run(
        [PYTHON_BIN, STATS_PY, "--ai-level", player1, player2, "--nb-games", str(NB_GAMES), "--output", output_file]
    )
    diff = time.time() -before
    p.check_returncode()
    with open(output_file + ".txt", mode="w", encoding="utf-8") as f:
        f.write(str(time.time()-before))


# Script ------------------------------

# eval, depth, eval, depth
games = [
    (1, 6, 1, 3),
    (1, 3, 1, 6), # fix
    (1, 7, 1, 4),
    (1, 4, 1, 7),

    (2, 5, 2, 2),
    (2, 2, 2, 5),
    (2, 6, 2, 3),
    (2, 3, 3, 6), # fix

    (3, 6, 3, 3),
    (3, 3, 3, 6),
    (3, 7, 3, 4),
    (3, 4, 3, 7), # fix

    (4, 5, 4, 2),
    (4, 2, 4, 5),
    (4, 6, 4, 3),
    (4, 3, 4, 6),

    # Evals

    (2, 5, 1, 5),
    (1, 5, 2, 5),

    (3, 5, 1, 5),
    (1, 5, 3, 5),

    (4, 5, 1, 5),
    (1, 5, 4, 5),

    (3, 5, 2, 5),
    (2, 5, 3, 5),

    (4, 5, 2, 5),
    (2, 5, 4, 5),

    (3, 5, 4, 5),
    (4, 5, 3, 5),
]

def to_config(games):
    # eval, board_action, algo, depth
    add_more = lambda _eval, depth: (_eval, 2, "AB", depth)
    for game in games:
        player1 = add_more(game[0], game[1])
        player2 = add_more(game[2], game[3])
        player1_str = player_config_to_str(player1)
        player2_str = player_config_to_str(player2)
        yield player1_str, player2_str

os.makedirs(OUT_DIR, exist_ok=True)

pool = Pool()

print("Start...")

for game in to_config(games):
    print(game)

pool.map(run_stats, to_config(games))

print("End!")
