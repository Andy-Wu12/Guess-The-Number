import json

import util
import GameExceptions

varNameToStatName = {
        "wins": "Games Won",
        "losses": "Games Lost",
        "num_guesses": "Total # of valid guesses",
        "num_first_correct": "Number of correct first guesses",
        "num_easy_wins": "Wins on easy mode",
        "num_med_wins": "Wins on medium mode",
        "num_hard_wins": "Wins on hard mode"
    }

class StatManager:
    def __init__(self):
        # Counters
        self.wins = 0
        self.losses = 0
        self.num_guesses = 0
        self.num_first_correct = 0
        self.num_easy_wins = 0
        self.num_med_wins = 0
        self.num_hard_wins = 0

    def __str__(self):
        return "\n".join(f"{stat}: {value}" for stat, value in self.__dict__.items())

    def to_json(self):
        return self.__dict__

    def pretty_print(self):
        print("\nYour game statistics")
        util.printWithBorder("\n".join(f"{varNameToStatName[stat]}: {value}" for stat, value in self.__dict__.items()))

    def save(self, filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_json(), f, indent=2)
        f.close()
        print("Save successful!")

    def load(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                stat_data = json.loads(f.read())
            f.close()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise e

        # Don't depend on current StatManager object. Create fresh instance and compare keys and value types with it
        if not isValidDict(StatManager().__dict__, stat_data):
            raise GameExceptions.InvalidSaveFormatError

        self.__dict__ = stat_data
        print("Load successful!")
        return True


def isValidDict(desired_dict, dict_to_check):
    # JSON in file, but does not contain the necessary stats required by StatManager
    for key, value in desired_dict.items():
        if key not in dict_to_check:
            return False
        # Stat value is the incorrect type
        if not isinstance(dict_to_check[key], type(value)):
            return False

    return True
