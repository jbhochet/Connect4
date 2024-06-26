from player import *
from game import Game
from board import Board

nb_game = 100
score_r = 0
score_y = 0

player_r = HardPlayer()
player_y = HardPlayer()

for i in range(nb_game):
    game = Game(player_r, player_y)

    while not game.has_ended():
        game.display()
        game.player_turn()

    game.display()

    winner = None
    if game.is_winner(Board.RED):
        winner = Board.RED
        score_r += 1
    elif game.is_winner(Board.YELLOW):
        winner = Board.YELLOW
        score_y += 1

    if winner is not None:
        print(f"Player {winner} has won !")
    else:
        print("Draw !")

###############
# Final results
###############

print()
print("===== Results =====")
print(f"Number of games : {nb_game}")
print(f"Victories of RED : {score_r} ({score_r * 100 / nb_game}%)")
print(f"Victories of YELLOW : {score_y} ({score_y * 100 / nb_game}%)")
