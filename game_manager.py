from os.path import exists

class GameManager:
    def __init__(self, range_start: int = 1, range_end: int = 10, chances: int = 5):
        self.ANSWER_RANGE_START = range_start
        self.ANSWER_RANGE_END = range_end
        self.STARTING_CHANCES = chances
        self.HAS_SAVE = exists("./persistent")

        self.menu_options = {
            1: "Play",
            2: "Save data (Creates local file in game directory)",
            3: "Load save data",
            4: "Statistics",
            9: "Quit"
        }

    def updateRange(self, start: int, end: int):
        self.ANSWER_RANGE_START = start
        self.ANSWER_RANGE_END = end

    def updateChances(self, chances: int):
        self.STARTING_CHANCES = chances
