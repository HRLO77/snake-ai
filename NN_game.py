import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from keras.models import load_model
from keras import Sequential
import numpy as np
import time
from game_class import Environment
env = Environment(cube=6)
env.reset()
env.random_food()
print('loading...')
NN: Sequential = load_model('./snake-NN')  # type: ignore
print('loaded')
flatten = lambda x, y=[]: [*x[:-1]] + [y := y + [*i] for i in x[-1]][-1]
print(flatten(env.get_current_state()))
move = np.argmax(NN.predict([flatten(env.get_current_state())], verbose=0))
for i in '*'*100:
    state, reward, dead, eaten = env.move(move)
    if eaten:
        env.random_food()
    if dead:
        env.reset()
        env.random_food()
    env.refresh()
    move = np.argmax(NN.predict([flatten(state)], verbose=0))
    # time.sleep(0.25)