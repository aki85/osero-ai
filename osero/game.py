# coding: utf-8
from .board import OseroBoard
class OseroGame(OseroBoard):
    def __init__(self, board_size=8):
        self.board_size = board_size
        self.start_new_game()


    def set_players(self, black_player, white_player):
        # self.turn(1 or -1)でplを選択するための処置
        self.players = [0, black_player, white_player]


    def swap_players(self):
        self.players = [0, self.players[1], self.players[-1]]


    def proceed_step(self):
        # 置けない手による終了などは考慮しない
        if self.get_can_put_list(self.board, self.turn) != []:
            self.put_stone(self.turn, *self.players[self.turn].next_move(self.board, self.turn))
            self.players[-self.turn].feedback(self.board)

        self.turn = -self.turn


    def start_new_game(self):
        black, white = self.STONES
        self.board = self.create_new_squares(self.board_size)
        self.turn = black


    def play_game(self):
        while not self.is_game_set():
            self.proceed_step()
        self.players[1].feedback(self.board)
        self.players[-1].feedback(self.board)


    def put_stone(self, stone, x, y):
        self.board = self.create_next_squares(self.board, stone, x, y)


    def count_game_score(self):
        return self.count_score(self.board)


    def is_game_winner(self):
        return self.is_winner(self.board)


    def is_game_set(self):
        return self.cant_put_stone(self.board)


    def print_board(self):
        self.print_squares(self.board)
        

    def print_result(self, with_board=False):
        if with_board:
            self.print_board()
        score = self.game_score()
        if not self.is_game_set():
            print('This game is still playing')
            print("Black: %d White: %d" % score)
            return
        
        black_count, white_count = score
        if black_count == white_count:
            print("TIE")
            print("Black: %d White: %d" % score)
        elif black_count > white_count:
            print("Black WIN")
            print("Black: %d White: %d" % score)
        else:
            print("White WIN")
            print("Black: %d White: %d" % score)