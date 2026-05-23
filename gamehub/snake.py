"""
This module contains the Snake class which is responsible for the Snake game.
"""
import curses
from curses import wrapper
import time
from collections import deque
import random

class Snake:
    """
    This class contains the methods used to run the Snake game.
    
    Parameters:
        difficulty: The difficulty of the game that can be "Easy", "Medium" or "Hard".
    Attributes initialized:
        delta_time: Seconds between two frames of the game, determined by the difficulty.
        difficulty: The difficulty of the game, specified by the player.
        score: The current score of the player.
        highscore: The highest score of the player.
    """
    def __init__(self, difficulty="Medium") -> None:
        self.delta_time = None
        self.difficulty = difficulty
        if self.difficulty == "Easy":
            self.delta_time = 0.1
        elif self.difficulty == "Medium":
            self.delta_time = 0.05
        else:
            self.delta_time = 0.025
        self.score = 0
        self.highscore = 0
        
    def calculate_new_position(self,
                             y : int,
                             x : int,
                             direction : str,
                             SNAKE_BOUNDS : tuple[int, int, int, int]) -> tuple[int, int]:
        """
        Calculates the new position of the snake's head.

        Parameters:
            y: The current row of the snake's head.
            x: The current column of the snake's head.
            direction: The current direction of the snake's movement.
            SNAKE_BOUNDS: The bounds of the snake's movement.
        Returns:
            A tuple containing the new position of the snake's head.
        """
        if direction == "UP":
            if y > SNAKE_BOUNDS[0]:
                y -= 1
        elif direction == "DOWN":
            if y < SNAKE_BOUNDS[1]:
                y += 1
        elif direction == "LEFT":
            if x > SNAKE_BOUNDS[2]:
                x -= 2
        elif direction == "RIGHT":
            if x < SNAKE_BOUNDS[3]:
                x += 2
        return y, x

    def calculate_direction(self, current_direction : str, key : str) -> str:
        """
        Calculates the new direction of the snake's movement.

        Parameters:
            current_direction: The current direction of the snake's movement.
            key: The direction specified by the player.
        Returns:
            The new direction of the snake's movement.
        """
        if key == "KEY_UP" and current_direction != "DOWN":
            return "UP"
        elif key == "KEY_DOWN" and current_direction != "UP":
            return "DOWN"
        elif key == "KEY_LEFT" and current_direction != "RIGHT":
            return "LEFT"
        elif key == "KEY_RIGHT" and current_direction != "LEFT":
            return "RIGHT"
        return current_direction

    def draw_snake(self, window, body : deque[tuple[int, int]], color : int) -> None:
        """
        Draws the snake on the screen.

        Parameters:
            window: The window where the snake will be drawn.
            body: The entire snake.
            color: The color used in the drawing.
        """
        for y, x in body:
            window.addstr(y, x, "  ", color)

    def draw_food(self, window, y : int, x : int, color : int) -> None:
        """
        Draws the food on the screen.

        Parameters:
            window: The window where the food will be drawn.
            y: The row where the food will be drawn.
            x: The column where the food will be drawn.
            color: The color used in the drawing.
        """
        window.addstr(y, x, "  ", color)

    def draw_thick_border(self, window, ROWS : int, COLS : int, color : int) -> None:
        """
        Draws the thick border of the window.

        Parameters:
            window: The window whose border will be drawn.
            ROWS: The number of rows used.
            COLS: The number of columns used.
            color: The color used in the drawing.
        """
        for i in range(ROWS - 1):
            window.addstr(i, 1, " ", color)
            window.addstr(i, COLS - 2, " ", color)
        
    def draw_game_over(self, window, ROWS : int, COLS : int) -> None:
        """
        Draws the game over message on the screen.

        Parameters:
            window: The window where the game over screen will be drawn.
            ROWS: The number of rows of the window.
            COLS: The number of columns of the window.
        """
        window.addstr(ROWS//2 - 3, COLS//2 - 10, "GAME OVER", curses.A_BOLD)
        window.addstr(ROWS//2 - 2, COLS//2 - 10, "SCORE: " + str(self.score), curses.A_BOLD)
        window.addstr(ROWS//2 - 1, COLS//2 - 10, "HIGHSCORE: " + str(self.highscore), curses.A_BOLD)
        window.addstr(ROWS//2, COLS//2 - 10, "Press any key to play again...", curses.A_BLINK)
        window.refresh()
        time.sleep(1)

    def new_food_coordinates(self, body : deque[tuple[int, int]], SNAKE_BOUNDS : int) -> tuple:
        """
        Generates new coordinates for the food.

        Parameters:
            body: The snake.
            SNAKE_BOUNDS: The bounds of the snake's movement.
        Returns:
            A tuple containing the new coordinates for the food.
        """
        y= random.randint(SNAKE_BOUNDS[0], SNAKE_BOUNDS[1])
        x= random.randint(SNAKE_BOUNDS[2], SNAKE_BOUNDS[3])
        if x%2!=0:
            x-=1
        while (y,x) in body:
            y= random.randint(SNAKE_BOUNDS[0], SNAKE_BOUNDS[1])
            x= random.randint(SNAKE_BOUNDS[2], SNAKE_BOUNDS[3])
            if x%2!=0:
                x-=1
        return y, x
        
    def check_food_eaten(self, body : deque[tuple[int, int]], y_food : int, x_food : int) -> bool:
        """
        Checks if the snake has eaten the food.

        Parameters:
            body: The snake.
            y_food: The row of the food.
            x_food: The column of the food.
        Returns:
            True if the snake has eaten the food, False otherwise.
        """
        return body[-1] == (y_food, x_food)

    def verify_collision(self, body : deque[tuple[int, int]]) -> bool:
        """
        Verifies if the snake has collided with itself.

        Parameters:
            body: The snake.
        Returns:
            True if the snake has collided with itself, False otherwise.
        """
        return any(body[-1] == body[i] for i in range(len(body) - 1))
    
    def check_terminal_size(self, min_lines : int, min_cols : int, window : object) -> bool:
        """
        Check if the terminal size is enough to play.

        Parameters:
            min_lines: The minimum number of lines required.
            min_cols: The minimum number of columns required.
            window: The window where the message will be displayed.
        Returns:
            A boolean flag indicating if the terminal size is enough to play.
        """
        if curses.COLS < min_cols or curses.LINES < min_lines:
            window.addstr(0, 0, "Resize the terminal (" + str(min_cols) + "x" + str(min_lines) + ")", curses.A_BOLD)
            window.refresh()
            time.sleep(2)
            return False
        return True

    def set_up_curses(self, stdscr) -> None:
        """
        Set up the curses environment.

        Parameters:
            stdscr: The standard screen.
        """
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(True) # Non-blocking input

        # Define colors
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_WHITE)

        LINES_MAIN_WINDOW = curses.LINES - 6
        if curses.COLS % 2 == 0:
            COLS_MAIN_WINDOW = curses.COLS - 10
        else:
            COLS_MAIN_WINDOW = curses.COLS - 11

        main_window = curses.newwin(LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, 3, 5)
        score_window = curses.newwin(2, 12, 0, curses.COLS - 20)
        stdscr.refresh()

        return curses.color_pair(1), curses.color_pair(2), curses.color_pair(3), LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, main_window, score_window

    def update_main_window(self,
                           main_window : object,
                           color_border : int,
                           color_snake : int,
                           color_food : int,
                           LINES_MAIN_WINDOW : int,
                           COLS_MAIN_WINDOW : int,
                           body : deque[tuple[int, int]],
                           x_food : int, y_food : int,
                           game_over=False) -> None:
        """
        Update the main window.

        Parameters:
            main_window: The main window.
            color_border: The color of the border.
            color_snake: The color of the snake.
            color_food: The color of the food.
            LINES_MAIN_WINDOW: The number of lines of the main window.
            COLS_MAIN_WINDOW: The number of columns of the main window.
            body: The snake.
            x_food: The column of the food.
            y_food: The row of the food.
            game_over: A boolean flag indicating if the game is over or not.
        """
        main_window.clear()
        main_window.border(color_border, color_border, color_border, color_border, color_border, color_border, color_border, color_border)
        self.draw_thick_border(main_window, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, color_border)
        self.draw_snake(main_window, body, color_snake)
        self.draw_food(main_window, y_food, x_food, color_food)
        if game_over:
            self.draw_game_over(main_window, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW)
        main_window.refresh()
    
    def update_score_window(self, score_window) -> None:
        """
        Update the score window.

        Parameters:
            score_window: The window where the scores (Score and Best score) will be displayed.
        """
        score_window.clear()
        score_window.addstr(0, 0, "Score: " + str(self.score))
        score_window.addstr(1, 0, "Best: " + str(self.highscore))
        score_window.refresh()

    def get_input_and_delay(self, stdscr) -> str:
        """
        Get the input from the player and delay the game.

        Parameters:
            stdscr: The standard screen.
        Returns:
            The string pressed by the player.
        """
        try:
            key = stdscr.getkey()
        except curses.error:
            key = None
        finally:
            time.sleep(self.delta_time)
        return key
    
    def get_input_end_game(self, stdscr) -> str:
        """
        Get the input from the player to check if ESC is pressed.

        Parameters:
            stdscr: The standard screen.
        Returns:
            The string pressed by the player.
        """
        stdscr.nodelay(False)
        key = stdscr.getkey()
        return key
    
    def restart_game(self, stdscr) -> None:
        """
        Restart the game.

        Parameters:
            stdscr: The standard screen.
        """
        self.score = 0
        stdscr.nodelay(True)
        return deque([(2,4), (2,6)]), "RIGHT", "KEY_RIGHT"

    def gameloop(self, stdscr) -> None:
        """
        The loop of the Snake game.

        Parameters:
            stdscr: The standard screen object.
        """
        if not self.check_terminal_size(15, 40, stdscr):
            return

        COLOR_GREEN_GREEN, COLOR_RED_RED, COLOR_WHITE_WHITE, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, main_window, score_window = self.set_up_curses(stdscr)
        SNAKE_BOUNDS = (1, LINES_MAIN_WINDOW - 2, 2, COLS_MAIN_WINDOW - 4) # (y1,y2,x1,x2) : snake can't get out of this bounds (but it can walk over this bounds)

        # Initial snake
        body = deque([(2,4)])
        direction = "RIGHT"
        last_key = "KEY_RIGHT"

        y_food, x_food = self.new_food_coordinates(body, SNAKE_BOUNDS)
        self.update_score_window(score_window)

        while last_key != '\x1b':
            (y, x) = self.calculate_new_position(body[-1][0], body[-1][1], direction, SNAKE_BOUNDS)
            body.append((y, x))
            if self.verify_collision(body):
                self.update_main_window(main_window, COLOR_WHITE_WHITE, COLOR_GREEN_GREEN, COLOR_RED_RED, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, body, x_food, y_food, True)
                if last_key != '\x1b' and self.get_input_end_game(stdscr) != '\x1b':
                    body, direction, last_key = self.restart_game(stdscr)
                    self.update_score_window(score_window)
                    y_food, x_food = self.new_food_coordinates(body, SNAKE_BOUNDS)
                else:
                    break
            if self.check_food_eaten(body, y_food, x_food):
                body.append((y, x))
                y_food, x_food = self.new_food_coordinates(body, SNAKE_BOUNDS)
                self.score += 1
                if self.score > self.highscore:
                    self.highscore = self.score
                self.update_score_window(score_window)
            else:
                body.popleft()

            direction = self.calculate_direction(direction, last_key)
            self.update_main_window(main_window, COLOR_WHITE_WHITE, COLOR_GREEN_GREEN, COLOR_RED_RED, LINES_MAIN_WINDOW, COLS_MAIN_WINDOW, body, x_food, y_food)
            last_key = self.get_input_and_delay(stdscr)
        
    def init_game(self) -> None:
        """
        Starting the game.
        """
        wrapper(self.gameloop)  # Call the function via wrapper
