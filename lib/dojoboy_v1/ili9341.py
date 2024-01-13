#
# MicroPython ILI9341 3.2" TFT Display driver, SPI interfaces for DojoBoy
#
#   Display Driver for DojoBoy V1.0 13/01/24
#

from micropython import const
from machine import Pin, SPI
from dojoboy_v1.djbframebuf import djbFrameBuffer
from framebuf import RGB565
from time import sleep_ms
import gc

__version__ = "1.0 13/01/24"
__repo__ = "https://github.com/zorglupy/dojoboy"

# register definitions
SWRESET                      = const(b'\x01')  # Software reset
RDDID                        = const(b'\x04')  # Read display ID info
RDDST                        = const(b'\x09')  # Read display status
SLPIN                        = const(b'\x10')  # Enter sleep mode
SLPOUT                       = const(b'\x11')  # Exit sleep mode
PTLON                        = const(b'\x12')  # Partial mode on
NORON                        = const(b'\x13')  # Normal display mode on
RDMODE                       = const(b'\x0A')  # Read display power mode
RDMADCTL                     = const(b'\x0B')  # Read display MADCTL
RDPIXFMT                     = const(b'\x0C')  # Read display pixel format
RDIMGFMT                     = const(b'\x0D')  # Read display image format
RDSELFDIAG                   = const(b'\x0F')  # Read display self-diagnostic
INVOFF                       = const(b'\x20')  # Display inversion off
INVON                        = const(b'\x21')  # Display inversion on
GAMMASET                     = const(b'\x26')  # Gamma set
DISPLAY_OFF                  = const(b'\x28')  # Display off
DISPLAY_ON                   = const(b'\x29')  # Display on
SET_COLUMN                   = const(b'\x2A')  # Column address set
SET_PAGE                     = const(b'\x2B')  # Page address set
WRITE_RAM                    = const(b'\x2C')  # Memory write
READ_RAM                     = const(b'\x2E')  # Memory read
PTLAR                        = const(b'\x30')  # Partial area
VSCRDEF                      = const(b'\x33')  # Vertical scrolling definition
MADCTL                       = const(b'\x36')  # Memory access control
VSCRSADD                     = const(b'\x37')  # Vertical scrolling start address
PIXFMT                       = const(b'\x3A')  # COLMOD: Pixel format set
WRITE_DISPLAY_BRIGHTNESS     = const(b'\x51')  # Brightness hardware dependent!
READ_DISPLAY_BRIGHTNESS      = const(b'\x52')
WRITE_CTRL_DISPLAY           = const(b'\x53')
READ_CTRL_DISPLAY            = const(b'\x54')
WRITE_CABC                   = const(b'\x55')  # Write Content Adaptive Brightness Control
READ_CABC                    = const(b'\x56')  # Read Content Adaptive Brightness Control
WRITE_CABC_MINIMUM           = const(b'\x5E')  # Write CABC Minimum Brightness
READ_CABC_MINIMUM            = const(b'\x5F')  # Read CABC Minimum Brightness
FRMCTR1                      = const(b'\xB1')  # Frame rate control (In normal mode/full colors'
FRMCTR2                      = const(b'\xB2')  # Frame rate control (In idle mode/8 colors'
FRMCTR3                      = const(b'\xB3')  # Frame rate control (In partial mode/full colors'
INVCTR                       = const(b'\xB4')  # Display inversion control
DFUNCTR                      = const(b'\xB6')  # Display function control
PWCTR1                       = const(b'\xC0')  # Power control 1
PWCTR2                       = const(b'\xC1')  # Power control 2
PWCTRA                       = const(b'\xCB')  # Power control A
PWCTRB                       = const(b'\xCF')  # Power control B
VMCTR1                       = const(b'\xC5')  # VCOM control 1
VMCTR2                       = const(b'\xC7')  # VCOM control 2
#RDID1                        = const(b'\xDA')  # Read ID 1
#RDID2                        = const(b'\xDB')  # Read ID 2
#RDID3                        = const(b'\xDC')  # Read ID 3
#RDID4                        = const(b'\xDD')  # Read ID 4
GMCTRP1                      = const(b'\xE0')  # Positive gamma correction
GMCTRN1                      = const(b'\xE1')  # Negative gamma correction
DTCA                         = const(b'\xE8')  # Driver timing control A
DTCB                         = const(b'\xEA')  # Driver timing control B
POSC                         = const(b'\xED')  # Power on sequence control
ENABLE3G                     = const(b'\xF2')  # Enable 3 gamma control
PUMPRC                       = const(b'\xF7')  # Pump ratio control

