import random
from ..board import OseroBoard

class RandomPlayer:
    def __init__(self, color, board_size):
        self.color = color
        self.name = 'random'
        OseroBoard.board_size = board_size


    def next_move(self, board, color):
        moves = OseroBoard.get_can_put_list(board, color)
        best_move = moves[random.randint(0,len(moves) - 1)]
        return best_move


    def feedback(self, board):
        pass