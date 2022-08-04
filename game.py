# Built-in modules
from random import randint
from json import JSONDecodeError
import sys
import os.path

# Custom modules
from stat_manager import StatManager
from bot import GuessBot
import util
import game_exceptions


class Game:
    def __init__(self, stat_manager: StatManager, difficulty: str = 'easy',
                 range_start: int = 1, range_end: int = 10, chances: int = 5):
        # Config
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
            6: "Simulate Optimal Game",
            9: "Quit"
        }

        self.stat_manager = stat_manager

    def run(self):
        while True:
            self.printMenu()
            user_in = input("Please select an option from above: ")
            try:
                option_key = int(user_in)
                self.handleMenuChoice(option_key)
            except (ValueError, game_exceptions.OutOfRangeError):
                print("You did not enter a valid option. Please try again.\n")
                continue

    def printMenu(self):
        menu_str = ''
        for key, option in self.menu_options.items():
            # Remove load option if save is invalid or doesn't exist
            if not self.HAS_SAVE and option == "Load save data":
                continue
            menu_str += f"{key} -- {option}\n"

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
            except FileNotFoundError:
                print("No save file found!")
            except (JSONDecodeError, game_exceptions.InvalidSaveFormatError):
                print("Error loading save file!")
                print("Make a new one by saving or completing a game!")
                self.HAS_SAVE = False
        elif menu_choice == 4:
            self.stat_manager.pretty_print()
        elif menu_choice == 5:
            difficulty_mess = "Enter difficulty (easy, medium, hard): "
            self.changeDifficulty(input(difficulty_mess))
        elif menu_choice == 6:
            try:
                start_mess = "Enter the lowest value for the sim: "
                end_mess = "Enter the highest value for the sim: "
                start_num = int(input(start_mess))
                end_num = int(input(end_mess))
                # New line to reduce statement cluster
                print()
                if start_num >= end_num:
                    raise game_exceptions.InvalidRangeError
                runOptimalSim(start_num, end_num)
            except ValueError:
                print("Both inputs need to be numbers! Try again.")
            except game_exceptions.InvalidRangeError:
                print("Cannot simulate between the given range of numbers!")
                print("The starting number must be less than the end!\n")
        elif menu_choice == 9:
            stopGame()
        else:
            raise game_exceptions.OutOfRangeError

    def playGame(self):
        lower_guesses = []
        higher_guesses = []

        lowest_num = self.ANSWER_RANGE_START
        highest_num = self.ANSWER_RANGE_END

        answer = randint(lowest_num, highest_num)
        tries_left = self.STARTING_CHANCES

        while True:
            if tries_left < self.STARTING_CHANCES:
                self.printGuessHistory(
                    tries_left, lower_guesses, higher_guesses
                )
            input_mess = f"Enter a number between " \
                         f"{lowest_num} and {highest_num}, inclusive: "
            guess_str = input(input_mess)
            try:
                guess_int = int(guess_str)
                # Handle error where user guesses that cannot be correct
                if self.isOutOfRange(guess_int):
                    raise game_exceptions.OutOfRangeError
            except (ValueError, game_exceptions.OutOfRangeError):
                print("You did not enter an integer in the given range!")
                continue

            self.stat_manager.num_guesses += 1

            if isCorrectGuess(guess_int, answer):
                self.handleCorrectGuess(tries_left)
                break

            if guess_int > answer:
                print("Your guess was higher than the answer.\n")
                higher_guesses.append(guess_int)
            else:
                print("Your guess was lower than the answer.\n")
                lower_guesses.append(guess_int)

            tries_left -= 1

            if tries_left == 0:
                self.lose()
                print("You are out of guesses.")
                break

        print(f"The number was {answer}. Thanks for playing!")
        # Automatically save stats after every completed game
        self.saveGameStats()

    def printGuessHistory(self, chances_left, lower_list, higher_list):
        num_guesses = self.STARTING_CHANCES - chances_left
        if num_guesses > 1:
            print(f"In {num_guesses} guesses you have tried: ")
        else:
            print(f"In {num_guesses} guess you have tried: ")

        print(f"Lower: {lower_list}")
        print(f"Higher: {higher_list}")

        print(f"Guesses remaining: {chances_left}\n")

    def saveGameStats(self):
        self.stat_manager.save(self.SAVEFILE_NAME)
        self.HAS_SAVE = True

    def firstGuessWin(self):
        self.stat_manager.num_first_correct += 1
        self.win()

    def handleCorrectGuess(self, chances_left):
        if chances_left == self.STARTING_CHANCES:
            print("You guessed it on the first try!")
            self.firstGuessWin()
        else:
            print("You guessed it!")
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

    def isOutOfRange(self, guess: int):
        lower_bound = self.ANSWER_RANGE_START
        upper_bound = self.ANSWER_RANGE_END
        if guess < lower_bound or guess > upper_bound:
            raise False


def stopGame():
    print("Exiting program...")
    sys.exit()


def isCorrectGuess(guess: int, answer: int):
    if guess == answer:
        return True

    return False


def runOptimalSim(start_num: int, end_num: int):
    bot = GuessBot(start_num, end_num)
    answer = randint(start_num, end_num)
    print(f"The bot is looking for {answer}.")
    bot_guess = bot.getNextGuess()
    num_guesses = 1
    guesses = [bot_guess]

    while bot_guess != answer:
        if bot_guess > answer:
            bot.setUpperBound(bot_guess - 1)
        else:
            bot.setLowerBound(bot_guess + 1)

        bot_guess = bot.getNextGuess()
        num_guesses += 1
        guesses.append(bot_guess)

    print(f"The bot guessed the correct answer in {num_guesses} guesses.\n")
    print(f"It's guess order is: {guesses}\n")


if __name__ == "__main__":
    game = Game(StatManager())
    game.run()
