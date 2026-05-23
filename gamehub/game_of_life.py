"""
This module contains the GameOfLife class that implements the Game of Life game.
"""
import curses
from curses import wrapper
import random
import time

class GameOfLife:
    """
    Class used to run the Game of Life game.

    Attributes:
    - speed: The speed of the game in milliseconds
    - delta_time: How many seconds to sleep between each iteration
    - mode: The mode of the game (Automatic or Manual)
    - density: The percentage of alive cells in the initial matrix
    - matrix: The matrix of cells
    """
    def __init__(self, speed: int = 100, mode: str = "Automatic", density: int = 30):
        self.speed = speed
        self.delta_time = speed / 1000
        self.mode = mode
        self.density = density
        self.matrix = None

    def initialize_matrix(self, rows : int, cols : int, density : int) -> list[list[int]]:
        """
        Initialize a matrix (rows x cols) with random values (0 or 1)
        based on the density parameter.

        Parameters:
        - rows: The number of rows of the matrix
        - cols: The number of columns of the matrix
        - density: The percentage of cells that will be alive

        Return:
        - list[list[int]] -> The matrix of cells
        """
        matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if random.randint(0, 100) < density:
                    matrix[i][j] = 1
        return matrix

    def count_live_neighbors(self, matrix : list[list[int]], y : int, x : int) -> int:
        """
        Count the number of live neighbors (cells with value 1)
        of the cell in position (y, x) in the matrix.

        Parameters:
        - matrix: The matrix of cells
        - y: The row of the cell
        - x: The column of the

        Return:
        - int -> The number of live neighbors
        """
        count = 0
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if i == y and j == x:
                    continue
                if i < 0 or j < 0 or i >= len(matrix) or j >= len(matrix[0]):
                    continue
                count += matrix[i][j]
        return count

    def update_matrix(self, matrix : list[list[int]]) -> list[list[int]]:
        """
        Update the matrix based on the rules of the Game of Life:
        - Any live cell with fewer than two live neighbors dies (underpopulation)
        - Any live cell with two or three live neighbors lives on to the next generation
        - Any live cell with more than three live neighbors dies (overpopulation)
        - Any dead cell with exactly three live neighbors becomes a live cell (reproduction)

        Parameters:
        - matrix: The matrix of cells

        Return:
        - The updated matrix of cells
        """
        new_matrix = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                live_neighbors = self.count_live_neighbors(matrix, i, j)
                if matrix[i][j] == 1: # Cell is alive
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_matrix[i][j] = 0 # Die (underpopulation or overpopulation)
                    else:  # Survive
                        new_matrix[i][j] = 1
                else: # Cell is dead
                    if live_neighbors == 3: # Reproduce
                        new_matrix[i][j] = 1
        return new_matrix

    def draw_board(self, stdscr : curses.window, matrix : list[list[int]], color : int) -> None:
        """
        Draw the matrix in the terminal with the given color.
        Each cell is represented by two spaces.

        Parameters:
        - stdscr: The standard screen object of curses
        - matrix: The matrix of cells
        - color: The color to use to draw the cells
        """
        stdscr.clear()
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 1:
                    try:
                        stdscr.addstr(i, j * 2, "  ", color)
                    except curses.error:
                        pass
        stdscr.refresh()

    def get_input_and_sleep(self, stdscr : curses.window) -> str:
        """
        Get the last key pressed by the user and sleep for
        delta_time seconds if the mode is "Automatic".

        Return:
        - The last key pressed by the user
        """
        try:
            last_key = stdscr.getkey()
        except curses.error:
            last_key = None

        if self.mode == "Automatic":
            time.sleep(self.delta_time)

        return last_key

    def init_curses(self, stdscr) -> tuple[int, int, int]:
        """
        Initialize the curses library.

        Return:
        - The color to use to draw the cells
        - The number of rows of the terminal
        - The number of columns of the terminal
        """
        curses.curs_set(0)  # Hide cursor

        if self.mode == "Automatic":
            stdscr.nodelay(True) # Non-blocking input

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)

        return curses.color_pair(1), curses.LINES, curses.COLS//2

    def gameloop(self, stdscr) -> None:
        """
        Main game loop of Game of Life.
        """
        COLOR_WHITE_WHITE, LINES, COLS = self.init_curses(stdscr)
        self.matrix = self.initialize_matrix(LINES, COLS, self.density)
        last_key = None
        while last_key != '\x1b':
            self.draw_board(stdscr, self.matrix, COLOR_WHITE_WHITE)
            self.matrix = self.update_matrix(self.matrix)
            last_key = self.get_input_and_sleep(stdscr)

    def init_game(self) -> None:
        """
        Run the Game of Life game.
        """
        wrapper(self.gameloop)  # Call the function via wrapper
