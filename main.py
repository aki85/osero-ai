# coding: utf-8
from osero import Osero

env = Osero(board_size=6)
exit()
from logger import EpisodeLogger
from model import NetworkModel
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

env = Osero(board_size=4)
nb_actions = env.action_space.n

model = NetworkModel.create_simple_nn(env)
print(model.summary())


memory = SequentialMemory(limit=10000, window_length=1)

policy = EpsGreedyQPolicy(eps=0.1) 
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
               target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])
# dqn.load_weights('results/190621/10000.h5')
history = dqn.fit(env, nb_steps=10000, visualize=False, verbose=2, nb_max_episode_steps=300)

cb_ep = EpisodeLogger()
dqn.test(env, nb_episodes=10, visualize=False, callbacks=[cb_ep], nb_max_episode_steps=300)
# dqn.save_weights('results/190621/10000.h5')

cb_ep.make_log()
