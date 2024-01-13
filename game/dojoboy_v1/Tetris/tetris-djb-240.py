# Original source code for tetris.py by Vincent Mistler for YouMakeTech
# Modified By HalloSpaceBoy for the PicoBoy
# Modified By Yoyo Zorglup for DojoBoy 25 12 2023
from micropython import const
from dojoboy_v1.dojoboy import DojoBoy
import time
import os
from random import randint
import machine
#import _thread
import gc

#from rpmidi import RPMidi

#os.rename("./main.py", "./tetris.py")
#os.rename("./title.py", "./main.py")

BLOCK_SIZE = 12 # Size of a single tetromino block in pixels
GRID_OFFSET = 2
GRID_ROWS  = 20
GRID_COLS  = 10
currentmusic=[0xF0]

djb = DojoBoy(show_intro=True,width=240,height=240,framerate=30)

#midi=RPMidi()

# image definitions 12x12 pixels
theme=[0x90,76, 1,9, 0x91,64, 0,245, 0x92,71, 0x80, 0,16, 0x81, 0,218, 0x82, 0,16, 0x90,72, 0x91,64, 0,234, 0x80, 
0,11, 0x90,74, 0,15, 0x81, 0,235, 0x91,64, 0,250, 0x92,72, 0x80, 0,10, 0x81, 0,219, 0x82, 0,15, 0x90,71, 
0x91,64, 0,235, 0x80, 0,15, 0x90,69, 0,11, 0x81, 0,255, 0x91,57, 0,245, 0x90,69, 0,16, 0x81, 0,218, 0x80, 
0,16, 0x90,72, 0x91,57, 0,234, 0x80, 0,11, 0x90,76, 0,15, 0x81, 0,235, 0x91,57, 0,250, 0x92,74, 0x80, 0,10, 
0x81, 0,219, 0x82, 0,15, 0x90,72, 0x91,57, 0,235, 0x80, 0,15, 0x90,71, 0,11, 0x81, 0,255, 0x91,56, 0,245, 
0x90,71, 0,16, 0x81, 0,218, 0x80, 0,16, 0x90,72, 0x91,56, 0,234, 0x80, 0,11, 0x90,74, 0,15, 0x81, 0,235, 
0x91,56, 0,250, 0x90,76, 0,10, 0x81, 0,234, 0x91,56, 0,245, 0x80, 0,5, 0x90,72, 0,11, 0x81, 0,255, 0x91,57, 
0,245, 0x92,69, 0x80, 0,16, 0x81, 0,234, 0x90,57, 0,245, 0x91,69, 0x82, 0,15, 0x80, 0,235, 0x90,57, 0,250, 
0x91,59, 0,10, 0x80, 0,203, 0x81, 0,31, 0x90,60, 0,219, 0x80, 1,36, 0x90,74, 0,5, 0x91,62, 1,5, 0x81, 
0,229, 0x90,77, 0,5, 0x91,62, 0,229, 0x80, 0,16, 0x90,81, 0,15, 0x81, 0,235, 0x91,62, 0,229, 0x80, 0,15, 
0x90,79, 0,16, 0x81, 0,234, 0x90,62, 0,16, 0x91,77, 0,229, 0x81, 0,16, 0x91,76, 0x80, 0,250, 0x90,60, 1,4, 
0x80, 0,235, 0x90,72, 0x91,60, 0,229, 0x80, 0,15, 0x90,76, 0,16, 0x81, 0,234, 0x91,60, 0,219, 0x80, 0,21, 
0x81, 0,10, 0x90,74, 0,235, 0x80, 0,10, 0x90,72, 0,21, 0x91,60, 0,214, 0x80, 0,15, 0x90,71, 0,32, 0x81, 
0,229, 0x91,56, 1,4, 0x81, 0,219, 0x90,72, 0,15, 0x91,56, 0,219, 0x80, 0,16, 0x90,74, 0,26, 0x81, 0,255, 
0x91,56, 0,219, 0x80, 0,15, 0x90,76, 0,27, 0x81, 0,234, 0x91,56, 0,234, 0x92,72, 0x80, 0,26, 0x81, 0,235, 
0x90,57, 0,234, 0x91,69, 0x82, 0,26, 0x80, 0,234, 0x90,57, 0,235, 0x91,69, 0,26, 0x80, 0,255, 0x90,57, 0,229, 
0x81, 0,32, 0x80, 0,234, 0x90,57, 0,239, 0x91,76, 0,21, 0x80, 0,250, 0x90,57, 1,10, 0x80, 0,229, 0x90,57, 
0,208, 0x81, 0,32, 0x91,72, 0,26, 0x80, 0,234, 0x90,57, 1,5, 0x80, 0,234, 0x90,57, 0,208, 0x81, 0,31, 
0x91,74, 0,21, 0x80, 0,250, 0x90,56, 1,10, 0x80, 0,229, 0x90,56, 0,203, 0x81, 0,37, 0x91,71, 0,26, 0x80, 
0,234, 0x90,56, 1,5, 0x80, 0,234, 0x90,56, 0,203, 0x81, 0,36, 0x91,72, 0,21, 0x80, 0,250, 0x90,57, 1,10, 
0x80, 0,229, 0x90,57, 0,208, 0x81, 0,32, 0x91,69, 0,26, 0x80, 0,234, 0x90,57, 1,5, 0x80, 0,234, 0x90,57, 
0,203, 0x81, 0,36, 0x91,68, 0,21, 0x80, 0,250, 0x90,56, 1,10, 0x80, 0,229, 0x90,56, 0,172, 0x81, 0,68, 
0x91,71, 0,26, 0x80, 0,234, 0x90,56, 1,5, 0x80, 0,234, 0x90,56, 0,208, 0x81, 0,31, 0x91,76, 0,21, 0x80, 
0,250, 0x90,57, 1,10, 0x80, 0,229, 0x90,57, 0,208, 0x81, 0,32, 0x91,72, 0,26, 0x80, 0,234, 0x90,57, 1,5, 
0x80, 0,234, 0x90,57, 0,182, 0x81, 0,57, 0x91,74, 0,73, 0x80, 0,198, 0x90,56, 1,10, 0x80, 0,229, 0x90,56, 
0,203, 0x81, 0,37, 0x91,71, 0,26, 0x80, 0,234, 0x90,56, 1,4, 0x80, 0,235, 0x90,56, 0,135, 0x80, 0,42, 
0x81, 0,62, 0x90,72, 1,213, 0x80, 0,42, 0x90,76, 1,239, 0x90,81, 3,221, 0x80, 0,5, 0x90,80, 7,203, 0x80, 
0xF0]

