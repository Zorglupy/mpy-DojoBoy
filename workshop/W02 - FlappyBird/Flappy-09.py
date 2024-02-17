#
#  Flappy Bird for DojoBoy v1.0 01/2024
#

from random import randint
from dojoboy_v1 import DojoBoy

djb = DojoBoy(show_intro=True,width=160,height=128)

PIPE_HOLE_SIZE = 40
PIPE_W = 26
PIPE_H = 100
ALPHA_COLOR = djb.display.color(0,0,0)
BACKGROUND_COLOR = djb.display.color(112,197,206)

djb.display.add_sprite_from_file("flappy1.bin", 19, 14)
djb.display.add_sprite_from_file("pipedown.bin", 26, 100)
djb.display.add_sprite_from_file("pipeup.bin", 26, 100)

def draw_pipe(p_x, p_y):
    djb.display.sprite(1, p_x, p_y, ALPHA_COLOR)
    djb.display.sprite(2, p_x, p_y+ PIPE_H + PIPE_HOLE_SIZE, ALPHA_COLOR)

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

VELOCITY_Y_UP = -3.0
velocity_y = 0
ACCELERATION_Y = 0.2

VELOCITY_PIPE_X = -2

game_over = False

pipe_1_pos_x, pipe_1_pos_y = create_pipe()
pipe_2_pos_x, pipe_2_pos_y = create_pipe()
pipe_2_pos_x = pipe_2_pos_x + (djb.display.width + 19)//2

while True:
    djb.display.fill(BACKGROUND_COLOR) # remplir l'ecran en noir
    djb.scan_jst_btn() # scan position joystick et boutons
    
    if djb.pressed(djb.btn_A):  # si joystick haut
        velocity_y = VELOCITY_Y_UP
        pos_y = pos_y + velocity_y  # reduit la valeur de pos_y

    velocity_y = velocity_y + ACCELERATION_Y
    pos_y = pos_y + velocity_y # augmente la valeur de pos_y
    
    pipe_1_pos_x = pipe_1_pos_x + VELOCITY_PIPE_X
    pipe_2_pos_x = pipe_2_pos_x + VELOCITY_PIPE_X
    
    if pos_y > djb.display.height - 14:
        pos_y = djb.display.height - 14
    
    if pipe_1_pos_x < -PIPE_W:
        pipe_1_pos_x, pipe_1_pos_y = create_pipe()
    if pipe_2_pos_x < -PIPE_W:
        pipe_2_pos_x, pipe_2_pos_y = create_pipe()

    draw_pipe(pipe_1_pos_x, pipe_1_pos_y)
    draw_pipe(pipe_2_pos_x, pipe_2_pos_y)
    
    djb.sprite(0, int(pos_x), int(pos_y), ALPHA_COLOR)

    if check_pipe_collision(pos_x, pos_y, pipe_1_pos_x, pipe_1_pos_y):
        game_over = True
    if check_pipe_collision(pos_x, pos_y, pipe_2_pos_x, pipe_2_pos_y):
        game_over = True

    if game_over:
        djb.display.center_text("GAME OVER",djb.display.WHITE_H)
        djb.display.show()
        break
    
    djb.display.show_and_wait() # affiche l'ecran a 30 image par seconde