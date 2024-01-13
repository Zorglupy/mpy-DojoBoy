#
# Original source files for PicoGameBoy.py by Vincent Mistler for YouMakeTech
# Modified By HalloSpaceBoy for the PicoBoy
# Modified By Yoyo Zorglup for the DojoBoy
#
#   DojoBoy Standard Library v1.0 13/01/24
#

from machine import Pin, PWM, Timer, ADC
from framebuf import RGB565, MONO_VLSB
from time import sleep_ms, ticks_ms, ticks_diff
from os import uname
from micropython import const

__version__ = "v1.0 13/01/24"


#
#   Rapsberry Pi Pico /W Devices Pinout
#
_SCK        = const(14)
_MOSI       = const(15)
_DC         = const(12)
_CS         = const(13)
_BL         = const(28)
_B_A        = const(0)
_B_B        = const(1)
_B_X        = const(2)
_B_Y        = const(3)
_D_B_A      = const(10) # not used with analog control
_D_B_B      = const(11) # not used with analog control
_B_HOME     = const(6)
_B_START    = const(7)
_B_VOLUME   = const(8)
_B_MENU     = const(9)
_ADC_X      = const(26)
_ADC_Y      = const(27)
_D_UP       = const(0) # not used with analog control
_D_DOWN     = const(1) # not used with analog control
_D_LEFT     = const(2) # not used with analog control
_D_RIGHT    = const(3) # not used with analog control
_CH_BEEP_0  = const(21)
_CH_BEEP_1  = const(22)
_TIMER_ID_0 = const(-1)
_TIMER_ID_1 = const(-1)


'''
#
#   LILYGO® T8 V1.7.1 ESP32 Devices Pinout
#
_SCK        = const(18)
_MOSI       = const(23)
_DC         = const(21)
_CS         = const(5)
_BL         = const(14)
_B_A        = const(32)
_B_B        = const(33)
_B_X        = const(12)
_B_Y        = const(15)
_D_B_A      = const(10)
_D_B_B      = const(11)
_B_HOME     = const(4)
_B_START    = const(27)
_B_VOLUME   = const(19)
_B_MENU     = const(13)
_ADC_X      = const(35)
_ADC_Y      = const(34)
_D_UP       = const(0)
_D_DOWN     = const(1)
_D_LEFT     = const(2)
_D_RIGHT    = const(3)
_CH_BEEP_0  = const(25)
_CH_BEEP_1  = const(26)
_TIMER_ID_0 = const(0)
_TIMER_ID_1 = const(1)
'''
'''
#
#   VCC-GND Studio YD-ESP32-S3 Devices Pinout
#
_SCK        = const(13)
_MOSI       = const(11)
_DC         = const(12)
_CS         = const(10)
_BL         = const(3)
_B_A        = const(4)
_B_B        = const(5)
_B_X        = const(6)
_B_Y        = const(7)
_D_B_A      = const(41)
_D_B_B      = const(42)
_B_HOME     = const(15)
_B_START    = const(16)
_B_VOLUME   = const(17)
_B_MENU     = const(18)
_ADC_X      = const(1)
_ADC_Y      = const(2)
_D_UP       = const(47)
_D_DOWN     = const(48)
_D_LEFT     = const(2)
_D_RIGHT    = const(1)
_CH_BEEP_0  = const(20)
_CH_BEEP_1  = const(21)
_TIMER_ID_0 = const(0)
_TIMER_ID_1 = const(1)
'''

#
#    Display ST7735 160x128 1.8"
#
from dojoboy_v1.st7735 import Display 
_LCD_WIDTH      = const(160)
_LCD_HEIGHT     = const(128)
_LCD_BAUDRATE   = const(40_000_000)

