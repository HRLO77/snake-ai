# a deprecated environment for the snake game 
import asyncio
import json
import os
import pickle
import random
import sys
import aioconsole
import keyboard
import numpy as np
import multiprocessing
import tracemalloc
tracemalloc.start()
position = {}
cube = 20

to_char = "ㅤ"

size = 2
my_pos = ((0, 0), f"\033[48;2;256;256;256m{to_char}\033[0m")

total_pos = [my_pos]

ENDSTR = f"\033[0m{to_char}\n"
dir = "up"
lookup = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
eaten: bool = False


def setup():
    global total_pos
    global my_pos
    for i in range(0, cube):
        for v in range(0, cube):
            if v != (cube - 1):
                if v == i and (v == ((cube // 2) - 1)):
                    position[(i, v)] = f"\033[48;2;256;256;256m{to_char}\033[0m"
                    my_pos = ((i, v), f"\033[48;2;256;256;256m{to_char}\033[0m")
                    total_pos = [my_pos]
                else:
                    position[(i, v)] = f"\033[48;2;0;0;0m{to_char}"
            else:
                n = "\n"
                if v == (cube - 1) and i != (cube - 1):
                    position[(i, v)] = f"\033[48;2;0;0;0m\033[0m\n"
                elif v == (cube - 1) and i == (cube - 1):
                    position[(i, v)] = f"\033[48;2;0;0;0m\033[0m"

def refresh():
    # async def split(array, number):
    #     c = 0
    #     a=[]
    #     for i in array[::number]:
    #         a += [array[c * number : (c * number) + number :]]
    #         c += 1
    #     return a
    # for i in out:
    # await aioconsole.aprint('\n'*50)
    # await asyncio.sleep(0.2)
    # await aioconsole.aprint('\033[2J')
    print(f'\033[{cube}A\033[0m{to_char}\n' + f"\033[0m".join(f"\033[0m".join(i) for i in np.array(tuple(position.values()), dtype=str).reshape((cube, cube))), end='\r'
)
    # await aioconsole.aprint(f'{data[-1]}', end='\r')
    # await aioconsole.aprint()
    # await aioconsole.aprint(position.items()[:3])
    # await aioconsole.aprint(f'\033[0mScore: {size-1}\033[0m')


# def func(args: keyboard._keyboard_event.KeyboardEvent):
#     global dir
#     global to_call
#     # print('run')
#     if json.loads(args.to_json())["event_type"] == "down":
#         # print('ran')
#         if len(to_call) > 0:
#             if lookup.get(json.loads(args.to_json())["name"]) != to_call[-1]:
#                 to_call += [json.loads(args.to_json())["name"]]
#         else:
#             to_call = [json.loads(args.to_json())["name"]]
#     # print(out)


# keyboard.on_press(func)

apple = (0, 0)
def random_food() -> tuple[int, int]:
    global apple
    global eaten
    eaten = False
    while True:
        x = random.randint(0, cube - 1)
        y = random.randint(0, cube - 1)
        if position[(x, y)] == f"\033[48;2;0;0;0m{to_char}":
            position[(x, y)] = f"\033[48;2;256;0;0m{to_char}"
            return (x, y)


setup()


def game():
    global apple
    # console = aioconsole.AsynchronousConsole()
    apple = random_food()
    while not eaten and not dead:
        # await asyncio.sleep(1)
        # await asyncio.sleep(0.1)
        refresh()
    # await asyncio.sleep(0.085)


def update():
    global total_pos, total_pos, position, size
    total_pos = [(i, f"\033[48;2;0;0;0m{to_char}") for i, k in total_pos[::-size-1]] + total_pos[-size-1::]
    position.update({i:v for i,v in total_pos})
    total_pos = total_pos[-size-1::]

def move(action=None):
    global dir, my_pos, size, total_pos, sync, eaten, to_call, queue, dead
    blank = f"\033[48;2;0;0;0m{to_char}"
    snake = f"\033[0m\033[48;2;256;256;256m{to_char}"
    food = f"\033[48;2;256;0;0m{to_char}"
    sync = True
    if action is not None:
        action = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}[action]
        to_call.append(action)
    if len(to_call) > 0:
        dir = to_call.pop(0)

    if dir == "left":
        if (my_pos[0][1] - 1) < 0:
            dead = True
        elif position[(my_pos[0][0], (my_pos[0][1] - 1))] == snake:
            dead = True
        elif position[(my_pos[0][0], (my_pos[0][1] - 1))] == food:
            size += 1
            my_pos = ((my_pos[0][0], my_pos[0][1] - 1), snake)
            eaten = True
            total_pos.append(my_pos)
            update()

        elif position[(my_pos[0][0], my_pos[0][1] - 1)] == blank:
            my_pos = ((my_pos[0][0], my_pos[0][1] - 1), snake)
            total_pos.append(my_pos)
            update()
    elif dir == "right":
        if my_pos[0][1] + 1 >= cube - 1:
            dead = True
        elif position[(my_pos[0][0], my_pos[0][1] + 1)] == snake:
            dead = True
        elif position[(my_pos[0][0], my_pos[0][1] + 1)] == food:
            size += 1
            my_pos = ((my_pos[0][0], my_pos[0][1] + 1), snake)
            total_pos.append(my_pos)
            eaten = True
            update()
        elif position[(my_pos[0][0], my_pos[0][1] + 1)] == blank:
            my_pos = ((my_pos[0][0], my_pos[0][1] + 1), snake)
            total_pos.append(my_pos)
            update()
    elif dir == "up":
        if (my_pos[0][0] - 1) < 0:
            dead = True
        elif position[((my_pos[0][0] - 1), my_pos[0][1])] == snake:
            dead = True
        elif position[((my_pos[0][0] - 1), my_pos[0][1])] == food:
            size += 1
            my_pos = ((my_pos[0][0] - 1, my_pos[0][1]), snake)
            total_pos.append(my_pos)
            eaten = True
            update()
        elif position[((my_pos[0][0] - 1), my_pos[0][1])] == blank:
            my_pos = (((my_pos[0][0] - 1), my_pos[0][1]), snake)
            total_pos.append(my_pos)
            update()
    elif dir == "down":
        if (my_pos[0][0] + 1) > cube - 1:
            dead = True
        elif position[((my_pos[0][0] + 1), my_pos[0][1])] == snake:
            dead = True
        elif position[((my_pos[0][0] + 1), my_pos[0][1])] == food:
            size += 1
            my_pos = ((my_pos[0][0] + 1, my_pos[0][1]), snake)
            total_pos.append(my_pos)
            eaten = True
            update()
        elif position[((my_pos[0][0] + 1), my_pos[0][1])] == blank:
            my_pos = (((my_pos[0][0] + 1), my_pos[0][1]), snake)
            total_pos.append(my_pos)
            update()
            
    return cube*my_pos[0][0] + my_pos[0][1], 1 if eaten else (-2 if dead else 0), dead, eaten

# sys.__excepthook__, sys.excepthook = [lambda *args, **kwargs: pickle.dump(data[:-1], open('data.pickle', 'wb'))]*2
# sys.excepthook = lambda *args, **kwargs: pickle.dump(data[:-1], open('data.pickle', 'wb'))
def randAction():
    return np.random.choice(4)

def get_current_state():
    global data
    blank = f"\033[48;2;0;0;0m"
    snake = f"\033[48;2;256;256;256m"
    food = f"\033[48;2;256;0;0m"

    danger = [0, 0, 0, 0]
    current_dir = dir
    apple_dir = [0, 0, 0, 0]
    if (my_pos[0][1] - apple[1]) > 0:
        apple_dir[0] = 1
    elif (my_pos[0][1] - apple[1]) < 0:
        apple_dir[0] = 0
        apple_dir[2] = 1
    elif (my_pos[0][1] - apple[1]) == 0:
        pass
    if (my_pos[0][0] - apple[0]) > 0:
        apple_dir[3] = 1
    elif (my_pos[0][0] - apple[0]) < 0:
        apple_dir[3] = 0
        apple_dir[1] = 1
    elif (my_pos[0][0] - apple[0]) == 0:
        pass
    # data = np.array([*position.keys()], dtype=np.int8).reshape((cube, cube))
    pos = [*my_pos[0]]
    danger[0] = (pos[1] + 1) == cube
    danger[1] = (pos[0] - 1) == cube
    danger[2] = (pos[1] - 1) == cube
    danger[3] = (pos[0] + 1) == cube
    if not danger[0]:
        if (pos[0], pos[1]+1) in position:
            danger[0] = '256;256;256' in position[(pos[0], pos[1]+1)]# up
        else:
            danger[0] = True
    if not danger[1]:
        if (pos[0]-1, pos[1]) in position:
            danger[1] = '256;256;256' in position[(pos[0]-1, pos[1])]
        else:
            danger[1] = True# left
    if not danger[2]:
        if (pos[0], pos[1]-1) in position:
            danger[2] = '256;256;256' in position[(pos[0], pos[1]-1)] 
        else:
            danger[2] = True
        # dowm
    if not danger[3]:
        if (pos[0]+1, pos[1]) in position:
            danger[3] = '256;256;256' in position[(pos[0]+1, pos[1])]# right
        else:
            danger[3] = True
    data += [(*danger, *apple_dir, current_dir,)]
    
    return data
            
            

async def store_data(testing: bool=False):
    global position, sync, data
    blank = f"\033[48;2;0;0;0m"
    snake = f"\033[48;2;256;256;256m"
    food = f"\033[48;2;256;0;0m"
    async def encode_array(arr):
        return np.array([{blank: 0, snake: 1, food: 2}[i.replace('\033[0m', '').replace(to_char, '').replace('\n', '').strip()] for i in arr], dtype=np.int8).reshape((cube, cube, 1))
    data += [(await encode_array(position.values()), {'up': 0, 'left': 1, 'down': 2, 'right': 3}[dir])]
    
    if not testing:
        try:
            async with open('data.pickle', 'x') as f:pass
        except FileExistsError:pass
        # d = {''.join(v):i for i, v in enumerate(zip((blank, snake, food, '\033[0m'+blank, '\033[0m'+snake, '\033[0m'+food)*36, (*['']*6, *[f'\033[0m{to_char}']*6, *[f'\033[0m{to_char}\n']*6, *[to_char]*6, *[f'{to_char}\033[0m{to_char}']*6,*[f'{to_char}\033[0m']*6),))}
        
        while True:
            await asyncio.sleep(0.1)
            data += [(await encode_array(position.values()), {'up': 0, 'left': 1, 'down': 2, 'right': 3}[dir])]
    else:
        while True:
            data = []
            data += [await encode_array(position.values())]
            await asyncio.sleep(0.1)
def reset():
    global dead, eaten
    setup()
    eaten = False
    dead= False
    return 0,0,dead, eaten
to_call = []
sync = False
data = []
dead = False
done = False
async def main():
    global sync, data, to_call
    try:
        # to_call = [lambda x: {0: 'up', 1: 'left', 2: 'down', 3: 'right'}[x],map(np.argmax, feed)]
        task1 = asyncio.create_task(game())
        task2 = asyncio.create_task(move())
        # task3 = asyncio.create_task(get_current_state())
        await asyncio.wait([task1, task2])
    except BaseException:
        print(data[0])
        with open('data.pickle', 'wb') as f:pickle.dump(data[:-1], f)
        print('Game Over')

if __name__ == '__main__':
    asyncio.run(main())