djb.display.add_sprite_from_file('tetris_wall.bin',12,12) #0
djb.display.add_sprite_from_file('bottom_border.bin',12,12) #1
djb.display.add_sprite_from_file('corner.bin',12,12) #2
djb.display.add_sprite_from_file('left_border.bin',12,12) #3
djb.display.add_sprite_from_file('right_border.bin',12,12) #4
djb.display.add_sprite_from_file('top_border.bin',12,12) #5

field = [[-1 for col in range(GRID_COLS)] for row in range(GRID_ROWS)]

# shape of the 7 tetrominos
# [0][1]
# [2][3]
# [4][5]
# [6][7]
# e.g. [3,4,5,7] is:
#    [ ]
# [ ][ ]
#    [ ]
tetrominos = [[1,3,5,7],
              [2,4,5,7],
              [3,5,4,6],
              [3,5,4,7],
              [2,3,5,7],
              [3,5,7,6],
              [2,3,4,5]]

# Game Boy Color Tetrominos colors
tetrominos_colors =[djb.display.color(239,146,132),
             djb.display.color(222,146,239),
             djb.display.color(239,170,132),
             djb.display.color(165,211,132),
             djb.display.color(99,219,222),
             djb.display.color(231,97,115),
             djb.display.color(0,0,0)]

# Color scheme
GRID_BACKGROUND_COLOR = djb.display.color(255,211,132)
BACKGROUND_COLOR = djb.display.color(99,154,132)
BACKGROUND_COLOR2 = djb.display.color(57,89,41)
TEXT_COLOR = djb.display.BLACK
TEXT_BACKGROUND_COLOR = djb.display.WHITE

lines = 0
level = 0
score = 0
music=True
last_button="NONE"
has_rotated=False
now = time.ticks_ms()
n =randint(0, 6)
next_n = randint(0, 6)
x=[0,0,0,0]
y=[0,0,0,0]
prev_x=[0,0,0,0]
prev_y=[0,0,0,0]
for i in range(0,4):
    x[i]=(tetrominos[n][i]) % 2;
    y[i]=int(tetrominos[n][i] / 2);
    
    x[i]+=int(GRID_COLS/2)
    
