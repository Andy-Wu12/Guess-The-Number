import game
import game_manager
import stat_manager

import os.path

class TestSaves:
    # Ensure persistent file exists after saving
    def test_save(self):
        gm = game_manager.GameManager()
        sm = stat_manager.StatManager()

        game.saveGameStats(gm, sm)
        assert os.path.exists("./persistent")
