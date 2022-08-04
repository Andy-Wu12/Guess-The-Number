import os.path
import random
import string
import sys

import pytest
import json

from game import Game, isCorrectGuess
from stat_manager import StatManager


def get_stat_data(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as f:
        stat_data = json.load(f)
    f.close()

    return stat_data


def generateRandStr(num_letters: int):
    return ''.join(random.choices(string.ascii_lowercase, k=num_letters))


class TestGame:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Setup code needed before tests run
        self.game = Game(StatManager())
        self.difficulties = ['easy', 'medium', 'hard']
        # Actual tests run while yielding
        yield
        # Teardown by deleting SAVE FILE after each test
        if os.path.exists(self.game.SAVEFILE_NAME):
            from os import remove
            remove(self.game.SAVEFILE_NAME)

    # Ensure persistent file exists after saving
    def test_savefile_created_on_save(self):
        self.game.saveGameStats()
        assert os.path.exists(self.game.SAVEFILE_NAME)

    # Ensure saving stats provides correct values.
    # Additional tests can be added to check for specific stats
    def test_saving_default__data(self):
        self.game.saveGameStats()
        stat_data = get_stat_data(self.game.SAVEFILE_NAME)
        assert stat_data == self.game.stat_manager.__dict__

    # Ensure winning a game increases number of wins by exactly one
    def test_winning(self):
        num_wins = 0
        for i in range(1000):
            self.game.win()
            assert self.game.stat_manager.wins == num_wins + 1
            num_wins += 1

    # Ensure losing a game increases number of losses by exactly one
    def test_losing(self):
        num_losses = 0
        for i in range(1000):
            self.game.lose()
            assert self.game.stat_manager.losses == num_losses + 1
            num_losses += 1

    # Ensure game difficulty changes properly after valid setdifficulty() call
    def test_set_difficulty(self):
        rand_diffs = self.generateDifficultiesList(1000)
        # Default difficulty test
        assert self.game.DIFFICULTY == 'easy'
        for difficulty in rand_diffs:
            self.game.setDifficulty(difficulty)
            assert self.game.DIFFICULTY == difficulty

    # Ensure invalid 'difficulty' parameter doesn't do anything
    def test_set_invalid_diff(self):
        invalid_diffs = [generateRandStr(3) for _ in range(1000)]
        print(invalid_diffs)
        self.game.setDifficulty('medium')

        for diff in invalid_diffs:
            self.game.setDifficulty(diff)
            assert self.game.DIFFICULTY == 'medium'

    # Ensure wins on easy mode increment "num_easy_wins" and wins
    def test_easy_win(self):
        num_easy_wins = self.generateDiffWinTest('easy', 10)
        assert self.game.stat_manager.num_easy_wins == num_easy_wins

    # Ensure wins on med mode increment "num_med_wins"
    def test_med_win(self):
        num_med_wins = self.generateDiffWinTest('medium', 10)
        assert self.game.stat_manager.num_med_wins == num_med_wins

    # Ensure wins on hard increment "num_hard_wins"
    def test_hard_wins(self):
        num_hard_wins = self.generateDiffWinTest('hard', 10)
        assert self.game.stat_manager.num_hard_wins == num_hard_wins

    # Ensure stat incremented after player guesses correctly on first try
    def test_first_guess_win(self):
        num_first_guesses = 0
        num_total_wins = 0
        win_types = [self.game.win, self.game.firstGuessWin]

        # regular_win_name = win_types[0].__name__
        first_guess_win_name = win_types[1].__name__

        rand_wins = [random.choice(win_types) for _ in range(1000)]

        for win in rand_wins:
            win()
            if win.__name__ == first_guess_win_name:
                num_first_guesses += 1

            num_total_wins += 1

        assert self.game.stat_manager.wins == num_total_wins
        assert self.game.stat_manager.num_first_correct == num_first_guesses

    # Ensure isCorrectGuess returns True if numbers are equal, False otherwise
    def test_correct_guess(self):
        num_iterations = 10000
        upper_bound = sys.maxsize
        for i in range(num_iterations):
            answer = random.randint(1, upper_bound)
            guess = random.randint(1, upper_bound)
            if answer == guess:
                assert isCorrectGuess(answer, guess)
            else:
                assert not isCorrectGuess(answer, guess)

    # Helpers
    def setDiffAndWin(self, difficulty: str):
        self.game.setDifficulty(difficulty)
        self.game.win()

    def generateDifficultiesList(self, amount: int):
        return [random.choice(self.difficulties) for _ in range(amount)]

    def generateDiffWinTest(self, diffToCheck: str, iter_count: int):
        num_diff_wins = 0
        rand_diffs = self.generateDifficultiesList(iter_count)

        for difficulty in rand_diffs:
            self.game.setDifficulty(difficulty)
            self.game.win()
            if difficulty == diffToCheck:
                num_diff_wins += 1

        return num_diff_wins
