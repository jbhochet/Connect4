from player import *
from game import Game
from board import Board

player_r = RandomPlayer()
player_y = EasyAI()

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
