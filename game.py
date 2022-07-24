# Built-in modules
from random import randint
import sys

# Custom modules
from stat_manager import StatManager
from game_manager import GameManager
import util
import GameExceptions

def run():
    stat_mngr = StatManager()
    game_mngr = GameManager()

    while True:
        printMenu(game_mngr)
        user_in = input("Please select an option from above: ")
        try:
            option_key = int(user_in)
            handleMenuChoice(option_key, game_mngr, stat_mngr)
        except (ValueError, GameExceptions.OutOfRangeError):
            print("You did not enter a valid option. Please try again.\n")
            continue

def printMenu(gm: GameManager):
    if gm.HAS_SAVE:
        menu_str = ("\n".join(f"{key} -- {option}" for key, option in gm.menu_options.items()))
    # Disable load option in menu
    else:
        menu_str = ("\n".join(
            f"{key} -- {option}" for key, option in gm.menu_options.items() if option != "Load save data")
        )

    util.printWithBorder(menu_str.strip())

def handleMenuChoice(menu_choice: int, gm: GameManager, sm: StatManager):
    if menu_choice == 1:
        playGame(gm, sm)
    elif menu_choice == 2:
        print("Saving data...")
        saveGameStats(gm, sm)
    elif menu_choice == 3 and gm.HAS_SAVE:
        sm.load()
    elif menu_choice == 4:
        sm.prettyPrint()
    elif menu_choice == 9:
        print("Exiting program...")
        sys.exit()
    else:
        raise GameExceptions.OutOfRangeError

def playGame(gm: GameManager, sm: StatManager):
    lowest_num = gm.ANSWER_RANGE_START
    highest_num = gm.ANSWER_RANGE_END

    answer = randint(lowest_num, highest_num)
    tries_left = gm.STARTING_CHANCES

    while True:
        print(f"You have {tries_left} guesses remaining\n")
        guess_str = input(f"Enter a number between {lowest_num} and {highest_num}, inclusive: ")
        try:
            guess_int = int(guess_str)
            # Make it easier for user by handling error where they enter a number that the answer cannot possibly be
            if guess_int < gm.ANSWER_RANGE_START or guess_int > gm.ANSWER_RANGE_END:
                raise GameExceptions.OutOfRangeError
        except (ValueError, GameExceptions.OutOfRangeError):
            print("You did not enter an integer in the given range!")
            continue

        sm.num_guesses += 1
        if guess_int == answer:
            print(f"You guessed it! The number was {answer}.")
            sm.wins += 1
        elif guess_int > answer:
            print("Your guess was higher than the answer.\n")
            tries_left -= 1
        else:
            print("Your guess was lower than the answer.\n")
            tries_left -= 1

        if tries_left == 0:
            sm.losses += 1
            print("You are out of guesses.")

    print("Thanks for playing. Returning to menu..")
    # Automatically save stats after every completed game, otherwise user must do it manually
    saveGameStats(gm, sm)

def saveGameStats(gm: GameManager, sm: StatManager):
    sm.save()
    gm.HAS_SAVE = True

if __name__ == "__main__":
    run()
