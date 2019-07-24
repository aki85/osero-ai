import random, os, pickle
from copy import deepcopy
from ..board import OseroBoard


class QlearningPlayer:
    INF = float('inf')
    INITIAL_Q = 1

    def __init__(self, color, board_size, e=0.2, alpha=0.1, gamma=0.9):
        self.color = color
        self.name = 'qlearning'
        self._e = e
        self._initial_e = e
        self._alpha = alpha
        self._gamma = gamma
        self._q = {}
        self._last_board = None
        self._last_move = None
        OseroBoard.board_size = board_size


    def set_opponent(self, opponent):
        self.opponent = opponent


    def next_move(self, board, color):
        move = self.policy(board, color)
        return move


    def flatten_board(self, board):
        return [square for row in board for square in row]


    def policy(self, board, color):
        self._last_board = deepcopy(board)

        qs = self.make_qs(board, color)

        max_q = max(qs)

        positions = OseroBoard.get_can_put_list(board, color)
        indexes = [i for i in range(len(positions)) if qs[i] == max_q]
        i = random.choice(indexes)

        move = positions[i]

        self._last_move = move
        return move


    def get_q(self, state, act):
        if self._q.get((state, act)) is None:
            self._q[(state, act)] = self.INITIAL_Q
        return self._q.get((state, act))


    def save_q(self, file='q'):
        with open(file+'.pickle', 'wb') as f:
            pickle.dump(self._q, f)


    def load_q(self, file='q'):
        if os.path.exists(file+'.pickle'):
            print('loading q...')
            with open(file+'.pickle', 'rb') as f:
                self._q = pickle.load(f)
            print('loaded')

    def print_q(self):
        for k, v in self._q.items():
            print(k, v)


    def feedback(self, board):
        is_game_set = OseroBoard.cant_put_stone(board)

        reward = 0
        if is_game_set:
            winner = OseroBoard.is_winner(board)

            if winner == self.color:
                reward = 1
            elif winner == 0:
                reward = 0
            elif winner != self.color:
                reward = -1
                
        if self._last_move != None:
            self.learn(reward, board, is_game_set)

            self._last_board = None
            self._last_move = None


    def learn(self, reward, board, is_game_set):
        flattend_last_board = tuple(self.flatten_board(self._last_board))
        last_action = self._last_move

        qs = self.make_qs(board, self.color)

        if is_game_set or qs == []:
            max_q = 0
        else:
            max_q = max(qs)

        last_q = self.get_q(flattend_last_board, last_action)
        self._q[(flattend_last_board, last_action)] = last_q + self._alpha * ((reward + self._gamma * max_q) - last_q)


    def make_qs(self, board, color):
        positions = OseroBoard.get_can_put_list(board, color)
        qs = []
        for position in positions:
            qs.append(self.get_q(tuple(self.flatten_board(board)), position))
        return qs


    def to_learning_mode(self):
        self._e = self._initial_e


    def to_battle_mode(self):
        self._e = 0