#
# snake-djb.py Game
# by Billy Cheung  2019 10 26
# Modified by Yoyo Zorglup for DojoBoy 2023 12 25
#

from dojoboy_v1.dojoboy import DojoBoy
from time import sleep_ms,ticks_ms, ticks_us, ticks_diff
from random import randint

djb = DojoBoy(show_intro=True,width=160,height=128,framerate=30)

#
# Initialisation de l'ecran
#

SNAKE_SIZE    = 10
SNAKE_LENGTH  = 4
SNAKE_EXTENT  = 2
COLS          = 0
ROWS          = 0
OX            = 0
OY            = 0

COLOR_BG      = djb.display.BLACK
COLOR_WALL    = djb.display.BLUE_H
COLOR_SNAKE   = djb.display.YELLOW_H
COLOR_APPLE   = djb.display.RED_H
COLOR_SCORE   = djb.display.WHITE_H
COLOR_LOST_BG = djb.display.RED_H
COLOR_LOST_FG = djb.display.BLACK

MODE_MENU     = 0
MODE_START    = 1
MODE_READY    = 2
MODE_PLAY     = 3
MODE_LOST     = 4
MODE_GAMEOVER = 5
MODE_EXIT     = 6

# ----------------------------------------------------------
# Game management
# ----------------------------------------------------------

def tick():
    handleButtons()

    if not game['refresh']:
        clearSnakeTail()
    if game['mode'] == MODE_PLAY:
        moveSnake()
        if game['refresh']:
            game['refresh'] = False
        if didSnakeEatApple():
            djb.play_tone('D6', 20)
            djb.play_tone('C5', 20)
            djb.play_tone('F4', 20)
            game['score'] += 1
            game['refresh'] = True
            extendSnakeTail()
            spawnApple()
        if didSnakeBiteItsTail() or didSnakeHitTheWall():
            djb.play_tone('C4', 500)
            game['mode'] = MODE_LOST
            game['refresh'] = True
    elif game['mode'] == MODE_LOST:
        # print ('LOST')
        game['life'] -= 1

        if game['life'] <= 0 :
            game['mode'] = MODE_GAMEOVER
        else :
            game['mode'] = MODE_START
        # print (game['mode'])
        sleep_ms(1000)
    elif game['mode'] == MODE_GAMEOVER:
        # print('gameOver')
        game['mode'] = MODE_MENU
        drawGameOver()
    elif game['mode'] == MODE_MENU:
        # print('Menu')
        pass
    elif game['mode'] == MODE_START:
        # print ("======================")
        game['refresh'] = True
        resetSnake()
        spawnApple()
        game['mode'] = MODE_READY
        game['score'] = 0
        game['time']  = 0
        if game['demo'] :
            game['demoOn'] = True
    elif game['mode'] == MODE_READY:
        # print ("READY")
        game['refresh'] = False
        moveSnake()
        if snakeHasMoved():
            djb.play_tone('C5', 100)
            game['mode'] = MODE_PLAY
    elif game['mode'] == MODE_EXIT:
        return
    else:
        handleButtons()

    draw()
    game['time'] += 1


def spawnApple():
    apple['x'] = randint (1, COLS - 2)
    apple['y'] = randint (1, ROWS - 2)

def smart():
    if randint(0,199) < 200 :
        return True
        return False

def noCrash (x,y):
    h = snake['head']
    n = snake['len']
    # hit walls ?
    if x < 0 or x > COLS-1 or y < 0 or y > ROWS-1:
        return False
    # hit snake body ?
    for i in range(n):
        if i !=h and snake['x'][i] == x and snake['y'][i] == y:
            return False
        i = (i + 1) % n
    return True

