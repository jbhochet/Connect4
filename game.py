from player import Player
from board import Board


class Game:
    def __init__(self, player_r: Player, player_y: Player) -> None:
        self.board = Board()
        self.player_r = player_r
        self.player_y = player_y
        # TODO: define the first player to play
        self.next_player = player_r

    def __get_symbol_from_player(self, player: Player) -> str:
        if player == self.player_r:
            return Board.RED
        else:
            return Board.YELLOW

    def has_ended(self) -> bool:
        """
        Return True if the game has ended, otherwise return False.
        """
        return any(
            [
                self.board.is_full(),
                self.is_winner(Board.RED),
                self.is_winner(Board.YELLOW),
            ]
        )

    def player_turn(self) -> None:
        """
        Starts the player's turn. The turn of the next_player.
        """
        player = self.next_player
        symbol = self.__get_symbol_from_player(player)
        column = self.next_player.play(symbol, self.board)
        symbol = self.__get_symbol_from_player(player)

        if self.board.put_symbol(symbol, column):
            if player == self.player_y:
                self.next_player = self.player_r
            else:
                self.next_player = self.player_y

    def is_winner(self, symbol: str) -> bool:
        """
        Return True if this symbol is the winner, otherwise False.
        """
        return self.board.is_winner(symbol)

    def display(self) -> None:
        """
        Print the board in the console.
        """
        print(str(self.board))
