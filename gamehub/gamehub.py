"""
This module contains the GameHub class, which is the main class of the application.
It is responsible for parsing the command line arguments and launching the selected game.
"""
import sys
import argparse
from gamehub.chess.chess import Chess
from . import snake, game_of_life, word_guesser

class GameHub:
    """
    The main class of the application. It is responsible for parsing
    the command line arguments and launching the selected game.

    Attribute initialized:
        args: argparse.Namespace object containing the parsed command line arguments.
    """
    def __init__(self) -> None:
        self.args = self.setup_parsers()

    @staticmethod
    def apply_bound(value : int, lower_bound : int, upper_bound : int) -> int:
        """
        Apply a lower and an upper bound to a given value.

        Parameters:
            value: The value to be bounded.
            lower_bound: The lower bound.
            upper_bound: The upper bound.
        Returns:
            The bounded value.
        """
        return max(lower_bound, min(value, upper_bound))
        
    def setup_parsers(self) -> argparse.Namespace:
        """
        Setup the command line argument parsers.

        Returns:
            argparse.Namespace object containing the parsed command line arguments.
        """
        parser = argparse.ArgumentParser(
            prog="gamehub",
            description="GameHub is a game launcher for the terminal.\n")
        subparsers = parser.add_subparsers(dest="game", help="The game to be played.\n")

        # Subparser for snake game
        snake_parser = subparsers.add_parser("snake", help="Play Snake, a game where you control a snake that moves around a bordered area, collecting food pellets. Each time the snake eats a pellet, it grows longer. The challenge is to avoid colliding with the snake's own body or the borders of the play area.\n")
        snake_parser.add_argument("--difficulty",
                                  type=str,
                                  default="Medium",
                                  choices=["Easy","Medium","Hard"],
                                  help="The difficulty level of the game.\n")

        # Subparser for Game of Life
        game_of_life_parser = subparsers.add_parser("game_of_life", help="Play Game of Life, a cellular automaton where you can observe the evolution of cells based on simple rules. It is a zero-player game, meaning that its evolution is determined by only its initial state, requiring no further input.\n")
        game_of_life_parser.add_argument("--mode",
                                         type=str,
                                         default="Automatic",
                                         choices=["Manual","Automatic"],
                                         help="Manual: press any key to update; Automatic: update happens periodically.\n")
        game_of_life_parser.add_argument("--speed",
                                         type=int,
                                         default=100,
                                         help="Choose the speed of the simulation in ms (useful just for Automatic mode).\n")
        game_of_life_parser.add_argument("--density",
                                         type=int,
                                         default=30,
                                         help="The initial density of the cells in the grid.\n")

        # Subparser for Word Guesser
        subparsers.add_parser("word_guesser", help="Play Word Guesser, a game where You have to guess a random 5-letter English word. After each attempt the letters that are not present in the target word are removed from the available letters list and the ones that are present are shown on the terminal. You have six attempts to guess the word.\n")
        
        # Subparser for Chess
        chess_parser = subparsers.add_parser("chess", help="Play the classic game of chess.\n")
        chess_parser.add_argument("--mode",
                                  type=str,
                                  default="Multiplayer",
                                  choices=["Singleplayer", "Multiplayer"],
                                  help="Two players can play on the same terminal (Multiplayer) or you can play alone against an AI (Singleplayer).\n")

        args = parser.parse_args()
        if args.game is None:
            parser.print_help()
            sys.exit(0)
        return args

    def run(self) -> object:
        """
        Run the selected game.
        """
        game = None
        if self.args.game == "snake":
            game = snake.Snake(self.args.difficulty)
        elif self.args.game == "game_of_life":
            game = game_of_life.GameOfLife(self.apply_bound(self.args.speed, 50, 10000),
                                    self.args.mode,
                                    self.apply_bound(self.args.density, 0, 100))
        elif self.args.game == "word_guesser":
            game = word_guesser.WordGuesser()
        elif self.args.game == "chess":
            game = Chess(self.args.mode)
            
        if game is not None:
            game.init_game()

        return game