def handleButtons():
  global SNAKE_SIZE
  djb.scan_jst_btn()

  if game['mode'] == MODE_MENU :
    sleep_ms(10)
    if djb.setVolume() :
        pass
    elif djb.setFrameRate():
        pass
    elif djb.just_pressed(djb.btn_Up):
        SNAKE_SIZE = 4 if SNAKE_SIZE == 2 else 6 if SNAKE_SIZE == 4 else 2
        djb.play_tone('C5', 100)
    elif djb.just_pressed(djb.btn_Down):
        game['demo'] = not game['demo']
        djb.play_tone('E5', 100)
    elif djb.just_released(djb.btn_A) or game['demoOn'] :
        game['mode'] = MODE_START
        game['life'] = 3
        game['reset'] = True
        djb.play_tone('F5', 100)
        if game['demo'] :
            djb.display.fill(0)
            djb.display.text('DEMO', 5, 0, djb.display.WHITE_H)
            djb.display.text('B to Stop', 5, 30, djb.display.WHITE_H)
            djb.display.show()
            sleep_ms(1000)

    elif djb.pressed(djb.btn_Left) :
        game['mode'] = MODE_EXIT
        djb.play_tone('G5', 100)
  else :
    if game['demo'] :
        if djb.just_released (djb.btn_B):
            game['demoOn'] = False
            game['mode'] = MODE_GAMEOVER
            djb.play_tone('G5', 100)
            djb.play_tone('F5', 100)
            djb.play_tone('E5', 100)

        #get snake's head position
        h = snake['head']
        Hx = snake['x'][h]
        Hy = snake['y'][h]
        #get snake's neck position
        # # print ("h={} {}:{}  C={} R={}".format (h,Hx,Hy, COLS, ROWS))

        # move closer to the apple, if smart enough
        if Hx < apple['x'] and smart() and noCrash(Hx+1, Hy):
            dirSnake(1, 0)
            # # print ("A")
        elif Hx > apple['x'] and smart() and noCrash(Hx-1, Hy):
            dirSnake(-1, 0)
            # # print ("B")
        elif Hy < apple['y'] and smart() and noCrash(Hx, Hy+1):
            dirSnake(0, 1)
            # # print ("C")
        elif Hy > apple['y'] and smart() and noCrash(Hx, Hy-1):
            dirSnake(0, -1)
            # # print ("D")
        elif  noCrash(Hx+1, Hy):
            dirSnake(1, 0)
            # # print ("E")
        elif noCrash(Hx-1, Hy):
            dirSnake(-1, 0)
            # # print ("F")
        elif noCrash(Hx, Hy+1):
            dirSnake(0, 1)
            # # print ("G")
        elif noCrash(Hx, Hy-1):
            dirSnake(0, -1)
            # # print ("H")
    else :
        if djb.just_pressed (djb.btn_Left):
            dirSnake(-1, 0)
        elif djb.just_pressed(djb.btn_Right):
            dirSnake(1, 0)
        elif djb.just_pressed(djb.btn_Up):
            dirSnake(0, -1)
        elif djb.just_pressed(djb.btn_Down):
            dirSnake(0, 1)
        elif djb.just_pressed(djb.btn_A):
            if snake['vx'] == 1:
                dirSnake(0, 1)
            elif snake['vx'] == -1:
                dirSnake(0, -1)
            elif snake['vy'] == 1:
                dirSnake(-1, 0)
            elif snake['vy'] == -1:
                dirSnake(1, 0)
            elif snake['vx']==0 and snake['vy']==0 :
                dirSnake(0, 1)
        elif djb.just_pressed(djb.btn_B):
            if snake['vx'] == 1:
                dirSnake(0, -1)
            elif snake['vx'] == -1:
                dirSnake(0, 1)
            elif snake['vy'] == 1:
                dirSnake(1, 0)
            elif snake['vy'] == -1:
                dirSnake(-1, 0)
            elif snake['vx']==0 and snake['vy']==0 :
                dirSnake(1, 0)

# ----------------------------------------------------------
# Snake management
# ----------------------------------------------------------

def resetSnake():
    global COLS, ROWS, OX, OY
    COLS          = (djb.display.width  - 4) // SNAKE_SIZE
    ROWS          = (djb.display.height - 4) // SNAKE_SIZE
    OX            = (djb.display.width  - COLS * SNAKE_SIZE) // 2
    OY            = (djb.display.height - ROWS * SNAKE_SIZE) // 2
    x = COLS // SNAKE_SIZE
    y = ROWS // SNAKE_SIZE
    snake['vx'] = 0
    snake['vy'] = 0
    # print (game['reset'])
    if game['reset'] :
        game['reset'] = False
        s = SNAKE_LENGTH
    else :
        s = snake['len']

    snake['x'] = []
    snake['y'] = []
    for _ in range(s):
        snake['x'].append(x)
        snake['y'].append(y)
        snake['head'] = s - 1
        snake['len']  = s

def dirSnake(dx, dy):
    snake['vx'] = dx
    snake['vy'] = dy

def moveSnake():
    h = snake['head']
    x = snake['x'][h]
    y = snake['y'][h]
    h = (h + 1) % snake['len']
    snake['x'][h] = x + snake['vx']
    snake['y'][h] = y + snake['vy']
    snake['head'] = h

def snakeHasMoved():
    return snake['vx'] or snake['vy']

def didSnakeEatApple():
    h = snake['head']
    return snake['x'][h] == apple['x'] and snake['y'][h] == apple['y']

def extendSnakeTail():
    i = snake['head']
    n = snake['len']
    i = (i + 1) % n
    x = snake['x'][i]
    y = snake['y'][i]
    for _ in range(SNAKE_EXTENT):
        snake['x'].insert(i, x)
        snake['y'].insert(i, y)
    snake['len'] += SNAKE_EXTENT

def didSnakeBiteItsTail():
    h = snake['head']
    n = snake['len']
    x = snake['x'][h]
    y = snake['y'][h]
    i = (h + 1) % n
    for _ in range(n-1):
        if snake['x'][i] == x and snake['y'][i] == y:
            return True
        i = (i + 1) % n
    return False

def didSnakeHitTheWall():
    h = snake['head']
    x = snake['x'][h]
    y = snake['y'][h]
    return x < 0 or x == COLS or y < 0 or y == ROWS

