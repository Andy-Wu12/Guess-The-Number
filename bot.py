
class GuessBot:
    def __init__(self, starting_lower_bound: int, starting_upper_bound: int):
        self.lower_bound = starting_lower_bound
        self.upper_bound = starting_upper_bound

    def setUpperBound(self, new_upper: int):
        self.upper_bound = new_upper

    def setLowerBound(self, new_lower: int):
        self.lower_bound = new_lower

    def getNextGuess(self):
        return self.upper_bound // 2

    def __str__(self):
        return f"Bot guessing in the range of {self.lower_bound} to {self.upper_bound}"
