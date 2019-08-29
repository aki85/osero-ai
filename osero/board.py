# coding: utf-8
import copy
class OseroBoard:
    VECS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    STONES = [1, -1]
    EMPTY_STONE = 0
    board_size = 8

    @classmethod
    def create_new_squares(cls, size=8):
        cls.board_size = size
        empty = cls.EMPTY_STONE
        black, white = cls.STONES
        squares = []
        for i in range(cls.board_size//2-1):
            squares = squares + [[empty]*cls.board_size]
        squares = squares + [[empty] * (cls.board_size//2-1) + [white,black] + [empty] * (cls.board_size//2-1)]
        squares = squares + [[empty] * (cls.board_size//2-1) + [black,white] + [empty] * (cls.board_size//2-1)]
        for i in range(cls.board_size//2-1):
            squares = squares + [[empty]*cls.board_size]
        return squares


    @classmethod
    def print_squares(cls, squares):
        empty = cls.EMPTY_STONE
        black, white = cls.STONES

        print('|---'*cls.board_size+'|')
        for row in squares:
            print('|', end='')
            for square in row:
                if square == empty:
                    square_text = '   '
                elif square == black:
                    square_text = ' x '
                elif square == white:
                    square_text = ' o '
                print(square_text+'|', end='')
            print('')
            print('|---'*cls.board_size+'|')
    

    @classmethod
    def count_score(cls, squares):
        empty = cls.EMPTY_STONE
        black, white = cls.STONES

        black_count = white_count = 0
        for row in squares:
            for square in row:
                if square == black:
                    black_count = black_count + 1
                elif square == white:
                    white_count = white_count + 1
        return (black_count, white_count)


    @classmethod
    def is_winner(cls, squares):
        score = cls.count_score(squares)
        black_count, white_count = score
        if black_count == white_count:
            return 0
        elif black_count > white_count:
            return 1
        else:
            return -1


    @classmethod
    def is_out_of_range(cls, i, j):
        return not (0 <= i and i < cls.board_size and
                    0 <= j and j < cls.board_size)


    @classmethod
    def can_put(cls, squares, stone, x, y):
        if squares[y][x] != cls.EMPTY_STONE:
            return False

        for vec in cls.VECS:
            i = x + vec[0]
            j = y + vec[1]
            if cls.is_out_of_range(i, j) or squares[j][i] in (stone, cls.EMPTY_STONE):
                continue
            while True:
                i += vec[0]
                j += vec[1]
                if cls.is_out_of_range(i, j) or squares[j][i] == cls.EMPTY_STONE:
                    break
                if squares[j][i] == stone:
                    return True

        return False


    @classmethod
    def get_can_put_list(cls, squares, stone):
        can_put_list = []
        for x in range(cls.board_size):
            for y in range(cls.board_size):
                if cls.can_put(squares, stone, x, y):
                    can_put_list.append((x, y))
        return can_put_list


    @classmethod
    def create_next_squares(cls, squares, your_stone, x, y):
        next_squares = copy.deepcopy(squares)
        next_squares[y][x] = your_stone
        for vec in cls.VECS:
            i = x + vec[0]
            j = y + vec[1]

            if cls.is_out_of_range(i, j) or next_squares[j][i] in (your_stone, 0):
                continue
            reverse_count = 1
            while True:
                i += vec[0]
                j += vec[1]
                if cls.is_out_of_range(i, j) or next_squares[j][i] == 0:
                    break
                if next_squares[j][i] == your_stone:
                    for s in range(reverse_count):
                        i -= vec[0]
                        j -= vec[1]
                        next_squares[j][i] = your_stone
                    break
                reverse_count += 1
                
        return next_squares
        

    @classmethod
    def cant_put_stone(cls, board):
        black, white = cls.STONES
        if cls.get_can_put_list(board, black) == [] and cls.get_can_put_list(board, white) == []:
           return True

        return False