import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from game_class import Environment
import numpy as np
import pickle
import pyximport
pyximport.install(True, True,)

# from tensorflow import function
# if you want this to run a bit faster, uncomment this import

done = False
epochs = 100_000_000_000_000  # games played
gamma = .99  # gamma is probably too high
epsilon = 1.  # same for epsilon
decay = 0.01  # decay is alright
qtable: dict[tuple, list] = Environment.gen()  # load a qtable

env = Environment()  # start the environment
env.reset()  # reset the environment
fast = False  # cut down on train time
try:
    # @function(jit_compile=True, reduce_retracing=True)  # if you want to jit compile training uncomment this 
    def f():
        global qtable, epochs, done, gamma, epsilon, fast, env
        for i in range(epochs):
            state, reward, dead, et = env.reset()
            env.random_food()
            state = env.get_current_state()
            steps = 0
            if not fast:tot = 0
            done = False
            while not done:
                steps += 1
                # act randomly sometimes to allow exploration
                if np.random.uniform() < epsilon:
                    action = env.randAction()
                # if not select max action in Qtable (act greedy)
                else:
                    if not state in qtable:qtable[state] = [np.random.random() for i in '****']
                    action = qtable[state].index(max(qtable[state]))
                next_state, reward, done, et = env.move(action)

                if not fast:tot += reward
                if reward > 0:
                    steps = 0
                    env.random_food()
                if len(env.total_pos) >= env.cube*env.cube:  # if snake is too big we stop the program (it has gotten to the max length possible)
                    raise KeyboardInterrupt
                if steps > 1_000:  # if 1_000 steps have gone by and it has not eaten, reset
                    done = True
                epsilon -= epsilon/10e5
                # update qtable value with Bellman equation
                if not next_state in qtable:qtable[next_state] = [np.random.random() for i in '****']
                if not state in qtable:qtable[state] = [np.random.random() for i in '****']
                qtable[state][action] = reward + (gamma * max(qtable[next_state]))
                if not fast:env.refresh()
                    
                state = next_state

            # The more we learn, the less we take random actions
            epsilon -= epsilon * decay
            # if not fast:  # log details
                # with open('./logs.csv', 'a') as f:
                #     try:
                #         f.write(f'epoch {i} - accuracy: {(steps/tot)*100} epsilon: {epsilon}')
                #     except Exception:
                #         f.write(f'epoch {i} - accuracy: UNAVAILABLE epsilon: {epsilon}')
    f()
except KeyboardInterrupt:
    pass
print('saving')
with open('./qtable.pickle', 'wb') as f:pickle.dump(qtable, f)