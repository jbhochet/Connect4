from player import Player

class Game:
    def __init__(self, player_r: Player, player_y: Player) -> None:
        self.board = None
        self.player_r = None
        self.player_y = None
        self.next_player = None
    
    def is_ended(self) -> bool:
        """
        Return True if the game is ended, otherwise return False.
        """

    def player_turn(self) -> None:
        """
        Starts the player's turn. The turn of the next_player.
        """

    def is_winner(self, symbol: str) -> bool:
        """
        Return True if this symbol is the winner, otherwise False.
        """

    def display(self) -> None:
        """
        Print the board in the console.
        """