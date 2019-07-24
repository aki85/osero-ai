import rl.callbacks
import os
import matplotlib.pyplot as plt
class EpisodeLogger(rl.callbacks.Callback):
    def __init__(self):
        self.observations = {}
        self.rewards = {}
        self.actions = {}

    def on_episode_begin(self, episode, logs):
        self.observations[episode] = []
        self.rewards[episode] = []
        self.actions[episode] = []

    def on_step_end(self, step, logs):
        episode = logs['episode']
        self.observations[episode].append(logs['observation'])
        self.rewards[episode].append(logs['reward'])
        self.actions[episode].append(logs['action'])

    def make_log(self):
        for obs in self.observations.values():
            plt.plot([o[0] for o in obs])
        plt.xlabel("step")
        plt.ylabel("pos")
        for i in range(99):
            test_png = 'results/190621/test{}.png'.format(i)
            if not os.path.exists(test_png):
                plt.savefig(test_png.replace('.png', ''))
                break