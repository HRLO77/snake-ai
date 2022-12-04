from game_class import Environment
import numpy as np
import pickle
import os
# from tensorflow import function
# if you want this to run a bit faster, uncomment this import
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
done = False
epochs = 25_000  # games played
gamma = .99  # gamma is probably too high
epsilon = 1.  # same for epsilon
decay = 0.01  # decay is alright
qtable: dict[tuple, list] = Environment.gen()  # instantiate a qtable

env = Environment()  # start the environment
env.reset()  # reset the environment
fast = True  # cut down on train time
try:
    # @function(jit_compile=True)  # if you want to jit compile training uncomment this 
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
                    action = qtable[state].index(max(qtable[state]))
                next_state, reward, done, et = env.move(action)
                if not fast:tot += reward
                if reward > 0:
                    steps = 0
                    env.random_food()
                if len(env.total_pos) >= env.cube*env.cube:  # if snake is too big we stop the program (it has gotten to the max length possible)
                    raise KeyboardInterrupt
                if steps > 500:  # if 500 steps have gone by and it has not eaten, reset
                    done = True
                epsilon -= epsilon/10e5
                # update qtable value with Bellman equation
                qtable[state][action] = reward + (gamma * max(qtable[next_state]))
                if not fast:env.refresh()
                state = next_state

            # The more we learn, the less we take random actions
            epsilon -= epsilon * decay
            if not fast:  # log details
                try:
                    print(f'epoch {i} - accuracy: {(steps/tot)*100} epsilon: {epsilon}', file=open('./logs.csv', 'a'))
                except Exception:
                    print(f'epoch {i} - accuracy: UNAVAILABLE epsilon: {epsilon}', file=open('./logs.csv', 'a'))
    f()    
except KeyboardInterrupt:
    pass
print('saving')

with open('./qtable.pickle', 'wb') as f:pickle.dump(qtable, f)