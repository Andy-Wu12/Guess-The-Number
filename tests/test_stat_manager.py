import os.path
import pytest
import json

from game import Game
from stat_manager import StatManager

def get_stat_data(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as f:
        stat_data = json.load(f)
    f.close()

    return stat_data

class TestSaves:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        # Setup code needed before tests run
        self.game = Game()
        self.stat_manager = StatManager()
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

    # TEST: Ensure saving stats works properly.
    # Additional tests can be added to check for updated stats, but it can get redundant
    def test_saving_default__data(self):
        self.game.saveGameStats()
        stat_data = get_stat_data(self.game.SAVEFILE_NAME)
        assert stat_data == self.stat_manager.__dict__
