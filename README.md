# Guess-The-Number ![picture](https://api.codiga.io/project/34133/score/svg) ![picture](https://api.codiga.io/project/34133/status/svg)
A command-line game where the player has to guess a randomly generated number in a given range with limited tries.


## Features
All the listed features are available from the in-game menu on startup.
### Play game
  - Start a new game on the currently set difficulty level (default 'easy').
### Difficulty levels (easy, medium, hard)
  - A higher difficulty increases the range that the generated number falls into, 
  while you only get a slight increase to your number of guesses.
### Statistics History
  - View various statistics regarding your game history such as number of wins and losses, guesses, etc.
### Simulate optimal playthroughs
  - Choose your own range for the generated number and get visual feedback for how the computer plays.
###  Save / Load statistics
  - Save your statistics before quitting so that you can load them in the next time the program is started.
  - Saves are made automatically after every game played, so manually saving is not entirely necessary.
    - Manually saving before loading your file on startup can be a way to reset your progress, should you choose to do so.
    
## Dependencies
- You will need at least [Python 3.7](https://www.python.org/downloads/) to run this program.
- If you want to create and / or run tests, you will also need the pytest module. <br>
  - You can install it via command-line with `pip3 install -U pytest`

## How to run
1. Download the game.py file onto your machine.
2. cd into the directory where the file was downloaded.
3. Run the command `python3 game.py`
