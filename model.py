from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
class NetworkModel:
    def __init__(self):
        pass

    @staticmethod
    def create_simple_nn(env):
        nb_actions = env.action_space.n
        model = Sequential()
        model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
        model.add(Dense(16))
        model.add(Activation('relu'))
        model.add(Dense(16))
        model.add(Activation('relu'))
        model.add(Dense(16))
        model.add(Activation('relu'))
        model.add(Dense(nb_actions))
        model.add(Activation('linear'))
        return model