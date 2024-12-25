#
# MicroPython ST7789 TFT Display driver, SPI interfaces for DojoBoy
#
#   Display Driver for DojoBoy V1.1 25/12/24
#

from micropython import const
from machine import Pin, SPI
from dojoboy_v1.djbframebuf import djbFrameBuffer
from framebuf import RGB565
from time import sleep_ms
import gc

__version__ = "1.1 25/12/24"
__repo__ = "https://github.com/zorglupy/dojoboy"
                           
# register definitions
SWRESET   = const(b'\x01')
SLPOUT    = const(b'\x11')
NORON     = const(b'\x13')
TEOFF     = const(b'\x34')
TEON      = const(b'\x35')
MADCTL    = const(b'\x36')
COLMOD    = const(b'\x3A')
GCTRL     = const(b'\xB7')
VCOMS     = const(b'\xBB')
LCMCTRL   = const(b'\xC0')
VDVVRHEN  = const(b'\xC2')
VRHS      = const(b'\xC3')
VDVS      = const(b'\xC4')
FRCTRL2   = const(b'\xC6')
PWCTRL1   = const(b'\xD0')
PORCTRL   = const(b'\xB2')
GMCTRP1   = const(b'\xE0')
GMCTRN1   = const(b'\xE1')
INVOFF    = const(b'\x20')
INVON     = const(b'\x21')
GAMSET    = const(b'\x26')
DISPOFF   = const(b'\x28')
DISPON    = const(b'\x29')
CASET     = const(b'\x2A')
RASET     = const(b'\x2B')
RAMWR     = const(b'\x2C')
PWMFRSEL  = const(b'\xCC')

class Display(djbFrameBuffer):
    
    def __init__(self, width=240, height=240, id_=0, sck=14, mosi=15,
                 dc=12, cs=13, bl=28, baudrate=62_500_000, framerate=30):
#                 dc=12, cs=13, rst=20, bl=28, baudrate=62_500_000, framerate=30):
        self.width = width
        self.height = height
        
        self._spi = SPI(id_, sck=Pin(sck), mosi=Pin(mosi), baudrate=baudrate, polarity=0, phase=0)
        self._dc = Pin(dc, Pin.OUT)
        #self._rst = Pin(rst, Pin.OUT)
        self._cs = Pin(cs, Pin.OUT)
        self._bl = Pin(bl, Pin.OUT)
        
        self.buffer_mode = RGB565
        
        gc.collect()

        self.buffer = memoryview(bytearray(height * width * 2))
        super().__init__(self.buffer, width, height, self.buffer_mode, framerate)

        self.init_display()
        self.init_frame()
        
    def write_cmd(self, cmd=None, data=None):
        self._cs(0)
        if cmd:
            self._dc(0) # command mode
            self._spi.write(cmd)
        if data:
            self._dc(1) # data mode
            self._spi.write(data)
        self._cs(1)

    def init_display(self):
        
        self._bl(0) # Turn backlight off initially to avoid nasty surprises
        
        # Hardware reset
        #self._dc(0)
        #self._rst(1)
        #sleep_ms(1)
        #self._rst(0)
        #sleep_ms(1)
        #self._rst(1)
        #sleep_ms(1)

        self.write_cmd(SWRESET)
        sleep_ms(150)
        self.write_cmd(SLPOUT)  # leave sleep mode
        sleep_ms(10)

        #self.write_cmd(INVON)   # set inversion mode -> 320x240 not set
        
        self.write_cmd(TEON) # enable frame sync signal if used
        self.write_cmd(COLMOD, const(b'\x05')) # 16 bits per pixel
        self.write_cmd(PORCTRL, const(b'\x0c\x0c\x00\x33\x33'))
        self.write_cmd(GCTRL, const(b'\x14'))
        self.write_cmd(VCOMS, const(b'\x37'))
        self.write_cmd(LCMCTRL, const(b'\x2c'))
        self.write_cmd(VDVVRHEN, const(b'\x01'))
        self.write_cmd(VRHS, const(b'\x12'))
        self.write_cmd(VDVS, const(b'\x20'))
        self.write_cmd(PWCTRL1, const(b'\xa4\xa1'))
        self.write_cmd(FRCTRL2, const(b'\x0f'))
        self.write_cmd(GMCTRP1, const(b'\xD0\x04\x0D\x11\x13\x2B\x3F\x54\x4C\x18\x0D\x0B\x1F\x23'))
        self.write_cmd(GMCTRN1, const(b'\xD0\x04\x0C\x11\x13\x2C\x3F\x44\x51\x2F\x1F\x1F\x20\x23'))
        
        self.write_cmd(MADCTL, const(b'\x60')) # Rotation 90°       
        #self.write_cmd(MADCTL, const(b'\xA0')) # Rotation 270°
        
        self.write_cmd(CASET, const(b'\x00\x00\x01\x3F'))  # 320x240 -> 0 , 319
        self.write_cmd(RASET, const(b'\x00\x00\x00\xEF'))  # 320x240 -> 0 , 239
        #self.write_cmd(CASET, const(b'\x00\x50\x01\x3F'))  # 240x240 -> 80 , 319
        #self.write_cmd(RASET, const(b'\x00\x00\x00\xEF'))  # 240x240 -> 0 , 239
        self.write_cmd(NORON)  # NORON Normal display mode
        self.write_cmd(DISPON)
   
        self._cs(0)
        self._dc(0)
        self._spi.write(RAMWR)
        self._dc(1)
        for hline in range (0, 240):
            for line in range(0, 320 * 2):
                self._spi.write(b'\x00')
        self._cs(1)
        
        self._bl(1) # Turn backlight on
        
    def init_frame(self):
        ws = ((320 - self.width)//2) # 320x240
        #ws = ((240 - self.width)//2)+80 # 240x240
        we = 319 - ((320 - self.width)//2) # 320x240
        #we = 239 - ((240 - self.width)//2)+80 #240x240
        web = we.to_bytes(2, 'big')
        wsb = ws.to_bytes(2, 'big')
        frame_w = wsb + web
        self.write_cmd(CASET, bytearray(frame_w))
        hs = ((240 - self.height)//2)
        he = 239 - ((240 - self.height)//2)
        heb = he.to_bytes(2, 'big')
        hsb = hs.to_bytes(2, 'big')
        frame_h = hsb + heb
        self.write_cmd(RASET, bytearray(frame_h))
        self.write_cmd(RAMWR)

    def power_off(self):
        pass

    def power_on(self):
        pass

    def contrast(self, contrast):
        pass

    def invert(self, invert):
        pass

    def rotate(self, rotate):
        pass

    def show(self):
        self.write_cmd(RAMWR, self.buffer)  #Write frame buffer to display buffer
