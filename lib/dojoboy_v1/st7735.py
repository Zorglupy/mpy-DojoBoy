#
# MicroPython ST7789 TFT Display driver, SPI interfaces for DojoBoy
#
# Display Driver for DojoBoy V1.1 25/12/24
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
RDDID     = const(b'\x04')
RDDST     = const(b'\x09')

SLPIN     = const(b'\x10')
SLPOUT    = const(b'\x11')
PTLON     = const(b'\x12')
NORON     = const(b'\x13')

INVOFF    = const(b'\x20')
INVON     = const(b'\x21')
DISPOFF   = const(b'\x28')
DISPON    = const(b'\x29')
CASET     = const(b'\x2A')
RASET     = const(b'\x2B')
RAMWR     = const(b'\x2C')
RAMRD     = const(b'\x2E')

VSCRDEF   = const(b'\x33')
VSCSAD    = const(b'\x37')

COLMOD    = const(b'\x3A')
MADCTL    = const(b'\x36')

FRMCTR1   = const(b'\xB1')
FRMCTR2   = const(b'\xB2')
FRMCTR3   = const(b'\xB3')
INVCTR    = const(b'\xB4')
DISSET5   = const(b'\xB6')

PWCTR1    = const(b'\xC0')
PWCTR2    = const(b'\xC1')
PWCTR3    = const(b'\xC2')
PWCTR4    = const(b'\xC3')
PWCTR5    = const(b'\xC4')
VMCTR1    = const(b'\xC5')

RDID1     = const(b'\xDA')
RDID2     = const(b'\xDB')
RDID3     = const(b'\xDC')
RDID4     = const(b'\xDD')

PWCTR6    = const(b'\xFC')
GMCTRP1   = const(b'\xE0')
GMCTRN1   = const(b'\xE1')

class Display(djbFrameBuffer):
    
    def __init__(self, width=160, height=128, id_=1, sck=14, mosi=15,
                 dc=12, cs=13, bl=28, baudrate=40_000_000, framerate=30):
#                 dc=12, cs=13, rst=20, bl=28, baudrate=40_000_000, framerate=30):
        self.width = width
        self.height = height
        self._spi = SPI(id_, sck=Pin(sck), mosi=Pin(mosi), baudrate=baudrate, polarity=0, phase=0)
        self._dc = Pin(dc, Pin.OUT)
        #self._rst = Pin(rst, Pin.OUT)
        self._cs = Pin(cs, Pin.OUT)
        self._bl = Pin(bl, Pin.OUT)
        
        self.buffer_mode = RGB565
        
        gc.collect()

        self.buffer = memoryview(bytearray(width * height * 2))
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
        
        self.write_cmd(SLPOUT)
        sleep_ms(150)

        self.write_cmd(FRMCTR1, const(b'\x01\x2C\x2D'))
        self.write_cmd(FRMCTR2, const(b'\x01\x2C\x2D'))
        self.write_cmd(FRMCTR3, const(b'\x01\x2C\x2D\x01\x2C\x2D'))

        self.write_cmd(INVCTR, const(b'\x07'))

        self.write_cmd(PWCTR1, const(b'\xA2\x02\x84'))
        self.write_cmd(PWCTR2, const(b'\xC5'))
        self.write_cmd(PWCTR3, const(b'\x0A\x00'))
        self.write_cmd(PWCTR4, const(b'\x8A\x2A'))
        self.write_cmd(PWCTR5, const(b'\x8A\xEE'))
        self.write_cmd(VMCTR1, const(b'\x0E'))

        self.write_cmd(INVOFF)

        #TFTRotations = [0x00, 0x60, 0xC0, 0xA0]
        #self.write_cmd(MADCTL, const(b'\x00')
        self.write_cmd(MADCTL, const(b'\x60'))

        self.write_cmd(COLMOD, const(b'\x05'))  # COLMAG x05 RGB565 16b / x03 RGB444 12b

        #self.write_cmd(CASET, const(b'\x00\x00\x00\x7F')
        self.write_cmd(CASET, const(b'\x00\x00\x00\x9F'))              # OK 159
        #self.write_cmd(RASET, const(b'\x00\x00\x00\x9F')
        self.write_cmd(RASET, const(b'\x00\x00\x00\x7F'))              # OK 127

        #self.write_cmd(GMCTRP1, const(b'\x0F\x1A\x0F\x18\x2F\x28\x20\x22\x1F\x1B\x23\x37\x00\x07\x02\x10'))
        self.write_cmd(GMCTRP1, const(b'\x02\x1c\x07\x12\x37\x32\x29\x2d\x29\x25\x2B\x39\x00\x01\x03\x10')) # Hinch.
        #self.write_cmd(GMCTRN1, const(b'\x0F\x1B\x0F\x17\x33\x2C\x29\x2E\x30\x30\x39\x3F\x00\x07\x03\x10'))
        self.write_cmd(GMCTRN1, const(b'\x03\x1d\x07\x06\x2E\x2C\x29\x2D\x2E\x2E\x37\x3F\x00\x00\x02\x10')) # Hinch
        
        self.write_cmd(NORON)
        sleep_ms(10)
        self.write_cmd(DISPON)
        sleep_ms(100)

        self._cs(0)
        self._dc(0)
        self._spi.write(RAMWR)
        self._dc(1)
        for hline in range (0, 128):
            for line in range(0, 160 * 2):
                self._spi.write(b'\x00')
        self._cs(1)
        
        self._bl(1) # Turn backlight on

    def init_frame(self):
        frame_w = [0, ((160 - self.width)//2), 0, 159 - ((160 - self.width)//2)] 
        self.write_cmd(CASET, bytearray(frame_w))
        frame_h = [0, ((128 - self.height)//2), 0, 127 - ((128 - self.height)//2)]
        self.write_cmd(RASET, bytearray(frame_h))
        self.write_cmd(RAMWR)
                
    def power_off(self):
        self._bl(0) # Turn backlight off

    def power_on(self):
        self._bl(1) # Turn backlight on

    def contrast(self, contrast):
        pass

    def invert(self, invert):
        pass

    def rotate(self, rotate):
        pass

    def show(self):
        self.write_cmd(RAMWR, self.buffer)
