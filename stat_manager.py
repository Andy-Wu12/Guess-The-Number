import json

import util

varNameToStatName = {
        "wins": "Games Won",
        "losses": "Games Lost",
        "num_guesses": "Total # of valid guesses",
        "num_first_correct": "Number of correct first guesses",
        "fastest_win_in_turns": "Lowest # of tries used to win",
        "slowest_win_in_turns": "Highest # of tries used to win",
        "highest_difficulty_win": "Highest difficulty beaten",
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

        # Miscellaneous
        self.fastest_win_in_turns = -1
        self.slowest_win_in_turns = -1
        self.highest_difficulty_win = ""
        self.num_easy_wins = 0
        self.num_med_wins = 0
        self.num_hard_wins = 0

    def __str__(self):
        return "\n".join(f"{stat}: {value}" for stat, value in self.__dict__.items())

    def toJson(self):
        return self.__dict__

    def prettyPrint(self):
        print("\nYour game statistics")
        util.printWithBorder("\n".join(f"{varNameToStatName[stat]}: {value}" for stat, value in self.__dict__.items()))

    def save(self):
        with open("persistent", "w") as f:
            json.dump(self.toJson(), f, indent=2)
        print("Save successful!")

    def load(self):
        try:
            with open("persistent", "r") as f:
                stat_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error in loading save file! Make sure to save or play a game first before attempting to load!")
            return

        self.__dict__ = stat_data
        print("Load successful!")



