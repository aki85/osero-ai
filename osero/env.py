# coding: utf-8
import gym
import gym.spaces
import numpy as np
from .game import OseroGame
from .player.random_player import RandomPlayer
from .player.input_player import InputPlayer
from .player.qlearning_player import QlearningPlayer
from .player.alphabeta_player import AlphabetaPlayer

# オセロのを学習させるための環境
class Osero(gym.core.Env):
    # TIE, Black WIN, White WIN
    finish_count = [0, 0, 0]

    def __init__(self, board_size):
        board_size = 8
        black, white = OseroGame.STONES
        game = OseroGame(board_size=board_size)
        self.game = game
        black_player = RandomPlayer(black, board_size)
        white_player = QlearningPlayer(white, board_size)
        game.set_players(black_player, white_player)

        white_player.load_q('q8x8_200000')
        white_player.to_battle_mode()

        self.print_results()
        play_count = 1000
        print_times = 10
        save_times = 0
        for i in range(play_count):
            game.start_new_game()
            game.play_game()
            self.add_finish_count()
            if i % (play_count/print_times) == (play_count/print_times)-1:
                self.print_results()
            if save_times != 0 and i % (play_count/save_times) == (play_count/save_times)-1:
                return
                white_player.save_q('q8x8_'+str(play_count+i+1))
                
        # game.print_result(with_board=True)
        
        
    def step(self, action):
        pass


    def reset(self):
        pass


    def clear_finish_count(self):
        self.finish_count = [0, 0, 0]


    def add_finish_count(self):
        winner = self.game.is_game_winner()
        if winner == 0:
            self.finish_count[0] += 1
        elif winner == 1:
            self.finish_count[1] += 1
        else:
            self.finish_count[-1] += 1


    def print_results(self):
        print("%d x %d Game Count: %d" % (self.game.board_size, self.game.board_size, sum(self.finish_count)))
        print("TIEs: %d, Black WINs: %d, White WINs: %d" % (self.finish_count[0], self.finish_count[1], self.finish_count[-1]))