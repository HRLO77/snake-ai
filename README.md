# snake-ai
A reinforcement learning algorithm written in python using numpy.
## installing requirements
`python -m pip install -r req.txt`
## playing
To play snake on the terminal yourself, run `python console.py`.
## training
To train your computer to play snake, run `python train.py` with your hyper-parameters.
* epsilon
* gamma
* epochs
* decay

Epsilon is a float between 0-1, representing the chance of random actions taken to explore the environment.
Gamma is the discount factor (see the Bellman equation), how much the model agent should give priority to long-term rewards
Epochs in training are how many times the model should play the game before it dies.
Decay is how much Epsilon should decrease over time.
For more information on the model learns, see the [Bellman equation](https://en.wikipedia.org/wiki/Bellman_equation) and train.py
## playing
To make the computer play after training, run `python play.py` and open the pickle file you want the qtable from.
## Environment
The environment is a grid, with one apple and snake.
There are 1024 possible states that the agent can see.
(Through Environment.get_current_state in game_class.py)
Being a tuple of integers.
(danger_up: 0|1, danger_left: 0|1, danger_down: 0|1, danger_right: 0|1, apple_up: 0|1, apple_lef: 0|1, apple_down: 0|1, apple_right: 0|1, current_direction: 0|1|2|3)

To create your own environment, use the `Environment` class from game_class.py
Example:
```python
from game_class import Environment
env = Environment(cube=50, to_char='@')  # a 50x50 grid with '@' as the character used.
state, reward, dead, eaten = env.reset()  # start the environment
env.random_food()  # spawn an apple
state: tuple[int] = env.get_current_state()  # get the current state
qtable: dict[tuple[int], list[int]] = Environment.gen()  # instantiate the q-table
```
# end
Thanks for checking out this repository!
