import random
import numpy as np
import pandas as pd
from tqdm import tqdm

from bot import Agent
from wordle import Wordle

ROWS = 6
LETTERS = 5
GAMES = 10

w_bank = pd.read_csv('data/words.csv')
w_bank = w_bank[w_bank['words'].str.len()==LETTERS]
w_bank['words'] = w_bank['words'].str.upper() #Convert all words to uppercase

control = input('What would you like to do?\n\n-Test Solver [T]\n-Game Assist [A]\n-Play Game   [P]\n\n')
if 'T' in str(control).upper() or 'P' in str(control).upper():
    if 'P' in str(control).upper():
        print('PLAY GAME SELECTED\n---------------------')
    else:
        print('TEST SOLVER SELECTED\n---------------------\n')
    results = []
    if 'P' in str(control).upper():
        silent = True
        GAMES = 1
    else:
        silent = False
    for _ in tqdm(range(GAMES), desc='GAMES', disable=silent):
        word = random.choice(w_bank['words'].tolist())
        game = Wordle(
            word,
            rows=ROWS,
            letters=LETTERS
        )
        bot = Agent(game)
        while game.is_end() == False:
            if 'P' in str(control).upper():
                u_inp = input('\nPLEASE GUESS A 5 LETTER WORD\n')
            else:
                u_inp = bot.choose_action()
            if game.valid_guess(u_inp) == True:
                game.update_board(u_inp)
                if 'P' in str(control).upper():
                    print(game.colours[game.g_count-1])
            else:
                print('ERROR - WORDS MUST BE 5 LETTERS')
        r = game.game_result()
        if 'P' in str(control).upper():
            if r[0] == True:
                if r[1] > 0:
                    print(f'\nCONGRATS YOU WON IN {r[1] + 1} GUESSES!\n')
                else:
                    print(f'\nCONGRATS YOU WON IN {r[1] + 1} GUESS!\n')
            else:
                print(f'\nSORRY YOU DID NOT WIN.\n')
            print(np.array(game.board),'\n')
        results.append({'word':word,'result':r[0],'moves':r[1]+1})

    results = pd.DataFrame(results)
    print(results)
    print(f'Win Percent = {(len(results[results["result"]==True]) / len(results)) * 100}%\nAverage Moves = {results[results["result"]==True]["moves"].mean()}')
elif 'A' in str(control).upper():
    print('GAME ASSIST ACTIVATED\n---------------------')
    game = Wordle(
        None,
        rows=ROWS,
        letters=LETTERS
    )
    bot = Agent(game)
    for i in range(ROWS):
        guess = bot.choose_action()
        print(f'\nSuggested Word = {guess}\n')
        u_inp = input('What were the colours returned [ex. ybggy]?\n')
        game.colours[i] = [s for s in str(u_inp).upper()]
        game.board[i] = [s for s in str(guess).upper()]
        game.g_count += 1
        for x, s in enumerate(game.colours[i]):
            if s == 'Y':
                if guess[x] in bot.y_letters:
                    bot.y_letters[guess[x]].append(x)
                else:
                    bot.y_letters[guess[x]] = [x]
            elif s == 'B':
                if guess[x] in bot.g_letters:
                    bot.g_letters.append(guess[x])
            elif s == 'G':
                bot.prediction[x] = guess[x]
