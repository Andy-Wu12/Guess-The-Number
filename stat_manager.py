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
        self.slowest_win = -1
        self.highest_difficulty_beaten = -1
        self.num_easy_wins = 0
        self.num_med_wins = 0
        self.num_hard_wins = 0

    def __str__(self):
        pass

    def save(self):
        pass

    def load(self):
        pass

