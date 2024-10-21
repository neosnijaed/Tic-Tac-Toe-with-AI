class Board:
    """
    The Board class represents a 3x3 Tic-Tac-Toe game board.
    """
    EMPTY_CELL = '_'
    SYMBOLS = {'X', 'O'}
    BOARD_SIZE = 3

    def __init__(self) -> None:
        """
        Initializes the game board with empty cells and no winning symbol.
        """
        self.board = [[self.EMPTY_CELL for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.winning_symbol = None

    def display_board(self) -> None:
        """
        Displays the current state of the game board.
        """
        print('-' * 9)
        for line in self.board:
            print('| ', end='')
            for cell in line:
                print('  ', end='') if cell == '_' else print(f'{cell} ', end='')
            print('|')
        print('-' * 9)

    def is_full(self) -> bool:
        """
        Checks if the board is full.
        :return: bool: True if the board is full, False otherwise.
        """
        return all(self.EMPTY_CELL not in row for row in self.board)

    def get_empty_cells(self) -> list[tuple[int, int]]:
        """
        Returns a list of coordinates of empty cells on the board.
        :return: list[tuple[int, int]]: List of coordinates of empty cells on the board.
        """
        return [(row, col) for row in range(self.BOARD_SIZE) for col in range(self.BOARD_SIZE) if
                self.board[row][col] == self.EMPTY_CELL]

    def set_cell(self, row: int, col: int, value: str) -> None:
        """
        Sets the value of a specified cell on the board.
        :param row: integer row number
        :param col: integer column number
        :param value: string containing 'X', 'O' or '_'
        """
        self.board[row][col] = value

    def is_cell_occupied(self, row: int, col: int) -> bool:
        """
        Checks if a specified cell is occupied.
        :param row: integer row number
        :param col: integer column number
        :return: boolean: True if the cell is occupied, False otherwise.
        """
        return self.board[row][col] in self.SYMBOLS

    def check_three_in_row(self) -> bool:
        """
        Checks if there are three matching symbols in any row.
        :return: boolean: True if there are three matching symbols in any row, False otherwise.
        """
        return any(self.check_winning_condition(row) for row in self.board)

    def check_three_in_column(self) -> bool:
        """
        Checks if there are three matching symbols in any column.
        :return: boolean: True if there are three matching symbols in any column, False otherwise.
        """
        return any(self.check_winning_condition([self.board[row][col] for row in range(self.BOARD_SIZE)]) for col in
                   range(self.BOARD_SIZE))

    def check_three_in_diagonal(self) -> bool:
        """
        Checks if there are three matching symbols in any diagonal.
        :return: boolean: True if there are three matching symbols in any diagonal, False otherwise.
        """
        diagonals = [[self.board[i][i] for i in range(self.BOARD_SIZE)],
                     [self.board[i][self.BOARD_SIZE - 1 - i] for i in range(self.BOARD_SIZE)]]
        return any(self.check_winning_condition(diagonal) for diagonal in diagonals)

    def check_winning_condition(self, line: list[str]) -> bool:
        """
        Checks if a line contains three matching symbols.
        :param line: List containing 3 string symbols.
        :return: boolean: True if the line contains three matching symbols, False otherwise.
        """
        for symbol in self.SYMBOLS:
            if all(cell == symbol for cell in line):
                self.winning_symbol = symbol
                return True
        return False

    def find_two_in_line(self, symbol: str) -> list[tuple[int, int]]:
        """
        Finds and returns positions with two matching symbols in a row, column, or diagonal.
        :param symbol: String containing 'X' or 'O'
        :return: List of coordinates with two matching symbols in a row, column and diagonal.
        """
        return self.check_two_in_row(symbol) + self.check_two_in_column(symbol) + self.check_two_in_diagonal(symbol)

    def check_two_in_row(self, symbol: str) -> list[tuple[int, int]]:
        """
        Checks for two matching symbols in any row and returns positions.
        :param symbol: String containing 'X' or 'O'
        :return: List of coordinates with two matching symbols in a row.
        """
        ai_options = []
        for i, row in enumerate(self.board):
            for j in range(self.BOARD_SIZE):
                if row.count(symbol) == 2 and self.board[i][j] == self.EMPTY_CELL:
                    ai_options.append((i, j))
        return ai_options

    def check_two_in_column(self, symbol: str) -> list[tuple[int, int]]:
        """
        Checks for two matching symbols in any column and returns positions.
        :param symbol: String containing 'X' or 'O'
        :return: List of coordinates with two matching symbols in a column.
        """
        ai_options = []
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if (self.board[row][col] == self.EMPTY_CELL and self.board[row - 1][col] == symbol and
                        self.board[row - 2][col] == symbol):
                    ai_options.append((row, col))
        return ai_options

    def check_two_in_diagonal(self, symbol: str) -> list[tuple[int, int]]:
        """
        Checks for two matching symbols in any diagonal and returns positions.
        :param symbol: String containing 'X' or 'O'
        :return: List of coordinates with two matching symbols in a diagonal.
        """
        ai_options = []
        for i in range(self.BOARD_SIZE):
            if (self.board[i][i] == self.EMPTY_CELL and self.board[i - 1][i - 1] == symbol and
                    self.board[i - 2][i - 2] == symbol):
                ai_options.append((i, i))
        if self.board[0][2] == self.EMPTY_CELL and self.board[1][1] == symbol and self.board[2][0] == symbol:
            ai_options.append((0, 2))
        if self.board[0][2] == symbol and self.board[1][1] == self.EMPTY_CELL and self.board[2][0] == symbol:
            ai_options.append((1, 1))
        if self.board[0][2] == symbol and self.board[1][1] == symbol and self.board[2][0] == self.EMPTY_CELL:
            ai_options.append((2, 0))
        return ai_options
