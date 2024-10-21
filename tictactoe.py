from board import Board
from enums import Status
from game import Game

START_OPTIONS = {'easy', 'medium', 'hard', 'user'}
START_COMMAND = 'start'
EXIT_COMMAND = 'exit'


def is_valid_command(params: list[str]) -> bool:
    """
    :param params: A list of strings representing command parameters. The list should either
                   contain a single element that matches the EXIT_COMMAND or three elements
                   where the first is START_COMMAND, and the other two elements are in START_OPTIONS.
    :return: True if the command parameters are valid according to the rules specified, otherwise False.
    """
    return ((len(params) == 1 and params[0] == EXIT_COMMAND) or
            (len(params) == 3 and params[0] == START_COMMAND and params[1] in START_OPTIONS and
             params[2] in START_OPTIONS))


def get_validated_user_input() -> list[str]:
    """
    Gathers user input from the command line, validates the input, and either returns the valid input as a list of
    strings or prompts the user to input again if the input is invalid.

    :return: A list of strings representing the validated user input
    """
    params = input('Input command: ').strip().split()
    if is_valid_command(params):
        return params
    else:
        print('Bad parameters!')
        return get_validated_user_input()


def start_new_game(user_input) -> None:
    """
    :param user_input: The initial setup or moves to start the game with.
    :return: None
    """
    board = Board()
    game = Game(board)
    game.play(user_input)


def main():
    """
    Manages the main game loop including user input handling and game status transitions.

    :return: None
    """
    game_status = Status.START

    while game_status == Status.START:
        user_input = get_validated_user_input()
        command = user_input[0]

        if command == EXIT_COMMAND:
            game_status = Status.EXIT
        elif command == START_COMMAND:
            start_new_game(user_input)


if __name__ == '__main__':
    main()
