 #
# ArduBoy Jet Pac
# Version 1.1
# 2nd Feb 2017
# by Mike McRoberts (a.k.a. TheArduinoGuy)
# MicroPython port for DojoBoy by Yoyo Zorglup 26 12 23
#

from time import sleep_ms,ticks_ms, ticks_us, ticks_diff
from random import randint
from dojoboy_v1 import DojoBoy
import machine

#machine.freq(240_000_000)

djb = DojoBoy(show_intro=True,width=128,height=64,framerate=60)

level = 1
gameDifficulty = 2
levelStep = 0
rocketStep = 0
monsterType = 0
gameState = 4
subState = 0
highScore = 0
lives = 4
score = 0

# fuel cells
fuelX = 0
fuelY = -8
fuelPercent = 0

# Jet man data
jetManX = 60
jetManY= 47
jetManXRate = 0
jetManYRate = 0
jetManDirection = 1
jetManState = 0

# rocket data
topRocketX = 0
topRocketY = 0
middleRocketX = 0
middleRocketY = 0
bottomRocketX = 0
bottomRocketY = 0

# data for the bonus items
bonusX = 0
bonusY = 0
bonusState = 0
bonusType = 0

cloudIndex = 0
jetPacFired = 0
buttonBPressed = False
animToggle = 0
frameRate = 0
lastPressed = 0

platforms = [2,4,3,7,5,2,11,3,3]
rocketParts = [24,24,60,32,76,55]


class movingObjects():
        x: float = 0
        y: float = 0
        xRate: float = 0
        yRate: float = 0
        direction: bool = True

monsters = []
for x in range (0,11):
    monsters.append(movingObjects())


#@dataclass
class cloudObjects:
        state: int = 0
        x: int = 0
        y: int = 0
        time: int = 0

clouds = []
for x in range (0,11):
    clouds.append(cloudObjects())

class laserObjects:
        x: int = 0
        y: int = 0
        length: int = 0
        direction: bool = True
        time: int = 0

laserbeams = []
for x in range (0,21):
    laserbeams.append(laserObjects())

laserIndex = 0