currentmusic=[0xF0]

'''
def play_music():
    global midi
    global currentmusic
    global theme
    while True:
        del midi
        midi=RPMidi()
        try:
            midi.play_song(currentmusic)
        except:
            currentmusic=theme
            

def no_music():
    global currentmusic
    global rept
    try:
        currentmusic=[0xF0]
        midi.stop_all_music()
        #midi.stop_all()
    except:
        "foo"
'''

def append_to_board(score):
    try:
        with open("highscorestetris.sc", "r") as s:
            scores=s.read()
        scores=scores.split("\n")
        for r in range(len(scores)):
            try:
                scores[r]=int(scores[r])
            except:
                "foo"
        newscores=scores
        newscores.append(int(score))
        newscores.sort(reverse=True)
        for i in range(len(newscores)): newscores[i]=str(newscores[i])
        with open("highscorestetris.sc", "w+") as w:
            w.write("\n".join(newscores[:10]))
    except:
        return

def view_scores():
    #x=open("highscorestetris.sc", "r")
    #scores=x.read()
    #x.close()
    #del x
    scores = "100"
    scores=scores.split("\n")
    while True:
        djb.scan_jst_btn()
        if djb.pressed(djb.btn_B):
            time.sleep(0.1)
            return
        if djb.pressed(djb.btn_Home):
            homebootstop=open("/noboot", "w")
            homebootstop.close()
            djb.display.fill(djb.display.BLACK)
            djb.display.show()
            machine.reset()
            break
        djb.display.fill(djb.display.BLACK)
        djb.display.center_text_XY("High Scores:", -1, 15, djb.display.WHITE)
        for i in range(len(scores)):
            djb.display.center_text_XY("Score "+str(i+1)+": "+str(scores[i]), -1, 50+i*15, djb.display.WHITE)
        djb.display.center_text_XY("Press B to exit", -1, 220, djb.display.WHITE)
        djb.display.show()

def pause_screen():
    global currentmusic
    no_music()
    djb.display.fill_rect(10,90,220,80,djb.display.BLACK)
    djb.display.center_text_XY("Game Paused",djb.display.WHITE)
    djb.display.center_text_XY("Press Start or Menu", -1, 135, djb.display.WHITE)
    djb.display.center_text_XY("to resume.", -1, 147, djb.display.WHITE)
    djb.display.show()
    time.sleep(0.5)
    while True:
        djb.scan_jst_btn()
        if djb.pressed(djb.btn_Home):
            homebootstop=open("/noboot", "w")
            homebootstop.close()
            djb.display.fill(djb.display.BLACK)
            djb.display.show()
            machine.reset()
            break
        elif djb.pressed(djb.btn_Menu) or djb.pressed(djb.btn_Start):
            time.sleep(0.5)
            return

def collision(x,y):
    for i in range(4):
        # check collision against the border
        if x[i]<0 or x[i]>=GRID_COLS or y[i]>=GRID_ROWS:
            return True
        # check collision against another triomino
        if field[y[i]][x[i]]>=0:
            return True         
    return False

def title_screen():
    # title screen
    now = time.ticks_ms()
    while True:
        djb.scan_jst_btn()
        if djb.pressed(djb.btn_Home):
            homebootstop=open("/noboot", "w")
            homebootstop.close()
            djb.display.fill(djb.display.BLACK)
            djb.display.show()
            machine.reset()
            break
        djb.display.load_image("tetris_title.bin")
        djb.display.show()
        
        if time.ticks_diff(time.ticks_ms(), now) > 200:
            now = time.ticks_ms()
            djb.display.center_text("PRESS ANY BUTTON",djb.display.WHITE)
            djb.display.show()
            while time.ticks_diff(time.ticks_ms(), now) < 200:
                time.sleep(0.020)
            now = time.ticks_ms()
        if djb.pressed(djb.btn_Menu) or djb.pressed(djb.btn_Start):
            view_scores()
        elif djb.pressed(djb.btn_A):
            break
            
