# snake-ai
A reinforcement learning algorithm written in python using numpy.
## installing requirements
`python -m pip install -r req.txt`
## playing
To play snake on the terminal yourself, run `python console.py`.
## compression ops
To automatically compress or decompress q-table data, run `python compress_ops.py` in this directory. It determines whether to compress or decompress data by itself.
## training
To train your computer to play snake, run `python _train.py` with your hyper-parameters.
* epsilon
* gamma
* epochs
* decay
(note that def_train.cp310-win_amd64.pyd is _train.py with current hyper-parameters compiled using cython)
Epsilon is a float between 0-1, representing the chance of random actions taken to explore the environment.

Gamma is the discount factor (see the Bellman equation), how much the model agent should give priority to long-term rewards.

Epochs in training are how many times the model should play the game before it dies.

Decay is how much Epsilon should decrease over time.

For more information on the model learns, see the [Bellman equation](https://en.wikipedia.org/wiki/Bellman_equation) and train.py.

## playing
To make the computer play after training, run `python play.py` and open the pickle file you want the qtable from.
## New states!
For more accurate (but longer, slower, heavier training) more accurate states are returned for the agent.
* An encoded 7x7 grid around the head of the snake is returned along with the rest of the previous state.
* apple position instead of quadrant

This provides far more states for more precision to update!

However, because of the complexity of these extra items, qtable values cannot be instantiated on demand without taking a very long time, lots of resources and returning impossible (to reach) states.

So during training, states that have not be recorded are added on the training (like interpreting VS compiling).

I updated qtable values stored them in *qtable.pickle*, you can randomize values of the dictionary for your own training if you wish.
```python
from game_class import Environment
import random
env = Environment(cube=50)  # a 50x50 grid with '@' as the character used.
state, reward, dead, eaten = env.reset()  # start the environment
env.random_food()  # spawn an apple
state: tuple[int] = env.get_current_state()  # get the current state
qtable = Environment.gen()  # load the q-table
qtable = {i: [random.random() for i in  '*'*4]for i in qtable.keys()}  # randomize qtable values
```
# end
Thanks for checking out this repository!
