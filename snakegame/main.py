import random
import copy
from collections import deque

from blessed import Terminal

#定义所需要用到的常量.
term = Terminal()
UP = term.KEY_UP
RIGHT = term.KEY_RIGHT
LEFT = term.KEY_LEFT
DOWN = term.KEY_DOWN
direction = RIGHT

BORDER = '-'
BODY = '*'
HEAD = '#'
APPLE = 'x'
SPACE = ' '

#定义snake的主体.
snake = deque([[6, 5], [6, 4], [6, 3]])  #蛇
food = [5, 10]  #定义食物

h, w = 10, 15
#定义游戏一开始的分数
score = 0
#定义蛇的速度
speed = 3
MAX_SPEED = 6

def list_empty_spaces(world,space):

    """收集 world 二维数组中为空的元素到 list 中"""
    res = []
    for i in range(len(world)):  #  循环二维列表的高度
        for j in range(len(world[i])):
            if world[i][j] == SPACE:
                res.append([i,j])
    return res

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

    #编写逻辑
    #定义变量
    val = ''
    #定义moving是否移动
    moving = False
    #循环判断
    while val.lower() != 'q':  #quit
    #接收键盘的输入
        val = term.inkey(timeout= 1 / speed )  #ctrl+鼠标左键点击
    # 判断按键输入的内容
        if val.code in [UP, DOWN, RIGHT, LEFT]:
            moving = True
        if not moving:
            continue  #跳过此次循环

    #判断移动方向 按了上键  => uP 并且 当前的方向向下
    #DOWN -> UP
        if val.code == UP and direction != DOWN:
            direction = UP
        if val.code == RIGHT and direction != LEFT:
            direction = RIGHT
        if val.code == LEFT and direction != RIGHT:
            direction = LEFT
        if val.code == DOWN and direction != UP:
            direction = DOWN

        #具体移动它 移动蛇的头部
        head = copy.copy(snake[0])
        if direction == UP:
            head[0] -= 1  # Y 轴需要 -1
        elif direction == RIGHT:
            head[1] += 1  # X 轴需要 +1
        elif direction == LEFT:
            head[1] -= 1
        elif direction == DOWN:
            head[0] += 1
        #蛇头移动之后,所在位置原本的内容
        heading = world[head[0]][head[1]]
        ate_food = False  #ate是eat的过去式
        if heading == APPLE:
            ate_food = True
            #获得当前情况下空的元素
            empty_spaces = list_empty_spaces(world, SPACE)
            #随机获得其中的一个元素
            food = random.choice(empty_spaces)
            #放置新的APPLE
            world[food[0]][food[1]] = APPLE
            speed = min(MAX_SPEED,speed * 1.07)
        elif heading == BORDER:
            break
            #撞到墙

        elif heading == BODY and head != snake[-1]:
             #蛇前进时,头会前进一格,尾巴也会前进一格
             #环 =>蛇头与蛇尾连在一起时, head == snake[-1]
            break

        if not ate_food:
            #  deque  [1,2,3] = >[0,1,2]
            #  将尾部弹出
            tail = snake.pop()  # *
            #将蛇尾变为空字符
            world[tail[0]][tail[1]] = SPACE

        snake.appendleft(head)

        #重新绘制
        for s in snake:
            world[s[0]][s[1]] = BODY
        head = snake[0]
        world[head[0]][head[1]] = HEAD
        print(term.move_yx(0, 0))

        #窗体二维矩阵重新绘制
        for row in world:
            print(' '.join(row))

        score = len(snake) - 3

        print(f'score{score} - speed: {speed: .1f}')

print('game over')