'''
#
#   Display ST7789 240x240 1.54"
#
from dojoboy_v1.st7789 import Display 
_LCD_WIDTH      = const(240)
_LCD_HEIGHT     = const(240)
_LCD_BAUDRATE   = const(62_500_000)
'''
'''
#
#   Display ILI9341 320x240 3.2"
#
from dojoboy_v1.ili9341 import Display 
_LCD_WIDTH      = const(320)
_LCD_HEIGHT     = const(240)
_LCD_BAUDRATE   = const(62_500_000)
'''
'''
#
#   Display SSD1309 128x64 2.42"
#
from dojoboy_v1.ssd1309 import Display 
_LCD_WIDTH      = const(128)
_LCD_HEIGHT     = const(64)
_LCD_BAUDRATE   = const(10_000_000)
'''

class DojoBoy():
    
    max_vol = 6
    duty = {0:0,1:5,2:15,3:45,4:135,5:405,6:1215}
    #duty = {0:0,1:512,2:1024,3:2048,4:4096,5:8192,6:16384}
    tones = {
    #" ": 0,    
    "B0": 31,
    "C1": 33,
    "C#1": 35,
    "D1": 37,
    "D#1": 39,
    "E1": 41,
    "F1": 44,
    "F#1": 46,
    "G1": 49,
    "G#1": 52,
    "A1": 55,
    "A#1": 58,
    "B1": 62,
    "C2": 65,
    "C#2": 69,
    "D2": 73,
    "D#2": 78,
    "E2": 82,
    "F2": 87,
    "F#2": 93,
    "G2": 98,
    "G#2": 104,
    "A2": 110,
    "A#2": 117,
    "B2": 123,
    "C3": 131,
    "C#3": 139,
    "D3": 147,
    "D#3": 156,
    "E3": 165,
    "F3": 175,
    "F#3": 185,
    "G3": 196,
    "G#3": 208,
    "A3": 220,
    "A#3": 233,
    "B3": 247,
    "C4": 262,
    "C#4": 277,
    "D4": 294,
    "D#4": 311,
    "E4": 330,
    "F4": 349,
    "F#4": 370,
    "G4": 392,
    "G#4": 415,
    "A4": 440,
    "A#4": 466,
    "B4": 494,
    "C5": 523,
    "C#5": 554,
    "D5": 587,
    "D#5": 622,
    "E5": 659,
    "F5": 698,
    "F#5": 740,
    "G5": 784,
    "G#5": 831,
    "A5": 880,
    "A#5": 932,
    "B5": 988,
    "C6": 1047,
    "C#6": 1109,
    "D6": 1175,
    "D#6": 1245,
    "E6": 1319,
    "F6": 1397,
    "F#6": 1480,
    "G6": 1568,
    "G#6": 1661,
    "A6": 1760,
    "A#6": 1865,
    "B6": 1976,
    "C7": 2093,
    "C#7": 2217,
    "D7": 2349,
    "D#7": 2489,
    "E7": 2637,
    "F7": 2794,
    "F#7": 2960,
    "G7": 3136,
    "G#7": 3322,
    "A7": 3520,
    "A#7": 3729,
    "B7": 3951,
    "C8": 4186,
    "C#8": 4435,
    "D8": 4699,
    "D#8": 4978
    }
        
    def __init__(self, show_intro=True, width=_LCD_WIDTH, height=_LCD_HEIGHT, framerate=30, refreshBeep=5):
        
        print("DojoBoy Module:",__version__)
        
        self.display = Display(width=width, height=height, id_=1, sck=_SCK, mosi=_MOSI,
                        dc=_DC, cs=_CS, bl=_BL, baudrate=_LCD_BAUDRATE, framerate=framerate)
        
        #
        #   Analog Controls
        #
        self.__button_A = Pin(_B_A, Pin.IN, Pin.PULL_UP)
        self.__button_B = Pin(_B_B, Pin.IN, Pin.PULL_UP)
        self.__button_X = Pin(_B_X, Pin.IN, Pin.PULL_UP)
        self.__button_Y = Pin(_B_Y, Pin.IN, Pin.PULL_UP)
        if uname()[0] == "rp2":
            self.__adcX = ADC(_ADC_X)
            self.__adcY = ADC(_ADC_Y)
        elif uname()[0] == "esp32":
            self.__adcX = ADC(_ADC_X,atten=ADC.ATTN_11DB)
            self.__adcY = ADC(_ADC_Y,atten=ADC.ATTN_11DB)
        
        self.btn_Up = 1 << 1
        self.btn_Left = 1 << 2
        self.btn_Right = 1 << 3
        self.btn_Down = 1 << 4
        self.btn_A = 1 << 5
        self.btn_B = 1 << 6
        self.btn_Home = 1 << 7
        self.btn_Start = 1 << 8
        self.btn_Volume = 1 << 9
        self.btn_Menu = 1 << 10
        self.btn_X = 1 << 11
        self.btn_Y = 1 << 12
        
        '''
        #
        #   Digital Controls
        #
        self.__up = Pin(_D_UP, Pin.IN, Pin.PULL_UP)
        self.__down = Pin(_D_DOWN, Pin.IN, Pin.PULL_UP)
        self.__left = Pin(_D_LEFT, Pin.IN, Pin.PULL_UP)
        self.__right = Pin(_D_RIGHT, Pin.IN, Pin.PULL_UP)
        self.__button_A = Pin(_D_B_A, Pin.IN, Pin.PULL_UP)
        self.__button_B = Pin(_D_B_B, Pin.IN, Pin.PULL_UP)
        
        self.btn_Up = 1 << 1
        self.btn_Left = 1 << 2
        self.btn_Right = 1 << 3
        self.btn_Down = 1 << 4
        self.btn_A = 1 << 5
        self.btn_B = 1 << 6
        self.btn_Home = 1 << 7
        self.btn_Start = 1 << 8
        self.btn_Volume = 1 << 9
        self.btn_Menu = 1 << 10
        '''
            
        self.__button_home = Pin(_B_HOME, Pin.IN, Pin.PULL_UP)
        self.__button_start = Pin(_B_START, Pin.IN, Pin.PULL_UP)
        self.__button_volume = Pin(_B_VOLUME, Pin.IN, Pin.PULL_UP)
        self.__button_menu = Pin(_B_MENU, Pin.IN, Pin.PULL_UP)
        
        self.__buzzer = [PWM(Pin(_CH_BEEP_0)), PWM(Pin(_CH_BEEP_1))]
        
        self.vol = [6, (self.max_vol//2) + 1]

        self.songIndex = 0
        self.songSpeed = 1
        self.songTimeUnit = 1
        self.notes = False
        self.songBuf = []
        self.songRunning = False

        self.soundBuf = []
        self.soundRunning = False

        self.mute_sound = False

        self.channelTimer_0 = ticks_ms()
        self.channelLock_0 = False
        self.timer_0 = Timer(_TIMER_ID_0)
        self.timer_0.init(period=refreshBeep, mode=Timer.PERIODIC, callback=self.update_channel_0)

        self.channelTimer_1 = ticks_ms()
        self.channelLock_1 = False
        self.timer_1 = Timer(_TIMER_ID_1)
        self.timer_1.init(period=refreshBeep, mode=Timer.PERIODIC, callback=self.update_channel_1)

        self.bequiet(0)
        self.bequiet(1)
                     
        self.btnUval = 0
        self.btnDval = 0
        self.btnLval = 0
        self.btnRval = 0
        
        self.btns = 0
        self.lastBtns = 0
        
        if show_intro:
            self.show_start_screen()
            
    #-----------------------------------------------------------------
    # Manage memory methods - USELESS ???
    #-----------------------------------------------------------------
        
    def free_mem(self):
        import gc, sys
        print('Before:Free Mem',gc.mem_free(),"Alloc Mem",gc.mem_alloc())
        for key in sys.modules:
            del sys.modules[key]
        gc.collect()
        print("After:Free Mem",gc.mem_free(),"Alloc Mem",gc.mem_alloc())

    #-----------------------------------------------------------------
    # Start Screen methods
    #-----------------------------------------------------------------
            
    def show_start_screen(self):
        MCU = uname()[0]+"-"+uname()[2]
        VERSION = __version__

        if self.display.width == 128:
            if self.display.buffer_mode == RGB565:
                self.display.load_image("/lib/dojoboy_v1/djb-start-128x64.bin")
            elif self.display.buffer_mode == MONO_VLSB:
                self.display.load_image("/lib/dojoboy_v1/djb-start-128x64-mono.bin")
            rect_y = 38
        elif self.display.width == 160:
            self.display.load_image("/lib/dojoboy_v1/djb-start-160x128.bin")
            rect_y = 96
        elif self.display.width == 240:
            self.display.load_image("/lib/dojoboy_v1/djb-start-240x240.bin")
            rect_y = 180
        elif self.display.width == 320:
            self.display.load_image("/lib/dojoboy_v1/djb-start-320x240.bin")
            rect_y = 195
        else:
            self.display.fill(self.display.BLACK)

        self.display.center_text_XY(MCU, y=self.display.height-20, color=self.display.RED_H)
        self.display.center_text_XY(VERSION, y=self.display.height-10, color=self.display.RED_H)
        self.display.show()
        sleep_ms(500)
        rect_h = self.display.height // 16
        rect_w = self.display.width // 4
        rect_h_half = rect_h // 2
        
        self.display.rect(0,rect_y,rect_w,rect_h,self.display.RED_H, True)
        self.display.triangle(rect_w,rect_y,rect_w+rect_h_half,rect_y,rect_w,rect_y+rect_h-1,self.display.RED_H, True)
        self.display.show()
        self.play_tone("C4",250)
        sleep_ms(250)
        self.display.rect(rect_w+rect_h_half,rect_y,rect_w-rect_h_half,rect_h,self.display.YELLOW_H, True)
        self.display.triangle(rect_w+1,rect_y+rect_h-1,rect_w+rect_h_half,rect_y+rect_h-1,rect_w+rect_h_half,rect_y,self.display.YELLOW_H, True)
        self.display.triangle(2*rect_w,rect_y,2*rect_w+rect_h_half,rect_y,2*rect_w,rect_y+rect_h-1,self.display.YELLOW_H, True)
        self.display.show()
        self.play_tone("D4",250)
        sleep_ms(250)
        self.display.rect(2*rect_w+rect_h_half,rect_y,rect_w-rect_h_half,rect_h,self.display.GREEN_H, True)
        self.display.triangle(2*rect_w+1,rect_y+rect_h-1,2*rect_w+rect_h_half,rect_y+rect_h-1,2*rect_w+rect_h_half,rect_y,self.display.GREEN_H, True)
        self.display.triangle(3*rect_w,rect_y,3*rect_w+rect_h_half,rect_y,3*rect_w,rect_y+rect_h-1,self.display.GREEN_H, True)
        self.display.show()
        self.play_tone("F4",250)
        sleep_ms(250)
        self.display.rect(3*rect_w+rect_h_half,rect_y,rect_w-rect_h_half,rect_h,self.display.CYAN_H, True)
        self.display.triangle(3*rect_w+1,rect_y+rect_h-1,3*rect_w+rect_h_half,rect_y+rect_h-1,3*rect_w+rect_h_half,rect_y,self.display.CYAN_H, True)
        self.display.show()
        self.play_tone("C4",500)
        sleep_ms(2000)
    
    #-----------------------------------------------------------------
    # SOUND methods
    #-----------------------------------------------------------------

    def mute(self, status=True):
        self.mute_sound = status
        
    def play_tone(self, tone, duration=0):
        if not self.mute_sound:
            if duration == 0:
                self.__buzzer[0].freq(DojoBoy.tones[tone])
                self.__buzzer[0].duty_u16(DojoBoy.duty[self.vol[0]])
                return
            return self.sound(tone=tone, duration=duration)
        
    def play_freq(self, freq, duration=0):
        if not self.mute_sound and freq > 30:
            if duration == 0:
                self.__buzzer[0].freq(freq)
                self.__buzzer[0].duty_u16(DojoBoy.duty[self.vol[0]])
                return
            return self.sound(freq=freq, duration=duration)
            
    def sound(self, freq=None, tone=None, duration=0):
        #print('B:',len(self.soundBuf))
        if len(self.soundBuf) < 10: # max 10 sound in queue
            self.soundRunning = True
            self.soundBuf.append([freq, tone, duration])
            return False
        return True

    def bequiet(self, channel=0):
        self.__buzzer[channel].duty_u16(0)

    def stop_sound(self):
        self.bequiet(0)
    
    def set_volume(self, channel=0, volume=0):
        self.vol[channel] = volume
            
    def update_channel_0(self, timer): # Sound      
        if self.channelLock_0:
            timer_dif_0 = ticks_diff(ticks_ms(), self.channelTimer_0)
            if timer_dif_0 > self.soundBuf[0][2]:
                self.__buzzer[0].duty_u16(0)
                self.channelLock_0 = False
                self.soundBuf.pop(0)
                if len(self.soundBuf) == 0:
                    self.soundRunning = False
        else:
            if len(self.soundBuf) > 0:
                freq, tone, duration = self.soundBuf[0]
                self.__buzzer[0].freq(freq if freq else DojoBoy.tones[tone])
                self.__buzzer[0].duty_u16(DojoBoy.duty[self.vol[0]])
       
                self.channelLock_0 = True
                self.channelTimer_0 = ticks_ms()

    def update_channel_1(self, timer): # Song
        if self.songRunning:
            if self.channelLock_1:
                timer_dif_1 = ticks_diff(ticks_ms(), self.channelTimer_1)
                if timer_dif_1 > self.songBuf[self.songIndex+1] * self.songTimeUnit * self.songSpeed:
                    self.__buzzer[1].duty_u16(0)
                    self.channelLock_1 = False
                    self.songIndex += 2
                    if self.songIndex + 1 > len(self.songBuf): # end of song ?
                        if self.songLoop:
                            self.songIndex = 0
                        else:
                            self.songRunning = False
            else:
                if not self.songBuf[self.songIndex] == 0:
                    if self.notes:
                        self.__buzzer[1].freq(DojoBoy.tones[self.songBuf[self.songIndex]])
                    else :
                        #print('notes:',self.soundBuf[self.songIndex],'duration:',self.soundBuf[self.songIndex+1])
                        self.__buzzer[1].freq(self.songBuf[self.songIndex])
                
                self.__buzzer[1].duty_u16(DojoBoy.duty[self.vol[1]])
 
                self.channelLock_1 = True
                self.channelTimer_1 = ticks_ms()
    
    # songbuf = [ djb.start_song, NotesorFreq , timeunit,
    #             freq1, duration1, freq2, duration2,
    #             djb.songLoop  or djb.songEnd]
    # Notes or Freq : False=song coded frequencies (Hz), True=song coded in notes, e.djb. 'F4' 'F#4')
    # timeunit = value to multiple durations with that number of milli-seconds. Default 1 milli-second.
    # freq1 can be replaced with note, e.djb. [djb.start_song, 'C4', 200,'D4', 200,'E4',300,'F4', 300,'F#4', 300,'G4', 300,djb.songEnd]
    # freq1 = 0 for silence notes
    # duration1 is multipled with tempo to arrive at a duration for the  note in millseconds

    def start_song(self, songBuf=None, songLoop=False):
        if songBuf != None and not self.mute_sound :
            self.songBuf = songBuf
        else:
            return
        self.notes = self.songBuf[0]
        self.songTimeUnit = self.songBuf[1]
        self.songLoop = songLoop
        #print('notes or freq:',self.songBuf[0],'time unit:',self.songBuf[1])
        
        self.songIndex = 0
        self.songBuf = self.songBuf[2:]
        self.songRunning = True
        #print('notes:',self.songBuf[0],'duration:',self.songBuf[1])

    def stop_song(self):
        self.bequiet(1)
        self.songRunning = False
        self.soundBuf.clear()
        self.songIndex = 0
        
    #-----------------------------------------------------------------
    # Controls methods
    #-----------------------------------------------------------------

    def pressed (self,btn) :
        return (self.btns & btn)

    def just_pressed (self,btn) :
        return (self.btns & btn) and not (self.lastBtns & btn)

    def just_released (self,btn) :
        return (self.lastBtns & btn) and not (self.btns & btn)
    
    def scan_jst_btn(self) :
        self.lastBtns = self.btns
        self.btns = 0
        
        #
        # Analog Control
        #
        val = self.__adcX.read_u16()
        self.btnRval = 1 if val > 40000 else 0
        self.btnLval = 1 if val < 20000 else 0
        #print('X=',self.btnRval)
        
        val = self.__adcY.read_u16()
        self.btnUval = 1 if val > 40000 else 0 #48000
        self.btnDval = 1 if val < 20000 else 0 #16000
        #print('Y=',self.btnUval)
        
        self.btns = self.btns | \
                    (self.btnUval) << 1 | \
                    (self.btnLval) << 2 | \
                    (self.btnRval) << 3 | \
                    (self.btnDval) << 4 | \
                    (not self.__button_A.value()) << 5 | \
                    (not self.__button_B.value()) << 6 | \
                    (not self.__button_home.value()) << 7 | \
                    (not self.__button_start.value()) << 8 | \
                    (not self.__button_volume.value()) << 9 | \
                    (not self.__button_menu.value()) << 10 | \
                    (not self.__button_X.value()) << 11 | \
                    (not self.__button_Y.value()) << 12
        #print(val)

        '''
        #
        # Digital Control
        # 
        self.btnUval = not self.__up.value()
        self.btnDval = not self.__down.value()
        self.btnLval = not self.__left.value()
        self.btnRval = not self.__right.value()
    
        self.btns = self.btns | \
                    (self.btnUval) << 1 | \
                    (self.btnLval) << 2 | \
                    (self.btnRval) << 3 | \
                    (self.btnDval) << 4 | \
                    (not self.__button_A.value()) << 5 | \
                    (not self.__button_B.value()) << 6 | \
                    (not self.__button_home.value()) << 7 | \
                    (not self.__button_start.value()) << 8 | \
                    (not self.__button_volume.value()) << 9 | \
                    (not self.__button_menu.value()) << 10
        '''
        return self.btns

    #-----------------------------------------------------------------
    # Manage Volume and Framerate methods
    #-----------------------------------------------------------------

    def setVolume(self, volume=None, channel=0 ) :
        if volume != None:
            self.vol[channel] = min (volume, self.max_vol)
            return False
        if self.pressed(self.btn_Volume):
            if self.just_pressed(self.btn_Up):
                self.vol[channel] = min (self.vol[channel]+1, self.max_vol)
                self.play_tone('C4', 100)
                return True
            elif self.just_pressed(self.btn_Down):
                self.vol[channel] = max (self.vol[channel]-1, 0)
                self.play_tone('D4', 100)
                return True
        return False

    def setFrameRate(self) :
        if self.pressed(self.btn_Menu):
            if self.just_pressed(self.btn_Up):
                self.display.frame_rate = self.display.frame_rate + 5 if self.display.frame_rate < 120 else 5
                self.play_tone('E4', 100)
                return True
            elif self.just_pressed(self.btn_Down):
                self.display.frame_rate = self.display.frame_rate - 5 if self.display.frame_rate > 5 else 120
                self.play_tone('F4', 100)
                return True
        self.display.set_frame_rate(self.display.frame_rate)
        return False

            
if __name__ == "__main__":
       
    djb = DojoBoy()
  
    djb.display.fill(djb.display.BLACK)
    
    # The DojoBoy uses a framebuffer
    # The framebuffer is only transfered to the actual screen and become visible
    # when calling show()
    djb.display.show()

    # Drawing primitive shapes
    # The screen resolution is WIDTH x HEIGHT pixels but Python like many programming 
    # languages starts counting from zero, not one.
    # The top left corner is (0,0) and bottom right is (WIDTH,HEIGHT)
    djb.display.pixel(0,0,djb.display.BLUE_H)
    djb.display.pixel(djb.display.width,djb.display.height,djb.display.BLUE_H)
    djb.display.show()
    sleep_ms(1000)
    
    djb.display.line(0,0,djb.display.width,djb.display.height,djb.display.RED_H)
    djb.display.line(0,djb.display.height,djb.display.width,0,djb.display.RED_H)
    djb.display.show()
    sleep_ms(1000)
    
    djb.display.rect(10,10,djb.display.width-20,djb.display.height-20,djb.display.WHITE_H)
    djb.display.show()
    sleep_ms(1000)
    
    djb.display.rect(10,10,djb.display.width-20,djb.display.height-20,djb.display.WHITE_H, True)
    djb.display.show()
    sleep_ms(1000)

    # text font
    djb.display.fill(djb.display.BLACK)
    djb.display.center_text('Hello from DojoBoy!',djb.display.GREEN_H, font_name='justabit12')
    djb.display.show()
    sleep_ms(2000)
    
    # text
    djb.display.fill(djb.display.BLACK)
    import gc, sys
    freeMem = "Free Mem:"+str(gc.mem_free())+" B"
    allocMem = "Alloc Mem:"+str(gc.mem_alloc())+" B"
    djb.display.text('Before GC',0,0,djb.display.RED_H)
    djb.display.text(freeMem,0,10,djb.display.WHITE_H)
    djb.display.text(allocMem,0,20,djb.display.WHITE_H)
    for key in sys.modules:
            del sys.modules[key]
    gc.collect()
    freeMem = "Free Mem:"+str(gc.mem_free())+" B"
    allocMem = "Alloc Mem:"+str(gc.mem_alloc())+" B"
    djb.display.text('After GC',0,30,djb.display.GREEN_H)
    djb.display.text(freeMem,0,40,djb.display.WHITE_H)
    djb.display.text(allocMem,0,50,djb.display.WHITE_H)

    for x in range (0,8):
        djb.display.rect(x*(djb.display.width//8), 90, djb.display.width//8,15, djb.display.color_pal[x], True)
        djb.display.rect(x*(djb.display.width//8), 105, djb.display.width//8,15, djb.display.color_pal[x+8], True)

    djb.display.show()
    sleep_ms(8000)
           
    x = djb.display.width // 2 - 5
    y = djb.display.height // 2 - 5
    djb.display.fill(djb.display.BLACK)

    bgColor = 0
    shColor = 1
    
    while True:
        djb.display.rect(x,y, 10, 10, djb.display.color_pal[shColor % 16], True)
        djb.display.show()
        djb.scan_jst_btn()
        if djb.pressed(djb.btn_Right):
            x += 1
        elif djb.pressed(djb.btn_Left):
            x -= 1
        elif djb.pressed(djb.btn_Up):
            y -= 1
        elif djb.pressed(djb.btn_Down):
            y += 1
        elif djb.pressed(djb.btn_Home):
            djb.display.fill(djb.display.color_pal[bgColor % 16])
        elif djb.just_pressed(djb.btn_Start):
            bgColor += 1
            djb.display.fill(djb.display.color_pal[bgColor % 16])
        elif djb.just_pressed(djb.btn_Volume):
            shColor += 1
        elif djb.pressed(djb.btn_Menu):
            bgColor = 0
            djb.display.fill(djb.display.color_pal[bgColor % 16])
            