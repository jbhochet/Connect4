from player import *
from game import Game
from board import Board
from typing import Tuple, Type
from player import MMAIPlayer, AlphaBetaPlayer


###############
# Functions
###############

def input_int(message: str):
    res = None
    while res is None:
        try:
            res = int(input(message))
        except:
            pass
    return res


def get_ia_player_algo() -> Type[MMAIPlayer | AlphaBetaPlayer]:
    while True:
        print("Which algorithm would you like to use?")
        print("1) Minimax")
        print("2) Alpha Beta")

        n = input_int("Please input the algorithm number: ")

        if n == 1:
            return MMAIPlayer
        elif n == 2:
            return AlphaBetaPlayer


def build_ia_player() -> Player:
    print("Build a new AI player.")
    ia_player_algo = get_ia_player_algo()
    depth = input_int("Please enter the algorithm's depth: ")
    return ia_player_algo(depth)


def create_players() -> Tuple[Player, Player]:
    while True:
        print("Which mode do you want to play?")
        print("1) Human vs Human")
        print("2) Human vs AI")
        print("3) AI vs AI")

        n = input_int("Please input the game mode number: ")
    
        if n == 1:
            return HumanPlayer(), HumanPlayer()
        elif n == 2:
            return HumanPlayer(), build_ia_player()
        elif n == 3:
            return build_ia_player(), build_ia_player()
        else:
            print("This mode is invalid!")


def choose_player_color(player1: Player, player2: Player) -> Tuple[Player, Player]:
    while True:
        print("Select the player's colour.")
        print(f"=> {player1} is red")
        print(f"=> {player2} is yellow")
        n = input_int("Would you like to invert the colours? [0: no | 1: yes]: ")
        if n == 0:
            return player1, player2
        elif n == 1:
            return player2, player1
        else:
            print("Your answer is not valid!")


def start_game(player_r: Player, player_y: Player):
    game = Game(player_r, player_y)
    while not game.has_ended():
        game.display()
        game.player_turn()

    game.display()

    winner = None
    if game.is_winner(Board.RED):
        winner = Board.RED
    elif game.is_winner(Board.YELLOW):
        winner = Board.YELLOW

    if winner is not None:
        print(f"Player {winner} has won !")
    else:
        print("Draw !")


###############
# Main Script
###############

print(">> Connect 4 <<")

player1, player2 = create_players()

player_r, player_y = choose_player_color(player1, player2)

start_game(player_r, player_y)
