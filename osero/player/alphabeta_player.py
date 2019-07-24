import copy
from ..board import OseroBoard


class AlphabetaPlayer:
    INF = float('inf')

    def __init__(self, color, board_size, depth=5):
        self.color = color
        self.name = 'alphabeta'
        OseroBoard.board_size = board_size
        self.depth = depth


    def next_move(self, board, color):
        (move, value) = self.max_val(board, -self.INF, self.INF, self.depth, color)
        return move


    def max_val(self, state, alpha, beta, depth, color):
        if OseroBoard.cant_put_stone(state):
            return None, self.finish_evalution(state, color)
        elif depth == 0:
            return None, self.evaluation(state, color)
        best_move = None
        v = -self.INF
        moved_states = self.make_moved_states(state, color)
        for (move, state) in moved_states:
            value = self.min_val(state, alpha, beta, depth - 1, color)[1]
            if best_move is None or value > v:
                best_move = move
                v = value
            if v >= beta:
                return best_move, v
            alpha = max(alpha, v)
        return best_move, v


    def min_val(self, state, alpha, beta, depth, color):
        if OseroBoard.cant_put_stone(state):
            return None, self.finish_evalution(state, color)
        elif depth == 0:
            return None, self.evaluation(state, color)
        best_move = None
        v = self.INF
        moved_states = self.make_moved_states(state, -color)
        for (move, state) in moved_states:
            value = self.max_val(state, alpha, beta, depth - 1, color)[1]
            if best_move is None or value < v:
                best_move = move
                v = value
            if alpha >= v:
                return best_move, v
            beta = min(beta, v)
        return best_move, v


    def make_moved_states(self, state, color):
        moves = []
        can_put_list = OseroBoard.get_can_put_list(state, color)
        
        for move in can_put_list:
            new_state = OseroBoard.create_next_squares(state, color, *move)
            moves.append((move, new_state))
        return moves


    def finish_evalution(self, state, color):
        black, white = OseroBoard.STONES
        score = OseroBoard.count_score(state)
        value = 0
        if score[0] == score[1]:
            value = 0
        elif score[0] > score[1] and color == black:
            value = self.INF
        elif score[0] < score[1] and color == white:
            value = self.INF
        else:
            value = -self.INF
        return value


    def evaluation(self, state, color):
        result = 0
        return result
        

    def feedback(self, board):
        pass