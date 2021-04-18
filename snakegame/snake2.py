"""
1.我们控制的是食物,而不是蛇
2.让蛇可以自动的加速
3.让蛇的身体可以自动的变长
4.蛇的大体移动的方向是食物所在的方向
"""



import random
import copy
from collections import deque

from blessed import Terminal

#定义所需要用到的常量
term = Terminal()
UP = term.KEY_UP
RIGHT = term.KEY_RIGHT
LEFT = term.KEY_LEFT
DOWN = term.KEY_DOWN
direction = RIGHT
MOVEMENT_MAP = {LEFT: [0, -1], UP: [-1, 0], RIGHT: [0, 1], DOWN: [1, 0]}
dead = False

BORDER = '-'
BODY = '*'
HEAD = '#'
APPLE = 'x'
SPACE = ' '

#定义snake的主体
snake = deque([[6, 5], [6, 4], [6, 3]])  #蛇
food = [5, 10]  #定义食物

h, w = 10, 15
#定义游戏一开始的分数
score = 0
#定义蛇的速度
speed = 3
MAX_SPEED = 6

#自动 -> 变量 -> 循环的轮数来实现蛇的速度和体长的变化

# turn -> turn % N2 < N1 -> speed = speed * 1.07
N1 = 1
N2 = 2

#turn % M == 0 增长蛇的体长
M = 9

#with上下文管理器
with term.cbreak(), term.hidden_cursor():

    print(term.home + term.clear)
    world = [[SPACE] * w for _ in range(h)]

    #绘制竖线
    for i in range(h):
        world[i][0] = BORDER
        world[i][-1] =BORDER

    #绘制横线
    for i in range(w):
        world[0][i] = BORDER
        world[-1][i] = BORDER

    #绘制蛇的位置
    for s in snake:
        world[s[0]][s[1]] = BODY
    #绘制头部的位置
    head = snake[0]
    world[head[0]][head[1]] = HEAD
    world[food[0]][food[1]] = APPLE

    #row是每一行
    for row in world:
        print(' '.join(row))

        # 定义变量
    val = ''
    # 定义moving是否移动
    moving = False
    turn = 0  # 当前游戏轮数
    # 循环判断
    while val.lower() != 'q':  # quit
        # 接收键盘的输入
        val = term.inkey(timeout=1 / speed)  # ctrl+鼠标左键点击
        # 判断按键输入的内容
        if val.code in [UP, DOWN, RIGHT, LEFT]:
            moving = True
        if not moving:
            continue  # 跳过此次循环

        #蛇想移动的方向 => 食物所在的位置 => 食物的坐标和蛇头的坐标
        head = snake[0]
        y_diff = food[0] - head[0]
        x_diff = food[1] - head[1]

        #蛇希望移动的方向
        want_move = None
        if abs(y_diff) > abs(x_diff):  #上或下 移动蛇
            if y_diff <= 0:
                want_move = UP

            else:
                want_move = DOWN

        else:
            if x_diff <= 0:
                want_move = LEFT
            else:
                want_move = RIGHT

        want_moves = [want_move] + [UP, DOWN, LEFT, RIGHT]
        next_move = None
        for move in want_moves:
            movement = MOVEMENT_MAP.get(move)
            head_copy = copy.copy(head)
            #移动蛇头
            head_copy[0] += movement[0]
            head_copy[1] += movement[1]

            #原本的内容
            heading = world[head_copy[0]][head_copy[1]]
            if heading == BORDER:
                continue
            elif heading == BODY:
                if head_copy == snake[-1] and turn % M != 0:
                    next_move = head_copy
                    break
                else:
                    continue

            else:
                next_move = head_copy
                break

        # 所有动作都尝试过了,依旧无法移动
        if next_move is None:
            break


        turn += 1

        # 在蛇具体移动前,需要清理一下当下食物所在的位置
        world[food[0]][food[1]] = SPACE

        snake.appendleft(next_move)
        world[head[0]][head[1]] = BODY
        if turn % M != 0:
            #蛇尾弹出,维持蛇的体长不变
            tail = snake.pop()
            world[tail[0]][tail[1]] = SPACE
        if turn % N2 < N1:
            #  修改速度让蛇变快
            speed = min(MAX_SPEED,speed * 1.07)
        world[next_move[0]][next_move[1]]


        food_copy = copy.copy(food)
        if val.code in [UP, DOWN, LEFT, RIGHT]:
            direction = val.code
            movement = MOVEMENT_MAP.get(direction)
            head_copy = copy.copy(head)
            food_copy[0] += movement[0]
            food_copy[1] += movement[1]

        food_heading = world[food_copy[0]][food_copy[1]]
        if food_heading == HEAD:
            dead = True

        if food_heading == BODY:
            dead = True
        #  只能移动到空白处
        if heading == SPACE:
                food = food_copy

        if not dead:
            world[food[0]][food[1]] = APPLE

        print(term.move_yx(0, 0))
        for row in world:
            print(' '.join(row))

        score = len(snake) - 3

        print(f'score: {score} - speed: {speed: .1f}')

        if dead:
            break

# 输出
print('game over')