import numpy as np
import pandas as pd

import random

class Wordle:
    def __init__(self, word, rows=6, letters=5):
        self.g_count = 0
        self.word = word
        self.rows = rows
        self.letters = letters
        self.board = [['' for _ in range(letters)] for _ in range(rows)]
        self.colours = [['' for _ in range(letters)] for _ in range(rows)]
        self.alph = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    def is_end(self):
        if self.board[-1] != ['','','','','']:
            return True
        else:
            r = self.game_result()
            if r[0] == True:
                return True
            else:
                return False

    def game_result(self):
        win = (False, 0)
        for i, r in enumerate(self.board):
            if self.word == ''.join(r):
                win = (True, i)
                break
        return win

    def update_board(self, u_inp):
        for i, s in enumerate(str(u_inp).upper()):
            self.board[self.g_count][i] = s
            if self.word[i] == s:
                self.colours[self.g_count][i] = 'G' #Correct place and letter
            elif s in word:
                self.colours[self.g_count][i] = 'Y' #Wrong place but letter in word
            else:
                self.colours[self.g_count][i] = 'B' #Letter not in word
        print(f'\n{"".join(self.board[self.g_count])}\n{self.colours[self.g_count]}')
        self.g_count += 1

    def valid_guess(self, u_inp):
        if len(u_inp) == 5 and False not in [False for s in str(u_inp).upper() if s not in self.alph]:
            return True
        else:
            return False

class Agent:
    def __init__(self, game):
        self.vowels = 'A|E|I|O|U|Y'
        w_bank = pd.read_csv('5L-Words.csv')
        w_bank['words'] = w_bank['words'].str.upper() #Convert all words to uppercase
        #w_bank['v-count'] = w_bank['words'].str.count(self.vowels) #Count amount of vowels in words

        #w_bank['w-score'] = [1.] * len(w_bank)

        v_perc = {}
        for l in ['A','E','I','O','U','Y']:
            w_bank[f'{l}-count'] = w_bank['words'].str.count(l) #Count amount of vowels in words
            v_perc[l] = w_bank[f'{l}-count'].sum()/len(w_bank)
        w_bank['w-score'] = w_bank['A-count'] * v_perc['A']
        w_bank['w-score'] += w_bank['E-count'] * v_perc['E']
        w_bank['w-score'] += w_bank['I-count'] * v_perc['I']
        w_bank['w-score'] += w_bank['O-count'] * v_perc['O']
        w_bank['w-score'] += w_bank['U-count'] * v_perc['U']
        w_bank['w-score'] += w_bank['Y-count'] * v_perc['Y']

        l_pos = {}
        for x in range(5):
            l_pos[x] = w_bank['words'].str[x].value_counts(normalize=True).to_dict()

        for x in range(5):
            w_bank['w-score'] *= w_bank['words'].str[x].map(l_pos[x])

        '''
        l_pos = {}
        v_pos = {}
        w_count = len(w_bank)
        for x in range(5):
            l_pos[x] = w_bank['words'].str[x].value_counts().to_dict()
            v_prob = {}
            for l in ['A','E','I','O','U','Y']:
                v_prob[l] = l_pos[x][l]
            v_tot = sum(v_prob.values())
            v_pos[x] = {k: v / v_tot for k, v in v_prob.items()}
            l_pos[x] = {k: v / w_count if k not in v_pos[x] else v_pos[x][k] for k, v in l_pos[x].items()}

        for x in range(5):
            w_bank['w-score'] *= w_bank['words'].str[x].map(l_pos[x])
        '''

        print(w_bank)

        self.w_bank = w_bank
        self.game = game
        self.prediction = ['','','','','']
        self.y_letters = {}
        self.g_letters = []

    def parse_board(self):
        for y, r in enumerate(self.game.colours):
            if r == ['','','','','']:
                break
            else:
                for x, c in enumerate(r):
                    letter = self.game.board[y][x]
                    if c == 'Y':
                        if letter not in self.y_letters:
                            self.y_letters[letter] = [x]
                        else:
                            self.y_letters[letter].append(x)
                    elif c == 'G':
                        self.prediction[x] = letter
                    else:
                        if letter not in self.g_letters:
                            self.g_letters.append(letter)

    def choose_action(self):
        self.parse_board()
        if len(self.g_letters) > 0 and len(self.y_letters) > 0:
            self.w_bank = self.w_bank[(~self.w_bank['words'].str.contains('|'.join(self.g_letters)))&(self.w_bank['words'].str.contains('|'.join(list(self.y_letters.keys()))))]
            for s, p in self.y_letters.items():
                for i in p:
                    self.w_bank = self.w_bank[self.w_bank['words'].str[i]!=s]
            for i, s in enumerate(self.prediction):
                if s != '':
                    self.w_bank = self.w_bank[self.w_bank['words'].str[i]==s]
            self.y_letters = {}
            self.g_letters = []
        mv_bank = self.w_bank[self.w_bank['w-score']==self.w_bank['w-score'].max()] #Find max vowel words
        result = random.choice(mv_bank['words'].tolist())
        return result

word = 'HACKS'
#word = random.choice(w_bank['words'].tolist())
game = Wordle(word, rows=15)
bot = Agent(game)

while game.is_end() == False:
    #u_inp = input('\nPLEASE GUESS A 5 LETTER WORD\n')
    u_inp = bot.choose_action()
    if game.valid_guess(u_inp) == True:
        game.update_board(u_inp)
    else:
        print('ERROR - WORDS MUST BE 5 LETTERS')

r = game.game_result()
if r[0] == True:
    if r[1] > 0:
        print(f'\nCONGRATS YOU WON IN {r[1] + 1} GUESSES!\n')
    else:
        print(f'\nCONGRATS YOU WON IN {r[1] + 1} GUESS!\n')
else:
    print(f'\nSORRY YOU DID NOT WIN.\n')
print(np.array(game.board))
