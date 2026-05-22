"""
This module contains the WordGuesser class which is responsible for the Word Guesser game.
"""
import curses
from curses import wrapper
from importlib.resources import files
import random
import string
import time
import sys

class WordGuesser:
    """
    This class contains the methods used to run the Word Guesser game.
    
    Attribute initialized:
        won: A boolean flag to check if the player has won the game or not initialized as False.
    """
    def __init__(self):
        self.won = False

    def draw_initial_board(self,
                           stdscr : object,
                           guessed_word : str,
                           guesses : int,
                           alphabet : list) -> None:
        """
        Draw the initial board of the game.

        Parameters:
            stdscr: The standard screen object.
            guessed_word: A void word where the player will insert the letters.
            guesses: The total of guesses at the beginning.
            alphabet: The available letters.
        """
        stdscr.clear()
        stdscr.addstr(1, 30, "Enter a five letter word, press Enter to confirm or ESC to exit.")
        stdscr.addstr(2, 30, "Inserted word: " + "".join(guessed_word))
        stdscr.addstr(3, 30, "Until now: " + "".join(guessed_word))
        stdscr.addstr(4, 30, "Guesses left: " + str(guesses))
        stdscr.addstr(6, 30, "Available letters: " + "".join(alphabet))
        stdscr.refresh()

    def draw_inserted_word(self, stdscr : object, void_guessed_word : list) -> None:
        """
        Draw the word inserted by the player.

        Parameters:
            stdscr: The standard screen object.
            void_guessed_word: The word inserted by the player.
        """
        stdscr.addstr(2, 30, "Inserted word: " + "".join(void_guessed_word))
        stdscr.refresh()

    def draw_after_update(self,
                          stdscr : object,
                          guessed_word : list,
                          guesses : int,
                          alphabet : list) -> None:
        """
        Draw the new game board after the player has inserted a valid (meaningful) word.

        Parameters:
            stdscr: The standard screen object.
            guessed_word: The word that the player has guessed until now.
            guesses: The total of guesses left.
            alphabet: The available letters left after the player has inserted a word.
        """
        stdscr.addstr(3, 30, "Until now: " + "".join(guessed_word))
        stdscr.addstr(4, 30, "Guesses left: " + str(guesses))
        stdscr.addstr(6, 30, "                                                                                  ")
        stdscr.addstr(6, 30, "Available letters: " + "".join(alphabet))
        stdscr.refresh()

    def draw_losing_message(self, stdscr : object, word_to_guess : str) -> None:
        """
        Draw the losing message.

        Parameters:
            stdscr: The standard screen object.
            word_to_guess: The word that the player was supposed to guess.
        """
        stdscr.clear()
        stdscr.addstr(0, 30, "Game over! You ran out of guesses.")
        stdscr.addstr(1, 30, "The word was: " + word_to_guess)
        stdscr.refresh()
        time.sleep(2)

    def draw_winning_message(self, stdscr : object) -> None:
        """"
        Draw the winning message.

        Parameters:
            stdscr: The standard screen object.
        """
        stdscr.clear()
        stdscr.addstr(0, 30, "You won!.")
        stdscr.refresh()
        time.sleep(2)

    def draw_after_invalid_input(self, stdscr : object) -> None:
        """
        Draw a warning message after the player has inserted an invalid word.

        Parameters:
            stdscr: The standard screen object.
        """
        stdscr.addstr(5, 30, "The inserted word is invalid. Please choose another word.")
        stdscr.refresh()
        time.sleep(1)
        stdscr.addstr(5, 30, "                                                         ")
        stdscr.refresh()

    def generate_list_of_words(self, stdscr) -> list:
        """
        Generate a list of meaningful English words of exactly five letters from a file.

        Parameters:
            stdscr: The standard screen object.
        Returns:
            A list of meaningful English words of exactly five letters.
        """
        try:
            words = files("gamehub").joinpath("words.txt").read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            stdscr.addstr(0, 0, "Unable to locate words dictionary.", curses.A_BOLD)
            stdscr.refresh()
            time.sleep(2)
            sys.exit(1)

        return words

    def generate_updated_guess(self,
                               new_guessed : str,
                               to_guess : str,
                               alphabet : list,
                               old_guessed : str) -> tuple:
        """
        Generate the letters present in the target word and the updated alphabet.

        Parameters:
            new_guessed: The word guessed now.
            to_guess: The target word.
            alphabet: The available letters.
            old_guessed: The word guessed before to be compared with the new guessed word.
        Returns:
            A tuple containing the updated guessed word and the updated alphabet.
        """
        updated_guess = ["_" for _ in range(5)]
        # For every character in the guessed word check if it is in the target word
        for i in range(5):
            if new_guessed[i] in to_guess: # If it is, put it wherever it is needed
                for j in range(5):
                    if new_guessed[i] == to_guess[j]:
                        updated_guess[j] = new_guessed[i]
            else:
                # Remove guessed[i] from the alphabet only if it is still there
                if new_guessed[i] in alphabet:
                    alphabet.remove(new_guessed[i])
        
        for i in range(5): # Check if the character is already guessed or not
            if updated_guess[i] == "_" and old_guessed[i] != "_":
                updated_guess[i] = old_guessed[i]

        return updated_guess, alphabet

    def check_terminal_size(self, min_lines : int, min_cols : int, stdscr : object) -> bool:
        """
        Check if the terminal size is enough to play.

        Parameters:
            min_lines: The minimum number of lines required.
            min_cols: The minimum number of columns required.
            stdscr: The standard screen object.
        Returns:
            A boolean flag indicating if the terminal size is enough to play.
        """
        if curses.COLS < min_cols or curses.LINES < min_lines:
            stdscr.addstr(0, 0, "Resize the terminal (" + str(min_cols) + "x" + str(min_lines) + ")", curses.A_BOLD)
            stdscr.refresh()
            time.sleep(2)
            return False
        return True
    
    def initialize_game(self, stdscr : object) -> tuple:
        """
        Initialize the game by hiding the cursor, generating a list of meaningful words,
        choosing one of them as the word to guess and drawing the initial game board.

        Parameters:
            stdscr: The standard screen object.
        Returns:
            A tuple containing the list of all words, the target word, the void guessed word,
            the six guesses available, the entire alphabet and a flag to stop the game.
        """
        curses.curs_set(0)
        meaningful_words = self.generate_list_of_words(stdscr)
        word_to_guess = random.choice(meaningful_words)
        guessed_word = ["_" for _ in range(5)] # The letters that the player has guessed
        guesses = 6
        alphabet = list(string.ascii_lowercase)
        game_stopped = False # Flag to stop the game (when the player wins or loses)
        self.draw_initial_board(stdscr, guessed_word, guesses, alphabet)

        return meaningful_words, word_to_guess, guessed_word, guesses, alphabet, game_stopped
    
    def get_key(self, stdscr) -> str:
        """
        Get a key from the player.

        Parameters:
            stdscr: The standard screen object.
        Returns:
            The string pressed by the player.
        """
        return stdscr.getkey()

    def gameloop(self, stdscr : object) -> None:
        """
        The loop of the Word Guesser game.

        Parameters:
            stdscr: The standard screen object.
        """
        # Check if the terminal size is enough to play the game
        if not self.check_terminal_size(10, 100, stdscr):
            return
        
        meaningful_words, word_to_guess, guessed_word, guesses, alphabet, game_stopped = self.initialize_game(stdscr)

        while not game_stopped:
            characters = 0 # Number of characters inserted by the player
            void_guessed_word = ["_" for _ in range(5)] # A new guess from the player
            self.draw_inserted_word(stdscr, void_guessed_word)

            while characters <= 5:
                inserted_char = self.get_key(stdscr)               
                if inserted_char == '\x1b': # If the player presses ESC then exit the game
                    break
                elif inserted_char == '\x7f' and characters > 0: # If the player presses Backspace
                    characters -= 1 # then delete the last inserted character
                    void_guessed_word[characters] = "_"
                    self.draw_inserted_word(stdscr, void_guessed_word)
                elif inserted_char in list(string.ascii_lowercase) and inserted_char != '\n' and characters != 5:
                    characters += 1
                    void_guessed_word[characters - 1] = inserted_char
                    self.draw_inserted_word(stdscr, void_guessed_word)
                elif inserted_char == '\n' and characters == 5:
                    break

            if inserted_char == '\x1b':
                break

            void_guessed_word = ''.join(void_guessed_word) # Check if the guessed word is meaningful
            if void_guessed_word not in meaningful_words:
                self.draw_after_invalid_input(stdscr)
            else:
                guesses -= 1
                guessed_word, alphabet = self.generate_updated_guess(void_guessed_word, word_to_guess, alphabet, guessed_word)
                self.draw_after_update(stdscr, guessed_word, guesses, alphabet)
                
                if guesses >= 0 and void_guessed_word == word_to_guess:
                    game_stopped = True
                    self.won = True
                    self.draw_winning_message(stdscr)
                
                if guesses == 0 and void_guessed_word != word_to_guess:
                    game_stopped = True
                    self.draw_losing_message(stdscr, word_to_guess)
                    
    def init_game(self) -> None:
        """
        Starting the game.
        """
        wrapper(self.gameloop)