class Display(djbFrameBuffer):

    def __init__(self, width=320, height=240, id_=1, sck=14, mosi=15,
                 dc=12, cs=13, rst=20, bl=28, baudrate=62_500_000, framerate=30):
        self.width = width
        self.height = height
        
        self._spi = SPI(id_, sck=Pin(sck), mosi=Pin(mosi), baudrate=baudrate, polarity=0, phase=0)
        self._dc = Pin(dc, Pin.OUT)
        self._rst = Pin(rst, Pin.OUT)
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

        self._cs(1)
        self._dc(0)
        
        # Hardware reset
        self._rst(1)
        sleep_ms(50)
        self._rst(0)
        sleep_ms(50)
        self._rst(1)
        sleep_ms(50)

        self.write_cmd(SWRESET)  # Software reset
        sleep_ms(100)
        self.write_cmd(PWCTRB, const(b'\x00\xC1\x30'))  # Pwr ctrl B
        self.write_cmd(POSC, const(b'\x64\x03\x12\x81'))  # Pwr on seq. ctrl
        self.write_cmd(DTCA, const(b'\x85\x00\x78'))  # Driver timing ctrl A
        self.write_cmd(PWCTRA, const(b'\x39\x2C\x00\x34\x02'))  # Pwr ctrl A
        self.write_cmd(PUMPRC, const(b'\x20'))  # Pump ratio control
        self.write_cmd(DTCB, const(b'\x00\x00'))  # Driver timing ctrl B
        self.write_cmd(PWCTR1, const(b'\x23'))  # Pwr ctrl 1
        self.write_cmd(PWCTR2, const(b'\x10'))  # Pwr ctrl 2
        self.write_cmd(VMCTR1, const(b'\x3E\x28'))  # VCOM ctrl 1
        self.write_cmd(VMCTR2, const(b'\x86'))  # VCOM ctrl 2
        self.write_cmd(MADCTL, const(b'\xE8'))  # Memory access ctrl
        
        self.write_cmd(SET_COLUMN, b'\x00\x00\x01\x3F') # 319
        self.write_cmd(SET_PAGE, b'\x00\x00\x00\xEF') # 239
        
        self.write_cmd(VSCRSADD, const(b'\x00'))  # Vertical scrolling start address
        self.write_cmd(PIXFMT, const(b'\x55'))  # COLMOD: Pixel format
        self.write_cmd(FRMCTR1, const(b'\x00\x18'))  # Frame rate ctrl
        self.write_cmd(DFUNCTR, const(b'\x08\x82\x27'))
        self.write_cmd(ENABLE3G, const(b'\x00'))  # Enable 3 gamma ctrl
        self.write_cmd(GAMMASET, const(b'\x01'))  # Gamma curve selected
        self.write_cmd(GMCTRP1, const(b'\x0F\x31\x2B\x0C\x0E\x08\x4E\xF1\x37\x07\x10\x03\x0E\x09\x00'))
        self.write_cmd(GMCTRN1, const(b'\x00\x0E\x14\x03\x11\x07\x31\xC1\x48\x08\x0F\x0C\x31\x36\x0F'))
        self.write_cmd(SLPOUT)  # Exit sleep
        sleep_ms(100)
        self.write_cmd(DISPLAY_ON)  # Display on
        sleep_ms(100)

        self._cs(0)
        self._dc(0)
        self._spi.write(WRITE_RAM)
        self._dc(1)
        for hline in range (0, 240):
            for line in range(0, 320 * 2):
                self._spi.write(b'\x00')
        self._cs(1)

        self._bl(1)

    def init_frame(self):
        ws = ((320 - self.width)//2)
        we = 319 - ((320 - self.width)//2)
        web = we.to_bytes(2, 'big')
        wsb = ws.to_bytes(2, 'big')
        frame_w = wsb + web
        self.write_cmd(SET_COLUMN, bytearray(frame_w))
        hs = ((240 - self.height)//2)
        he = 239 - ((240 - self.height)//2)
        heb = he.to_bytes(2, 'big')
        hsb = hs.to_bytes(2, 'big')
        frame_h = hsb + heb
        self.write_cmd(SET_PAGE, bytearray(frame_h))
        self.write_cmd(WRITE_RAM)
        
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
        self.write_cmd(WRITE_RAM, self.buffer)
