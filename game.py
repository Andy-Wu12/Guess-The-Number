from random import randint

# TODO: Create menu options to allow for difficulty levels with higher value ranges
ANSWER_RANGE_START = 1
ANSWER_RANGE_END = 10
STARTING_TRIES = 5

def play(lowest_num, highest_num):
    answer = randint(lowest_num, highest_num)
    tries_left = STARTING_TRIES
    game_over = False

    while not game_over:
        guess_str = input(f"Enter a number between {lowest_num} and {highest_num}, inclusive: ")
        try:
            guess_int = int(guess_str)

        # Don't handle issue of user guessing a number out of range, as that is part of the game.
        except ValueError:
            print("You did not enter an integer.")
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
    play(ANSWER_RANGE_START, ANSWER_RANGE_END)