def game_over_screen():
    global midi
    global music
    global musicthread
    global score
    global lines
    global level
    global currentmusic
    #no_music()
    '''
    djb.display.fill(djb.display.BLACK)
    djb.display.center_text_XY("GAME OVER",-1,85,djb.display.RED_H)
    djb.display.text("Press A to play again.", 35, 105, djb.display.WHITE)
    djb.display.text("Press home to quit.", 40, 120, djb.display.WHITE)
    djb.display.center_text_XY("Press Menu/start", -1, 135, djb.display.WHITE)
    djb.display.center_text_XY("to view scores.", -1, 150, djb.display.WHITE)
    djb.display.center_text_XY("Score: "+str(score), -1, 165, djb.display.CYAN_H)
    djb.display.show()
    '''
    append_to_board(score)
    while True:
        djb.scan_jst_btn()
        djb.display.fill(djb.display.BLACK)
        djb.display.center_text_XY("GAME OVER",-1,85,djb.display.RED_H)
        djb.display.text("Press A to play again.", 35, 105, djb.display.WHITE)
        djb.display.text("Press home to quit.", 40, 120, djb.display.WHITE)
        djb.display.center_text_XY("Press Menu/start", -1, 135, djb.display.WHITE)
        djb.display.center_text_XY("to view scores.", -1, 150, djb.display.WHITE)
        djb.display.center_text_XY("Score: "+str(score), -1, 165, djb.display.CYAN_H)
        djb.display.show()
        if djb.pressed(djb.btn_Home):
            homebootstop=open("/noboot", "w")
            homebootstop.close()
            djb.display.fill(djb.display.BLACK)
            djb.display.show()
            machine.reset()
            break
        if djb.pressed(djb.btn_Menu) or djb.pressed(djb.btn_Start):
            view_scores()
        elif djb.pressed(djb.btn_A):
            lines=0
            level=0
            score=0
            print("A")
            clear_lines()
            break
