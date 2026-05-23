"""
This module contains the TestSnake class which is
responsible for testing the Snake game.
"""
from collections import deque
import pytest # type: ignore
from gamehub.snake import Snake
from hypothesis import given, strategies, settings # type: ignore
from hypothesis.strategies import composite, integers # type: ignore

class TestSnake:
    """
    This class contains the methods used to test the Snake game.
    """
    def test_constructor_isinstance(self) -> None:
        """
        Test if the constructor of the Snake class returns an instance of the Snake class.
        """
        s = Snake()
        assert isinstance(s, Snake)

    @pytest.mark.parametrize("difficulty, expected",
                             [("Easy", 0.1),
                                ("Medium", 0.05),
                                ("Hard", 0.025)])
    def test_constructor(self, difficulty : str, expected : float) -> None:
        """
        Test the constructor of the Snake class.
        """
        s = Snake(difficulty)
        assert s.delta_time == expected

    def test_constructor_default(self) -> None:
        """
        Test the default behavior of the constructor of the Snake class.
        """
        s = Snake()
        assert s.delta_time == 0.05

    @pytest.mark.parametrize("key, current_direction, expected",
                             [("KEY_UP", "DOWN", "DOWN"),
                                ("KEY_DOWN", "RIGHT", "DOWN"),
                                ("KEY_LEFT", "UP", "LEFT"),
                                ("KEY_DOWN", "DOWN", "DOWN"),
                                ("KEY_RIGHT", "LEFT", "LEFT")])
    def test_calculate_direction(self, key : str, current_direction : str, expected : str) -> None:
        """
        Test the calculation of the new direction of the snake.
        """
        snake_t = Snake()
        assert snake_t.calculate_direction(current_direction, key) == expected

    @pytest.mark.parametrize("y, x, direction, SNAKE_BOUNDS, expected",
                             [(1, 2, "UP", (1, 10, 2, 20), (1, 2)),
                              (1, 2, "RIGHT", (1, 10, 2, 20), (1, 4)),
                              (10, 10, "DOWN", (1, 10, 2, 20), (10, 10)),
                              (9, 8, "LEFT", (1, 10, 2, 20), (9, 6)),
                              (5, 4, "UP", (1, 10, 2, 20), (4,4))])
    def test_calculate_new_position(self,
                                    y : int,
                                    x : int,
                                    direction : str,
                                    SNAKE_BOUNDS : tuple[int, int, int, int],
                                    expected : tuple[int, int]) -> None:
        """
        Test the calculation of the new position of the snake.
        """
        s = Snake()
        assert s.calculate_new_position(y, x, direction, SNAKE_BOUNDS) == expected

    @composite
    def smaller_than_y(draw) -> tuple[int, int]:
        """
        Generate two integers where the second one is greater than the first one.
        """
        a = draw(integers(min_value=1))
        b = draw(integers(min_value=a))
        return a, b
    @composite
    def smaller_than_x(draw) -> tuple[int, int]:
        """
        Generate two big integers where the second one is greater than the first one.
        """
        a = draw(integers(min_value=1)) * 2
        b = draw(integers(min_value=a)) * 2
        return a, b
    @given(strategies.tuples(
            smaller_than_y(),
            smaller_than_x(),
            strategies.just("UP") |
            strategies.just("DOWN") |
            strategies.just("LEFT") |
            strategies.just("RIGHT")))
    @settings(max_examples=20)
    def test_property_calculate_new_position_always_inside(self, t : tuple) -> None:
        """
        Test that the new position found for the snake is always inside the bounds.
        """
        s = Snake()
        SNAKE_BOUNDS = (1, t[0][1], 2, t[1][1])
        res_y, res_x = s.calculate_new_position(t[0][0],t[1][0],t[2],SNAKE_BOUNDS)
        assert res_y >= SNAKE_BOUNDS[0] and res_y <= SNAKE_BOUNDS[1] and res_x >= SNAKE_BOUNDS[2] and res_x <= SNAKE_BOUNDS[3] and res_x % 2 == 0
       
    @pytest.mark.parametrize("body, SNAKE_BOUNDS",
                             [   ([(1, 2), (1, 4), (1, 6)], (1, 5, 2, 10)),
                                 ([(1, 2), (1, 4), (1, 6)], (1, 5, 2, 10)),
                                 ([(2, 2), (3, 2), (3, 4)], (1, 5, 2, 10)),
                                 ([(2, 2), (3, 2), (3, 4)], (1, 5, 2, 10)),
                                 ([(1, 2), (1, 4)], (1, 1, 2, 6))])
    def test_new_food_coordinates(self,
                                  body : deque[tuple[int, int]],
                                  SNAKE_BOUNDS : tuple[int, int, int, int]) -> None:
        """
        Test the generation of new food coordinates.
        """
        s = Snake()
        (y, x) = s.new_food_coordinates(body, SNAKE_BOUNDS)
        assert (y, x) not in body

    @given(strategies.tuples(
        strategies.integers(min_value=10),
        strategies.integers(min_value=20)
        ))
    @settings(max_examples=10)
    def test_property_new_food_coordinates_always_inside(self, t : tuple[int, int]) -> None:
        """
        Test that the food coordinates generated are always inside the bounds.
        """
        s = Snake()
        SNAKE_BOUNDS = (1, t[0], 2, t[1])
        (y, x) = s.new_food_coordinates([], SNAKE_BOUNDS)
        assert y >= SNAKE_BOUNDS[0] and y <= SNAKE_BOUNDS[1] and x >= SNAKE_BOUNDS[2] and x <= SNAKE_BOUNDS[3] and x % 2 == 0

    @pytest.mark.parametrize("body, y_food, x_food, expected",
                             [  ([(0, 0), (0, 2), (0, 4)], 0, 6, False),
                                ([(0, 0), (0, 2), (0, 4)], 0, 4, True),
                                ([(4, 6), (5, 6)], 12, 2, False),
                                 ([(4, 6), (5, 6)], 5, 6, True) ])
    def test_check_food_eaten(self,
                              body : deque[tuple[int, int]],
                              y_food : int,
                              x_food : int,
                              expected : bool) -> None:
        """
        Test the verification of food eaten by the snake.
        """
        s = Snake()
        assert s.check_food_eaten(body, y_food, x_food) == expected
    
    @pytest.mark.parametrize("body, expected",
                             [  ([(0, 0), (0, 2), (0, 4)], False),
                                ([(0, 0), (0, 2), (0, 4), (1,4), (1,2), (0,2)], True),
                                ([(9, 6), (10, 6), (11, 6)], False),
                                ([(9, 6), (10, 6), (10, 4), (9,4), (9,6)], True) ])
    def test_verify_collision(self, body : deque[tuple[int, int]], expected : bool) -> None:
        """
        Test the verification of collision of the snake with itself
        """
        s = Snake()
        assert s.verify_collision(body) == expected

    def test_gameloop_without_restart(self, monkeypatch) -> None:
        """
        Test the gameloop method of the Snake class in the following scenario:

        the player always presses the right key, 3 food items are spawned on its path (same row but different columns) and
        a fourth one is spawned on a different row. The game should end when the snake collides with the right wall.
        The score (and the highscore as well) should be 3.
        """
        def food_coordinates_factory():
            coordinates = [(2, 8), (2, 12), (2, 16), (5, 6)]
            for coord in coordinates:
                yield coord

        food_coords_gen = food_coordinates_factory()
        
        def get_next_food_coordinates(self, *args):
            return next(food_coords_gen)
        
        def setup_curses(self, *args):
            return (None, None, None, 30, 60, None, None)

        # Mock all the gameloop methods related to curses to avoid the need of a terminal
        monkeypatch.setattr(Snake, "check_terminal_size", lambda *args: True)
        monkeypatch.setattr(Snake, "set_up_curses", setup_curses)
        monkeypatch.setattr(Snake, "update_main_window", lambda *args: None)
        monkeypatch.setattr(Snake, "update_score_window", lambda *args: None)
        monkeypatch.setattr(Snake, "get_input_end_game", lambda *args: '\x1b')

        # Mock the input method to always return KEY_RIGHT
        monkeypatch.setattr(Snake, "get_input_and_delay", lambda *args: "KEY_RIGHT")
        monkeypatch.setattr(Snake, "new_food_coordinates", get_next_food_coordinates)

        s = Snake()
        s.gameloop(None)
        assert s.score == 3 and s.highscore == 3

    def test_gameloop_with_restart(self, monkeypatch) -> None:
        """
        Test the gameloop method of the Snake class in the following scenario:

        the player presses 'a' to restart the game after losing.
        Then the player always presses the right key, 2 food items are spawned on its path (same row but different columns) and
        a third food item is spawned on a different row. The game should end when the snake collides with the right wall.
        The score should be 2 while the best score should be 3.
        """
        def food_coordinates_factory():
            coordinates = [ (2, 8), (2, 12), (2, 16), (5, 6), 
                            (2, 12), (2, 16), (5, 6)]
            for coord in coordinates:
                yield coord

        food_coords_gen = food_coordinates_factory()
        
        def get_next_food_coordinates(self, *args):
            return next(food_coords_gen)
        
        def input_factory():
            inputs = ['a', '\x1b']
            for input in inputs:
                yield input

        inputs_gen = input_factory()
        
        def get_next_input(self, *args):
            return next(inputs_gen)
        
        def setup_curses(self, *args):
            return (None, None, None, 30, 60, None, None)
        
        def mock_restart_game(self, *args):
            self.score = 0
            return deque([(2, 4), (2, 6)]), "RIGHT", "KEY_RIGHT"

        # Mock all the gameloop methods related to curses to avoid the need of a terminal
        monkeypatch.setattr(Snake, "check_terminal_size", lambda *args: True)
        monkeypatch.setattr(Snake, "set_up_curses", setup_curses)
        monkeypatch.setattr(Snake, "update_main_window", lambda *args: None)
        monkeypatch.setattr(Snake, "update_score_window", lambda *args: None)
        monkeypatch.setattr(Snake, "get_input_end_game", get_next_input)
        monkeypatch.setattr(Snake, "restart_game", mock_restart_game)

        # Mock the input method to always return KEY_RIGHT
        monkeypatch.setattr(Snake, "get_input_and_delay", lambda *args: "KEY_RIGHT")
        monkeypatch.setattr(Snake, "new_food_coordinates", get_next_food_coordinates)

        s = Snake()
        s.gameloop(None)
        assert s.score == 2 and s.highscore == 3
