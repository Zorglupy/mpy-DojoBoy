#
# Simon for DojoBoy
#

from time import sleep_ms
from random import randint
from dojoboy_v1 import DojoBoy

djb = DojoBoy()

MODE_MENU     = 0
MODE_START    = 1
MODE_SEQUENCE = 2
MODE_INPUT    = 3
MODE_LOST     = 4
MODE_GAMEOVER = 5
MODE_EXIT     = 6

RED           = 1
GREEN         = 2
BLUE          = 3
YELLOW        = 4

etape = 0

# ----------------------------------------------------------
# Game management
# ----------------------------------------------------------

def tick():
    global etape
    
    handleButtons()

    if game['mode'] == MODE_SEQUENCE:
        #print("sequence")
        drawScore()
        #clearScreen()
        #drawWalls()
        #drawPlateau()
        joue_sequence(1000 - (len(game['sequence'])*50))
            
    elif game['mode'] == MODE_INPUT:
        pass
    
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
        #print ("======================")
        game['refresh'] = True
        etape = 0
        game['sequence'].clear()
        ajout_sequence()
        clearScreen()
        drawPlateau()
        drawScore()
        game['mode'] = MODE_SEQUENCE
        game['level'] = 0
        game['time']  = 0
        
        if game['demo'] :
            game['demoOn'] = True
          

    elif game['mode'] == MODE_EXIT:
        return
    else:
        handleButtons()

    draw()
    game['time'] += 1
    
    
    
def handleButtons():
    djb.scan_jst_btn()

    if game['mode'] == MODE_MENU :
        sleep_ms(10)
        if djb.setVolume() :
            pass
    #elif djb.just_pressed(djb.btn_Up):
    #    SNAKE_SIZE = 4 if SNAKE_SIZE == 2 else 6 if SNAKE_SIZE == 4 else 2
    #    djb.play_tone('C5', 100)
    #elif djb.just_pressed(djb.btn_Right) :
    #    djb.play_tone('D5', 100)
    #    if djb.pressed(djb.btn_B) :
    #        djb.frameRate = djb.frameRate - 5 if djb.frameRate > 5 else 100
    #    else :
    #        djb.frameRate = djb.frameRate + 5 if djb.frameRate < 100 else 5
        elif djb.just_pressed(djb.btn_Down):
            game['demo'] = not game['demo']
            djb.play_tone('E5', 100)
            
        elif djb.just_released(djb.btn_A) or game['demoOn'] :
            game['mode'] = MODE_START
            djb.play_tone('F5', 100)
            
            if game['demo'] :
                djb.display.fill(0)
                djb.display.text('DEMO', 5, 0, djb.WHITE_H)
                djb.display.text('B to Stop', 5, 30, djb.WHITE_H)
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

        elif game['mode'] == MODE_INPUT:
            #print("input")
            if djb.just_pressed (djb.btn_Left):
                djb.play_tone('C4',500)
                drawGreenOn()
            elif djb.just_released(djb.btn_Left):
                drawGreenOff()
                djb.bequiet()
                verifie_sequence(GREEN)
            elif djb.just_pressed(djb.btn_Right):
                djb.play_tone('D4',500)
                drawRedOn()
            elif djb.just_released(djb.btn_Right):
                drawRedOff()
                djb.bequiet()
                verifie_sequence(RED)
            elif djb.just_pressed(djb.btn_Up):
                djb.play_tone('E4',500)
                drawYellowOn()
            elif djb.just_released(djb.btn_Up):
                drawYellowOff()
                djb.bequiet()
                verifie_sequence(YELLOW)
            elif djb.just_pressed(djb.btn_Down):
                djb.play_tone('F4',500)
                drawBlueOn()
            elif djb.just_released(djb.btn_Down):
                drawBlueOff()
                djb.bequiet()
                verifie_sequence(BLUE)
                
            elif djb.just_pressed(djb.btn_A):
                pass
            elif djb.just_pressed(djb.btn_B):
                pass

def ajout_sequence():
    game['sequence'].append(randint (1, 4))
    
