from board import Board
from player_ai import Participant


class Game:
    """Create object of the Game class."""

    def __init__(self, board: Board):
        """
        Initialize the Game class with a board object.
        :param board: An instance of the Board class.
        """
        self.board = board

    def play(self, params):
        """
        Start playing the game.
        :param params: A list of parameters to set up the players (or AI).
        """
        participant = Participant()
        participant.set_player_or_ai(*params)
        self.board.display_board()
        while True:
            self.make_move(participant.participant_1)
            if self.game_over():
                break
            self.make_move(participant.participant_2)
            if self.game_over():
                break

    def game_over(self) -> bool:
        """
        Check if the game is over.
        :return: True if the game is over (either a win or a draw), False otherwise.
        """
        if self.check_win():
            print(f'{self.board.winning_symbol} wins')
            return True
        elif self.board.is_full():
            print('Draw')
            return True
        else:
            return False

    def make_move(self, participant):
        """
        Make a move for the given participant.
        :param participant: An instance representing a player or AI participant.
        """
        participant.place_piece_in_board(self.board)
        self.board.display_board()

    def check_win(self) -> bool:
        """
        Check if there is a winning condition on the board.
        :return: True if there is a win, False otherwise.
        """
        return any([self.board.check_three_in_row(), self.board.check_three_in_column(),
                    self.board.check_three_in_diagonal()])
