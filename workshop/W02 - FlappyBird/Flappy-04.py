from random import randint
from dojoboy_v1 import DojoBoy

djb = DojoBoy(False)

pos_x = 50
pos_y = 50

VELOCITY_Y_UP = -2.4
velocity_y = 0
ACCELERATION_Y = 0.2

VELOCITY_PIPE_X = -2
pipe_pos_x = djb.display.width
pipe_pos_y = 80

while True:
    djb.display.fill(djb.display.BLACK) # remplir l'ecran en noir
    djb.scan_jst_btn() # scan position joystick et boutons
    
    if djb.pressed(djb.btn_A):  # si joystick haut
        velocity_y = VELOCITY_Y_UP
        pos_y = pos_y + velocity_y  # reduit la valeur de pos_y

    velocity_y = velocity_y + ACCELERATION_Y
    pos_y = pos_y + velocity_y # augmente la valeur de pos_y
    
    pipe_pos_x = pipe_pos_x + VELOCITY_PIPE_X
    
    if pos_y > djb.display.height - 14:
        pos_y = djb.display.height - 14
    
    if pipe_pos_x < -26:
        pipe_pos_x = djb.display.width
        pipe_pos_y = randint(30, djb.display.height)
        
    djb.display.rect(pipe_pos_x,pipe_pos_y, 26, 100, djb.display.RED_H, True)
    
    djb.display.rect(pos_x, int(pos_y), 19, 14, djb.display.YELLOW_H, True) # dessine un rectangle a la position pos_x , pos_y
    djb.display.show_and_wait() # affiche l'ecran a 30 image par seconde