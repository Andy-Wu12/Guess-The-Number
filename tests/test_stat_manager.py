import pytest
import json

from stat_manager import StatManager

def get_stat_data(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as f:
        stat_data = json.load(f)
    f.close()

    return stat_data

BAD_JSON = {'randomField': 'hi', 'secondField': 'world'}
GOOD_JSON = StatManager().__dict__
NO_JSON = "random text that isn't json"

def create_test_files(tmp_path):
    temp_dir = tmp_path / "test_root"
    temp_dir.mkdir()
    bad_json_file = temp_dir / "bad_json.txt"
    bad_json_file.write_text(json.dumps(BAD_JSON))
    good_json_file = temp_dir / "good_json.txt"
    good_json_file.write_text(json.dumps(GOOD_JSON))
    no_json = temp_dir / "no_json.txt"
    no_json.write_text(NO_JSON)

class TestStatManager:
    @pytest.fixture(autouse=True, scope='function')
    def setup(self, tmp_path):
        # Setup code needed before tests run
        self.stat_manager = StatManager()
        create_test_files(tmp_path)

    # TEST: Ensure requested filename should load if it contains JSON
    def test_valid_filename_load(self):
        pass

    # TEST: Ensure error thrown if filename not found
    def test_invalid_filename_load(self):
        pass

    # TEST: StatManager should handle exception where save file does not contain JSON
    def test_file_no_json(self):
        pass

    # TEST: Ensure JSON document provides all the necessary stats for StatsManager
    def test_file_bad_json(self):
        pass
