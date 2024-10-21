import random

from board import Board
from enums import Mode


class Participant:
    """Represents a participant in the game which can be either a player or an AI."""

    def __init__(self):
        """
        Initializes the Participant class with default or specific values.
        """
        self.participant_1 = None
        self.participant_2 = None

    @staticmethod
    def configure_participant(piece: str, parameter: str):
        """
        Static method to configure participant with specific piece and parameter.
        :param piece: String contains 'X' for first or 'O' for second participant.
        :param parameter: String contains commands from the command prompt.
        :return: Participant instance.
        """
        if parameter == 'user':
            return Player(piece)
        elif parameter in {'easy', 'medium', 'hard'}:
            return Ai(piece, Mode(parameter))
        return None

    def set_player_or_ai(self, _, *params) -> None:
        """
        Sets whether a participant is a player or an AI based on the given parameters.
        :param _: Parameter 'start' or 'exit' ignored.
        :param params: List of strings containing commands from the command prompt.
        """
        self.participant_1 = self.configure_participant('X', params[0])
        self.participant_2 = self.configure_participant('O', params[1])

    def place_piece_in_board(self, board: Board) -> None:
        """Places a piece onto the game board."""
        pass


class Player(Participant):
    """Inherits Participant and represents a human player."""

    def __init__(self, piece: str):
        """
        Initializes the Player class with a piece.
        :param piece: The piece ('X' or 'O') associated with the player.
        """
        super().__init__()
        self.piece = piece

    def place_piece_in_board(self, board: Board) -> None:
        """
        Overridden method to handle placing the player's piece on the board.
        :param board: Instance from the class Board.
        """
        while True:
            coordinates = self.get_player_coordinates()
            if not self.coordinates_valid(coordinates):
                continue
            row, col = int(coordinates[0]) - 1, int(coordinates[1]) - 1
            if board.is_cell_occupied(row, col):
                print('This cell is occupied! Choose another one!')
                continue
            board.set_cell(row, col, self.piece)
            break

    @staticmethod
    def get_player_coordinates() -> list[str]:
        """
        Static method to get valid coordinates from the player.
        :return: List of commands from the command prompt.
        """
        return input('Enter the coordinates: ').strip().split()

    @staticmethod
    def coordinates_valid(coordinates: list[str]) -> bool:
        """
        Static method to validate the player provided coordinates.
        :param coordinates: List of commands from the command prompt.
        :return: Boolean if coordinates are valid.
        """
        for coord in coordinates:
            if not coord.isdigit():
                print('You should enter numbers!')
                return False
            elif int(coord) < 1 or int(coord) > 3:
                print('Coordinates should be from 1 to 3!')
                return False
        return True


class Ai(Participant):
    """Inherits Participant and represents an AI player."""

    def __init__(self, piece: str, mode: Mode):
        """
        Initializes the Ai class with a given piece and difficulty mode.
        :param piece: The piece ('X' or 'O') associated with the Ai.
        :param mode: The difficulty mode (e.g., EASY, MEDIUM, HARD) of the AI.
        """
        super().__init__()
        self.piece = piece
        self.mode = mode

    def place_piece_in_board(self, board: Board) -> None:
        """
        Overridden method to handle placing the AI's piece on the board based on its algorithm.
        :param board: Instance from the class Board.
        """
        print(f'Making move level "{self.mode.value}"')
        cell_coordinates = None
        if self.mode == Mode.EASY:
            cell_coordinates = self.make_easy_move(board)
        elif self.mode == Mode.MEDIUM:
            cell_coordinates = self.make_medium_move(board)
        elif self.mode == Mode.HARD:
            cell_coordinates = self.make_hard_move(board)
        board.set_cell(cell_coordinates[0], cell_coordinates[1], self.piece)

    @staticmethod
    def make_easy_move(board: Board) -> tuple[int, int]:
        """
        Determines a move for the AI in the EASY mode.
        :param board: Instance from the class Board.
        :return: Tuple with the chosen position on board to place the Ai's piece.
        """
        return random.choice(board.get_empty_cells())

    def make_medium_move(self, board: Board) -> tuple[int, int]:
        """
        Determines a move for the AI in the MEDIUM mode.
        :param board: Instance from the class Board.
        :return: Tuple with the chosen position on board to place the Ai's piece.
        """
        opponent_piece = 'X' if self.piece == 'O' else 'O'
        ai_win_options = set(board.find_two_in_line(self.piece))
        ai_def_options = set(board.find_two_in_line(opponent_piece))
        if ai_win_options:
            return random.choice(list(ai_win_options))
        elif ai_def_options:
            return random.choice(list(ai_def_options))
        return self.make_easy_move(board)

    def make_hard_move(self, board: Board) -> tuple[int, int]:
        """
        Determines a move for the AI in the HARD mode with the minimax algorithm.
        :param board: Instance from the class Board.
        :return: Tuple with the chosen position on board to place the Ai's piece.
        """

        def minimax(current_board: Board, depth: int, is_maximizing: bool) -> int:
            """
            Minimax algorithm for Tic-Tac-Toe with the given Board instance.
            :param current_board: Instance from the class Board.
            :param depth: Integer of the calculation's depth.
            :param is_maximizing: Boolean of maximizing Ai's score.
            :return: Integer of the score.
            """
            scores = {self.piece: 1, 'X' if self.piece == 'O' else 'O': -1, 'draw': 0}

            current_piece = self.piece if is_maximizing else ('X' if self.piece == 'O' else 'O')

            # Base case for minimax algorithm if player or ai wins
            if (current_board.check_three_in_row() or
                    current_board.check_three_in_column() or
                    current_board.check_three_in_diagonal()):
                if current_board.winning_symbol:
                    return scores[current_board.winning_symbol]

            # Base case for minimax algorithm if it is a draw
            if current_board.is_full():
                return scores['draw']

            if is_maximizing:
                best_score = float('-inf')
                for cell in current_board.get_empty_cells():
                    current_board.set_cell(cell[0], cell[1], self.piece)
                    score = minimax(current_board, depth + 1, False)
                    current_board.set_cell(cell[0], cell[1], Board.EMPTY_CELL)
                    best_score = max(score, best_score)
                return best_score
            else:
                best_score = float('inf')
                opponent_piece = 'X' if self.piece == 'O' else 'O'
                for cell in current_board.get_empty_cells():
                    current_board.set_cell(cell[0], cell[1], opponent_piece)
                    score = minimax(current_board, depth + 1, True)
                    current_board.set_cell(cell[0], cell[1], Board.EMPTY_CELL)
                    best_score = min(score, best_score)
                return best_score

        best_score = float('-inf')
        best_move = None
        for cell in board.get_empty_cells():
            board.set_cell(cell[0], cell[1], self.piece)
            score = minimax(board, 0, False)
            board.set_cell(cell[0], cell[1], Board.EMPTY_CELL)
            if score > best_score:
                best_score = score
                best_move = cell

        return best_move
