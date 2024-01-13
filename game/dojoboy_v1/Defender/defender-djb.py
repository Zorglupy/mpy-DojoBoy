#from LCD_1inch14 import LCD_1inch14
# all display, buttons, sound logics are in dojoboy.py module
from dojoboy_v1.dojoboy import DojoBoy

from machine import Pin,SPI,PWM, Timer
import framebuf, math
import utime, gc
from random import randint
from usys import exit
from micropython import const

# Initializing djb object
djb = DojoBoy(show_intro=True,width=160,height=128,framerate=30)


class Obj():
    def __init__(self,x,y,ax,ay,w,h):
        self.x = x
        self.y = y
        self.oldx = 0
        self.oldy = 0
        self.offsetx = 0
        self.ax = ax
        self.ay = ay
        self.onscreen = 0
        self.max_y = 128
        self.atmax_y = 0
        self.buf = bytearray(256)
        self.h = h
        self.w = w
        self.exp = 0
        self.dir = -1

class Screen():
    def __init__(self):
        self.xmax = 160
        self.xmin = 0
        self.oldxmin = 0
        self.set = 0

class Missile():
    def __init__(self):
        self.x_start = 0
        self.x_point = 0
        self.x_trail = 0
        self.x_erase = 0
        self.y = 0
        self.dir = 10
        self.active = 1
        
class Point():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.ax = 0
        self.ay = 0
        self.c = 0
        self.exp = 0
        self.deg = 0

player_xmax = 50 #220
PLAYER_XMIN = 10
SCREEN_XOFFSET = 10
DEMO_MODE = const(0)

player = Obj(10,100,1,-1,16,8)
screen = Screen()

aliens = []
m = Missile()
e = []         # explode point list
alien_e = []   # alien explode list


gticks = 0
debounce = 0


ship1_gfx = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x94, 0x94, 0xc5, 0xda, 0x39, 0xc8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0xa4, 0xf6, 0xa5, 0x16, 0x9c, 0xf5, 0xb5, 0x98, 0x4a, 0x4a, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0xf8, 0x00, 0xac, 0xb3, 0x9d, 0x16, 0x9c, 0xf5, 0x9d, 0x17, 0xad, 0x98, 0x5a, 0xac, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x84, 0xf3, 0xf8, 0x9f, 0xf8, 0x1f, 0xd2, 0x2c, 0x9d, 0x16, 0xa5, 0x37, 0xb5, 0x58, 0xb5, 0x98, 0x8b, 0xf8, 0x10, 0x19, 0x48, 0xf6, 0xff, 0x00, 0x00, 0x01, 0x08, 0x21, 0x00, 0x20, 
  0xf8, 0x00, 0xa5, 0x13, 0xf0, 0xfe, 0xf8, 0x1f, 0xf8, 0x1c, 0xf8, 0x1f, 0xd2, 0x5b, 0x9d, 0x55, 0x9c, 0xf6, 0xad, 0x35, 0xb5, 0x96, 0xad, 0x76, 0x9c, 0xd8, 0xb5, 0x98, 0xff, 0xff, 0x06, 0x60, 
  0x00, 0x20, 0x00, 0x00, 0xd0, 0x1a, 0xf8, 0x1f, 0xf8, 0x1f, 0xc3, 0x19, 0xdf, 0x5c, 0x9f, 0xd3, 0x03, 0xa0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

ship2_gfx = [  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x39, 0xc8, 0xc5, 0xda, 0x94, 0x94, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x4a, 0x4a, 0xb5, 0x98, 0x9c, 0xf5, 0xa5, 0x16, 0xa4, 0xf6, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x5a, 0xac, 0xad, 0x98, 0x9d, 0x17, 0x9c, 0xf5, 0x9d, 0x16, 0xac, 0xb3, 0xf8, 0x00, 
  0x00, 0x20, 0x08, 0x21, 0x00, 0x01, 0xff, 0x00, 0x48, 0xf6, 0x10, 0x19, 0x8b, 0xf8, 0xb5, 0x98, 0xb5, 0x58, 0xa5, 0x37, 0x9d, 0x16, 0xd2, 0x2c, 0xf8, 0x1f, 0xf8, 0x9f, 0x84, 0xf3, 0x00, 0x00, 
  0x06, 0x60, 0xff, 0xff, 0xb5, 0x98, 0x9c, 0xd8, 0xad, 0x76, 0xb5, 0x96, 0xad, 0x35, 0x9c, 0xf6, 0x9d, 0x55, 0xd2, 0x5b, 0xf8, 0x1f, 0xf8, 0x1c, 0xf8, 0x1f, 0xf0, 0xfe, 0xa5, 0x13, 0xf8, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0xa0, 0x9f, 0xd3, 0xdf, 0x5c, 0xc3, 0x19, 0xf8, 0x1f, 0xf8, 0x1f, 0xd0, 0x1a, 0x00, 0x00, 0x00, 0x20, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00]