def draw_background():
    djb.display.fill(BACKGROUND_COLOR)
    
    for i in range(0,int(240/BLOCK_SIZE),2):
        for j in range(0,int(240/BLOCK_SIZE),2):
            djb.display.fill_rect(j*BLOCK_SIZE,i*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE,BACKGROUND_COLOR2)
            djb.display.fill_rect((j+1)*BLOCK_SIZE,(i+1)*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE,BACKGROUND_COLOR2)
            
    djb.display.fill_rect(GRID_OFFSET*BLOCK_SIZE,0,
                  GRID_COLS*BLOCK_SIZE,GRID_ROWS*BLOCK_SIZE,
                  GRID_BACKGROUND_COLOR)
    
    # add walls
    for i in range(GRID_ROWS):
        djb.display.sprite(0,(GRID_OFFSET-1)*BLOCK_SIZE,i*BLOCK_SIZE)
        djb.display.sprite(0,(GRID_OFFSET+GRID_COLS)*BLOCK_SIZE,i*BLOCK_SIZE)
    
    # draw text (LINES)
    djb.display.fill_rect((GRID_OFFSET+GRID_COLS+1)*BLOCK_SIZE+1,16*BLOCK_SIZE,
                  BLOCK_SIZE*7,BLOCK_SIZE*2,
                  TEXT_BACKGROUND_COLOR)
    djb.display.text("LINES",(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE+1,16*BLOCK_SIZE+1,TEXT_COLOR)
    djb.display.text("%8s" % lines,(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE+1,17*BLOCK_SIZE+1,TEXT_COLOR)
    
    # draw text (LEVEL)
    djb.display.fill_rect((GRID_OFFSET+GRID_COLS+1)*BLOCK_SIZE+1,13*BLOCK_SIZE,
                  BLOCK_SIZE*7,BLOCK_SIZE*2,
                  TEXT_BACKGROUND_COLOR)
    djb.display.text("LEVEL",(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE+1,13*BLOCK_SIZE+1,TEXT_COLOR)
    djb.display.text("%8s" % level,(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE+1,14*BLOCK_SIZE+1,TEXT_COLOR)
    
    # draw text (SCORE)
    djb.display.fill_rect((GRID_OFFSET+GRID_COLS+1)*BLOCK_SIZE+1,10*BLOCK_SIZE,
                  BLOCK_SIZE*7,BLOCK_SIZE*2,
                  TEXT_BACKGROUND_COLOR)
    djb.display.text("SCORE",(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE+1,10*BLOCK_SIZE+1,TEXT_COLOR)
    djb.display.text("%8s" % score,(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE+1,11*BLOCK_SIZE+1,TEXT_COLOR)
    
    # next tetromino box
    djb.display.fill_rect((GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE,2*BLOCK_SIZE,
                  BLOCK_SIZE*6 ,BLOCK_SIZE*7,TEXT_BACKGROUND_COLOR)
    
    djb.display.sprite(2,(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE,2*BLOCK_SIZE) #upper left corner
    djb.display.sprite(5,(GRID_OFFSET+GRID_COLS+3)*BLOCK_SIZE,2*BLOCK_SIZE) #top border
    djb.display.sprite(5,(GRID_OFFSET+GRID_COLS+4)*BLOCK_SIZE,2*BLOCK_SIZE) #
    djb.display.sprite(5,(GRID_OFFSET+GRID_COLS+5)*BLOCK_SIZE,2*BLOCK_SIZE) #
    djb.display.sprite(5,(GRID_OFFSET+GRID_COLS+6)*BLOCK_SIZE,2*BLOCK_SIZE) #
    djb.display.sprite(2,(GRID_OFFSET+GRID_COLS+7)*BLOCK_SIZE,2*BLOCK_SIZE) #upper right corner
    
    djb.display.sprite(2,(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE,8*BLOCK_SIZE) #lower left corner
    djb.display.sprite(1,(GRID_OFFSET+GRID_COLS+3)*BLOCK_SIZE,8*BLOCK_SIZE) #lower border
    djb.display.sprite(1,(GRID_OFFSET+GRID_COLS+4)*BLOCK_SIZE,8*BLOCK_SIZE) #
    djb.display.sprite(1,(GRID_OFFSET+GRID_COLS+5)*BLOCK_SIZE,8*BLOCK_SIZE) #
    djb.display.sprite(1,(GRID_OFFSET+GRID_COLS+6)*BLOCK_SIZE,8*BLOCK_SIZE) #
    djb.display.sprite(2,(GRID_OFFSET+GRID_COLS+7)*BLOCK_SIZE,8*BLOCK_SIZE) #lower right corner
    
    for k in range(3,8):
        djb.display.sprite(3,(GRID_OFFSET+GRID_COLS+2)*BLOCK_SIZE,k*BLOCK_SIZE) #left border
        djb.display.sprite(4,(GRID_OFFSET+GRID_COLS+7)*BLOCK_SIZE,k*BLOCK_SIZE) #right border
    
    for i in range(4):
        draw_block((GRID_OFFSET+GRID_COLS+2)+tetrominos[next_n][i] % 2,
                   3+int(tetrominos[next_n][i] / 2), next_n)

def draw_block(j,i,n):
    # draw a tetris block of type n at the ith row and jth column
    # of the grid

    x = (GRID_OFFSET+j)*BLOCK_SIZE
    y = i*BLOCK_SIZE
    
    djb.display.fill_rect(x,y,BLOCK_SIZE,BLOCK_SIZE,tetrominos_colors[n]) # main color
    djb.display.rect(x,y,BLOCK_SIZE,BLOCK_SIZE,djb.display.
                     BLACK) # black border
    djb.display.line(x+3,y+3,x+5,y+3,djb.display.WHITE)
    djb.display.line(x+3,y+3,x+3,y+5,djb.display.WHITE)
 
 # show title screen and wait for a button

def clear_lines():
    for i in range(20):
        try:
            k=GRID_ROWS-i
            for i in range(GRID_ROWS-1,0,-1):
                count=0
                for j in range(GRID_COLS):
                    if field[i][j]>=0:
                        count+=1
                    field[k][j]=field[i][j]
        except:
            print("out of range")

def main_game():
    global last_button
    global delay
    global now
    global n
    global next_n
    global has_rotated
    global musicthread
    global score
    global lines
    global BLOCK_SIZE
    global GRID_OFFSET
    global GRID_ROWS
    global GRID_COLS
    global currentmusic
    global theme
    #no_music()
    draw_background()
    djb.display.show()
    # game loop
    while True:
        currentmusic=theme
        djb.scan_jst_btn()
        if djb.pressed(djb.btn_Home):
            homebootstop=open("/noboot", "w")
            homebootstop.close()
            djb.display.fill(djb.display.BLACK)
            djb.display.show()
            machine.reset()
            break
        if djb.pressed(djb.btn_Menu) or djb.pressed(djb.btn_Start):
            pause_screen()
        dx=0
        dy=1
        rotate=False

        if djb.pressed(djb.btn_A) and not n==6:
            if last_button!="UP":
                rotate=True
            last_button="UP"
        elif djb.pressed(djb.btn_Left):
                last_button="RIGHT"
                dx=-1
        elif djb.pressed(djb.btn_Right):
                last_button="RIGHT"
                dx=1
        elif djb.pressed(djb.btn_Down):
            last_button="DOWN"
            delay=0
        else:
            last_button="NONE"
        if djb.pressed(djb.btn_B) or djb.pressed(djb.btn_Down):
            delay=50
        else:
            delay=500

        # save current position to restore it
        # in case the requested move generates a collision
        for i in range(4):
            prev_x[i] = x[i]
            prev_y[i] = y[i]
        
        # move left & right
        for i in range(4):
            x[i]+=dx
            
        if collision(x, y):
            # collision detected => impossible move
            # => restore previous position
            for i in range(4):
                x[i] = prev_x[i]
                y[i] = prev_y[i]
            
        # rotate
        if rotate:
            # center of rotation
            x0 = x[1]
            y0 = y[1]
            for i in range(4):
                x_=y[i]-y0
                y_=x[i]-x0
                x[i]=x0-x_
                y[i]=y0+y_
            
            if collision(x, y):
                # collision detected => impossible move
                # => restore previous position
                for i in range(4):
                    x[i] = prev_x[i]
                    y[i] = prev_y[i]
            else:
                has_rotated=True

        # move down
        ticks_ms = time.ticks_ms()
        if time.ticks_diff(ticks_ms, now) > delay:
            now = ticks_ms
            
            if has_rotated:
                freq=180
            elif delay>0:
                freq=140
            else:
                freq=0
            has_rotated = False
            
            for i in range(4):
                prev_x[i]=x[i]
                prev_y[i]=y[i]
                y[i]+=dy
               
            if collision(x,y):
                # collision detected
                
                # collision at the top of the screen?
                # => game over
                for i in range(4):
                    if prev_y[i]<=1:
                        return
                
                # => Store the last good position in the field
                for i in range(4):
                    field[prev_y[i]][prev_x[i]]=n
                
                # => choose randomly the next trinomino
                n = next_n
                next_n = randint(0, 6)
                for i in range(4):
                    x[i]=(tetrominos[n][i]) % 2;
                    y[i]=int(tetrominos[n][i] / 2);
                    
                    x[i]+=int(GRID_COLS/2)
            
        # check lines
        k=GRID_ROWS-1
        for i in range(GRID_ROWS-1,0,-1):
            count=0
            for j in range(GRID_COLS):
                if field[i][j]>=0:
                    count+=1
                field[k][j]=field[i][j]
            if count<GRID_COLS:
                k-=1
            else:
                # ith line complete
                lines+=1
                score+=40
                
                # make the line blink white <-> black
                
                for l in range(3):
                    djb.display.fill_rect(GRID_OFFSET*BLOCK_SIZE,i*BLOCK_SIZE,
                                  GRID_COLS*BLOCK_SIZE,BLOCK_SIZE,djb.display.WHITE)
                    djb.display.show()
                    time.sleep(0.050)
                    djb.display.fill_rect(GRID_OFFSET*BLOCK_SIZE,i*BLOCK_SIZE,
                                  GRID_COLS*BLOCK_SIZE,BLOCK_SIZE,djb.display.BLACK)
                    djb.display.show()
                    time.sleep(0.050)
                
        ############### update screen 
        
        # background
        draw_background()

        # draw all the previous blocks
        for i in range(GRID_ROWS):
            for j in range(GRID_COLS):
                if field[i][j]>=0:
                    # non empty
                    draw_block(j,i,field[i][j])
        
        # draw the current block
        for i in range(4):
            draw_block(x[i],y[i],n)
        
        # transfer the frame buffer to the actual screen over the SPI bus
        djb.display.show()

        
title_screen()   
#musicthread= _thread.start_new_thread(play_music, ())
while True:
    main_game()
    game_over_screen()