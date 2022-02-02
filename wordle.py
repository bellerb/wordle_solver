from copy import deepcopy

class Wordle:
    def __init__(self, word, rows=6, letters=5):
        self.g_count = 0
        self.word = word
        self.w_hash_table = {}
        if word is not None:
            for l in word:
                if l in self.w_hash_table:
                    self.w_hash_table[l] += 1
                else:
                    self.w_hash_table[l] = 1
        self.rows = rows
        self.letters = letters
        self.board = [['' for _ in range(letters)] for _ in range(rows)]
        self.colours = [['' for _ in range(letters)] for _ in range(rows)]
        self.alph = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    def is_end(self):
        if self.board[-1] != ['' for _ in range(self.letters)]:
            return True
        else:
            r = self.game_result()
            if r[0] == True:
                return True
            else:
                return False

    def game_result(self):
        win = (False, 99)
        for i, r in enumerate(self.board):
            if self.word == ''.join(r):
                win = (True, i)
                break
        return win

    def update_board(self, u_inp):
        w_hash_table = deepcopy(self.w_hash_table)
        for i, s in enumerate(str(u_inp).upper()):
            self.board[self.g_count][i] = s
            if self.word[i] == s:
                self.colours[self.g_count][i] = 'G' #Correct place and letter
                w_hash_table[s] -= 1
            elif s in w_hash_table and w_hash_table[s] >= 1:
                self.colours[self.g_count][i] = 'Y' #Wrong place but letter in word
                w_hash_table[s] -= 1
            else:
                self.colours[self.g_count][i] = 'B' #Letter not in word
        self.g_count += 1

    def valid_guess(self, u_inp):
        if len(u_inp) == 5 and False not in [False for s in str(u_inp).upper() if s not in self.alph]:
            return True
        else:
            return False