def joue_sequence(tempo):
    sleep_ms(200 + tempo)
    for i in range (len(game['sequence'])) :
        #print('etape',i)
        sleep_ms(int(tempo/2))
        if game['sequence'][i] == RED :
            drawRedOn()
            djb.play_tone('D4', tempo//2)
            sleep_ms(tempo//2)
            drawRedOff()
        if game['sequence'][i] == BLUE :
            drawBlueOn()
            djb.play_tone('F4', tempo//2)
            sleep_ms(tempo//2)
            drawBlueOff()
        if game['sequence'][i] == GREEN :
            drawGreenOn()
            djb.play_tone('C4', tempo//2)
            sleep_ms(tempo//2)
            drawGreenOff()
        if game['sequence'][i] == YELLOW :
            drawYellowOn()
            djb.play_tone('E4', tempo//2)
            sleep_ms(tempo//2)
            drawYellowOff()
    game['mode'] = MODE_INPUT

def verifie_sequence(bouton):
    global etape
    #print(etape, len(game['sequence']))
    #print('*',game['sequence'][etape])
    if game['sequence'][etape] == bouton:
        etape += 1
        if etape == len(game['sequence']):
            game['level'] = etape
            etape = 0
            ajout_sequence()
            game['mode'] = MODE_SEQUENCE
    else:
        game['mode'] = MODE_GAMEOVER
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
        elif game['mode'] == MODE_SEQUENCE:
            pass
            #clearScreen()
            #drawWalls()
            #drawPlateau()
        elif game['mode'] == MODE_INPUT:
            pass
            #clearScreen()
            #drawWalls()
            #drawPlateau()       
    #display.show()

def clearScreen():
    color = djb.display.RED_H if game['mode'] == MODE_LOST else djb.display.BLACK
    djb.display.fill(color)

def drawGameMenu():
    global SNAKE_SIZE
    clearScreen()
    djb.display.text('SIMON', 60, 20, djb.display.RED_H, 2)
    djb.display.rect(50,10,100,32, djb.display.BLUE_H)
    
    djb.display.rect(djb.display.width - djb.max_vol * 5 - 4, 0, djb.max_vol * 5 + 2, 6, djb.display.WHITE_H)
    djb.display.rect(djb.display.width - djb.max_vol * 5 - 3,1, djb.vol[0] * 5, 4, djb.display.RED_H, True)

    djb.display.text("Button A : START  ",0,60, djb.display.WHITE_H)
    if game['demo'] :
        djb.display.text('Button Down : AI-PLAYER', 0,80, djb.display.WHITE_H)
    else :
        djb.display.text('Button Down : 1-PLAYER', 0,80, djb.display.WHITE_H)
    #djb.display.text("Button Up : SIZE {}".format(SNAKE_SIZE),0,100,COLOR_SCORE)
    #djb.display.text("Button B + L/R : FRAME {}".format(djb.frameRate),0,120,COLOR_SCORE)
    djb.display.text("Button B + U/D : VOLUME",0,140, djb.display.WHITE_H)
    djb.display.text("Button U+D : EXIT",0,160, djb.display.RED_H)

def drawGameOver():
    djb.display.fill(djb.display.RED_H)
    djb.display.fill_rect(40, 100, 164, 34, djb.display.BLACK)
    djb.display.text('GAME OVER', 50, 110, djb.display.RED_H, 2)
    djb.display.text('Level {}'.format(game['level']), 60, 170, djb.display.WHITE_H, 2)
    djb.display.show()
    djb.play_tone('C4', 100)
    djb.play_tone('E4', 100)
    djb.play_tone('G4', 100)
    sleep_ms(3000)

def drawPlateau():
    djb.display.circle(120,120,119, djb.display.WHITE_H)
    djb.display.circle(120,120,115, djb.display.WHITE_H)
    djb.display.circle(120,120,15, djb.display.WHITE_H)
    drawBlueOff()
    drawRedOff()
    drawGreenOff()
    drawYellowOff()
    
def drawWalls():
    color = djb.display.RED_L if game['mode'] == MODE_LOST else djb.display.BLUE_H
    djb.display.rect(0, 0, djb.display.width, djb.display.height,color)

def drawScore():
    #djb.display.text('Score {}'.format(game['score']),5,2,2, djb.WHITE_H)
    djb.display.fill_rect(180,2,60,16, djb.display.BLACK)
    djb.display.text('L{}'.format(game['level']), 190, 2, djb.display.WHITE_H, 2)

def drawBlueOn():
    djb.display.circle(120,180,40, djb.display.BLUE_H, True)
    djb.display.show()

def drawBlueOff():
    djb.display.circle(120,180,40, djb.display.BLUE_L, True)
    djb.display.show()
    
def drawRedOn():
    djb.display.circle(180,120,40, djb.display.RED_H, True)
    djb.display.show()
    
def drawRedOff():
    djb.display.circle(180,120,40, djb.display.RED_L, True)
    djb.display.show()
    
def drawGreenOn():
    djb.display.circle(60,120,40, djb.display.GREEN_H, True)
    djb.display.show()
    
def drawGreenOff():
    djb.display.circle(60,120,40, djb.display.GREEN_L, True)
    djb.display.show()
    
def drawYellowOn():
    djb.display.circle(120,60,40, djb.display.YELLOW_H, True)
    djb.display.show()
    
def drawYellowOff():
    djb.display.circle(120,60,40, djb.display.YELLOW_L, True)
    djb.display.show()    


# ----------------------------------------------------------
# Initialization
# ----------------------------------------------------------

game = {
    'mode':    MODE_MENU,
    'score':   0,
    'level':   0,
    'sequence': [],
    'time':    0,
    'refresh': True,
    'reset':   True,
    'demo':    False,
    'demoOn' : False
}




# ----------------------------------------------------------
# Main loop
# ----------------------------------------------------------
while game['mode'] != MODE_EXIT :
  tick()
  djb.display.show_and_wait()
