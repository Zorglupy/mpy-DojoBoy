#
# invaders.py
# by Billy Cheung  2019 10 26
# Modified By Yoyo Zorglup for the DojoBoy 2023 12 25
#

from time import sleep_ms
from random import randint

from dojoboy_v1.dojoboy import DojoBoy

djb = DojoBoy(show_intro=True,width=160,height=128,framerate=30)

djb.bgm = 0
djb.maxBgm = 3
bgmBuf= [
    [False, 1, 0, 1],
    # Empire Strikes Back
    [True, 100, 0, 4,
    'G3',1,0,1,'G3',1,0,1,'G3',1,0,1,'C4',8,'G4',8,0,4,'F4',2,'E4',2,'D4',2,'C5',8,'G4',8, 0,4,'F4',2,'E4',2,'D4',2,'C5',8,'G4',8,0,4,'F4',2,'E4',2,'F4',2,'D4',8,0,8,
    'G3',1,0,1,'G3',1,0,1,'G3',1,0,1,'C4',8,'G4',8,0,4,'F4',2,'E4',2,'D4',2,'C5',8,'G4',8, 0,4,'F4',2,'E4',2,'D4',2,'C5',8,'G4',8,0,4,'F4',2,'E4',2,'F4',2,'D4',8,0,8,
    'G3',1,0,1,'G3',1,0,1,'G3',4,0,4,'F4',2,'E4',2,'D4',2,'C4',1,0,1,'C4',2,'D4',1,'E4',1,'D4',2,'A3',2,'B3',4,
    'G3',1,0,1,'G3',1,0,1,'A3',4,0,4,'F4',2,'E4',2,'D4',2,'C4',1,0,1,'G4',2,0,1,'D4',1,'D4',4,0,4,
    'G3',1,0,1,'G3',1,0,1,'A3',4,0,4,'F4',2,'E4',2,'D4',2,'C4',1,0,1,'C4',2,'D4',1,'E4',1,'D4',2,'A3',2,'B3',4,
    'E4',1,0,1,'E4',2,'A4',2,'G4',2,'F4',2,'E4',2,'D4',2,'C4',2,'B3',2,'A3',2,'E4',8, 0, 8
     ],

    # The Imperial March
    [False, 1, 0, 400,
    440, 400, 0, 100, 440, 400, 0, 100, 440, 400, 0,100, 349, 350, 523, 150,   440, 500, 349, 350, 523, 150, 440, 650, 0,500, 659, 500, 659, 500, 659, 500,  698, 350, 523, 150, 415, 500, 349, 350, 523, 150, 440, 650, 0, 500,
    880, 500, 440, 300, 440, 150, 880, 500, 830, 325, 784, 175, 740, 125, 698, 125,  740, 250, 0, 325,  445, 250, 622, 500, 587, 325,   554, 175,   523, 125,  466, 125,   523, 250,  0, 350,
    349, 250,  415, 500, 349, 350, 440, 125, 523, 500, 440, 375,   523, 125, 659, 650, 0, 500,349, 250,  415, 500, 349, 375, 523, 125, 440, 500,  349, 375,   523, 125, 440, 650,0, 650,
    880, 500, 440, 300, 440, 150, 880, 500, 830, 325, 784, 175, 740, 125, 698, 125,  740, 250, 0, 325,  445, 250, 622, 500, 587, 325,   554, 175,   523, 125,  466, 125,   523, 250,  0, 350,
    349, 250,  415, 500, 349, 350, 440, 125, 523, 500, 440, 375,   523, 125, 659, 650, 0, 500,349, 250,  415, 500, 349, 375, 523, 125, 440, 500,  349, 375,   523, 125, 440, 650,0, 650,
    ],
    # Tetris
    [False,200, 0, 4,
    659,2, 494, 1, 523,1, 587,2, 523, 1, 493, 1, 440, 2, 440, 1, 523,1, 659,2,587,1,523,1,493,2, 493,1,523,1,587,2,659,2,523,2,440,2,440,2,0,2,587, 1,698,1,880,2,783,1,698,1,659,2,523,1,659,2,587,1,523,1,493,2,493,1,523,1,587,2,659,2,523,2,440,2,440,2,0,2,
    329,4,261,4,293,4,246,4,261,4,220,4,207,4,246,4,329,4,261,4,293,4,246,4,261,2,329,2,440,4,415,6,0,2,
    ]
    ]

