# plays snake with the q-table saved from training
from game_class import Environment
import numpy as np
import pickle
from time import sleep
qtable = Environment.gen()
env = Environment()
state, reward, done, et = env.reset()
steps = 0
epsilon = 0.01
done = False
d = False
env.random_food()
state = env.get_current_state()

while 1:
    action = qtable[state].index(max(qtable[state]))
    if np.random.uniform() < epsilon:
        state, reward, done, et = env.move(env.randAction())
    else:
        state, reward, done, et = env.move(action)
    if done:
        env.reset()
        env.random_food()
    epsilon -= epsilon/10e4
    env.refresh()
    if reward > 0:
        epsilon -= 0.01
        et = False
        env.random_food()
    