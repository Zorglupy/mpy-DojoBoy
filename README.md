# DojoBoy
<img src="https://github.com/Zorglupy/DojoBoy/assets/16744276/fda8a7f1-d7f9-4e1a-b42d-519674a0cf89" width=25% height=25%>

The DojoBoy console is a DIY handheld game console project based on MicroPython

The main objectives of the project are:
- Cheap and easy to make with common components (no exotic components or custom PCB)
- Simple assembly with reduced tooling (soldering iron, screwdriver, Dremel tool)
- Easy printing of the case (3 parts only without supports)
- Game coding easy with only MicroPython libraries (no custom C codes, orginal MicroPython image based)
  - v 1.0 : All In One library
  - v 2.0 (WIP): Module with libraries (multiple objects) : object oriented coding, vector methods, extended features...

# Hardware

Multiple platforms are compatible/available:
- Raspeberry Pi Pico or Pico W board and RP2040 clones
- LILYGO® T8 V1.7.1 ESP32 board.
- VCC-GND Studio YD-ESP32-S3 (DevKitC 1 clone)

Specs:
- Display:
  - ST7735 160x128 1.8"
  - ST7789 240x240 1.54"
  - ILI9341 320x240 3.2"
  - SSD1309 128x64 2.42"
- LiPo battery with charge management
- Joystick or directional buttons + 8 buttons
- 2 beeper channels (PWM)
- Expansion port (I2C, GPIO, I2S)
- SD card
- 3D Printable case

# Software

<img src="https://github.com/Zorglupy/DojoBoy/blob/main/making/case/DojoBoy.Top.PNG" width=25% height=25%>

Schema :

WIP

Sources and inspirations :

- https://gist.github.com/samneggs
- https://github.com/harlepengren/PicoGame
- https://github.com/YouMakeTech/Pi-Pico-Game-Boy
- https://github.com/HalloSpaceBoy5/PicoBoy
- https://github.com/MLXXXp/Arduboy2
- https://github.com/peterhinch
- https://github.com/mchobby
- and more....
