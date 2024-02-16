from player import HumanPlayer, RandomPlayer
from game import Game
from board import Board

player_r = RandomPlayer()
player_y = RandomPlayer()

game = Game(player_r, player_y)

while not game.is_ended():
    game.display()
    game.player_turn()

game.display()

winner = None
if game.is_winner(Board.RED):
    winner = Board.RED
elif game.is_winner(Board.YELLOW):
    winner = Board.YELLOW

if winner is not None:
    print(f"Player {winner} have win!")
else:
    print("Game is a draw!")
