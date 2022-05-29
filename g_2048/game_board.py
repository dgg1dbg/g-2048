import gym
from gym import spaces
import random
import numpy as np
import math
import pprint



class GameBoardEnv(gym.Env):
    def __init__(self):
        self.observation_space = spaces.Box(0, 3000, (4, 4), dtype=int)
        self.action_space = spaces.Discrete(4)
        

    def reset(self):
        self.score = 0
        self.reward = 0
        self.ended = 0
        self.won = 0
        self.board = np.zeros((4, 4))
        i, j = np.random.randint(0, 16, 2)
        while [math.trunc(i/4), i%4] == [math.trunc(j/4), j%4]:
            i, j = np.random.randint(0, 16, 2)
        self.board[math.trunc(i/4), i%4] = np.random.choice([2, 4])
        self.board[math.trunc(j/4), j%4] = np.random.choice([2, 4])
        return self.board

    def step(self, action):
        rec = self.board
        if action == 0:
            self.board = np.flip(self.move(np.flip(self.board, axis=1)), axis=1)
        elif action == 1:
            self.board = self.move(self.board)
        elif action == 2:
            self.board = np.transpose(self.move(np.transpose(self.board)))
        elif action == 3:
            self.board = np.transpose(np.flip(self.move(np.flip(np.transpose(self.board), axis=1)), axis=1))
        if np.all(self.board != 0) or (rec == self.board).all():
            pass
        else:
            i = np.random.randint(0, 16)
            while self.board[math.trunc(i/4)][i%4] != 0:
                i = np.random.randint(0, 16)
            self.board[math.trunc(i/4)][i%4] = 2
        board1 = np.flip(self.move(np.flip(self.board, axis=1), True), axis=1)
        board2 = self.move(self.board, True)
        board3 = np.transpose(self.move(np.transpose(self.board), True))
        board4 = np.transpose(np.flip(self.move(np.flip(np.transpose(self.board), axis=1), True), axis=1))
        if np.any(self.board >= 2048):
            self.won = 1
            self.ended = 1
        elif (board1 == board2).all() and (board1 == board3).all() and (board1 == board4).all() and (board2 == board3).all() and (board3 == board4).all():
            self.ended = 1

        return self.board, self.reward, self.ended, {'score': self.score, 'won': self.won}

    def move(self, b, test = False):
        result = []
        if not test:
            self.reward = 0
        for i in b:
            vector = i.tolist()
            for j in range(1, len(vector)):
                if j == 0:
                    continue
                else:
                    k = j-1
                    while k > 0 and vector[k] == 0:
                        k -= 1
                    if vector[k] == 0:
                        vector[k] = vector[j]
                        vector[j] = 0
                    elif vector[k] == vector[j]:
                        vector[k] *= 2
                        if not test:
                            self.score += vector[k]
                            self.reward += vector[k]
                        vector[k] = str(vector[k])
                        vector[j] = 0
                    else:
                        if k+1 == j:
                            continue
                        else:
                            vector[k+1] = vector[j]
                            vector[j] = 0

            result.append([int(float(x)) for x in vector])
        result = np.array(result)
        return result


    def render(self):
        pprint.pprint(self.board)


if __name__ == "__main__":
    game = GameBoardEnv()
    game.reset()
    game.render()
    while not game.ended:
        print(game.step(int(input())))
        print()
