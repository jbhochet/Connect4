from player import *
from game import Game
from board import Board
from typing import Tuple
from player import EasyPlayer, MediumPlayer, HardPlayer


###############
# Functions
###############


def input_int(message: str):
    res = None
    while res is None:
        try:
            res = int(input(message))
        except:
            print("Your answer is not valid !")
    return res


def build_ia_player() -> Player:
    while True:
        print("Please select AI's level : ")
        print("1) Easy")
        print("2) Medium")
        print("3) Hard")

        n = input_int("Please select AI's difficulty : ")

        if n == 1:
            return EasyPlayer()
        elif n == 2:
            return MediumPlayer()
        elif n == 3:
            return HardPlayer()
        else:
            print("This level is not valid !")


def create_players() -> Tuple[Player, Player]:
    while True:
        print("Please select the playing mode : ")
        print("1) Human vs Human")
        print("2) Human vs AI")
        print("3) AI vs AI")

        n = input_int("Please input the game mode number : ")

        if n == 1:
            return HumanPlayer(), HumanPlayer()
        elif n == 2:
            return HumanPlayer(), build_ia_player()
        elif n == 3:
            return build_ia_player(), build_ia_player()
        else:
            print("This mode is not valid !")


def choose_player_color(player1: Player, player2: Player) -> Tuple[Player, Player]:
    while True:
        print("Select the player's colour : ")
        print(f"=> {player1} is red")
        print(f"=> {player2} is yellow")
        n = input_int("Would you like to invert colours ? [0 : No | 1 : Yes] : ")
        if n == 0:
            return player1, player2
        elif n == 1:
            return player2, player1
        else:
            print("Your answer is not valid !")


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
