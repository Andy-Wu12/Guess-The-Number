from random import randint

import GameExceptions

ANSWER_RANGE_START = 1
ANSWER_RANGE_END = 10
STARTING_TRIES = 5

menu_options = {
        1: "Play",
        2: "Save data (Creates local file in game directory)",
        3: "Load save data",
        4: "Quit"
    }

def run():
    while True:
        printMenu()
        user_in = input("Please select an option from above: ")
        try:
            option_key = int(user_in)
            handleMenuChoice(option_key)
        except (ValueError, GameExceptions.OutOfRangeError):
            print("You did not enter a valid option. Please try again.")
            continue

def printMenu():
    print("\n----------------------------------------------------")
    print("----------------------------------------------------")
    for key, option in menu_options.items():
        print(f"{key} -- {option}")
    print("----------------------------------------------------")
    print("----------------------------------------------------\n")

def handleMenuChoice(menu_choice: int):
    if menu_choice == 1:
        playGame(ANSWER_RANGE_START, ANSWER_RANGE_END)
    elif menu_choice == 2:
        print("Saving is still in development. Check back later!")
    elif menu_choice == 3:
        print("Loading is still in development. Check back later!")
    elif menu_choice == 4:
        print("Exiting program...")
        exit(0)
    else:
        raise GameExceptions.OutOfRangeError

def playGame(lowest_num: int, highest_num: int):
    answer = randint(lowest_num, highest_num)
    tries_left = STARTING_TRIES
    game_over = False

    while not game_over:
        guess_str = input(f"Enter a number between {lowest_num} and {highest_num}, inclusive: ")
        try:
            guess_int = int(guess_str)
            if guess_int < ANSWER_RANGE_START or guess_int > ANSWER_RANGE_END:
                raise GameExceptions.OutOfRangeError
        # Don't handle issue of user guessing a number out of range, as that is part of the game.
        except (ValueError, GameExceptions.OutOfRangeError):
            print("You did not enter an integer in the given range!")
            continue

        if guess_int == answer:
            print(f"You guessed it! The number was {answer}.")
            game_over = True
        elif guess_int > answer:
            print(f"Your guess was higher than the answer.")
            tries_left -= 1
        else:
            print(f"Your guess was lower than the answer.")
            tries_left -= 1

    print(f"Thanks for playing")

if __name__ == "__main__":
    run()




