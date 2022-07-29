# Built-in modules
from random import randint
import sys
import os.path
from json import JSONDecodeError

# Custom modules
from stat_manager import StatManager
import util
import GameExceptions

class Game:
    def __init__(self, difficulty: str = 'easy', range_start: int = 1, range_end: int = 10, chances: int = 5):
        self.ANSWER_RANGE_START = range_start
        self.ANSWER_RANGE_END = range_end
        self.STARTING_CHANCES = chances
        self.SAVEFILE_NAME = "./persistent"
        self.HAS_SAVE = os.path.exists(self.SAVEFILE_NAME)
        self.DIFFICULTY = difficulty

        self.menu_options = {
            1: "Play",
            2: "Save data (Creates local file in game directory)",
            3: "Load save data",
            4: "Statistics",
            5: "Choose difficulty",
            9: "Quit"
        }
        self.stat_manager = StatManager()

    def run(self):
        while True:
            self.printMenu()
            user_in = input("Please select an option from above: ")
            try:
                option_key = int(user_in)
                self.handleMenuChoice(option_key)
            except (ValueError, GameExceptions.OutOfRangeError):
                print("You did not enter a valid option. Please try again.\n")
                continue

    def printMenu(self):
        if self.HAS_SAVE:
            menu_str = ("\n".join(f"{key} -- {option}" for key, option in self.menu_options.items()))
        # Disable load option in menu
        else:
            menu_str = ("\n".join(
                f"{key} -- {option}" for key, option in self.menu_options.items() if option != "Load save data")
            )

        util.printWithBorder(menu_str.strip())

    def handleMenuChoice(self, menu_choice: int):
        if menu_choice == 1:
            self.playGame()
        elif menu_choice == 2:
            print("Saving data...")
            self.saveGameStats()
        elif menu_choice == 3 and self.HAS_SAVE:
            try:
                self.stat_manager.load(self.SAVEFILE_NAME)
            except (FileNotFoundError, JSONDecodeError, GameExceptions.InvalidSaveFormatError):
                print("Error loading save file!")
                print("Complete a game or use the save option to generate a new save file!")
                self.HAS_SAVE = False
        elif menu_choice == 4:
            self.stat_manager.pretty_print()
        elif menu_choice == 5:
            self.changeDifficulty(input("Enter difficulty (easy, medium, hard): "))
        elif menu_choice == 9:
            self.stopGame()
        else:
            raise GameExceptions.OutOfRangeError

    def playGame(self):
        lowest_num = self.ANSWER_RANGE_START
        highest_num = self.ANSWER_RANGE_END

        answer = randint(lowest_num, highest_num)
        tries_left = self.STARTING_CHANCES

        while True:
            print(f"You have {tries_left} guesses remaining\n")
            guess_str = input(f"Enter a number between {lowest_num} and {highest_num}, inclusive: ")
            try:
                guess_int = int(guess_str)
                # Make it easier for user by handling error where they enter a number that the answer cannot possibly be
                if guess_int < self.ANSWER_RANGE_START or guess_int > self.ANSWER_RANGE_END:
                    raise GameExceptions.OutOfRangeError
            except (ValueError, GameExceptions.OutOfRangeError):
                print("You did not enter an integer in the given range!")
                continue

            self.stat_manager.num_guesses += 1
            if guess_int == answer:
                if tries_left:
                    print("You guessed it on the first try!")
                    self.firstGuessWin()
                else:
                    print("You guessed it!")
                    self.win()
                break
            if guess_int > answer:
                print("Your guess was higher than the answer.\n")
                tries_left -= 1
                print(self.STARTING_CHANCES)
            else:
                print("Your guess was lower than the answer.\n")
                tries_left -= 1

            if tries_left == 0:
                self.lose()
                print("You are out of guesses.")
                break

        print(f"The number was {answer}. Thanks for playing!")
        # Automatically save stats after every completed game, otherwise user must do it manually
        self.saveGameStats()

    def saveGameStats(self):
        self.stat_manager.save(self.SAVEFILE_NAME)
        self.HAS_SAVE = True

    def firstGuessWin(self):
        self.stat_manager.num_first_correct += 1
        self.win()

    def win(self):
        self.stat_manager.wins += 1
        if self.DIFFICULTY == 'easy':
            self.stat_manager.num_easy_wins += 1
        elif self.DIFFICULTY == 'medium':
            self.stat_manager.num_med_wins += 1
        else:
            self.stat_manager.num_hard_wins += 1

    def lose(self):
        self.stat_manager.losses += 1

    def changeDifficulty(self, difficulty: str):
        if difficulty in ['easy', 'medium', 'hard']:
            self.setDifficulty(difficulty)
            print(f"Difficulty has been set to {self.DIFFICULTY}")
            print(f"This mode gives you {self.STARTING_CHANCES} chances")
        else:
            print("Invalid difficulty level entered!")

    def setDifficulty(self, difficulty: str):
        if difficulty == 'easy':
            self.DIFFICULTY = 'easy'
            self.setGenerateStartEnd(1, 10)
            self.STARTING_CHANCES = 5
        elif difficulty == 'medium':
            self.DIFFICULTY = 'medium'
            self.setGenerateStartEnd(1, 100)
            self.STARTING_CHANCES = 7
        elif difficulty == 'hard':
            self.DIFFICULTY = 'hard'
            self.setGenerateStartEnd(1, 1000)
            self.STARTING_CHANCES = 10

    def setGenerateStartEnd(self, start, end):
        self.ANSWER_RANGE_START = start
        self.ANSWER_RANGE_END = end

    @staticmethod
    def stopGame():
        print("Exiting program...")
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
