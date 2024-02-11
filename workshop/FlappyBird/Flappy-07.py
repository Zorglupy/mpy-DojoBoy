from random import randint
from dojoboy_v1 import DojoBoy

djb = DojoBoy(False)

PIPE_HOLE_SIZE = 40
PIPE_W = 26
PIPE_H = 100

def draw_pipe(p_x, p_y):
    djb.display.rect(p_x,p_y, PIPE_W, PIPE_H, djb.display.RED_H, True)
    djb.display.rect(p_x,p_y + PIPE_H + PIPE_HOLE_SIZE, PIPE_W, PIPE_H, djb.display.RED_L, True)

def check_collision(x1,y1,w1,h1,x2,y2,w2,h2):
    return x1 + w1 >= x2 and x1 <= x2 + w2 and y1 + h1 >= y2 and y1 <= y2 + h2

def create_pipe():
    pos_x_p = djb.display.width
    pos_y_p = randint(-PIPE_H,-PIPE_H + djb.display.height//2)
    return pos_x_p, pos_y_p

def check_pipe_collision(p_x, p_y, p_p_x, p_p_y):
    g_over = False
    if check_collision(p_x, p_y, 19, 14, p_p_x, p_p_y, PIPE_W, PIPE_H):
        g_over = True
    if check_collision(p_x, p_y, 19, 14, p_p_x, p_p_y + PIPE_H + PIPE_HOLE_SIZE, PIPE_W, PIPE_H):
        g_over = True
    return g_over

pos_x = 50
pos_y = 50

VELOCITY_Y_UP = -2.4
velocity_y = 0
ACCELERATION_Y = 0.2

VELOCITY_PIPE_X = -2

game_over = False

pipe_1_pos_x, pipe_1_pos_y = create_pipe()
pipe_2_pos_x, pipe_2_pos_y = create_pipe()
pipe_2_pos_x = pipe_2_pos_x + (djb.display.width + 19)//2

while True:
    djb.display.fill(djb.display.BLACK) # remplir l'ecran en noir
    djb.scan_jst_btn() # scan position joystick et boutons
    
    if djb.pressed(djb.btn_A):  # si joystick haut
        velocity_y = VELOCITY_Y_UP
        pos_y = pos_y + velocity_y  # reduit la valeur de pos_y

    velocity_y = velocity_y + ACCELERATION_Y
    pos_y = pos_y + velocity_y # augmente la valeur de pos_y
    
    if pos_y > djb.display.height - 14:
        pos_y = djb.display.height - 14
    
    pipe_1_pos_x = pipe_1_pos_x + VELOCITY_PIPE_X
    pipe_2_pos_x = pipe_2_pos_x + VELOCITY_PIPE_X
    
    if pipe_1_pos_x < -PIPE_W:
        pipe_1_pos_x, pipe_1_pos_ = create_pipe()
    if pipe_2_pos_x < -PIPE_W:
        pipe_2_pos_x, pipe_2_pos_ = create_pipe()

    if check_pipe_collision(pos_x, pos_y, pipe_1_pos_x, pipe_1_pos_y):
        game_over = True
    if check_pipe_collision(pos_x, pos_y, pipe_2_pos_x, pipe_2_pos_y):
        game_over = True

    draw_pipe(pipe_1_pos_x, pipe_1_pos_y)
    draw_pipe(pipe_2_pos_x, pipe_2_pos_y)
    
    djb.display.rect(pos_x, int(pos_y), 19, 14, djb.display.YELLOW_H, True) # dessine un rectangle a la position pos_x , pos_y

    if game_over:
        djb.display.center_text("GAME OVER",djb.display.WHITE_H)
        djb.display.show()
        break
    
    djb.display.show_and_wait() # affiche l'ecran a 30 image par seconde