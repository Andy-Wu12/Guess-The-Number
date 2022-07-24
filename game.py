from random import randint

import util
import stat_manager
import GameExceptions

# Global vars -- can be moved to some sort of config file
ANSWER_RANGE_START = 1
ANSWER_RANGE_END = 10
STARTING_TRIES = 5

menu_options = {
        1: "Play",
        2: "Save data (Creates local file in game directory)",
        3: "Load save data",
        4: "Statistics",
        9: "Quit"
    }

def run():
    manager = stat_manager.StatManager()

    while True:
        printMenu()
        user_in = input("Please select an option from above: ")
        try:
            option_key = int(user_in)
            handleMenuChoice(option_key, manager)
        except (ValueError, GameExceptions.OutOfRangeError):
            print("You did not enter a valid option. Please try again.\n")
            continue

def printMenu():
    menu_str = ("\n".join(f"{key} -- {option}" for key, option in menu_options.items()))

    util.printWithBorder(menu_str.strip())

def handleMenuChoice(menu_choice: int, manager: stat_manager):
    if menu_choice == 1:
        playGame(ANSWER_RANGE_START, ANSWER_RANGE_END, manager)
    elif menu_choice == 2:
        print("Saving data...")
        manager.save()
    elif menu_choice == 3:
        manager.load()
    elif menu_choice == 4:
        manager.prettyPrint()
    elif menu_choice == 9:
        print("Exiting program...")
        exit(0)
    else:
        raise GameExceptions.OutOfRangeError

def playGame(lowest_num: int, highest_num: int, manager: stat_manager):
    answer = randint(lowest_num, highest_num)
    tries_left = STARTING_TRIES

    while True:
        print(f"You have {tries_left} guesses remaining\n")
        guess_str = input(f"Enter a number between {lowest_num} and {highest_num}, inclusive: ")
        try:
            guess_int = int(guess_str)
            # Make it easier for user by handling error where they enter a number that the answer cannot possibly be
            if guess_int < ANSWER_RANGE_START or guess_int > ANSWER_RANGE_END:
                raise GameExceptions.OutOfRangeError
        except (ValueError, GameExceptions.OutOfRangeError):
            print("You did not enter an integer in the given range!")
            continue

        manager.num_guesses += 1
        if guess_int == answer:
            print(f"You guessed it! The number was {answer}.")
            manager.wins += 1
            break
        elif guess_int > answer:
            print(f"Your guess was higher than the answer.\n")
            tries_left -= 1
        else:
            print(f"Your guess was lower than the answer.\n")
            tries_left -= 1

        if tries_left == 0:
            manager.losses += 1
            print("You are out of guesses.")
            break

    print(f"Thanks for playing. Returning to menu..")
    # Automatically save stats after every completed game, otherwise user must do it manually
    manager.save()

if __name__ == "__main__":
    run()




