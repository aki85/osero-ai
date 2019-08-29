import numpy as np
from ..board import OseroBoard

def multiple(board):
    b_t = np.transpose(board) # transpose
    b_r = np.rot90(board, 2) # rotate
    b_rt = np.rot90(b_t, 2) # transpose and rotate

    boards = np.array([[board], [b_t], [b_r], [b_rt]])
    return boards

class DQN:
    def __init__(self, model, dump_scores=False):
        super().__init__()
        self.model = model
        self.dump_scores = dump_scores

    def next_move(self, board, color):
        moves = OseroBoard.get_can_put_list(board, color)
        if len(moves) == 0:
            return None
        
        boards = [multiple(board) for move in moves]
        boards = np.array(boards).reshape(-1, reversi.BOARD_SIZE, reversi.BOARD_SIZE)
        colors = np.array([color]*len(boards)).reshape(-1, 1)
        actions = [multiple(reversi.put(board, color, move)) for move in moves]
        actions = np.array(actions).reshape(-1, reversi.BOARD_SIZE, reversi.BOARD_SIZE)

        scores = self.model.predict([
            boards,
            colors,
            actions
        ])

        scores = scores.reshape([-1, 4])
        scores = np.max(scores, axis=1)
        max_move = np.argmax(scores)
        if self.dump_scores:
            for h, s in zip(moves, scores):
                print("{0}: {1}".format(move, s))
            print("choose:", moves[max_move])
        return moves[max_move]