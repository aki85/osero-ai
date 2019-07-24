import random
from ..board import OseroBoard

class InputPlayer:
    def __init__(self, color, board_size):
        self.color = color
        self.name = 'input'
        OseroBoard.board_size = board_size


    def next_move(self, board, color):
        black, white = OseroBoard.STONES
        OseroBoard.print_squares(board)
        print('Black(x) turn' if color == black else 'White(o) turn')
        print('Select and input hand: ', OseroBoard.get_can_put_list(board, color))
        best_move = map(int, input().split(', '))
        return best_move


    def feedback(self, board):
        pass