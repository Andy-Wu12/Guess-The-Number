import os.path
import random

import pytest
import json

import GameExceptions
from stat_manager import StatManager

TEMP_DIR_NAME = "test_root"

BAD_JSON = {'randomField': 'hi', 'secondField': 'world'}
GOOD_JSON = StatManager().__dict__
NO_JSON = "random text that isn't json"
MALFORMED_GOOD_JSON = StatManager().__dict__

for key, value in MALFORMED_GOOD_JSON.items():
    MALFORMED_GOOD_JSON[key] = "this is not an int!"

BAD_JSON_NAME = "bad_json.txt"
GOOD_JSON_NAME = "good_json.txt"
MALFORMED_GOOD_JSON_NAME = "partial_good_json.txt"
NO_JSON_NAME = "no_json.txt"


def get_stat_data(filename: str) -> dict:
    with open(filename, "r", encoding="utf-8") as f:
        stat_data = json.load(f)
    f.close()

    return stat_data

@pytest.fixture(scope="session")
def test_files(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp(TEMP_DIR_NAME, numbered=False)
    bad_json_file = temp_dir / BAD_JSON_NAME
    bad_json_file.write_text(json.dumps(BAD_JSON))
    good_json_file = temp_dir / GOOD_JSON_NAME
    good_json_file.write_text(json.dumps(GOOD_JSON))
    malformed_json_file = temp_dir / MALFORMED_GOOD_JSON_NAME
    malformed_json_file.write_text(json.dumps(MALFORMED_GOOD_JSON))
    no_json = temp_dir / NO_JSON_NAME
    no_json.write_text(NO_JSON)
    # Return path to base of temp directory in case it is needed
    return tmp_path_factory.getbasetemp()

def getFilePath(filenameWithoutPath: str, pathFromTMPFactory):
    return f"{pathFromTMPFactory}/{TEMP_DIR_NAME}/{filenameWithoutPath}"


class TestStatManager:
    @pytest.fixture(autouse=True, scope='function')
    def setup(self, test_files):
        # Setup code needed before tests run
        self.stat_manager = StatManager()

    # TEST: Ensure requested filename should load if it contains properly formatted JSON with correct value types
    def test_valid_filename_load(self, test_files):
        try:
            assert self.stat_manager.load(getFilePath(GOOD_JSON_NAME, test_files))
        except Exception:
            assert False

    # TEST: Ensure exception is raised if desired file does not contain JSON
    def test_file_no_json(self, test_files):
        with pytest.raises(json.JSONDecodeError):
            self.stat_manager.load(getFilePath(NO_JSON_NAME, test_files))

    # TEST: Ensure error thrown if filename not found
    def test_invalid_filename_load(self, test_files):
        with pytest.raises(FileNotFoundError):
            self.stat_manager.load(getFilePath("random_file_name.txt", test_files))

    # TEST: Ensure filenames are handled in a CASE-SENSITIVE way by StatManager
    def test_case_sensitive_load(self, tmp_path):
        # Make temporary directory to store persistent file
        d = tmp_path / "test_dir"
        d.mkdir()
        new_file_name = "Test.json"
        new_file = d / new_file_name
        new_file.write_text(json.dumps(GOOD_JSON))
        assert os.path.exists(f"{d}/{new_file_name}")
        with pytest.raises(FileNotFoundError):
            self.stat_manager.load(getFilePath(new_file_name.upper(), d))

    # TEST: Ensure method success if JSON document provides the necessary stats for StatsManager
    def test_file_correct_stats(self, test_files):
        required_keys = self.stat_manager.__dict__.keys()
        assert self.stat_manager.load(getFilePath(GOOD_JSON_NAME, test_files))

        for stat_key in required_keys:
            assert stat_key in self.stat_manager.__dict__

    # TEST: Ensure actual loaded values are what should have been saved after arbitray amount of games, wins, etc.
    def test_file_correct_stat_values(self, test_files):
        stat_vars = list(self.stat_manager.__dict__.keys())
        num_iterations = 5000

        for i in range(num_iterations):
            rand_key_idx = random.randint(0, len(stat_vars) - 1)
            rand_value = random.randint(0, 10000)
            self.stat_manager.__dict__[stat_vars[rand_key_idx]] = rand_value

        correct_vars = self.stat_manager.__dict__
        self.stat_manager.save(getFilePath('persistent', test_files))

        # Create new stat_manager and ensure loaded vars contain the correct value
        test_sm = StatManager()
        test_sm.load(getFilePath('persistent', test_files))
        assert correct_vars == test_sm.__dict__

    # TEST: Ensure exception is thrown if JSON document does not provide necessary stats
    def test_file_incorrect_stat_keys(self, test_files):
        with pytest.raises(GameExceptions.InvalidSaveFormatError):
            self.stat_manager.load(getFilePath(BAD_JSON_NAME, test_files))

    # TEST: Ensure exception is thrown if JSON document has correct stat keys, but incorrect data types for the values
    def test_file_invalid_stat_values(self, test_files):
        with pytest.raises(GameExceptions.InvalidSaveFormatError):
            self.stat_manager.load(getFilePath(MALFORMED_GOOD_JSON_NAME, test_files))
