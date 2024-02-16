from board import Board
from random import choice

class Player:
    def play(self, symbol: str, board: Board) -> int:
        """
        Return the column number to play the player move.
        """


class HumanPlayer(Player):
    def play(self, symbol: str, board: Board) -> int:
        colx = -1
        while colx < 0:
            try:
                colx = int(
                    input(f"Player {symbol}, which column do you want to play in? ")
                )
            except:
                colx = -1
        return colx


class RandomPlayer(Player):
    def play(self, symbol: str, board: Board) -> int:
        pos = []
        
        for column in range(board.columns):
            if not board.is_column_full(column):
                pos.append(column)

        return choice(pos)