alien_gfx = [  0x00, 0x00, 0x00, 0x00, 0x08, 0x01, 0x89, 0x3f, 0xa1, 0x3f, 0x00, 0x40, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x05, 0xc1, 0x99, 0x3f, 0xa0, 0xff, 0x00, 0x20, 0x06, 0x20, 0x00, 0x02, 0x00, 0x00, 
  0x00, 0x01, 0x05, 0xc0, 0x00, 0x01, 0x91, 0x1f, 0x99, 0x3f, 0xf8, 0x1f, 0x00, 0x02, 0x0d, 0xc0, 0x00, 0x40, 
  0x00, 0x41, 0x05, 0xc0, 0x00, 0x40, 0xf8, 0x1e, 0xca, 0x21, 0xf8, 0x3e, 0x00, 0x20, 0x05, 0xc2, 0x00, 0x20, 
  0x00, 0x20, 0x00, 0x20, 0x06, 0x20, 0xf0, 0x1e, 0xba, 0x20, 0xf8, 0x1f, 0x05, 0xa0, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x20, 0x05, 0xc0, 0x00, 0x21, 0xca, 0x03, 0x00, 0x00, 0x0d, 0xc0, 0x00, 0x01, 0x00, 0x00, 
  0x00, 0x02, 0x05, 0x60, 0x00, 0x03, 0x00, 0x01, 0xba, 0x40, 0x08, 0x00, 0x08, 0x03, 0x06, 0x00, 0x08, 0x03, 
  0x05, 0x60, 0x08, 0x02, 0x00, 0x01, 0x00, 0x60, 0xba, 0x40, 0x08, 0x00, 0x10, 0x01, 0x00, 0x40, 0x06, 0x00]





terrain =[0x2A,0xAA,0xAA,0xAA,0xAA,0xAA,0xAB,0xA1,0xD5,0x55,0x55,0x55,0x55,0x55,0xAA,0xBF,
0xFF,0xFF,0xFF,0xC0,0x00,0x00,0x00,0x55,0x55,0x57,0xFF,0xC0,0x01,0x55,0x55,0x55,
0x55,0x55,0x55,0x5F,0xE0,0x15,0x55,0x55,0x57,0xFF,0xF0,0x00,0x15,0x55,0x5F,0xFF,
0xFF,0xFF,0xFF,0x00,0x00,0x00,0x00,0x05,0x55,0x7F,0xFF,0xE0,0x00,0x05,0x55,0x55,
0x55,0x55,0xFC,0x05,0x55,0x55,0x50,0x01,0xFF,0xFF,0xFF,0xC0,0x00,0x0A,0xAA,0xAA,
0xAA,0xFF,0x00,0x00,0xFF,0xFF,0xFF,0xFF,0xF0,0x00,0x00,0x1F,0xE0,0x00,0x55,0x55,
0x55,0x40,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xB5,0x57,0xAA,0xAA,0xAA,0xF5,0x7F,0xD5,
0x55,0x55,0x57,0xFF,0x80,0x07,0xE0,0x7F,0xF1,0x55,0x7F,0xFF,0xFF,0x00,0x00,0x00,
0x00,0x00,0x0F,0xEF,0x76,0x91,0x11,0x11,0x5E,0xDB,0xE9,0x84,0x77,0xEC,0xC4,0x87,
0x47,0x98,0x08,0x98,0x3F,0xC3,0xCB,0xDB,0x9F,0xC7,0x5F,0x2F,0xC7,0x7D,0xEF,0xBF,
0xFA,0x4C,0x57,0x2B,0x61,0xEF,0xEF,0xFB,0xF7,0xE8,0x00,0x20,0x40,0x00,0x14,0x04,
0x04,0x3C,0x06,0x00,0x1D,0x07,0x3C,0xE1,0xA5,0x55,0x55,0x45,0x2A,0xAA,0xAA,0xAA,
0xA8,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x56,0xAA,0xAA,0xFE,0xAA,
0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xAA,0xEA,0xAA,0xAA,0xA8,0x02,0xAA,0xAA,0xAA,0xAA,
0xBF,0xBE,0x3E,0x63,0xFF,0xE0,0xD8,0x1C,0x18,0x2A,0xAB,0x1E,0x77,0x7A,0xAF,0xA8,
0x40,0x70,0x7D,0x40,0x0B,0xFB,0xFA,0xFF,0xC1,0x53,0x54,0x75,0x70,0x03,0x00,0x00]

