import pandas as pd
from math import pow
from random import shuffle
from player import EvalPlayer
import eval_tools
from game import Game
from board import Board
from threading import RLock
from time import time


# Configuration

EVALS = (1, 2,)
BOARD_ACTIONS = (2,)
ALGOS = ("AB", "MM")
DEPTHS = (2, 3, 4,)
NB_GAMES = 50
OUT_CSV = "stats2.csv"

# Global variable

TOTAL = int(pow(len(EVALS) * len(BOARD_ACTIONS) * len(ALGOS) * len(DEPTHS), 2))

colum_name_list = ("Al", "Ev", "Ba", "De", "Tm") * 2 + ("win", "draw")

df = pd.DataFrame(columns=colum_name_list)

lock = RLock()

# Utility -----------------------------------------------------------


def mean(iterable):
    return sum(iterable) / len(iterable)


def get_eval_fx(eval_n):
    return getattr(eval_tools, f"eval_{eval_n}")


def get_actions_fx(board_actions):
    return getattr(eval_tools, f"board_actions_{board_actions}")


def get_player(algo, eval_n, board_actions, depth):
    use_minimax = algo == "MM"
    eval_fx = get_eval_fx(eval_n)
    actions_fx = get_actions_fx(board_actions)
    return EvalPlayer("Test", eval_fx, actions_fx, depth, use_minimax)


def player_config_gen():
    for eval_n in EVALS:
        for board_actions in BOARD_ACTIONS:
            for algo in ALGOS:
                for depth in DEPTHS:
                    yield algo, eval_n, board_actions, depth


def players_configs_gen():
    for player_r in player_config_gen():
        for player_y in player_config_gen():
            yield player_r, player_y


def stats_games(player_r, player_y):
    r_win = 0
    draw = 0
    times_r = []
    times_y = []

    for i in range(NB_GAMES):
        game = Game(player_r, player_y)
        # game loop
        j = 0
        while not game.has_ended():
            before = time()
            # play
            game.player_turn()
            # save the time
            diff = time() - before
            if j % 2 == 0:
                times_r.append(diff)
            else:
                times_y.append(diff)
            j += 1
        # check win and update scores
        if game.is_winner(Board.RED):
            r_win += 1
        elif not game.is_winner(Board.YELLOW):
            draw += 1

    return r_win / NB_GAMES, draw / NB_GAMES, mean(times_r), mean(times_y)


def stats_maker(args):
    player_r, player_y = args
    r_win, draw, time_r, times_y = stats_games(
        get_player(*player_r), get_player(*player_y)
    )
    with lock:
        df.loc[len(df)] = player_r + (time_r,) + player_y + (times_y,) + (r_win, draw)
        return f"{len(df)}/{TOTAL} | {player_r} VS {player_y}"


# Script ------------------------------------------------------------

args = list(players_configs_gen())
shuffle(args)

print("START")
for config in players_configs_gen():
    print(stats_maker(config))
print("FINISH") 

df.to_csv(OUT_CSV)