# ----------------------------------------------------------
# Graphic display
# ----------------------------------------------------------

def draw():
    if game['mode'] == MODE_MENU:
        drawGameMenu()
    else :
        if game['mode'] == MODE_LOST:
            if game['life'] == 0 :
                drawGameover()
        elif game['refresh']:
            clearScreen()
            drawWalls()
            drawSnake()
        else:
            drawSnakeHead()
        drawScore()
        drawApple()
    #display.show()

def clearScreen():
    color = COLOR_LOST_BG if game['mode'] == MODE_LOST else COLOR_BG
    djb.display.fill(color)

def drawGameMenu():
    global SNAKE_SIZE
    clearScreen()
    djb.display.center_text_XY('SNAKE', -1, 16, COLOR_APPLE, 2)
    djb.display.rect(djb.display.width//2 - 50,10,100,26, COLOR_WALL)
    
    djb.display.rect(djb.display.width - djb.max_vol * 5 - 4, 0, djb.max_vol * 5 + 2, 6,COLOR_SCORE)
    djb.display.rect(djb.display.width - djb.max_vol * 5 - 3,1, djb.vol[0] * 5, 4,COLOR_APPLE, True)

    djb.display.text("Button A:START  ",0,40,COLOR_SCORE)
    if game['demo'] :
        djb.display.text('Button Dw:AI-PLAYER', 0,50, COLOR_WALL)
    else :
        djb.display.text('Button Dw:1-PLAYER', 0,50, COLOR_SCORE)
    djb.display.text("Button Up:SIZE{}".format(SNAKE_SIZE),0,60, COLOR_SCORE)
    djb.display.text("Button M+U/D:FR{}".format(djb.display.frame_rate),0,70, COLOR_SCORE)
    djb.display.text("Button V+U/D:VOL",0,80, COLOR_SCORE)
    djb.display.text("Button Up+Dw:EXIT",0,90, COLOR_APPLE)

def drawGameOver():
    djb.display.fill(djb.display.RED_H)
    djb.display.rect(0, 48,184,28, djb.display.BLACK, True)
    djb.display.center_text('GAME OVER', COLOR_APPLE, 2)
    djb.display.show()
    djb.play_tone('C4', 100)
    djb.play_tone('E4', 100)
    djb.play_tone('G4', 100)
    sleep_ms(3000)

def drawWalls():
    color = COLOR_LOST_FG if game['mode'] == MODE_LOST else COLOR_WALL
    djb.display.rect(0, 0, djb.display.width, djb.display.height,color)

def debugSnake():
    n = snake['len']
    i = snake['head']
    for _ in range(n):

        # # print(snake['x'][i], snake['y'][i])
        if (i - 1) < 0 :
            i=n-1
        else :
            i-=1

def drawSnake():
    isTimeToBlink = game['time'] % 4 < 2
    color = COLOR_LOST_FG if game['mode'] == MODE_LOST and isTimeToBlink else COLOR_SNAKE
    h = snake['head']
    n = snake['len']
    for i in range(n):
        if i == h :
          drawBox(snake['x'][i], snake['y'][i], color)
        else :
          drawDot(snake['x'][i], snake['y'][i], color)

def drawSnakeHead():
    h = snake['head']
    drawBox(snake['x'][h], snake['y'][h], COLOR_SNAKE)

def clearSnakeTail():
    h = snake['head']
    n = snake['len']
    t = (h + 1) % n
    drawDot(snake['x'][t], snake['y'][t], COLOR_BG)

def drawScore():
    djb.display.text('Score {}'.format(game['score']),5,2,COLOR_SCORE)
    djb.display.text('Level {}'.format(game['life']),80,2,COLOR_SCORE)

def drawApple():
    drawBox(apple['x'], apple['y'], COLOR_APPLE)
    djb.display.rect(OX + apple['x']* SNAKE_SIZE + int(SNAKE_SIZE/2), OY + apple['y'] * SNAKE_SIZE-1, 1,1, COLOR_APPLE)

def drawDot(x, y, color):
    djb.display.fill_rect(OX + x * SNAKE_SIZE, OY + y * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE,color)

def drawBox(x, y, color):
    djb.display.rect(OX + x * SNAKE_SIZE, OY + y * SNAKE_SIZE, SNAKE_SIZE, SNAKE_SIZE,color)


# ----------------------------------------------------------
# Initialization
# ----------------------------------------------------------

game = {
    'mode':    MODE_MENU,
    'score':   0,
    'life':    0,
    'time':    0,
    'refresh': True,
    'reset':   True,
    'demo':    False,
    'demoOn' : False
}

snake = {
    'x':    [],
    'y':    [],
    'head': 0,
    'len':  0,
    'vx':   0,
    'vy':   0
}

apple = { 'x': 0, 'y': 0 }

# ----------------------------------------------------------
# Main loop
# ----------------------------------------------------------
while game['mode'] != MODE_EXIT :
  tick()
  djb.display.show_and_wait()
                                                                                          