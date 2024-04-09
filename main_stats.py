import argparse
from typing import Tuple
import matplotlib.pyplot as plt
from player import EvalPlayer, EasyPlayer, MediumPlayer, HardPlayer
import eval_tools
from game import Game
from board import Board


# Utilities ----------------------------------------------------------------------

def plot_stats(ax, title: str, r_nb_win: int, y_nb_win: int, nb_games: int):
    draw_count = nb_games - (r_nb_win + y_nb_win)
    y = [r_nb_win, y_nb_win]
    colors = [ "red", "yellow" ]
    if draw_count > 0:
        y.append(draw_count)
        colors.append("grey")
    ax.pie(y, colors=colors)
    ax.set_title(title)

def stats_games(player_r, player_y, nb_games: int) -> Tuple[int, int]:
    r_win = 0
    y_win = 0

    for i in range(nb_games):
        print(f"Stats on game {i+1}/{nb_games}...")
        game = Game(player_r, player_y)
        # game loop
        while not game.has_ended():
            game.player_turn()
        # check win and update scores
        if game.is_winner(Board.RED):
            r_win += 1
        elif game.is_winner(Board.YELLOW):
            y_win += 1
    
    return r_win, y_win

def get_player(name: str):
    if ':' in name: # we want to test an eval
        temp = name.split(":")
        name, depth = temp[0], int(temp[1])
        eval_func = getattr(eval_tools, name)
        player = EvalPlayer(eval_func, depth)
        return player
    else: # we want to test a preset
        player_map = { 
            "easy": EasyPlayer,
            "medium": MediumPlayer,
            "hard": HardPlayer
        }
        return player_map[name]()

# Define parser ----------------------------------------------------------------

parser = argparse.ArgumentParser(
    prog="Connect 4 Stats",
    description="Compute stats about algorithms",
)

# Select on with levels compute stats
parser.add_argument(
    "--ai-level",
    #choices=("easy", "medium", "hard"),
    nargs=2,
    help="The AI to compute stats.",
)

# The number of game to play
parser.add_argument(
    "--nb-games", type=int, default=10, help="The number of game to play for each round."
)


# Process Argument -------------------------------------------------------------

args = parser.parse_args()

nb_games = args.nb_games
ai_level = args.ai_level


# Compute Stats ----------------------------------------------------------------

# define all instances of players
player_map = {
    "easy": EasyPlayer(),
    "medium": MediumPlayer(),
    "hard": HardPlayer()
}

if ai_level is None:
    # Stats all ai
    fig, axs = plt.subplots(3,2)
    x,y = 0, 0
    for level_r, player_r in player_map.items():
        for level_y, player_y in player_map.items():
            if level_r == level_y:
                continue
            print(f"Stats with {player_r} (red) and {player_y} (yellow)...")
            r_win_count, y_win_count = stats_games(player_r, player_y, nb_games)
            plot_stats(axs[x,y], f"{level_r} (red) vs {level_y} (yellow)", r_win_count, y_win_count, nb_games)
            y += 1
        x += 1
        y = 0
    fig.suptitle("AI Stats for Connect 4")
    plt.savefig("stats.png")
else:
    # Stats just on specified
    players = tuple(map(lambda e: get_player(e), ai_level))
    player_r = players[0]
    player_y = players[1]
    r_win_count, y_win_count = stats_games(player_r, player_y, nb_games)
    fig, ax = plt.subplots()
    plot_stats(ax, f"{ai_level[0]} (red) vs {ai_level[1]} (yellow)", r_win_count, y_win_count, nb_games)
    fig.suptitle("AI Stats for Connect 4")
    plt.savefig("stats.png")