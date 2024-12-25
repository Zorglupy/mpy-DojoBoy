#
# MicroPython SSD1309 128x64 2.42" OLED Monochrome Display driver, SPI interface for DojoBoy
#
#   Display Driver for DojoBoy V1.1 25/12/24
#

from micropython import const
from machine import Pin, SPI
from dojoboy_v1.djbframebuf import djbFrameBuffer
from framebuf import MONO_VLSB
from time import sleep_ms
import gc

__version__ = "1.1 25/12/24"
__repo__ = "https://github.com/zorglupy/dojoboy"


# Command constants from display datasheet
CONTRAST_CONTROL       = const(b'\x81')
ENTIRE_DISPLAY_ON      = const(b'\xA4')
ALL_PIXELS_ON          = const(b'\xA5')
INVERSION_OFF          = const(b'\xA6')
INVERSION_ON           = const(b'\xA7')
DISPLAY_OFF            = const(b'\xAE')
DISPLAY_ON             = const(b'\xAF')
NOP                    = const(b'\xE3')
COMMAND_LOCK           = const(b'\xFD')

# Scrolling commands
CH_SCROLL_SETUP_RIGHT  = const(b'\x26')
CH_SCROLL_SETUP_LEFT   = const(b'\x27')
CV_SCROLL_SETUP_RIGHT  = const(b'\x29')
CV_SCROLL_SETUP_LEFT   = const(b'\x2A')
DEACTIVATE_SCROLL      = const(b'\x2E')
ACTIVATE_SCROLL        = const(b'\x2F')
VSCROLL_AREA           = const(b'\xA3')
SCROLL_SETUP_LEFT      = const(b'\x2C')
SCROLL_SETUP_RIGHT     = const(b'\x2D')

# Addressing commands
LOW_CSA_IN_PAM         = const(b'\x00')
HIGH_CSA_IN_PAM        = const(b'\x10')
MEMORY_ADDRESSING_MODE = const(b'\x20')
COLUMN_ADDRESS         = const(b'\x21')
PAGE_ADDRESS           = const(b'\x22')
PSA_IN_PAM             = const(b'\xB0')
DISPLAY_START_LINE     = const(b'\x40')
SEGMENT_MAP_REMAP      = const(b'\xA0')
SEGMENT_MAP_FLIPPED    = const(b'\xA1')
MUX_RATIO              = const(b'\xA8')
COM_OUTPUT_NORMAL      = const(b'\xC0')
COM_OUTPUT_FLIPPED     = const(b'\xC8')
DISPLAY_OFFSET         = const(b'\xD3')
COM_PINS_HW_CFG        = const(b'\xDA')
GPIO                   = const(b'\xDC')

# Timing and driving scheme commands
DISPLAY_CLOCK_DIV      = const(b'\xD5')
PRECHARGE_PERIOD       = const(b'\xD9')
VCOM_DESELECT_LEVEL    = const(b'\xDB')

class Display(djbFrameBuffer):
    
    def __init__(self, width=128, height=64, id_=1, sck=14, mosi=15,
                 dc=12, cs=13, bl=28, baudrate=10_000_000, framerate=30):