# blit_image_file borrowed then butchered from Stewart Watkiss
# http://www.penguintutor.com/programming/picodisplayanimations
def blit_image_file (filename,width,height):
    display_buffer = bytearray(width * height * 2) 
#    global display_buffer
    with open (filename, "rb") as file:
        position = 0
        while position < (width * height * 2):
            current_byte = file.read(1)
            # if eof
            if len(current_byte) == 0:
                break
            # copy to buffer
            display_buffer[position] = ord(current_byte)
            position += 1
    file.close()
    return(display_buffer)

def show_title():
    buf=(framebuf.FrameBuffer(blit_image_file ("deftitle.bin",240,49),240,49, framebuf.RGB565))
    djb.display.blit(buf,00,40)
    djb.display.show()


def draw_terrain():
    step=10                                              # increment X by 10
    if screen.xmin != screen.oldxmin:
        for x in range(0,16):                            # screen = 24*10 wide
            y1=108+terrain[screen.oldxmin//10+x]//10
            y2=108+terrain[screen.oldxmin//10+x+1]//10
            x1=x*step-screen.oldxmin%10
            x2=x*step+10-screen.oldxmin%10            
            djb.display.line(x1,y1,x2,y2,djb.display.BLACK)
            y1=108+terrain[screen.xmin//10+x]//10
            y2=108+terrain[screen.xmin//10+x+1]//10
            x1=x*step-screen.xmin%10
            x2=x*step+10-screen.xmin%10
            djb.display.line(x1,y1,x2,y2,0x008A)  #brown


def init_explode(objhit,gfx): #n,s):  # obj, number, speed
    explode_cleanup()
    length = len(gfx)
    center = math.sqrt(length//2)//2
    j=0
    for i in range(0,length,2): #n):
        e.append(Point())
        ax= (j % objhit.w) - center
        ay= (j//objhit.w) - center
        e[j].x = objhit.offsetx + ax
        e[j].y=  objhit.y + ay
        e[j].ax = ax - player.ax
        e[j].ay = ay + objhit.ay
        e[j].c = gfx[i]+(gfx[i+1]<<8)
        j+=1
        
#         e[i].x=objhit.offsetx
#         e[i].y=objhit.y
#         e[i].ax = objhit.ax+randint(-10,10)/s
#         e[i].ay = objhit.ay+randint(-10,10)/s
       
def explode_cleanup():
    while len(e)>0:
        djb.display.pixel(int(e[0].x),int(e[0].y),djb.display.BLACK)
        d=e.pop(0)

def explode():    
    i=0
    while len(e)>0 and i< len(e):    
        if e[i].x >-1 and e[i].x<161 and e[i].y>-1 and e[i].y<129 and e[i].exp<50 and randint(0,10)>2:
            djb.display.pixel(int(e[i].x),int(e[i].y),djb.display.BLACK)
            e[i].x=int(e[i].x+e[i].ax)
            e[i].y=int(e[i].y+e[i].ay)
            djb.display.pixel(int(e[i].x),int(e[i].y),e[i].c) # djb.display.WHITE_H)
            e[i].exp+=1
        else:
            djb.display.pixel(int(e[i].x),int(e[i].y),djb.display.BLACK)
            d=e.pop(i)    # delete explosion point
            i-=1
        i+=1

def init_buffer(gfx,w,h):
    buf=bytearray()
    for i in gfx:
        buf.append(i)
    return(framebuf.FrameBuffer(buf,w,h, framebuf.RGB565))


def init_obj(obj,x,y,ax,ay,w,h):
    obj.x = x
    obj.y = y
    obj.ax = ax
    obj.ay = ay
    obj.h = h
    obj.w = w
    obj.exp = 0

def init_aliens():
    for i in range(0,10):
        aliens.append(Obj(randint(300,800),randint(5,120),0,0,9,8))
        aliens[i].buf=init_buffer(alien_gfx,aliens[i].w,aliens[i].h)

def offset_player(obj):
    global player_xmax                      # 
    obj.offsetx = obj.x                     # default x is on screen
    if obj.ax > 0:                          # if positive accel
        player_xmax-=1                      # move player left
        if player_xmax < 40:                # until 50 from left side
            player_xmax = 40
    else:
        player_xmax+=1                      # must be neg so move to right
        if player_xmax>120:                 # but limit to 40 from right side
            player_xmax = 120
    if obj.x > player_xmax :                # 
        obj.offsetx = player_xmax
        screen.xmax=obj.x + SCREEN_XOFFSET
        screen.oldxmin = screen.xmin
        screen.xmin=screen.xmax-160
    if obj.x < PLAYER_XMIN :
        obj.offsetx = PLAYER_XMIN
        screen.oldxmin = screen.xmin
        screen.xmin=  obj.x - SCREEN_XOFFSET
    if obj.x > 1000:
        obj.x = 140
    if obj.x < 0:
        obj.x = 1000
    #print("                  ",end="\r")
    #print(obj.x,obj.offsetx,screen.xmax,screen.xmin,end="\r")
    #utime.sleep(0.5)

def display_aliens():
    for i in aliens:
        i.onscreen = 0
        if i.x<screen.xmax+1 and i.x>screen.xmin-10:            
            i.onscreen = 1
            i.offsetx = i.x + (160-screen.xmax)
            move_aliens(i)
            if collision(i,player.offsetx,player.y) and player.exp == 0:
                if player.dir == 1:
                    init_explode(player,ship2_gfx)#20,3)
                else:
                    init_explode(player,ship1_gfx)#20,3)
                player.exp = 1
                djb.display.fill_rect(player.offsetx,player.y,16,9,djb.display.BLACK)
            show(i)
      

def move_aliens(obj):      # moves aliens up or down
    if randint(0,10)<5:
        obj.y+=1
    if randint(0,10)<5:
        obj.y-=1
        if obj.y < 1:
            obj.y=1
        

def move_object(obj):
    obj.oldx = obj.offsetx
    obj.oldy = obj.y
    obj.x+=obj.ax
    obj.y+=obj.ay
    if obj.y < 1:
        obj.y=1
    if obj.y > 125:
        obj.y=125
    if obj.y > obj.max_y:
        obj.y = obj.max_y
        obj.atmax_y = 1
    if obj.y <0:
        obj.y = 0


def show(obj):
    if obj.exp == 0:
        djb.display.rect(obj.oldx,obj.oldy,obj.w,obj.h,djb.display.BLACK)
        djb.display.blit(obj.buf,obj.offsetx,obj.y)


def move_missile():
    #m.x_point+=m.dir
    spec=m.dir*1
    tip=10*abs(m.dir)//m.dir
    djb.display.hline(m.x_point+spec+tip,m.y,2,djb.display.WHITE_H)                # white tip
    djb.display.hline(m.x_point+spec,m.y,10,djb.display.RED_H)                     # red main body
    if abs(m.x_point-m.x_start) > abs(spec) and randint(0,10)>4:  # speckle 
        djb.display.hline(m.x_point-spec,m.y,4,djb.display.BLACK)
    if m.dir>0:                                                       # erase right
        djb.display.hline(m.x_start,m.y,(m.x_point-m.x_start)//3,djb.display.BLACK)
    if m.dir<0:                                                       # erase left
        djb.display.hline(m.x_start-(m.x_start-m.x_point)//3,m.y,(m.x_start-m.x_point)//3,djb.display.BLACK)
    if m.x_point>160:
        djb.display.hline(m.x_start-m.dir,m.y,160-m.x_start+m.dir,djb.display.BLACK)     # erase all
        m.active = 0
    if m.x_point<0:
        djb.display.hline(0,m.y,m.x_start-spec,djb.display.BLACK) # erase all
        m.active = 0
    hit_aliens(m.x_point,m.y)
    #djb.display.show()
    m.x_point+=m.dir
    #exit()

def hit_aliens(x,y):
    i=0
    while len(aliens)>i and len(aliens)>0:
        if aliens[i].onscreen == 1 and collision(aliens[i],x,y):
            init_explode(aliens[i],alien_gfx) #(11-len(aliens))*2,3)
            djb.display.fill_rect(aliens[i].offsetx,aliens[i].y,9,9,djb.display.BLACK)
            d=aliens.pop(i)
            i-=1
        i+=1

def collision(obj,x,y): # check obj.x,y near x,y 
    return(obj.offsetx < x+8 and obj.offsetx > x-8 and obj.y < y+5 and obj.y > y-5) # return 1 if true
        

def init_missile():
    m.x_point=player.offsetx+0
    m.x_start=player.offsetx+0
    m.y=player.y+4
    m.dir = abs(m.dir) * (player.ax//abs(player.ax))
    m.active=1

    
def player_auto():
    if player.exp == 0 and m.active==0:
        init_missile()
    if player.x > 900:
        player.ax = -1
        player.buf=ship_L_buf
        player.dir = -1
    if player.x < 10:
        player.ax = 1
        player.buf=ship_R_buf
        player.dir = 1
    if player.y < 2:
        player.ay = 1
    if player.y > 120:
        player.ay = -1

def buttons():
    global rfire, debounce
    djb.scan_jst_btn() #scan buttons
    
    #if (key0.value() != 0) and (key1.value() != 0):
    player.ay=0
    if djb.pressed(djb.btn_Up):             # ship up:
        player.ay -= 1
    if djb.pressed(djb.btn_Down):             # ship down
        player.ay += 1
    if djb.pressed(djb.btn_A) and player.exp == 0 and m.active==0:
        init_missile()
    if djb.pressed(djb.btn_B) and debounce > 20:
        debounce = 0
        player.dir=-player.dir
        if player.dir == 1:
            player.buf=ship_L_buf
            player.ax=-1
        else:
            player.buf=ship_R_buf
            player.ax=1
    debounce+=1

def show_timer(timer):
    djb.display.show()


if __name__=='__main__':
    #pwm = PWM(Pin(BL))
    #pwm.freq(1000)
    #pwm.duty_u16(32768)#max 65535
    djb.display.fill(djb.display.BLACK)
    djb.display.show()
    

    #key0 = Pin(15,Pin.IN)
    #key1 = Pin(17,Pin.IN)
    #key2 = Pin(2 ,Pin.IN)
    #key3 = Pin(3 ,Pin.IN)

    init_obj(player,10,100,1,-1,16,8)
    player.buf=init_buffer(ship1_gfx,player.w,player.h)
    ship_R_buf=init_buffer(ship1_gfx,player.w,player.h)
    ship_L_buf=init_buffer(ship2_gfx,player.w,player.h)
    init_aliens()
    #show_title()
    t=1
    #utime.sleep(2)
    djb.display.fill(djb.display.BLACK)

    
    #tim = Timer(3)      #set the timer ESP32
    tim = Timer()      #set the timer ESP32
    tim.init(freq=30, mode=Timer.PERIODIC, callback=show_timer)  # Start timing

    
    try:
        while(0):
            gticks = utime.ticks_us()
            for i in range(0,100):
                player.offsetx=randint(0,160)
                player.y=randint(0,128)
                #djb.display.fill(djb.display.BLACK)
                djb.display.fill_rect(player.offsetx,player.y,player.w,player.h,randint(0,65535))
                #djb.display.blit(player.buf,player.offsetx,player.y)
                #djb.display.show()
                #show(player)
            djb.display.show()
            delta = utime.ticks_diff(utime.ticks_us(), gticks)
            fps=1_000_000/delta          # frames per second
            #print(gc.mem_free())
            print(delta/1_000_000)
         
            
        while(1):
            draw_terrain()
            move_object(player)
            if DEMO_MODE:
                player_auto()
            else:
                buttons()
            offset_player(player)
            for i in aliens:
                move_object(i)
            show(player)
            display_aliens()
            if m.active == 1:
                move_missile()
            t+=1
            if t==5:
                explode()
                t=0
            if player.exp==1 and len(e)==0:          #player dead
                init_obj(player,10,100,1,-1,16,8)
                player.buf=ship_R_buf
                djb.display.fill(djb.display.BLACK)
                screen.__init__()
            if len(aliens)<1:                       # aliens all dead
                init_aliens()
            
            delta = utime.ticks_diff(utime.ticks_us(), gticks)
            gticks = utime.ticks_us()
            fps=1_000_000/delta          # frames per second
            #print(gc.mem_free())
            print(fps)
            
    except KeyboardInterrupt:
        print(player.x,player.y)
        print('Explosions:',len(e))
        print('Aliens:',len(aliens))
        print('.ax:',player.ax)
        print('done')