xMargin = const (5)
yMargin = const(10)

#Limite Ecran
screenL = const (5) 
screenR = const(155)
screenT = const (10)
screenB = const (118)

dx = 5
vc = 3

gunW= const(5) # Largeur Canon
gunH = const (6) # Hauteur Canon

invaderSize = const(8) # Dimension Invader
invaders_rows = const(6) #Nbr de ligne Invader
invaders_per_row = const(11) #Nbr Invader par ligne

spaceShipSize_w = const(4) # Largeur Soucoupe
spaceShipSize_h = const(2) # Hauteur Soucoupe

INVADER_COLOR = djb.display.RED_H
SPACESHIP_COLOR = djb.display.BLUE_H
GUN_COLOR = djb.display.GREEN_H
BULLET_COLOR = djb.display.CYAN_H

class Rect (object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def move (self, vx, vy) :
        self.x = self.x + vx
        self.y = self.y + vy

    def colliderect (self, rect1) :
      if (self.x + self.w   > rect1.x and
        self.x < rect1.x + rect1.w  and
        self.y + self.h > rect1.y and
        self.y < rect1.y + rect1.h) :
        return True
      else:
        return False
    
def setUpInvaders():
    y = yMargin
    while y < yMargin + (invaderSize+2) * invaders_rows :
      x = xMargin
      while x < xMargin + (invaderSize+2) * invaders_per_row :
        invaders.append(Rect(x,y,invaderSize, invaderSize))
        x = x + invaderSize + 2
      y = y + invaderSize + 2

def drawSpaceships(posture) :
  if posture :
    for i in spaceships :
      djb.display.fill_rect(i.x+2, i.y, 5 , 3, SPACESHIP_COLOR)
      djb.display.fill_rect(i.x, i.y+1, 9, 1, SPACESHIP_COLOR)
      djb.display.fill_rect(i.x+1, i.y+1, 2, 1, 0)
  else :
    for i in spaceships :
      djb.display.fill_rect(i.x+2, i.y, 5 , 3, SPACESHIP_COLOR)
      djb.display.fill_rect(i.x, i.y+1, 9, 1, SPACESHIP_COLOR)
      djb.display.fill_rect(i.x+5, i.y+1, 2, 1, 0)

def drawInvaders(posture) :
  if posture :
    for i in invaders :
        djb.display.fill_rect(i.x, i.y, invaderSize , invaderSize, INVADER_COLOR)
        djb.display.fill_rect(i.x+1, i.y+2, invaderSize-2, invaderSize-2, 0)
  else :
      for i in invaders :
        djb.display.fill_rect(i.x, i.y, invaderSize , invaderSize, INVADER_COLOR)
        djb.display.fill_rect(i.x+1, i.y, invaderSize-2, invaderSize-2, 0)
def drawGun() :
  djb.display.fill_rect(gun.x+2, gun.y, 1, 2, GUN_COLOR)
  djb.display.fill_rect(gun.x, gun.y+2, gunW, 3, GUN_COLOR)

def drawBullets() :
  for b in bullets:
    djb.display.fill_rect(b.x, b.y, 1,3, BULLET_COLOR)

def drawAbullets() :
  for b in aBullets:
    djb.display.fill_rect(b.x, b.y, 1,3, BULLET_COLOR)

def drawScore () :
  djb.display.text('S:{}'.format (score), 0,0, djb.display.WHITE_H)
  djb.display.text('L:{}'.format (level), 50,0, djb.display.WHITE_H)
  for i in range (0, life) :
    djb.display.fill_rect(92 + (gunW+2)*i, 0, 1, 2, djb.display.WHITE_H)
    djb.display.fill_rect(90 + (gunW+2)*i, 2, gunW, 3, djb.display.WHITE_H)



exitGame = False
demoOn = False

while not exitGame:
  gameOver = False
  usePaddle = False
  if demoOn :
      demo = True
  else :
      demo = False
  life = 3

  djb.start_song(bgmBuf[djb.bgm])
  
  #menu screen
  while True:
    djb.display.fill(0)
    djb.display.text('Invaders', 0, 0, djb.display.WHITE_H)
    djb.display.rect(90,0, djb.max_vol*4+2,6, djb.display.WHITE_H)
    djb.display.fill_rect(91,1, djb.vol[1] * 4,4, djb.display.RED_H)
    djb.display.text('A Start', 0, 10,  djb.display.WHITE_H)
    djb.display.text('B+L Quit', 0, 70,  djb.display.WHITE_H)

    djb.display.text('Up Button', 0,20, djb.display.WHITE_H)
    
    if demo :
        djb.display.text('Dw AI-Player', 0,30, djb.display.WHITE_H)
    else :
        djb.display.text('Dw 1-Player', 0,30, djb.display.WHITE_H)
    djb.display.text('M + U/D Frame/s {}'.format(djb.display.frame_rate), 0,40, djb.display.WHITE_H)
    if djb.bgm :
        djb.display.text('L Music {}'.format(djb.bgm), 0, 50, djb.display.WHITE_H)
    else :
        djb.display.text('L Music Off', 0, 50, djb.display.WHITE_H)
    djb.display.text('V + U/D Volume', 0, 60, djb.display.WHITE_H)
    djb.display.show()
    sleep_ms(10)
    djb.scan_jst_btn()
    
    if djb.setVolume(channel=1) :
        pass
    elif djb.setFrameRate() :
        pass
    elif djb.pressed(djb.btn_B) and djb.just_pressed (djb.btn_Left) :
        exitGame = True
        gameOver= True
        break
    elif djb.just_pressed(djb.btn_A) or demoOn :
        if demo :
            demoOn = True
            djb.display.fill(0)
            djb.display.text('DEMO', 5, 0, djb.display.WHITE_H)
            djb.display.text('B+L to Stop', 5, 30, djb.display.WHITE_H)
            djb.display.show()
            sleep_ms(1000)
        break
    elif djb.just_pressed(djb.btn_Down) :
        demo = not demo
    elif djb.just_pressed(djb.btn_Left) :
        djb.bgm = 0 if djb.bgm >= djb.maxBgm else djb.bgm + 1
        if djb.bgm :
            djb.start_song(bgmBuf[djb.bgm])
        else :
            djb.stop_song()
            
  #reset the game
  score = 0
  frameCount = 0
  level = 0
  loadLevel = True
  postureA = False
  postureS = False
  # Chance from 1 to 128
  aBulletChance = 0
  spaceshipChance = 1

  while not gameOver:

    lost = False
    frameCount = (frameCount + 1 ) % 120
    djb.display.fill(0)

    if loadLevel :
      loadLevel = False
      spaceships = []
      invaders = []
      bullets = []
      aBullets = []
      setUpInvaders()
      gun = Rect(screenL+int((screenR-screenL)/2), screenB, gunW, gunH)
      aBulletChance = 5 + level * 5


    #generate space ships
    if randint (0,99) < spaceshipChance and len(spaceships) < 1 :
      spaceships.append(Rect(0,9, 9, 9))

    if len(spaceships) :
      if not frameCount % 3 :
        postureS = not postureS
        # move spaceships once every 4 frames
        for i in spaceships:
          i.move(2,0)
          if i.x >= screenR :
            spaceships.remove(i)
      if not djb.bgm :
          # only play sound effect if no background music
          if frameCount % 20 == 10 :
            djb.play_tone ('E5', 20)
          elif frameCount % 20 == 0 :
            djb.play_tone ('C5', 20)

    if not frameCount % 15 :
      postureA = not postureA
      # move Aliens once every 15 frames
      if not djb.bgm :
          # only play sound effect if no background music
          if postureA :
              djb.play_freq (80, 10)
          else:
              djb.play_freq (120, 10)
      
      for i in invaders:
        if i.x > screenR or i.x < screenL :
            dx = -dx
            for alien in invaders :
              alien.move (0, invaderSize)
              if alien.y + alien.h > gun.y :
                lost = True
                loadLevel = True
                djb.play_tone ('F4',300)
                djb.play_tone ('D4',100)
                djb.play_tone ('C5',100)
                break
            break

      for i in invaders :
        i.move (dx, 0)

    djb.scan_jst_btn()

    if djb.pressed (djb.btn_B) and djb.justReleased(djb.btn_Left) :
        gameOver= True
        demoOn = False
        break

    if demo :

        if randint (0,1) and len(bullets) < 2:
            bullets.append(Rect(gun.x+3, gun.y-1, 1, 3))
            djb.play_freq (200,5)
            djb.play_freq (300,5)
            djb.play_freq (400,5)

        if randint(0,1) :
            vc = 3
        else :
            vc = -3

        if (vc + gun.x + gunW) < screenR and (vc + gun.x)  >= 0 :
           gun.move (vc, 0)

    # Real player
    elif djb.pressed (djb.btn_A | djb.btn_B) and len(bullets) < 2:
      bullets.append(Rect(gun.x+3, gun.y-1, 1, 3))
      djb.play_freq (200,5)
      djb.play_freq (300,5)
      djb.play_freq (400,5)
  
    # move gun
    if djb.pressed (djb.btn_Left) and gun.x - 3 > 0 :
        vc = -3
    elif djb.pressed(djb.btn_Right) and (gun.x + 3 + gunW ) < djb.display.width :
        vc = 3
    else :
        vc = 0
    gun.move (vc, 0)

    # move bullets
    for b in bullets:
      b.move(0,-3)
      if b.y < 0 :
        bullets.remove(b)
      else :
        for i in invaders:
          if i.colliderect(b) :
            invaders.remove(i)
            bullets.remove(b)
            score +=1
            djb.play_tone ('C6',10)
            break
        for i in spaceships :
          if i.colliderect(b) :
            spaceships.remove(i)
            bullets.remove(b)
            score +=10
            djb.play_tone ('B4',30)
            djb.play_tone ('E5',10)
            djb.play_tone ('C4',30)
            break

    # Launch Alien bullets
    for i in invaders:
      if randint (0,1000) * len (invaders) * 10 < aBulletChance and len(aBullets) < 3 :
        aBullets.append(Rect(i.x+2, i.y, 1, 3))

    # move Alien bullets
    for b in aBullets:
      b.move(0,3)
      if b.y > djb.display.height  :
        aBullets.remove(b)
      elif b.colliderect(gun) :
        lost = True
        #print ('{} {} {} {} : {} {} {} {}'.format(b.x,b.y,b.x2,b.y2,gun.x,gun.y,gun.x2,gun.y2))
        aBullets.remove(b)
        djb.play_tone ('C5',30)
        djb.play_tone ('E4',30)
        djb.play_tone ('B4',30)
        break

    drawSpaceships (postureS)
    drawInvaders (postureA)
    drawGun()
    drawBullets()
    drawAbullets()
    drawScore()


    if len(invaders) == 0 :
      level += 1
      loadLevel = True
      djb.play_tone ('C4',100)
      djb.play_tone ('D4',100)
      djb.play_tone ('E4',100)
      djb.play_tone ('F4',100)
      djb.play_tone ('G4',100)
      djb.bgm = 0 if djb.bgm >= djb.maxBgm else djb.bgm + 1
      if djb.bgm :
        djb.start_song(bgmBuf[djb.bgm])

    if lost :
      lost = False;
      life -= 1
      djb.play_tone ('F4',100)
      djb.play_tone ('G4',100)
      djb.play_tone ('C4',100)
      djb.play_tone ('D4',100)
      sleep_ms (1000)
      if life < 0 :
        gameOver = True

    if gameOver :
      djb.display.fill_rect (3, 15, 120,20,0)
      djb.display.center_text ("GAME OVER", djb.display.WHITE_H)
      djb.play_tone ('B4',300)
      djb.play_tone ('E4',100)
      djb.play_tone ('C4',100)
      djb.display.show()
      sleep_ms(2000)

    djb.display.show_and_wait()

#djb.deinit()
#if djb.ESP32 :
#      del sys.modules["gameESP"]
#gc.collect()