JETMANRIGHTHEAD = bytearray(b'\xF8\x70\x8C\xDE\xDA\x0A\x80\x00')
djb.display.add_sprite(JETMANRIGHTHEAD,8,8, 1) # Sprite 0
del JETMANRIGHTHEAD
JETMANLEFTHEAD = bytearray(b'\x00\x80\x0a\xda\xde\x8c\x70\xf8')
djb.display.add_sprite(JETMANLEFTHEAD,8,8, 1) # Sprite 1
del JETMANLEFTHEAD
JETMANRIGHT1 = bytearray(b'\x1F\x18\x06\xDD\xDD\x82\x03\x02')
djb.display.add_sprite(JETMANRIGHT1,8,8, 1) # Sprite 2
del JETMANRIGHT1
JETMANLEFT1 = bytearray(b'\x02\x03\x82\xdd\xdd\x06\x18\x1f')
djb.display.add_sprite(JETMANLEFT1,8,8, 1) # Sprite 3
del JETMANLEFT1
JETMANRIGHT2 = bytearray(b'\x1f\xd8\xe6\xbd\xfd\xc2\x83\x02')
djb.display.add_sprite(JETMANRIGHT2,8,8, 1) # Sprite 4
del JETMANRIGHT2
JETMANLEFT2 = bytearray(b'\x02\x83\xc2\xfd\xbd\xe6\xd8\x1f')
djb.display.add_sprite(JETMANLEFT2,8,8, 1) # Sprite 5
del JETMANLEFT2
JETMANRIGHT3 = bytearray(b'\x9f\xd8\xb6\x3d\x3d\xe2\xc3\x82')
djb.display.add_sprite(JETMANRIGHT3,8,8, 1) # Sprite 6
del JETMANRIGHT3
JETMANLEFT3 = bytearray(b'\x82\xc3\xe2\x3d\x3d\xb6\xd8\x9f')
djb.display.add_sprite(JETMANLEFT3,8,8, 1) # Sprite 7
del JETMANLEFT3
JETMANRIGHTFLY1 = bytearray(b'\x5f\x98\x46\x2d\x0d\x7e\x6f\x42')
djb.display.add_sprite(JETMANRIGHTFLY1,8,8, 1) # Sprite 8
del JETMANRIGHTFLY1
JETMANRIGHTFLY2 = bytearray(b'\x9f\x58\xa6\x4d\x0d\x7e\x6f\x42')
djb.display.add_sprite(JETMANRIGHTFLY2,8,8, 1) # Sprite 9
del JETMANRIGHTFLY2
JETMANRIGHTFLY3 = bytearray(b'\x5f\xb8\x46\xad\x0d\x7e\x6f\x42')
djb.display.add_sprite(JETMANRIGHTFLY3,8,8, 1) # Sprite 10
del JETMANRIGHTFLY3
JETMANLEFTFLY1 = bytearray(b'\x42\x6f\x7e\x0d\x2d\x46\x98\x5f')
djb.display.add_sprite(JETMANLEFTFLY1,8,8, 1) # Sprite 11
del JETMANLEFTFLY1
JETMANLEFTFLY2 = bytearray(b'\x42\x6f\x7e\x0d\x4d\xa6\x58\x9f')
djb.display.add_sprite(JETMANLEFTFLY2,8,8, 1) # Sprite 12
del JETMANLEFTFLY2
JETMANLEFTFLY3 = bytearray(b'\x42\x6f\x7e\x0d\xad\x46\xb8\x5f')
djb.display.add_sprite(JETMANLEFTFLY3,8,8, 1) # Sprite 13
del JETMANLEFTFLY3
PLATFORM = bytearray(b'\x06\x03\x0f\x0f\x07\x03\x0f\x06')
djb.display.add_sprite(PLATFORM,8,8, 1) # Sprite 14
del PLATFORM
BOTTOMROCKET = bytearray(b'\xFF\x1F\x64\x7B\x7B\x64\x1F\xFF')
djb.display.add_sprite(BOTTOMROCKET,8,8, 1) # Sprite 15
del BOTTOMROCKET
MIDDLEROCKET = bytearray(b'\xE0\xF0\x0F\xFF\xFF\x0F\xF0\xE0')
djb.display.add_sprite(MIDDLEROCKET,8,8, 1) # Sprite 16
del MIDDLEROCKET
TOPROCKET = bytearray(b'\x00\x00\x6E\x6F\x6F\x6E\x00\x00')
djb.display.add_sprite(TOPROCKET,8,8, 1) # Sprite 17
del TOPROCKET
TOPSHUTTLE = bytearray(b'\x00\x00\xf8\xd6\xff\xff\x02\xfc')
djb.display.add_sprite(TOPSHUTTLE,8,8, 1) # Sprite 18
del TOPSHUTTLE
MIDDLESHUTTLE = bytearray(b'\x00\x00\xff\x24\xdb\xff\x00\xff')
djb.display.add_sprite(MIDDLESHUTTLE,8,8, 1) # Sprite 19
del MIDDLESHUTTLE
BOTTOMSHUTTLE = bytearray(b'\xfc\x42\x3f\x1c\x0f\x7f\xf0\x0f')
djb.display.add_sprite(BOTTOMSHUTTLE,8,8, 1) # Sprite 20
del BOTTOMSHUTTLE
TOPFAT = bytearray(b'\x80\xf0\x88\xf7\xff\xf8\xf0\x80')
djb.display.add_sprite(TOPFAT,8,8, 1) # Sprite 21
del TOPFAT
MIDDLEFAT = bytearray(b'\xfa\x0d\xfa\xad\xfa\xfd\xfa\xff')
djb.display.add_sprite(MIDDLEFAT,8,8, 1) # Sprite 22
del MIDDLEFAT
BOTTOMFAT = bytearray(b'\xcf\xf0\xdf\x3a\x3f\xdf\xff\xcf')
djb.display.add_sprite(BOTTOMFAT,8,8, 1) # Sprite 23
del BOTTOMFAT
TOPFUTURE = bytearray(b'\xc0\xb0\x4c\xff\xff\x0c\x30\xc0')
djb.display.add_sprite(TOPFUTURE,8,8, 1) # Sprite 24
del TOPFUTURE
MIDDLEFUTURE = bytearray(b'\xe3\x8e\x39\xff\xff\x38\x8c\xe3')
djb.display.add_sprite(MIDDLEFUTURE,8,8, 1) # Sprite 25
del MIDDLEFUTURE
BOTTOMFUTURE = bytearray(b'\xff\x1f\x40\x7f\x7f\x40\x1f\xff')
djb.display.add_sprite(BOTTOMFUTURE,8,8, 1) # Sprite 26
del BOTTOMFUTURE
# BONUS ITEMS
FUEL = bytearray(b'\x7e\xFF\xC1\xF5\xF5\xFD\xFF\x7E')
djb.display.add_sprite(FUEL,8,8, 1) # Sprite 27
del FUEL
DIAMOND = bytearray(b'\x18\x34\x6e\xee\xee\x6e\x34\x18')
djb.display.add_sprite(DIAMOND,8,8, 1) # Sprite 28
del DIAMOND
BREAD = bytearray(b'\x70\xc8\xe4\xf4\xf4\xf4\xf8\x70')
djb.display.add_sprite(BREAD,8,8, 1) # Sprite 29
del BREAD
GOLD = bytearray(b'\x80\xe0\x98\x86\x9e\xf8\xe0\x80')
djb.display.add_sprite(GOLD,8,8, 1) # Sprite 30
del GOLD
ATOM = bytearray(b'\x60\xd0\xf6\x6d\x7f\xd6\xf0\x60')
djb.display.add_sprite(ATOM,8,8, 1) # Sprite 31
del ATOM
NUKE = bytearray(b'\xe0\xe0\xee\x0e\xee\xe0\xe0\x00')
djb.display.add_sprite(NUKE,8,8, 1) # Sprite 32
del NUKE
# MISC ITEMS
LITTLEMAN = bytearray(b'\x10\x88\xfe\x7d\x7d\xfe\x88\x10')
djb.display.add_sprite(LITTLEMAN,8,8, 1) # Sprite 33
del LITTLEMAN
THRUST1 = bytearray(b'\x14\x7e\xa8\x76\xdc\xb6\x5a\x14')
djb.display.add_sprite(THRUST1,8,8, 1) # Sprite 34
del THRUST1
THRUST2 = bytearray(b'\x0c\x3a\x56\xbc\x5a\xac\x36\x0c')
djb.display.add_sprite(THRUST2,8,8, 1) # Sprite 35
del THRUST2
CLOUD1 = bytearray(b'\x30\x6c\x74\xba\x6a\x7e\x4c\x30')
djb.display.add_sprite(CLOUD1,8,8, 1) # Sprite 36
del CLOUD1
CLOUD2 = bytearray(b'\x00\x00\x30\xd8\x68\xec\xf8\x5c\xdc\xe8\x7c\xd8\xf0\x20\x00\x00\x00\x00\x0b\x14\x3f\x29\x36\x17\x3b\x1f\x2f\x12\x1e\x0b\x00\x00')
djb.display.add_sprite(CLOUD2,16,16, 1) # Sprite 37
del CLOUD2
CLOUD3 = bytearray(b'\x00\x40\x62\x18\x6c\x18\x14\x08\x34\x0A\x54\xAC\x60\xB1\x00\x00\x02\x00\x45\x1A\x3D\x04\xAA\x04\x10\x29\x14\x2A\x16\x0D\x42\x10')
djb.display.add_sprite(CLOUD3,16,16, 1) # Sprite 38
del CLOUD3
# BADDIES
ASTEROIDRIGHT1 = bytearray(b'\x2A\x55\x3E\x77\x5d\x7b\x26\x1c')
djb.display.add_sprite(ASTEROIDRIGHT1,8,8, 1) # Sprite 39
del ASTEROIDRIGHT1
ASTEROIDRIGHT2 = bytearray(b'\x55\x2a\x3e\x77\x5d\x7b\x26\x1c')
djb.display.add_sprite(ASTEROIDRIGHT2,8,8, 1) # Sprite 40
del ASTEROIDRIGHT2
ASTEROIDLEFT1 = bytearray(b'\x1c,0x26,0x7b,0x5d,0x77,0x3e,0x55,0x2a')
djb.display.add_sprite(ASTEROIDLEFT1,8,8, 1) # Sprite 41
del ASTEROIDLEFT1
ASTEROIDLEFT2 = bytearray(b'\x1c,0x26,0x7b,0x5d,0x77,0x3e,0x2a,0x55')
djb.display.add_sprite(ASTEROIDLEFT2,8,8, 1) # Sprite 42
del ASTEROIDLEFT2
FUZZY1 = bytearray(b'\x3c\x76\xeb\x76\xf7\x6a\x36\x1c')
djb.display.add_sprite(FUZZY1,8,8, 1) # Sprite 43
del FUZZY1
FUZZY2 = bytearray(b'\x1c\x76\x6a\xf7\x76\xeb\x76\x3c')
djb.display.add_sprite(FUZZY2,8,8, 1) # Sprite 44
del FUZZY2
BALL1 = bytearray(b'\x3c\x72\xf9\xfd\xff\xff\x7e\x3c')
djb.display.add_sprite(BALL1,8,8, 1) # Sprite 45
del BALL1
BALL2 = bytearray(b'\x1c\x32\x79\x7d\x7f\x7f\x3e\x1c')
djb.display.add_sprite(BALL2,8,8, 1) # Sprite 46
del BALL2
PLANE1 = bytearray(b'\x1e\xbc\xb8\xf8\xf8\xa8\xb0\x20')
djb.display.add_sprite(PLANE1,8,8, 1) # Sprite 47
del PLANE1
PLANE2 = bytearray(b'\x20\xb0\xa8\xf8\xf8\xb8\xbc\x1e')
djb.display.add_sprite(PLANE2,8,8, 1) # Sprite 48
del PLANE2
CROSS = bytearray(b'\x10\x28\x7c\xaa\x7c\x28\x10\x00')
djb.display.add_sprite(CROSS,8,8, 1) # Sprite 49
del CROSS
FALCON1 = bytearray(b'\x99\xbd\x66\x66\x7e\x3c\x24\x24')
djb.display.add_sprite(FALCON1,8,8, 1) # Sprite 50
del FALCON1
FALCON2 = bytearray(b'\x24\x24\x3c\x7e\x66\x66\xbd\x99')
djb.display.add_sprite(FALCON2,8,8, 1) # Sprite 51
del FALCON2
UFO1 = bytearray(b'\x20\x50\xf8\xdc\xfc\xd8\x70\x20')
djb.display.add_sprite(UFO1,8,8, 1) # Sprite 52
del UFO1
UFO2 = bytearray(b'\x20\x70\xd8\xfc\xdc\xf8\x50\x20')
djb.display.add_sprite(UFO2,8,8, 1) # Sprite 53
del UFO2
JELLY = bytearray(b'\x6c\xfe\xb9\x7b\x7f\xb9\xfa\x6c')
djb.display.add_sprite(JELLY,8,8, 1) # Sprite 54
del JELLY
BLANK = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00')
djb.display.add_sprite(BLANK,8,8, 1) # Sprite 55
del BLANK
LASER1 = bytearray(b'\x01\x01\x01\x01\x01\x01\x01\x01')
djb.display.add_sprite(LASER1,8,8, 1) # Sprite 56
del LASER1
LASER2 = bytearray(b'\x01\x01\x01\x01\x00\x00\x00\x00')
djb.display.add_sprite(LASER2,8,8, 1) # Sprite 57
del LASER2

