# Wordle Solver
[![Visits Badge](https://badges.pufler.dev/visits/bellerb/wordle_solver)](#)
[![Languages](https://img.shields.io/github/languages/count/bellerb/wordle_solver?style=flat-square
)](#)
[![Top Languages](https://img.shields.io/github/languages/top/bellerb/wordle_solver?style=flat-square
)](#)

### Description
The following is a program for playing Wordle in the console written in python3. When playing, the game will give you 3 options:

* Test Solver [T]
* Game Assist [A]
* Play Game [P]

#### Test Solver
The test solver option can be selected by typing in a "T". This will run the solver for how ever many games you have set up in the main.py file. To change this change the following variable.
```
GAMES = 10 
```

#### Game Assist
The game assist option is a way to have it help you choose your words when playing on the actual game. To play type in the suggested words. The agent will then ask you for what the game returned as hints. The agent will be looking for a responce like "bbygb". For this the options are:

* b = black/grey
* y = yellow
* g = green

#### Play Game
The play game option is a way to play wordle games in your console.

# Launch Instructions
step 1: open your console <br>
step 2: create a virtual enviroment <br>
step 3: type the following command "pip install -r requirements.txt"<br>
step 4: type the following command "cd [app directory]" <br>
step 5: type the following command "python3 main.py" <br>
step 6: type in the action you wish to perform.

# Write Up
To get a better understanding of why the code is written this way check out my detailed write up:

* https://medium.com/@bellerb/wordle-solver-using-python-3-3c3bccd3b4fb

## Reference
* https://github.com/dwyl/english-words
