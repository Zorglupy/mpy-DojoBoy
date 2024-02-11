from dojoboy_v1 import DojoBoy

djb = DojoBoy(False)

pos_x = 50
pos_y = 50

velocity_y = 2

while True:
    djb.display.fill(djb.display.BLACK) # remplir l'ecran en noir
    djb.scan_jst_btn() # scan si joystick ou boutons appuyés
    
    if djb.pressed(djb.btn_Up):  # si joystick haut
        pos_y = pos_y - velocity_y  # reduit la valeur de pos_y
    if djb.pressed(djb.btn_Down):  # si joystick bas
        pos_y = pos_y + velocity_y  # augmente la valeur de pos_y
    
    djb.display.rect(pos_x, int(pos_y), 19, 14, djb.display.YELLOW_H, True) # dessine un rectangle a la position pos_x , pos_y
    djb.display.show_and_wait() # affiche l'ecran a 30 image par seconde
    