################################

WHITE_H_PAL = djb.display.palette_mono(djb.display.WHITE_H, djb.display.BLACK)
BLUE_H_PAL = djb.display.palette_mono(djb.display.BLUE_H, djb.display.BLACK)
RED_H_PAL = djb.display.palette_mono(djb.display.RED_H, djb.display.BLACK)
GREEN_H_PAL = djb.display.palette_mono(djb.display.GREEN_H, djb.display.BLACK)
CYAN_H_PAL = djb.display.palette_mono(djb.display.CYAN_H, djb.display.BLACK)
MAGENTA_H_PAL = djb.display.palette_mono(djb.display.MAGENTA_H, djb.display.BLACK)
YELLOW_H_PAL = djb.display.palette_mono(djb.display.YELLOW_H, djb.display.BLACK)

################################

def RANDOMXL():
        return randint(-64,0)
    
def RANDOMXR():
        return randint(128,192)

def RANDOMY():
        return randint(48,56)

def RANDOMXRATE():
        return (0.15+(randint(0,90+(gameDifficulty*5))/100))

def RANDOMYRATE():
        return ((randint(0,40)/100)-0.2)

def FUELRANDOM():
        return (16+randint(0,48) if randint(0,1) else 88+randint(0,16))

#########################################
    
def initialiseGameState():
        global gameState, jetManX, jetManY,jetManDirection, jetManXRate, jetManYRate
        gameState = 1
        jetManX = 60
        jetManY = 47
        jetManDirection = 1 
        jetManXRate = 0
        jetManYRate = 0

        for index in range (0,9):
                clouds[cloudIndex].state = 0
                clouds[cloudIndex].x = 0
                clouds[cloudIndex].y = 0
                clouds[cloudIndex].time = 0
                
        for index in range (0,19):
                laserbeams[index].x = 0
                laserbeams[index].y = 0
                laserbeams[index].length = 0
                laserbeams[index].direction = 0
                laserbeams[index].time = 0

                
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def createMonsters():
        for index in range (0,9):
                DIRECTION = randint (0,1)
                monsters[index].x = (RANDOMXR() if DIRECTION else RANDOMXL())
                monsters[index].y = RANDOMY()
                monsters[index].xRate = RANDOMXRATE()
                monsters[index].yRate = RANDOMYRATE()
                monsters[index].directin = DIRECTION

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def initialiseRocket():
        global topRocketX,topRocketY,middleRocketX,middleRocketY,bottomRocketX,bottomRocketY, rocketParts
        topRocketX = rocketParts[0]
        topRocketY = rocketParts[1]
        middleRocketX = rocketParts[2]
        middleRocketY = rocketParts[3]
        bottomRocketX = rocketParts[4]
        bottomRocketY = rocketParts[5]

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def drawPlatforms():
        for index in range (0,9,3):
                length = platforms[index+2]
                for row in range (0,length):
                        platformX = platforms[index]
                        platformX = (platformX*8)+(row*8)
                        platformY = platforms[index+1]
                        platformY = platformY*8
                        djb.display.sprite(14, platformX, platformY,djb.display.BLACK,GREEN_H_PAL)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def drawJetMan():
        global jetManX, jetManY, jetManDirection, animToggle, jetManState
        if jetManState == 0: # standing
                if jetManDirection:
                        djb.display.sprite(0, int(jetManX), int(jetManY),djb.display.BLACK,WHITE_H_PAL) # 0 JETMANRIGHTHEAD
                        if jetManXRate == 0:
                                djb.display.sprite(2, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 2 JETMANRIGHT1
                        else:
                                if animToggle == 0:
                                        djb.display.sprite(2, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 2 JETMANRIGHT1
                       
                                elif animToggle == 1:
                                        djb.display.sprite(4, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 4 JETMANRIGHT2
                             
                                elif animToggle == 2:
                                        djb.display.sprite(6, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 6 JETMANRIGHT3
                               
                                elif animToggle == 3:
                                        djb.display.sprite(4, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL)
                                 
                else:
                        djb.display.sprite(1, int(jetManX), int(jetManY),djb.display.BLACK,WHITE_H_PAL) # 1 JETMANLEFTHEAD
                        if jetManXRate == 0:
                                djb.display.sprite(3, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 3 JETMANLEFT1
                        else:
                                if animToggle == 0:
                                        djb.display.sprite(3, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL)
                            
                                elif animToggle == 1:
                                        djb.display.sprite(5, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 5 JETMANLEFT2
                         
                                elif animToggle == 2:
                                        djb.display.sprite(7, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 7 JETMANLEFT3
                         
                                elif animToggle == 3:
                                        djb.display.sprite(5, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL)
                         

        if jetManState == 1 or jetManState==2: # Rising or falling
                if jetManDirection:
                        djb.display.sprite(0, int(jetManX), int(jetManY),djb.display.BLACK,WHITE_H_PAL)
                        
                        if animToggle == 0:
                                djb.display.sprite(8, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 8 JETMANRIGHTFLY1
                     
                        elif animToggle == 1:
                                djb.display.sprite(9, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 9 JETMANRIGHTFLY2
               
                        elif animToggle == 2:
                                djb.display.sprite(10, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 10 JETMANRIGHTFLY3
                 
                        elif animToggle == 3:
                                djb.display.sprite(9, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL)
               
                else:
                        djb.display.sprite(1, int(jetManX), int(jetManY),djb.display.BLACK,WHITE_H_PAL)
                        if animToggle == 0:
                                djb.display.sprite(11, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 11 JETMANLEFTFLY1
          
                        elif animToggle == 1:
                                djb.display.sprite(12, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 12 JETMANLEFTFLY2
                  
                        elif animToggle == 2:
                                djb.display.sprite(13, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL) # 13 JETMANLEFTFLY3
          
                        elif animToggle == 3:
                                djb.display.sprite(12, int(jetManX), int(jetManY)+8,djb.display.BLACK,WHITE_H_PAL)


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def drawThings():
        global animToggle, gameDifficulty, bonusState, monsterType, fuelX, fuelY, bonusX, bonusY
        for index in range (0,gameDifficulty):
                x = monsters[index].x
                y = monsters[index].y
                direction = monsters[index].direction

                if monsterType == 0:
                        if direction == 1:
                            djb.display.sprite(39 if (animToggle%2) == 0 else 40, int(x), int(y),djb.display.BLACK,RED_H_PAL) # 39:ASTEROIDRIGHT1 40:ASTEROIDRIGHT2
                        else:
                            djb.display.sprite(41 if (animToggle%2) == 0 else 42, int(x), int(y),djb.display.BLACK,YELLOW_H_PAL) # 41:ASTEROIDRIGHT1 42:ASTEROIDRIGHT2
                if monsterType == 1:
                        djb.display.sprite(43 if (animToggle%2) == 0 else 44, int(x), int(y),djb.display.BLACK,GREEN_H_PAL)
                if monsterType == 2:
                        djb.display.sprite(45 if (animToggle%2) == 0 else 46, int(x), int(y),djb.display.BLACK,GREEN_H_PAL)
                if monsterType == 3:
                        if direction == 1:
                            djb.display.sprite(47 if (animToggle%2) == 0 else 47, int(x), int(y),djb.display.BLACK,YELLOW_H_PAL) # PLANE1
                        else:
                            djb.display.sprite(48 if (animToggle%2) == 0 else 48, int(x), int(y),djb.display.BLACK,YELLOW_H_PAL) #PLANE2
                if monsterType == 4:
                        djb.display.sprite(49 if (animToggle%2) == 0 else 49, int(x), int(y),djb.display.BLACK,WHITE_H_PAL) # CROSS

                if monsterType == 5:
                        if direction == 1:
                            djb.display.sprite(50 if (animToggle%2) == 0 else 50, int(x), int(y),djb.display.BLACK,WHITE_H_PAL) # FALCON1
                        else:
                            djb.display.sprite(51 if (animToggle%2) == 0 else 51, int(x), int(y),djb.display.BLACK,WHITE_H_PAL) # FALCON2
                if monsterType == 6:
                        djb.display.sprite(52 if (animToggle%2) == 0 else 53, int(x), int(y),djb.display.BLACK,WHITE_H_PAL) # UFO1 UFO2
                if monsterType == 7:
                        djb.display.sprite(54 if (animToggle%2) == 0 else 54, int(x), int(y),djb.display.BLACK,WHITE_H_PAL) # JELLY

                djb.display.sprite(27, int(fuelX), int(fuelY),djb.display.BLACK,MAGENTA_H_PAL) # 27 FUEL
                drawRocket()

                if bonusState != 0:
                        if bonusType == 0:
                                djb.display.sprite(28 if (animToggle%2) == 0 else 55, int(bonusX), int(bonusY),djb.display.BLACK,YELLOW_H_PAL) # 55 BLANK 28 DIAMOND
                        elif bonusType == 1:
                                djb.display.sprite(29 if (animToggle%2) == 0 else 55, int(bonusX), int(bonusY),djb.display.BLACK,MAGENTA_H_PAL)
                        elif bonusType == 2:
                                djb.display.sprite(30 if (animToggle%2) == 0 else 55, int(bonusX), int(bonusY),djb.display.BLACK,YELLOW_H_PAL)
                        elif bonusType == 3:
                                djb.display.sprite(31 if (animToggle%2) == 0 else 55, int(bonusX), int(bonusY),djb.display.BLACK,CYAN_H_PAL)
                        elif bonusType == 4:
                                djb.display.sprite(32 if (animToggle%2) == 0 else 55, int(bonusX), int(bonusY),djb.display.BLACK,BLUE_H_PAL)                                
 
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def drawRocket():
        global topRocketX, topRocketY, middleRocketX, middleRocketY, bottomRocketX, bottomRocketY, subState, gameState,rocketStep 
        if rocketStep == 0:
                djb.display.sprite(17, int(topRocketX), int(topRocketY),djb.display.BLACK,CYAN_H_PAL) #17 TOPROCKET
                djb.display.sprite(16, int(middleRocketX), int(middleRocketY),djb.display.BLACK,CYAN_H_PAL) #16 MIDDLEROCKET
                djb.display.sprite(15, int(bottomRocketX), int(bottomRocketY),djb.display.BLACK,CYAN_H_PAL) # 15 BOTTOMROCKET
        elif rocketStep == 1:
                djb.display.sprite(18, int(topRocketX), int(topRocketY),djb.display.BLACK,WHITE_H_PAL)
                djb.display.sprite(19, int(middleRocketX), int(middleRocketY),djb.display.BLACK,WHITE_H_PAL)
                djb.display.sprite(20, int(bottomRocketX), int(bottomRocketY),djb.display.BLACK,WHITE_H_PAL)
        elif rocketStep == 2:
                djb.display.sprite(21, int(topRocketX), int(topRocketY),djb.display.BLACK,WHITE_H_PAL)
                djb.display.sprite(22, int(middleRocketX), int(middleRocketY),djb.display.BLACK,WHITE_H_PAL)
                djb.display.sprite(23, int(bottomRocketX), int(bottomRocketY),djb.display.BLACK,WHITE_H_PAL)
        elif rocketStep == 3:
                djb.display.sprite(24, int(topRocketX), int(topRocketY),djb.display.BLACK,WHITE_H_PAL)
                djb.display.sprite(25, int(middleRocketX), int(middleRocketY),djb.display.BLACK,WHITE_H_PAL)
                djb.display.sprite(26, int(bottomRocketX), int(bottomRocketY),djb.display.BLACK,WHITE_H_PAL)

        if subState == 11:
                djb.display.sprite(34 if (animToggle%2) == 0 else 35, int(bottomRocketX), int(bottomRocketY)+8,djb.display.BLACK,YELLOW_H_PAL) # 34 THRUST1 35 THRUST2
                topRocketY -= 0.2
                middleRocketY -= 0.2
                bottomRocketY -= 0.2
                jetManY = -20
                if bottomRocketY < -8:
                    gameState = 3
                explosionFX() # ***********************************************
 

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def rocketLand():
        global topRocketX, topRocketY, middleRocketY, bottomRocketX, bottomRocketY, frameRate, animToggle, cloudIndex, rocketStep
        while bottomRocketY <= 55:
                djb.display.fill(0)
                if rocketStep == 0:
                        djb.display.sprite(17, int(topRocketX), int(topRocketY),djb.display.BLACK,CYAN_H_PAL)
                        djb.display.sprite(16, int(middleRocketX), int(middleRocketY),djb.display.BLACK,CYAN_H_PAL)
                        djb.display.sprite(15, int(bottomRocketX), int(bottomRocketY),djb.display.BLACK,CYAN_H_PAL)
                elif rocketStep == 1:
                        djb.display.sprite(18, int(topRocketX), int(topRocketY),djb.display.BLACK,WHITE_H_PAL)
                        djb.display.sprite(19, int(middleRocketX), int(middleRocketY),djb.display.BLACK,WHITE_H_PAL)
                        djb.display.sprite(20, int(bottomRocketX), int(bottomRocketY),djb.display.BLACK,WHITE_H_PAL)
                elif rocketStep == 2:
                        djb.display.sprite(21, int(topRocketX), int(topRocketY),djb.display.BLACK,WHITE_H_PAL)
                        djb.display.sprite(22, int(middleRocketX), int(middleRocketY),djb.display.BLACK,WHITE_H_PAL)
                        djb.display.sprite(23, int(bottomRocketX), int(bottomRocketY),djb.display.BLACK,WHITE_H_PAL)
                elif rocketStep == 3:
                        djb.display.sprite(24, int(topRocketX), int(topRocketY),djb.display.BLACK,WHITE_H_PAL)
                        djb.display.sprite(25, int(middleRocketX), int(middleRocketY),djb.display.BLACK,WHITE_H_PAL)
                        djb.display.sprite(26, int(bottomRocketX), int(bottomRocketY),djb.display.BLACK,WHITE_H_PAL)

                djb.display.sprite(34 if (animToggle%2) == 0 else 35, int(bottomRocketX), int(bottomRocketY)+8,djb.display.BLACK,YELLOW_H_PAL) # 34 THRUST1 35 THRUST2
                topRocketY += 0.2
                middleRocketY += 0.2
                bottomRocketY += 0.2
                jetManY = -20
                djb.display.hline(0, 63, 128, djb.display.YELLOW_H) # ground
                drawPlatforms()
                djb.display.show()
                
                explosionFX() # ************************************
                if (ticks_ms()-frameRate) > 50:
                        animToggle += 1
                        if animToggle > 3:
                            animToggle = 0
                        frameRate = ticks_ms()
        
        clouds[cloudIndex].state = 1
        clouds[cloudIndex].x = bottomRocketX
        clouds[cloudIndex].y = bottomRocketY + 4
        clouds[cloudIndex].time = ticks_ms()
        cloudIndex += 1
        if cloudIndex > 9:
            cloudIndex = 0
        drawClouds()
        
        clouds[cloudIndex].state = 1
        clouds[cloudIndex].x = bottomRocketX - 4
        clouds[cloudIndex].y = bottomRocketY
        clouds[cloudIndex].time = ticks_ms()
        cloudIndex += 1
        if cloudIndex > 9:
            cloudIndex = 0
        drawClouds()
        
        clouds[cloudIndex].state = 1
        clouds[cloudIndex].x = bottomRocketX + 4
        clouds[cloudIndex].y = bottomRocketY
        clouds[cloudIndex].time = ticks_ms()
        cloudIndex += 1
        if cloudIndex > 9:
            cloudIndex = 0
        drawClouds()
        
        jetManX = 60
        jetManY = 47
        gameState = 1
        fuelPercent = 0
        fuelX = FUELRANDOM()
        fuelY = -8

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def drawClouds():
        for index in range (0,9):
                if clouds[index].state > 0:
                        if clouds[index].state == 1:
                                djb.display.sprite(36, int(clouds[index].x),int(clouds[index].y),djb.display.BLACK,WHITE_H_PAL) # 36 CLOUD1
                        elif clouds[index].state == 2:
                                djb.display.sprite(37, int(clouds[index].x),int(clouds[index].y),djb.display.BLACK,WHITE_H_PAL) # 37 CLOUD2
                        elif clouds[index].state == 3:
                                djb.display.sprite(38, int(clouds[index].x),int(clouds[index].y),djb.display.BLACK,WHITE_H_PAL) # 38 CLOUD3
                        if (ticks_ms()-clouds[index].time) > 100:
                                clouds[index].state += 1
                                if clouds[index].state > 3:
                                    clouds[index].state = 0
                                clouds[index].time = ticks_ms()

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def drawlasers():
        for index in range (0,20):
                if laserbeams[index].length != 0:
                        beamLength = laserbeams[index].length
                        if beamLength > 8:
                            beamLength = 8
                        for multiplier in range (0,beamLength):
                                if laserbeams[index].length > 4 and multiplier < 4:
                                    djb.display.sprite(57, int(laserbeams[index].x)+((8*multiplier)*(1 if laserbeams[index].direction else -1)),int(laserbeams[index].y),djb.display.BLACK,RED_H_PAL if multiplier%2 else GREEN_H_PAL) # 57 LASER2
                                else:
                                    djb.display.sprite(56, int(laserbeams[index].x)+((8*multiplier)*(1 if laserbeams[index].direction else -1)),int(laserbeams[index].y),djb.display.BLACK,BLUE_H_PAL if multiplier%2 else YELLOW_H_PAL) # 56 LASER1
                                checkForHit(int(laserbeams[index].x)+((8*multiplier)*(1 if laserbeams[index].direction else -1)), int(laserbeams[index].y))

                        if (ticks_ms()-laserbeams[index].time) > 20:
                                laserbeams[index].length += 1
                                if laserbeams[index].length > 8:
                                    laserbeams[index].x += (8*(1 if laserbeams[index].direction else -1))
                                if laserbeams[index].length > 16:
                                    laserbeams[index].length = 0
                                laserbeams[index].time = ticks_ms()

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def moveThings():
        global bonusState, jetManX, jetManY, subState, cloudIndex, gameDifficulty,bonusY,bonusX, fuelY, fuelX, fuelPercent, middleRocketY, middleRocketX, topRocketX, topRocketY
        for index in range (0,gameDifficulty):
                direction = monsters[index].direction
                xRate = monsters[index].xRate
                yRate = monsters[index].yRate

                monsters[index].x = monsters[index].x + (xRate if direction else -xRate)
                monsters[index].y = monsters[index].y + yRate

                topA = monsters[index].y
                bottomA = monsters[index].y + 7
                leftA = monsters[index].x
                rightA = monsters[index].x + 7
                # get the bounding boxes of the platforms and monsters
                for platformIndex in range (0,9,3):
                        length = platforms[platformIndex+2]
                        leftB = platforms[platformIndex]
                        leftB = leftB * 8
                        topB = platforms[platformIndex+1]
                        topB = topB * 8
                        rightB = leftB+(8*length)
                        bottomB = topB + 3

                        # check if object A (monster) has hit object B (platform)
                        if topA <= bottomB and bottomA >= topB and leftA <= rightB and rightA >= leftB:
                                if monsterType == 0:
                                        clouds[cloudIndex].state = 1
                                        clouds[cloudIndex].x = leftA
                                        clouds[cloudIndex].y = topA
                                        clouds[cloudIndex].time = ticks_ms()
                                        cloudIndex += 1
                                        if cloudIndex > 9:
                                            cloudIndex = 0

                                        DIRECTION = randint(0,1)
                                        monsters[index].x = RANDOMXR() if DIRECTION else RANDOMXL()
                                        monsters[index].y = RANDOMY()
                                        monsters[index].xRate = RANDOMXRATE()
                                        monsters[index].yRate = RANDOMYRATE()
                                        monsters[index].direction = DIRECTION
                                else:
                                        # horizontal collision
                                        if leftA < leftB or rightA > rightB:
                                                monsters[index].direction = -(monsters[index].direction)
                                        
                                        # vertical collision
                                        if bottomA > bottomB or topA < topB:
                                                monsters[index].yRate = -yRate
                if (monsters[index].x > 127) or (monsters[index].x < -7.0):
                        monsters[index].x = -7 if direction else 127
                        monsters[index].xRate = RANDOMXRATE()
        
                if (monsters[index].y > 57) or (monsters[index].y < 7):
                        monsters[index].yRate = -(monsters[index].yRate)
                
                if randint(0,3000) == 1500 and monsterType != 0:
                    monsters[index].direction = -monsters[index].direction;
                if randint(0,1000) == 500 and monsterType != 0:
                    monsters[index].yRate = RANDOMYRATE()

        if bonusState == 1:
                for index in range (0,9,3):
                        length = platforms[index+2]
                        platformX = platforms[index]
                        platformX = (platformX*8)
                        platformY = platforms[index+1]
                        platformY = platformY*8
                        platformEnd = platformX+(8*length)

                        if ( (bonusY == (platformY-8) and ((bonusX+6) >= platformX) and (bonusX+2) <= platformEnd)):
                                bonusY = platformY-8
                                bonusState = 2 # landed
                        else: bonusY += 0.1
                        if bonusY > 55:
                                bonusY = 55
                                bonusState = 2 # landed

        if subState == 1: #picked up middle rocket section
                middleRocketX = jetManX
                middleRocketY = jetManY+8
                if (jetManX == bottomRocketX):
                        subState=2

        elif subState == 2: # middle section falling
                middleRocketY += 0.2
                if middleRocketY >= 47:
                        middleRocketY = 47
                        subState = 3
        elif subState == 4: # picked up top section
                topRocketX = jetManX
                topRocketY = jetManY+8
                if jetManX == bottomRocketX:
                        subState = 5
        elif subState == 5: # top section falling
                topRocketY += 0.2
                if topRocketY >= 39:
                        topRocketY = 39

                        fuelX = FUELRANDOM()
                        fuelY = -8
                        subState = 6
        elif subState == 6: # fuel falling
                for index in range (0,9,3):
                        length = platforms[index+2]
                        platformX = platforms[index]
                        platformX = (platformX*8)
                        platformY = platforms[index+1]
                        platformY = platformY*8
                        platformEnd = platformX+(8*length)

                        if (fuelY == (platformY-8) and ((fuelX+6) >= platformX) and ((fuelX+2)<=platformEnd)):
                                fuelY = platformY-8
                                subState = 7
                        else: fuelY += 0.1
                        if fuelY > 55:
                                fuelY = 55
                                subState = 7
        elif subState == 8: # jet man carrying fuel
                fuelX = jetManX
                fuelY = jetManY+8
                if jetManX == bottomRocketX:
                        subState = 9
        elif subState == 9: # fuel falling onto rocket
                fuelY += 0.2
                if fuelY >= 55:
                        fuelX = FUELRANDOM()
                        fuelY = -8
                        fuelPercent += 25
                        subState = 6
                        if fuelPercent >= 100:
                            subState = 10

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def moveJetMan():
        global jetManX, jetManY, jetManXRate, jetManYRate, jetManDirection, jetManState
        jetManX = jetManX + (jetManXRate if jetManDirection else -jetManXRate)
        jetManY = jetManY + jetManYRate
        
        if jetManX > 119:
                jetManXRate = 0
                jetManX = 119

        if jetManX < 0:
                jetManXRate = 0
                jetManX = 0

        if jetManY < 0:
                jetManYRate = 0
                jetManY = 0

        if jetManY >= 47:
                jetManYRate = 0
                jetManY = 47
                jetManState = 0           # Standing

        for index in range (0,9,3):
                length = platforms[index+2]
                platformX = platforms[index]
                platformX = (platformX*8)
                platformY = platforms[index+1]
                platformY = platformY*8
                platformEnd = platformX+(8*length)

                if (jetManState == 0) and (jetManY < 47) and ((jetManX+6 < platformX) or (jetManX > platformEnd)):
                        jetManState = 2
                        jetManYRate = 0.5

                if (jetManX+6 >= platformX) and ((jetManX+4) <= platformEnd) and (jetManY == platformY-16):
                        jetManState = 0
                        jetManY = platformY-16
                        jetManXRate = 0
                        jetManYRate = 0

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def checkButtons():
        global subState, lastPressed, laserIndex, jetManX, jetManDirection, jetManXRate, jetManYRate
        
        djb.scan_jst_btn()
        
        if djb.pressed(djb.btn_A) or djb.pressed(djb.btn_Up):
                jetPacFire()

        if not djb.pressed(djb.btn_A) and not djb.pressed(djb.btn_Up):
                jetPacRelease()
        
        if not djb.pressed(djb.btn_Right):
                jetManXRate = 0

        if not djb.pressed(djb.btn_Left):
                jetManXRate = 0
        
        if djb.pressed(djb.btn_Right):
                jetManXRate = 1
                jetManDirection = 1

        if djb.pressed(djb.btn_Left):
                jetManXRate = 1
                jetManDirection = 0

        if (subState < 11) and (djb.pressed(djb.btn_B) or djb.pressed(djb.btn_Down)) and (ticks_ms()-lastPressed) > 100:
                laserbeams[laserIndex].x = jetManX + (10 if jetManDirection else -10)
                laserbeams[laserIndex].length = 1
                laserbeams[laserIndex].y = jetManY+9
                laserbeams[laserIndex].direction = jetManDirection
                laserbeams[laserIndex].time = ticks_ms()
                laserIndex += 1
                if laserIndex > 19:
                    laserIndex = 0
                
                '''
                for start in range (50,125):
                    digitalWrite(2, HIGH) #positive square wave
                    digitalWrite(5, LOW) #positive square wave
                    delayMicroseconds(start)      #192uS
                    digitalWrite(2, LOW) #neutral square wave
                    digitalWrite(5, HIGH) #positive square wave
                    delayMicroseconds(start) #192uS
                '''
                for freq in range (1000,500,-100):
                    djb.play_freq(freq,5)
                    
                lastPressed = ticks_ms()


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def jetPacFire():
        global jetPacFired, cloudIndex, jetManYRate, jetManX, jetManY, jetManState
        jetManState = 1 # rising;
        jetManYRate = -1

        if jetPacFired == False:
                clouds[cloudIndex].state = 1
                clouds[cloudIndex].x = jetManX
                clouds[cloudIndex].y = jetManY+8
                clouds[cloudIndex].time = ticks_ms()
                cloudIndex += 1
                if cloudIndex > 9:
                    cloudIndex = 0
        jetPacFired = True


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def jetPacRelease():
        global jetManState, jetManYRate, jetPacFired
        if jetManState == 1:
                jetManState = 2 # falling;
                jetManYRate = 0.5
        jetPacFired = False


#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def checkForHit(laserX, laserY):
        global score, cloudIndex, gameDifficulty
        for index in range (0,gameDifficulty):
                hit = False
                x = monsters[index].x
                y = monsters[index].y
                #boolean direction = monsters[index].direction;

                if (laserY >= y and laserY <= y+7) and (laserX >= x and laserX <= x+7):
                        hit = True

                if hit == True:
                        clouds[cloudIndex].state = 1

                        explosionFX()
                        explosionFX()

                        clouds[cloudIndex].x = x
                        clouds[cloudIndex].y = y
                        clouds[cloudIndex].time = ticks_ms()
                        cloudIndex += 1
                        if cloudIndex > 9:
                            cloudIndex = 0
                        score += 25

                        DIRECTION = randint(0,1)
                        monsters[index].x = RANDOMXR() if DIRECTION else RANDOMXL()
                        monsters[index].y = RANDOMY()
                        monsters[index].xRate = RANDOMXRATE()
                        monsters[index].yRate = RANDOMYRATE()
                        monsters[index].direction = DIRECTION

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def checkJetManHit():
        global jetManX, jetManY, subState, cloudIndex, lives, gameState, lives, gameDifficulty
        for index in range (0,gameDifficulty):
                hit = False
                x = monsters[index].x
                y = monsters[index].y
                manX = jetManX
                manY = jetManY
                #boolean direction = monsters[index].direction;

                if ((x >= manX+1 and x <= manX+6) and (y >= manY+1 and y <= manY+14)) or ((x+7 >= manX+1 and x+7 <= manX+6) and (y+7 >= manY+1 and y+7 <= manY+14)):
                        hit = True
                
                if hit == True:
                        if subState == 8:
                            subState = 6

                        explosionFX()
                        explosionFX()
                        explosionFX()
                        explosionFX()
                        
                        '''
                        clouds[cloudIndex].state = 1
                        clouds[cloudIndex].x = manX
                        clouds[cloudIndex].y = manY + 4
                        clouds[cloudIndex].time = ticks_ms()
                        cloudIndex += 1
                        if cloudIndex > 9:
                            cloudIndex = 0
                        #drawClouds() # useless ??????

                        clouds[cloudIndex].state = 1
                        clouds[cloudIndex].x = manX - 4
                        clouds[cloudIndex].y = manY
                        clouds[cloudIndex].time = ticks_ms()
                        cloudIndex += 1
                        if cloudIndex > 9:
                            cloudIndex = 0
                        #drawClouds() # useless ??????
                        '''
                        clouds[cloudIndex].state = 1
                        clouds[cloudIndex].x = manX + 4
                        clouds[cloudIndex].y = manY
                        clouds[cloudIndex].time = ticks_ms()
                        cloudIndex += 1
                        if cloudIndex > 9:
                            cloudIndex = 0
                        #drawClouds() # useless ??????
                        
                        gameState = 0
                        jetManX = 60
                        jetManY = 47
                        jetManDirection = 1
                        jetManXRate = 0
                        jetManYRate = 0

                        lives -= 1
                        if lives < 0:
                            gameState = 2
                        djb.play_freq(800,200)
                        djb.play_freq(600, 200)
                        djb.play_freq(200, 400)
                        for x in range (0,300):
                                djb.display.fill(0)
                                djb.display.hline(0, 63, 128, djb.display.YELLOW_H) # ground
                                drawPlatforms()
                                drawThings()
                                drawClouds()
                                drawlasers()
                                djb.display.show()

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def explosionFX():
        # Explosion sound
        for start in range (0,4):
                '''
                digitalWrite(2, HIGH);
                digitalWrite(5, LOW);
                delayMicroseconds(random(100));
                digitalWrite(2, LOW);
                digitalWrite(5, HIGH);
                delayMicroseconds(random(100));
                '''
                djb.play_freq(randint(10,100),5)
                #sleep_ms(10)
                #djb.stop_beep()

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def gameOn():
        global frameRate, fuelPercent, animToggle, subState, bonusState, bonusX, bonusY, bonusType
        djb.display.hline(0, 63, 128, djb.display.YELLOW_H) # ground
        if fuelPercent > 0 and subState < 11:
                if ((animToggle%2) == 0) and (fuelPercent == 100):
                    djb.display.hline(0,0,int(1.28*fuelPercent), djb.display.GREEN_H)
                if fuelPercent < 100:
                    djb.display.hline(0,0,int(1.28*fuelPercent), djb.display.RED_H)

        drawPlatforms()
        drawThings()
        if subState < 11:
                drawJetMan()
                checkJetManHit()
        drawClouds()
        drawlasers()
        pickUpItem()

        checkButtons()
        moveJetMan()
        moveThings()

        if subState > 6 and bonusState == 0 and randint(0,500) == 250:
                bonusX = FUELRANDOM()
                bonusY = -8
                bonusState = 1 # item created
                bonusType = randint(0,5)

        if (ticks_ms() - frameRate) > 50:
                animToggle += 1
                if animToggle > 3:
                    animToggle = 0
                frameRate = ticks_ms()

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def gameOver():
        global score, highScore, lives, gameState,rocketStep, level, gameDifficulty, subState,fuelPercent, levelStep, jetManX, jetManY, fuelY, jetManXRate, jetManYRate, jetManDirection, monsterType, jetManState 
        #if (score > highScore) EEPROM.put(SAVELOCATION, score); delay(100);
        djb.display.fill(0)
        djb.display.center_text("GAME OVER ", djb.display.RED_H)
        if score > highScore:
            djb.display.center_text_XY("NEW HIGH SCORE",-1, 2) # ?????? SIZE
        else:
            djb.display.center_text_XY("SCORE",-1, 2) # ???????? SIZE

        #len = floor (log10 (abs (int(score)))) + 1;
        djb.display.center_text_XY(str(score), -1, 15)
        djb.display.show()
        sleep_ms(3000)

        level = 1
        gameDifficulty = 2
        levelStep = 0
        rocketStep = 0
        monsterType = 0
        gameState = 0
        subState = 0
        lives = 4
        score = 0

        fuelY = -8
        fuelPercent = 0

        jetManX = 60
        jetManY= 47
        jetManXRate = 0
        jetManYRate = 0
        jetManDirection = 1
        jetManState = 0

        cloudIndex = 0
        jetPacFired = 0
        buttonBPressed = False

        initialiseGameState()
        initialiseRocket()
        createMonsters()
        levelStart()

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def levelStart():
        #EEPROM.get(SAVELOCATION, highScore);
        global gameState, bonusState, level, score, highScore
        djb.display.fill(0)

        djb.display.text("Score:", 0, 1)
        djb.display.text(str(score), 86, 1)

        djb.display.text("High Score:", 0, 14)
        djb.display.text(str(score if score > highScore else highScore), 86, 14)

        djb.display.sprite(33, 0, 27,djb.display.BLACK,RED_H_PAL) # 33
        djb.display.text(str(lives), 86, 27)

        djb.display.text("LEVEL ", 24, 46)
        djb.display.text(str(level), 86, 46)

        djb.display.show()
        
        djb.scan_jst_btn()
        while not djb.just_pressed(djb.btn_A) and not djb.just_pressed(djb.btn_B):
            djb.scan_jst_btn()
        djb.play_freq(1000, 200)
        sleep_ms(500)
        createMonsters()
        gameState = 1
        bonusState = 0

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def levelComplete():
        global subState, level, monsterType, levelStep, rocketStep, fuelPercent, gameDifficulty 
        initialiseGameState()
        subState = 0
        level += 1
        monsterType += 1
        if monsterType == 8:
                monsterType = 0
                gameDifficulty += 1
                if gameDifficulty > 10:
                    gameDifficulty = 10
        
        levelStart()
        levelStep += 1
        if levelStep != 5:
                rocketLand()
                subState = 6
        else:
                initialiseRocket()
                subState = 0
                levelStep = 0
                rocketStep += 1
                if rocketStep == 4:
                    rocketStep = 0
    
        fuelPercent = 0

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
def pickUpItem():
        global jetManX, jetManY, bonusState, subState, bonusX, bonusY, score, bottomRocketX, bottomRocketY, cloudIndex
        topJ = jetManY + 8
        bottomJ = jetManY + 15
        leftJ = jetManX
        rightJ = jetManX + 7

        if bonusState != 0: # pick up the bonus item
                topR = bonusY
                bottomR = bonusY + 7
                leftR = bonusX
                rightR = bonusX + 7
                if topJ <= bottomR and bottomJ >= topR and leftJ <= rightR and rightJ >= leftR:
                        bonusState = 0
                        score += 250
                        djb.play_tone('A5',50)
                        djb.play_tone('A6',50)
                        djb.play_tone('A7',100)
        if subState == 0: # pick up the middle rocket section
                topR = middleRocketY
                bottomR = middleRocketY + 7
                leftR = middleRocketX
                rightR = middleRocketX + 7
                if topJ <= bottomR and bottomJ >= topR and leftJ <= rightR and rightJ >= leftR:
                        subState = 1
                        score += 100
                        djb.play_tone('A4',50)
                        djb.play_tone('A5',50)
                        djb.play_tone('A6',100)
        if subState == 3: # pick up the top rocket section
                topR = topRocketY
                bottomR = topRocketY + 7
                leftR = topRocketX
                rightR = topRocketX + 7
                if topJ <= bottomR and bottomJ >= topR and leftJ <= rightR and rightJ >= leftR:
                        subState = 4
                        score += 100
                        djb.play_tone('A4',50)
                        djb.play_tone('A5',50)
                        djb.play_tone('A6',100)
        if subState == 6 or subState == 7: # pick up fuel cell
                topR = fuelY
                bottomR = fuelY + 7
                leftR = fuelX
                rightR = fuelX + 7
                if topJ <= bottomR and bottomJ >= topR and leftJ <= rightR and rightJ >= leftR:
                        subState = 8
                        score += 100
                        djb.play_tone('A4',50)
                        djb.play_tone('A5',50)
                        djb.play_tone('A6',100)
        if subState == 10: # Walk into the rocket
                topR = bottomRocketY
                bottomR = bottomRocketY + 7
                leftR = bottomRocketX
                rightR = bottomRocketX + 7
                if topJ <= bottomR and bottomJ >= topR and leftJ <= rightR and rightJ >= leftR:
                        subState = 11

                        clouds[cloudIndex].state = 1
                        clouds[cloudIndex].x = bottomRocketX
                        clouds[cloudIndex].y = bottomRocketY + 4
                        clouds[cloudIndex].time = ticks_ms()
                        cloudIndex += 1
                        if cloudIndex > 9:
                            cloudIndex = 0

                        clouds[cloudIndex].state = 1
                        clouds[cloudIndex].x = bottomRocketX - 4
                        clouds[cloudIndex].y = bottomRocketY
                        clouds[cloudIndex].time = ticks_ms()
                        cloudIndex += 1
                        if cloudIndex > 9:
                            cloudIndex = 0

                        clouds[cloudIndex].state = 1
                        clouds[cloudIndex].x = bottomRocketX + 4
                        clouds[cloudIndex].y = bottomRocketY
                        clouds[cloudIndex].time = ticks_ms()
                        cloudIndex += 1
                        if cloudIndex > 9:
                            cloudIndex = 0
                        djb.play_tone('A4',50)
                        djb.play_tone('A5',50)
                        djb.play_tone('A6',100)

                        score += 500

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=
                        
def menu():
        global gameState
        up = True

        while True:
                djb.scan_jst_btn()
                if djb.just_pressed(djb.btn_Up):
                        up = True
                        djb.display.fill(0)
                if djb.just_pressed(djb.btn_Down):
                        up = False
                        djb.display.fill(0)
                if up == True:
                        djb.display.circle(3,23,3,djb.display.BLUE_H, True)
                else:
                        djb.display.circle(3,43,3,djb.display.BLUE_H, True)

                if djb.just_pressed(djb.btn_A):
                    if up == True:
                      sleep_ms(150)
                      gameState = 0
                      break
                    else:
                      sleep_ms(150)
                      eraseEEPROM();
                      gameState = 0
                      break
              

                djb.display.text("NEW GAME", 9, 20)
                djb.display.text("RESET HIGH SCORE", 9, 40)

                djb.display.show()

def eraseEEPROM():

    djb.display.fill(0)
    up = False

    while True:
            djb.scan_jst_btn()
            if djb.just_pressed(djb.btn_Up):
                  up = True
                  djb.display.fill(0)
            if djb.just_pressed(djb.btn_Down):
                  up = False
                  djb.display.fill(0)
            if up == True:
                    djb.display.circle(13,23,3,djb.display.BLUE_H, True)
            else:
                    djb.display.circle(13,43,3,djb.display.BLUE_H, True)

            if djb.just_pressed(djb.btn_A):
              if up == True:
                sleep_ms(150)
                highScore = 0   # First time run of program only then comment out and reload
                #EEPROM.put(SAVELOCATION, highScore);    // First time run of program only
                gameState = 0
                break
              else:
                sleep_ms(150)
                gameState = 0
                break

            djb.display.text("ARE YOU SURE?", 20, 0)
            djb.display.text("YES", 20, 20)
            djb.display.text("NO", 20, 40)

            djb.display.show()


################################

djb.display.load_image('game/jetpacloading.bin')
djb.display.show()
sleep_ms(1000)
initialiseRocket()

while True:
    if djb.display.next_frame():    
        djb.display.fill(0)

        if gameState == 0:
                levelStart()
        elif gameState == 1:
                gameOn()
        elif gameState == 2:
                gameOver()
        elif gameState == 3:
                levelComplete()
        elif gameState == 4:
                menu()
        djb.display.show()   
    #print(djb.display.last_frame_duration)
    #djb.display.show_and_wait()