#                 dc=12, cs=13, rst=8, bl=28, baudrate=10_000_000, framerate=30):
        self.width = width
        self.height = height
        self._spi = SPI(id_, sck=Pin(sck), mosi=Pin(mosi), baudrate=baudrate, polarity=0, phase=0)
        self._dc = Pin(dc, Pin.OUT)
        #self._rst = Pin(rst, Pin.OUT)
        self._cs = Pin(cs, Pin.OUT)
        
        self.buffer_mode = MONO_VLSB
        
        gc.collect()

        self.buffer = memoryview(bytearray(height * width // 8))
        super().__init__(self.buffer, width, height, self.buffer_mode, framerate)

        self.init_display()
        
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

        # Hardware reset
        #self._rst(1)
        #sleep_ms(1)
        #self._rst(0)
        #sleep_ms(10)
        #self._rst(1)
        
        '''
        self.write_cmd(DISPLAY_OFF)
        self.write_cmd(DISPLAY_CLOCK_DIV, const(b'\x80'))               #out of sleep mode.
        self.write_cmd(MUX_RATIO, const(b'\x7F'))              #127.
        self.write_cmd(DISPLAY_OFFSET, const(b'\x00'))              #Frame rate control.
        self.write_cmd(DISPLAY_START_LINE)  #Frame rate control.
        self.write_cmd(MEMORY_ADDRESSING_MODE, const(b'\x00'))               #Display inversion control
        self.write_cmd(SEGMENT_MAP_FLIPPED)              #Frame rate control.
        self.write_cmd(COM_OUTPUT_FLIPPED)               #Display inversion control
        self.write_cmd(COM_PINS_HW_CFG, const(b'\x12'))              #Frame rate control.
        self.write_cmd(CONTRAST_CONTROL, const(b'\xFF'))              #Frame rate control.
        self.write_cmd(PRECHARGE_PERIOD, const(b'\xF1'))              #Frame rate control.
        self.write_cmd(VCOM_DESELECT_LEVEL, const(b'\x40'))               #Display inversion control
        self.write_cmd(ENTIRE_DISPLAY_ON)               
        self.write_cmd(INVERSION_OFF)               #Display inversion control
        self.write_cmd(DISPLAY_ON)               #Display inversion control
        '''
        self.write_cmd(DISPLAY_OFF)
        self.write_cmd(DISPLAY_CLOCK_DIV)               
        self.write_cmd(const(b'\x80'))               
        self.write_cmd(MUX_RATIO)             
        self.write_cmd(const(b'\x3F'))
        self.write_cmd(DISPLAY_OFFSET)              
        self.write_cmd(const(b'\x00'))              
        self.write_cmd(DISPLAY_START_LINE)
        self.write_cmd(MEMORY_ADDRESSING_MODE)               
        self.write_cmd(const(b'\x00'))               
        self.write_cmd(SEGMENT_MAP_FLIPPED)              
        self.write_cmd(COM_OUTPUT_FLIPPED)               
        self.write_cmd(COM_PINS_HW_CFG)              
        self.write_cmd(const(b'\x12'))              
        self.write_cmd(CONTRAST_CONTROL)              
        self.write_cmd(const(b'\xFF'))              
        self.write_cmd(PRECHARGE_PERIOD)              
        self.write_cmd(const(b'\x88')) # xF1             
        self.write_cmd(VCOM_DESELECT_LEVEL)               
        self.write_cmd(const(b'\x00'))  # x34 or 3C
        #self.write_cmd(const(b'\x21\x00\x7F')) # 127 COLUMN_ADDRESS, 
        #self.write_cmd(const(b'\x22\x00\x3F')) # pages-1 PAGE_ADDRESS
        
        #self.write_cmd(COLUMN_ADDRESS)
        #self.write_cmd(const(b'\x00\x7F')) # 127  
        #self.write_cmd(PAGE_ADDRESS)
        #self.write_cmd(const(b'\x00\x3F')) # pages-1
        
        self.write_cmd(ENTIRE_DISPLAY_ON)               
        self.write_cmd(INVERSION_OFF)               
        self.write_cmd(DISPLAY_ON)               

        self.fill(0)
        self.show()
        
    def power_off(self):
        self.write_cmd(DISPLAY_OFF)

    def power_on(self):
        self.write_cmd(DISPLAY_ON)

    def contrast(self, contrast): # 0-255
        self.write_cmd(CONTRAST_CONTROL)
        self.write_cmd(bytearray([contrast]))
                 
    def invert(self, invert):
        if invert:
            self.write_cmd(INVERSION_ON)
        else:
            self.write_cmd(INVERSION_OFF)

    def rotate(self, rotate):
        pass

    def show(self):
        self.write_cmd(data=self.buffer)
