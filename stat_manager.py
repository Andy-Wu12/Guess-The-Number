import json

import util

class StatManager:
    def __init__(self):
        # Counters
        self.wins = 0
        self.losses = 0
        self.num_guesses = 0
        self.num_first_guesses_correct = 0

        # Miscellaneous
        self.fastest_win_in_turns = -1
        self.slowest_win_in_turns = -1
        self.highest_difficulty_beaten = ""
        self.num_easy_wins = 0
        self.num_med_wins = 0
        self.num_hard_wins = 0

    def __str__(self):
        return "\n".join(f"{stat}: {value}" for stat, value in self.__dict__.items())

    def prettyPrint(self):
        print("\nYour game statistics")
        util.printWithBorder(self.__str__())

    def save(self):
        pass

    def load(self):
        pass

