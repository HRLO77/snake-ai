# plays snake with the q-table saved from training
import game_class
import numpy as np
import pickle
with open('./qtable.pickle', 'rb') as f:qtable: list = \
    pickle.load(f)
env = game_class.Environment()
state, reward, done, et = env.reset()
steps = 0
epsilon = 0.01
done = False
d = False
env.random_food()  # 5 random apples
state = env.get_current_state()
while not done:
    action = qtable[state].index(max(qtable[state]))
    # print(action)
    if np.random.uniform() < epsilon:
        state, reward, done, et = env.move(env.randAction())
    else:
        state, reward, done, et = env.move(action)
    epsilon -= epsilon/10e4
    env.refresh()
    if reward > 0:
        epsilon -= 0.01
        et = False
        env.random_food()