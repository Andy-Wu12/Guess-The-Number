import os.path

import pytest

from game import Game
from stat_manager import StatManager

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

