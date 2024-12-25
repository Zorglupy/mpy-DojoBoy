#
# djbframebuf.py
# MicroPython framebuf child class for DojoBoy
# By Yoyo Zorglup V1.1 25/12/24
#

from micropython import const
import framebuf
from time import sleep_ms, ticks_ms, ticks_diff
import array
import dojoboy_v1.fdrawer as FDrawer

__version__ = "1.1 25/12/24"
__repo__ = "https://github.com/zorglupy/dojoboy"

class djbFrameBuffer(framebuf.FrameBuffer):
    # Color definitions
    BLACK     = const(0x0000)
    WHITE     = const(0xFFFF)
    
    BLACK_L   = const(0xAA52)
    BLUE_L    = const(0x1000)
    RED_L     = const(0x0080)
    MAGENTA_L = const(0x1080)
    GREEN_L   = const(0x0004)
    CYAN_L    = const(0x1004)
    YELLOW_L  = const(0x0084)
    WHITE_L   = const(0x55AD)

    BLACK_H   = const(0x0000)
    BLUE_H    = const(0x1F00)
    RED_H     = const(0x00F8)
    GREEN_H   = const(0xE007)
    MAGENTA_H = const(0x1FF8)
    CYAN_H    = const(0xFF07)
    YELLOW_H  = const(0xE0FF)
    WHITE_H   = const(0xFFFF)
    
    color_pal = [BLACK_H,
                 BLUE_H,
                 RED_H,
                 MAGENTA_H,
                 GREEN_H,
                 CYAN_H,
                 YELLOW_H,
                 WHITE_H,
                 BLACK_L,
                 BLUE_L,
                 RED_L,
                 MAGENTA_L,
                 GREEN_L,
                 CYAN_L,
                 YELLOW_L,
                 WHITE_L
                 ]        
    def __init__(self, buffer, width, height, buffer_mode, framerate):
        
        super().__init__(buffer, width, height, buffer_mode)
        
        self.__fb = [] # Array of FrameBuffer objects for sprites
        self.__w = []
        self.__h = []
        
        #self._fd = FDrawer.FontDrawer( self, font_name = 'robotl_m8' )
        
        self.buffer_mode = buffer_mode
        self._prev_frame_time = ticks_ms()
        self.frame_rate = framerate
        self.set_frame_rate(self.frame_rate)
        
        self._each_frame_time = int(1000/self.frame_rate)
        #print(self._each_frame_time)
        self._just_rendered = False
        self.last_frame_duration = 0

    #-----------------------------------------------------------------
    # TEXT methods
    #-----------------------------------------------------------------
        
    def _reverse(self, s: string) -> string:
        t = ""
        for i in range(0, len(s)):
            t += s[len(s) - 1 - i]
        return t

    def text(self, s, x, y, color: int = 0xFFFF, scale: int = 1, rotation: int = 0, rot_letter = None, bgcolor = None, font_name = None):
        """
        large text drawing function uses the standard framebuffer font (8x8 pixel characters)
        writes text, s,
        to co-cordinates x, y
        size multiple, m (integer, eg: 1,2,3,4. a value of 2 produces 16x16 pixel characters)
        color, c [optional parameter, default value c=1]
        optional parameter, r is rotation of the text: 0, 90, 180, or 270 degrees
        optional parameter, t is rotation of each character within the text: 0, 90, 180, or 270 degrees
        """
        if scale == 1 and rotation == 0 and rot_letter == None and font_name == None:       
            return super().text( s, x, y, color)
        
        if type(font_name) == str:
            self._fd = FDrawer.FontDrawer( self, 'robotl_m8' if font_name == True else font_name )
            self._fd.color = color
            self._fd.bgcolor = bgcolor
            self._fd.scale = scale
            self._fd.print_str( s, x, y)
            return
        
        smallbuffer = bytearray(8)
        letter = framebuf.FrameBuffer(smallbuffer, 8, 8, framebuf.MONO_HMSB)
        rotation = rotation % 360 // 90
        dx = 8 * scale if rotation in (0, 2) else 0
        dy = 8 * scale if rotation in (1, 3) else 0
        if rotation in (2, 3):
            s = self._reverse(s)
        t = rotation if rot_letter is None else rot_letter % 360 // 90
        a, b, c, d = 1, 0, 0, 1
        for i in range(0, t):
            a, b, c, d = c, d, -a, -b
        x0 = 0 if a + c > 0 else 7
        y0 = 0 if b + d > 0 else 7
        for character in s:
            letter.fill(0)
            letter.text(character, 0, 0, 1)
            for i in range(0, 8):
                for j in range(0, 8):
                    if letter.pixel(i, j) == 1:
                        p = x0 + a * i + c * j
                        q = y0 + b * i + d * j
                        if scale == 1:
                            self.pixel(x + p, y + q, color)
                        else:
                            self.rect(x + p * scale, y + q * scale, scale, scale, color, True)
            x += dx
            y += dy

    def set_font(self, font_name = 'robotl_m8'):
        self._fd = FDrawer.FontDrawer( self, font_name = font_name )
        
    def font_text(self, s, x, y, color: int = 0xFFFF, bgcolor = None, scale: int = 1):
        self._fd.color = color
        self._fd.bgcolor = bgcolor

        self._fd.scale = scale
        self._fd.print_str( s, x, y)

    def center_text(self, s, color = WHITE_H, scale = 1, font_name = None):
        x = (self.width//2) - (len(s) * scale * 4)
        y = (self.height//2) - (scale * 4)
        self.text(s, x, y, color, scale, font_name=font_name)
        
    def center_text_XY(self, s,x=-1,y=-1, color = WHITE_H, scale = 1, font_name = None):
        if x == -1:
            x = (self.width//2) - (len(s) * scale * 4)
        if y == -1:
            y = (self.height//2) - (scale * 4)
        self.text(s, x, y, color, scale, font_name=font_name)

    def top_right_corner_text(self, s, color = WHITE_H, scale = 1, font_name = None):
        x = self.width - (len(s) * scale * 8)
        y = 0
        self.text(s, x, y, color, scale, font_name=font_name)

    #-----------------------------------------------------------------
    # SHAPE methods
    #-----------------------------------------------------------------

    def circle(self, x0, y0, radius, c, f: bool = False):
        """
        Circle drawing function.  Will draw a single pixel wide circle with
        center at x0, y0 and the specified radius
        colour c
        fill if f is True
        """
        self.ellipse(x0,y0, radius, radius, c, f)

    def triangle(self, x0, y0, x1, y1, x2, y2, c, f: bool = False):
        """
        Triangle drawing function.  Will draw a single pixel wide triangle
        around the points (x0, y0), (x1, y1), and (x2, y2)
        colour c
        fill if f is True
        """
        self.poly(0, 0, array.array ('h',[x0, y0, x1, y1, x2, y2]), c, f)

    #-----------------------------------------------------------------
    # SPRITE methods
    #-----------------------------------------------------------------
    
    def convert_buf_mode(self, buffer_mode):
        if buffer_mode == 1:
            buffer_mode = framebuf.MONO_VLSB
        elif buffer_mode == 16:
            buffer_mode = framebuf.GS4_HMSB
        else:
            buffer_mode = self.buffer_mode
        return buffer_mode
    
    # add_sprite(buffer,w,h) creates a new sprite from framebuffer
    # with a width of w and a height of h
    # The first sprite is #0 and can be displayed by sprite(0,x,y)
    # buffer_mode color :
    # 1 color (1b): MONO_VLSB
    # 16 colors (4b) : GS4_HMSB
    # default : same as display framebuffer (color RGB565 : 65535 colors)
    def add_sprite(self, buffer, w, h, buffer_mode=None):
        fb = framebuf.FrameBuffer(buffer, w, h, self.convert_buf_mode(buffer_mode))
        self.__fb.append(fb)
        self.__w.append(w)
        self.__h.append(h)
        return len(self.__fb)

    # add_sprite_from_file(filename, w, h, format_fb=RGB565) creates a new sprite from file
    # with a width of w and a height of h
    # The first sprite is #0 and can be displayed by sprite(0,x,y)
    def add_sprite_from_file(self,filename, w, h, buffer_mode=None):
        with open(filename,"rb") as file:
            fb = framebuf.FrameBuffer(bytearray(file.read()), w, h, self.convert_buf_mode(buffer_mode))
        self.__fb.append(fb)
        self.__w.append(w)
        self.__h.append(h)
        return len(self.__fb)
        
    # add_rect_sprite(color,w,h) creates a new rectangular sprite
    # with the specified color, width and height
    def add_rect_sprite(self, w, h, color):
        buffer = bytearray(w * h * 2) # 2 bytes per pixel
        # fill the buffer with the specified color
        lsb = (color & 0b0000000011111111)
        msb = (color & 0b1111111100000000) >> 8
        for i in range(0,w*h*2,2):
            buffer[i] = lsb
            buffer[i+1] = msb
        return self.add_sprite(buffer, w, h, framebuf.MONO_VLSB)
       
    # sprite(n,x,y) displays the nth sprite at coordinates (x,y)
    # the sprite must be created first by method add_sprite
    def sprite(self, n, x, y, transparent_color=-1, cpal=None):
        self.blit(self.__fb[n], x, y, transparent_color, cpal)
        
    # sprite_width(n) returns the width of the nth sprite in pixels
    def sprite_width(self,n):
        return self.__w[n]
    
    # sprite_height(n) returns the height of the nth sprite in pixels
    def sprite_height(self,n):
        return self.__h[n]

    def palette_mono(self, fcolor, bcolor):
        buf = bytearray(4)
        fb = framebuf.FrameBuffer(buf, 2, 1, self.buffer_mode)
        fb.pixel(1, 0, fcolor)
        fb.pixel(0, 0, bcolor)
        return fb

    def palette_4b(self):
        buf = bytearray(16 * 2) 
        fb = framebuf.FrameBuffer(buf, 16, 1, self.buffer_mode)
        for color in range (17):
            fb.pixel(color, 0, self.color_pal[color])
        return fb

    #-----------------------------------------------------------------
    # IMAGE methods
    #-----------------------------------------------------------------
    '''
    def load_comp_image(self, filename):
        i=0

        import gc, sys
        gc.enable()
        for key in sys.modules:
            del sys.modules[key]
        gc.collect()

        notdone=True
        while notdone:
            notcompleted=True
            while notcompleted:
                try:
                    print(i)
                    compressed_data = open(filename, 'rb').read(2048)
                    if not compressed_data:
                        notcompleted=False
                        notdone=False
                    open('tempimg.bin', 'wb').write(decompress(compressed_data))
                    i=i+1
                    notcompleted=False
                except:
                    foo="bar"
        del compressed_data
        super.load_image("tempimg.bin")
        remove("tempimg.bin")
    '''
    
    def load_image(self,filename):
        with open(filename,"rb") as file:
            file.readinto(self.buffer)
        
    def color(self, r, g, b):
        r5 = (r & 0b11111000) >> 3
        g6 = (g & 0b11111100) >> 2
        b5 = (b & 0b11111000) >> 3
        rgb565 = (r5 << 11) | (g6 << 5) | b5

        lsb = (rgb565 & 0b0000000011111111)
        msb = (rgb565 & 0b1111111100000000) >> 8
        
        return ((lsb << 8) | msb)
        
    def get_pixel(self, x, y):
        byte1 = self.buffer[2*(y*self.width+x)]
        byte2 = self.buffer[2*(y*self.width+x)+1]
        return byte2 << 8 + byte1

    #-----------------------------------------------------------------
    # FRAME CONTROL methods
    #-----------------------------------------------------------------

    def set_frame_rate(self, frame_rate):
        self.frame_rate = frame_rate
        self._each_frame_time = int(1000/self.frame_rate)
        return self._each_frame_time

    def show_and_wait(self, fill_color=None):
        self.show()
        if fill_color != None : self.fill(fill_color)

        frame_duration = ticks_diff( ticks_ms(), self._prev_frame_time)
        timer_dif = self._each_frame_time - frame_duration
        if timer_dif > 0:
            sleep_ms(timer_dif)
            #print(timer_dif)
        self._prev_frame_time = ticks_ms()
        
        #if ticks_diff(ticks_ms(), self._prev_frame_time) == self._each_frame_time:
        #    self.show()
        #    self._prev_frame_time = ticks_ms()

    def next_frame(self):
        frame_duration = ticks_diff( ticks_ms(), self._prev_frame_time)
        
        if self._just_rendered:
            self.last_frame_duration = frame_duration
            self._just_rendered = False
            return False
        elif frame_duration < self._each_frame_time:
            sleep_ms(1)
            return False
        
        self._just_rendered = True
        self._prev_frame_time = ticks_ms()
        #framecount
        return True