import os.path
import random
import string

import pytest
import json

from game import Game

def get_stat_data(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as f:
        stat_data = json.load(f)
    f.close()

    return stat_data

class TestGame:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Setup code needed before tests run
        self.game = Game()
        self.difficulties = ['easy', 'medium', 'hard']
        # Actual tests run while yielding
        yield
        # Teardown by deleting SAVE FILE after each test
        if os.path.exists(self.game.SAVEFILE_NAME):
            from os import remove
            remove(self.game.SAVEFILE_NAME)

    # TEST: Initial persistent file should not exist on very first startup
    def test_savefile_missing_on_first_start(self):
        assert not os.path.exists(self.game.SAVEFILE_NAME)

    # TEST: Ensure persistent file exists after saving
    def test_savefile_created_on_save(self):
        self.game.saveGameStats()
        assert os.path.exists(self.game.SAVEFILE_NAME)

    # TEST: Ensure saving stats provides correct values.
    # Additional tests can be added to check for specific stats, but it can get redundant
    def test_saving_default__data(self):
        self.game.saveGameStats()
        stat_data = get_stat_data(self.game.SAVEFILE_NAME)
        assert stat_data == self.game.stat_manager.__dict__

    # TEST: Ensure winning a game increases number of wins by exactly one
    def test_winning(self):
        num_wins = 0
        for i in range(1000):
            self.game.win()
            assert self.game.stat_manager.wins == num_wins + 1
            num_wins += 1

    # TEST: Ensure losing a game increases number of losses by exactly one
    def test_losing(self):
        num_losses = 0
        for i in range(1000):
            self.game.lose()
            assert self.game.stat_manager.losses == num_losses + 1
            num_losses += 1

    # TEST: Ensure game difficulty changes properly after valid setdifficulty() call
    def test_set_difficulty(self):
        rand_diffs = self.generateDifficultiesList(1000)
        # Default difficulty test
        assert self.game.DIFFICULTY == 'easy'
        for difficulty in rand_diffs:
            self.game.setDifficulty(difficulty)
            assert self.game.DIFFICULTY == difficulty

    # TEST: Ensure invalid 'difficulty' parameter doesn't do anything
    def test_set_invalid_diff(self):
        invalid_diffs = [''.join(random.choices(string.ascii_lowercase, k=5)) for _ in range(1000)]
        self.game.setDifficulty('medium')

        for diff in invalid_diffs:
            self.game.setDifficulty(diff)
            assert self.game.DIFFICULTY == 'medium'

    # TEST: Ensure wins on easy mode increment "num_easy_wins" and wins
    def test_easy_win(self):
        assert self.game.stat_manager.num_easy_wins == self.generateDifficultyWinTest('easy', 1000)

    # TEST: Ensure wins on med mode increment "num_med_wins"
    def test_med_win(self):
        assert self.game.stat_manager.num_med_wins == self.generateDifficultyWinTest('medium', 1000)

    # TEST: Ensure wins on hard increment "num_hard_wins"
    def test_hard_wins(self):
        assert self.game.stat_manager.num_hard_wins == self.generateDifficultyWinTest('hard', 1000)

    # Helpers
    def generateDifficultiesList(self, amount: int):
        return [random.choice(self.difficulties) for _ in range(amount)]

    def generateDifficultyWinTest(self, difficultyToCheck: str, iteration_count: int):
        num_diff_wins = 0
        rand_diffs = self.generateDifficultiesList(iteration_count)

        for difficulty in rand_diffs:
            self.game.setDifficulty(difficulty)
            self.game.win()
            if difficulty == difficultyToCheck:
                num_diff_wins += 1

        return num_diff_wins
