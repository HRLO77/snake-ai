# The class used for training the agent in an environment and testing it.
import json
import random
import keyboard
import numpy as np
import tracemalloc
import sys

class Environment:
    '''Represents the snake game and its agent (the snake)'''
  
    END = (lambda **k: k)(**{'end': '\r'})
    def setup(self):
        '''sets up the game (if training, run .reset() instead)'''
        self.position = {}
        self.total_pos = []
        self.my_pos = tuple()
        for i in range(0, self.cube):
            for v in range(0, self.cube):
                if v != (self.cube - 1):
                    if v == i and (v == ((self.cube // 2) - 1)):
                        self.position[(i, v)] = f"\033[48;2;256;256;256m{self.TO_CHAR}\033[0m"
                        self.my_pos = ((i, v), f"\033[48;2;256;256;256m{self.TO_CHAR}\033[0m")
                        self.total_pos = [self.my_pos]
                    else:
                        self.position[(i, v)] = f"\033[48;2;0;0;0m{self.TO_CHAR}"
                else:
                    if v == (self.cube - 1) and i != (self.cube - 1):
                        self.position[(i, v)] = f"\033[48;2;0;0;0m\033[0m\n"
                    elif v == (self.cube - 1) and i == (self.cube - 1):
                        self.position[(i, v)] = f"\033[48;2;0;0;0m\033[0m"

    def refresh(self,):
        '''Renders the game.'''
        sys.stdout.write(f'\033[{self.cube}A\033[0m{self.TO_CHAR}\n' + f"\033[0m".join(f"\033[0m".join(i) for i in np.array(tuple(self.position.values()), dtype=str)[:self.cube**2].reshape((self.cube, self.cube))) + ' \r '
)


    def random_food(self,):
        '''Replaces a random blank space in the grid with an apple.'''
        self.eaten = False
        while True:
            x = random.randint(0, self.cube - 1)
            y = random.randint(0, self.cube - 1)
            if self.position[(x, y)] == f"\033[48;2;0;0;0m{self.TO_CHAR}":
                self.position[(x, y)] = f"\033[48;2;256;0;0m{self.TO_CHAR}"
                self.apple = (x, y)
                return (x, y)
    
    
    def __init__(self, cube: int=20, to_char:str = "ㅤ", allow_keys: bool=False):
        '''
        :param cube: an integer for the width and height of the grid.
        :param to_char: The character that each square should be rendered with ANSI codes.
        :param allow_keys: A boolean, whether or not to take in key presses for the game. (Not supported with async, run console.py instead)'''
        self.position = {}
        self.size = 2
        self.my_pos = ((0, 0), f"\033[48;2;256;256;256m{to_char}\033[0m")
        self.total_pos = [self.my_pos]
        self.ENDSTR = f"\033[0m{to_char}\n"
        self.dir = "up"
        self.REVERSE = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        self.eaten: bool = False
        self.cube = cube
        self.TO_CHAR = to_char
        self.to_call = []
        self.dead = False
        tracemalloc.start()
        assert cube >= 7, "Grid must be 6x6 or greater"
        if allow_keys:
            def func(args: keyboard._keyboard_event.KeyboardEvent):
                if json.loads(args.to_json())["event_type"] == "down":
                    if len(self.to_call) > 0:
                        if self.REVERSE.get(json.loads(args.to_json())["name"]) != self.to_call[-1]:
                            self.to_call += [json.loads(args.to_json())["name"]]
                    else:
                        self.to_call = [json.loads(args.to_json())["name"]]

            keyboard.on_press(func)
        self.setup()
        self.apple = self.random_food()

    def game(self):
        '''Permanent loop that constantly refreshes (not meant for training)'''
        self.apple = self.random_food()
        while not self.eaten and not self.dead:
            self.refresh()


    def update(self,):
        '''Pulls the snake along.'''
        self.total_pos = [(i, f"\033[48;2;0;0;0m{self.TO_CHAR}") for i, k in self.total_pos[::(-(self.size)+1)]] + self.total_pos[(-(self.size)+1)::]
        self.position.update({i:v for i,v in self.total_pos})
        self.total_pos = self.total_pos[(-(self.size)+1)::]
        self.position.update({i:v for i,v in self.total_pos})
        
    def move(self, action=None):
        '''Moves the snake based on an action of 0-3 (inclusive). If action is not provided, the latest action from self.to_call is run.'''
        blank = f"\033[48;2;0;0;0m{self.TO_CHAR}"
        snake = f"\033[0m\033[48;2;256;256;256m{self.TO_CHAR}"
        food = f"\033[48;2;256;0;0m{self.TO_CHAR}"

        if action is not None:
            action = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}[action]
            self.to_call.append(action)
        if len(self.to_call) > 0:
            self.dir = self.to_call.pop(0)


        if self.dir == "left":
            if (self.my_pos[0][1] - 1) < 0:
                self.dead = True
            elif self.position[(self.my_pos[0][0], (self.my_pos[0][1] - 1))] == snake:
                self.dead = True
            elif self.position[(self.my_pos[0][0], (self.my_pos[0][1] - 1))] == food:
                self.size += 1
                self.my_pos = ((self.my_pos[0][0], self.my_pos[0][1] - 1), snake)
                self.eaten = True
                self.total_pos.append(self.my_pos)
                self.update()

            elif self.position[(self.my_pos[0][0], self.my_pos[0][1] - 1)] == blank:
                self.my_pos = ((self.my_pos[0][0], self.my_pos[0][1] - 1), snake)
                self.total_pos.append(self.my_pos)
                self.update()
        elif self.dir == "right":
            if self.my_pos[0][1] + 1 >= self.cube - 1:
                self.dead = True
            elif self.position[(self.my_pos[0][0], self.my_pos[0][1] + 1)] == snake:
                self.dead = True
            elif self.position[(self.my_pos[0][0], self.my_pos[0][1] + 1)] == food:
                self.size += 1
                self.my_pos = ((self.my_pos[0][0], self.my_pos[0][1] + 1), snake)
                self.total_pos.append(self.my_pos)
                self.eaten = True
                self.update()
            elif self.position[(self.my_pos[0][0], self.my_pos[0][1] + 1)] == blank:
                self.my_pos = ((self.my_pos[0][0], self.my_pos[0][1] + 1), snake)
                self.total_pos.append(self.my_pos)
                self.update()
        elif self.dir == "up":
            if (self.my_pos[0][0] - 1) < 0:
                self.dead = True
            elif self.position[((self.my_pos[0][0] - 1), self.my_pos[0][1])] == snake:
                self.dead  = True
            elif self.position[((self.my_pos[0][0] - 1), self.my_pos[0][1])] == food:
                self.size += 1
                self.my_pos = ((self.my_pos[0][0] - 1, self.my_pos[0][1]), snake)
                self.total_pos.append(self.my_pos)
                self.eaten = True
                self.update()
            elif self.position[((self.my_pos[0][0] - 1), self.my_pos[0][1])] == blank:
                self.my_pos = (((self.my_pos[0][0] - 1), self.my_pos[0][1]), snake)
                self.total_pos.append(self.my_pos)
                self.update()
        elif self.dir == "down":
            if (self.my_pos[0][0] + 1) > self.cube - 1:
                self.dead  = True
            elif self.position[((self.my_pos[0][0] + 1), self.my_pos[0][1])] == snake:
                self.dead  = True
            elif self.position[((self.my_pos[0][0] + 1), self.my_pos[0][1])] == food:
                self.size += 1
                self.my_pos = ((self.my_pos[0][0] + 1, self.my_pos[0][1]), snake)
                self.total_pos.append(self.my_pos)
                self.eaten = True
                self.update()
            elif self.position[((self.my_pos[0][0] + 1), self.my_pos[0][1])] == blank:
                self.my_pos = (((self.my_pos[0][0] + 1), self.my_pos[0][1]), snake)
                self.total_pos.append(self.my_pos)
                self.update()
        return self.get_current_state(), 1 if self.eaten else (-1 if self.dead else 0), self.dead, self.eaten

    @staticmethod
    def randAction():
        '''Returns a random action.'''
        return np.random.choice(4)

    def get_current_state(self):
        '''Returns the current state of the environment from the agents perspective.
        Returns an array with 1024 possible states.'''
        self.my_pos = self.my_pos
        cube = self.cube
        dir = self.dir
        apple = self.apple
        current_dir = dir
        # apple_dir = [0, 0, 0, 0]
        # if (self.my_pos[0][1] - apple[1]) > 0:
        #     apple_dir[0] = 1
        # elif (self.my_pos[0][1] - apple[1]) < 0:
        #     apple_dir[0] = 0
        #     apple_dir[2] = 1
        # elif (self.my_pos[0][1] - apple[1]) == 0:
        #     pass
        # if (self.my_pos[0][0] - apple[0]) > 0:
        #     apple_dir[3] = 1
        # elif (self.my_pos[0][0] - apple[0]) < 0:
        #     apple_dir[3] = 0
        #     apple_dir[1] = 1
        # elif (self.my_pos[0][0] - apple[0]) == 0:
        #     pass
        pos = [*self.my_pos[0]]
        # danger[0] = (pos[1] + 1) == cube
        # danger[1] = (pos[0] - 1) == cube
        # danger[2] = (pos[1] - 1) == cube
        # danger[3] = (pos[0] + 1) == cube
        # if not danger[0]:
        #     if (pos[0], pos[1]+1) in position:
        #         danger[0] = '256;256;256' in position[(pos[0], pos[1]+1)]# up
        #     else:
        #         danger[0] = True
        # if not danger[1]:
        #     if (pos[0]-1, pos[1]) in position:
        #         danger[1] = '256;256;256' in position[(pos[0]-1, pos[1])]
        #     else:
        #         danger[1] = True# left
        # if not danger[2]:
        #     if (pos[0], pos[1]-1) in position:
        #         danger[2] = '256;256;256' in position[(pos[0], pos[1]-1)]
        #     else:
        #         danger[2] = True
        #     # dowm
        # if not danger[3]:
        #     if (pos[0]+1, pos[1]) in position:
        #         danger[3] = '256;256;256' in position[(pos[0]+1, pos[1])]# right
        #     else:
        #         danger[3] = True
        # danger = [int(i) for i in danger]
        blank = f"\033[48;2;0;0;0m"
        snake = f"\033[48;2;256;256;256m"
        food = f"\033[48;2;256;0;0m"
        encoded: list[list[int]] = np.array([{blank: 0, snake: 1, food: 2}[i.replace('\033[0m', '').replace(self.TO_CHAR, '').replace('\n', '').strip()] for i in self.position.values()]).reshape((cube, cube)).tolist()
        ysub: int = pos[0]-3 if pos[0] > 3 else 0
        yadd: int = pos[0]+4 if pos[0] < self.cube-3 else self.cube
        xsub: int = pos[1]-3 if pos[1] > 3 else 0
        xadd: int = pos[1]+4 if pos[1] < self.cube-3 else self.cube
        encoded: list[list[int]] = encoded[ysub:yadd]
        encoded = [i[xsub: xadd] for i in encoded]
        outer_len: int = len(encoded)
        
        inner_len: int = len(encoded[0])
        pad_in: int = 2-inner_len
        pad_out: int = 2-outer_len
        pad_in_where: bool = inner_len == 6
        pad_out_where: bool = outer_len ==6

        if pad_in > 0:
            if pad_in_where:
                encoded = [i + [0]*pad_in for i in encoded if len(i) < 2]
            else:
                encoded = [[0]*pad_in + i for i in encoded if len(i) < 2]
        if pad_out > 0:
            if pad_out_where:
                encoded += [[0, 0]*pad_out]
        
        encoded = tuple([tuple(i) for i in encoded])
        return (self.apple, {'up': 0, 'left': 1, 'down': 2, 'right':\
            3}[current_dir], encoded)
    
    def reset(self):
        '''Resets the environment.'''
        self.setup()
        self.eaten = False
        self.dead= False
        return self.get_current_state(), 0, self.dead, self.eaten
   
    @staticmethod
    def gen():
        '''Loads the q-table.'''
        with open('./qtable.pickle', 'rb') as f:return __import__('pickle').load(f)
        
    @staticmethod
    def new(start_len: int = int(10e5)):
        '''Instantiates a q-table.
        :param start_len: The amount of states to start the qtable with (more can be added later in training).'''
        s = set()
        # with open('./test.pickle', 'rb') as f:s=pickle.load(f)
        possib = [0]*25 + [1]*24
        for b in '*'*start_len:
            tried = possib.copy()  # type: ignore
            np.random.shuffle(tried)
            tried = tried[:25]
            rand_ind = (3, 3)
            while rand_ind == (3,3):
                rand_ind = (random.randint(0,4), random.randint(0,4))
            tried: list[list[int]] = np.array(tried).reshape((5, 5)).tolist()
            tried[3][3] = 1
            tried[rand_ind[0]][rand_ind[1]] = 2
            tried = [tuple(i) for i in tried]
            s.add((tuple([random.choice([0, 1]) for i in '~'*8] +
                        [random.choice([0, 1, 2, 3])] + tried)))
        return {i: [random.random() for i in '_'*4] for i in s}
