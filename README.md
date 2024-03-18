# DojoBoy

<img src="https://github.com/Zorglupy/mpy-DojoBoy/assets/16744276/8284801b-4264-400b-b358-bb4537fcae4f" width=25% height=25%>

The DojoBoy console is a DIY handheld game console project based on MicroPython

The main objectives of the project are:
- Cheap and easy to make with common components (no exotic components, custom PCB or universal PCB)
- Simple assembly with reduced tooling (soldering iron, screwdriver, Dremel tool)
- Easy printing of the case (5 parts only without supports)
- Game coding easy with only MicroPython libraries (no custom C codes, orginal MicroPython image based)
  - v 1.0 : All In One library
  - v 2.0 (WIP): Module with libraries (multiple objects) : object oriented coding, vector methods, extended features...

# Hardware

<img src="https://github.com/Zorglupy/mpy-DojoBoy/blob/main/making/DojoBoy-Model%20A-Front.PNG" width=25% height=25%><img src="https://github.com/Zorglupy/mpy-DojoBoy/blob/main/making/DojoBoy-Model%20A-Inside.PNG" width=25% height=25%><img src="https://github.com/Zorglupy/mpy-DojoBoy/blob/main/making/DojoBoy-Model%20A-Inside%20Bottom.PNG" width=25% height=25%>

Multiple platforms are compatible/available:
- Raspberry Pi Pico or Pico W board and RP2040 clones
- LILYGO® T8 V1.7.1 ESP32 board.
- VCC-GND Studio YD-ESP32-S3 (DevKitC 1 clone)

Specs:
- Display:
  - ST7735 160x128 1.8"
  - ST7789 240x240 1.54"
  - ILI9341 320x240 3.2"
  - SSD1309 128x64 2.42"
- LiPo battery with charge management
- Joystick + 8 buttons
- 2 beeper channels (PWM)
- Expansion port (I2C, GPIO, I2S, SPI)
- SD card
- 3D Printable case

Schema :
![DojoBoy-Wiring-Amp-Speaker-V2_bb](https://github.com/Zorglupy/mpy-DojoBoy/assets/16744276/4e23aab9-eace-49b9-a9eb-817327e22c71)

|   Raspberry Pi Pico GPIO   |   Items Pin    |
|---    |:-:    |
|   GPIO00   |   A Button  |
|   GPIO01   |   B Button  |
|   GPIO02   |   X Button  |
|   GPIO03   |   Y Button  |
|   GPIO04   |   Ext Port - I2C 0 SDA |
|   GPIO05   |   Ext Port - I2C 0 SCL |
|   GPIO06   |   Home Button  |
|   GPIO07   |   Start Button  |
|   GPIO08   |   Volume Button  |
|   GPIO09   |   Menu Button  |
|   GPIO10   |   Ext Port - I2C 1 SDA  |
|   GPIO11   |   Ext Port - I2C 1 SCL  |
|   GPIO12   |   Display - SPI 1 A0 / DC  |
|   GPIO13   |   Display - SPI 1 CS  |
|   GPIO14   |   Display - SPI 1 SCK / CLK  |
|   GPIO15   |   Display - SPI 1 MOSI  |
|   GPIO16   |   Ext Port - SPI 0 MISO  |
|   GPIO17   |   Ext Port - SPI 0 CS  |
|   GPIO18   |   Ext Port - SPI 0 SCK / CLK  |
|   GPIO19   |   Ext Port - SPI 0 MOSI  |
|   GPIO20   |   Display - RST / Reset  |
|   GPIO21   |   PWM Sound Channel 0  |
|   GPIO22   |   PWM Sound Channel 1  |
|   GPIO26   |   Joystick X  |
|   GPIO27   |   Joystick Y  |
|   GPIO28   |   Display - LED  |
|   3.3V   |   Output 3.3V Power  |
|   VSYS   |   Input 5V Power from Bat. Charger  |
|   VBUS   |   Output 5V Power to Bat. Charger  |

# Wiring

![DojoBoy-Board-V1_bb](https://github.com/Zorglupy/mpy-DojoBoy/assets/16744276/791d6b58-fcc2-4fdd-84e0-f23f8cbee706)

# PCB
<img src="https://github.com/Zorglupy/mpy-DojoBoy/blob/main/making/PCB/PCB_PCB_DojoBoy-Model-A-Mainboard_2024-03-18.png" width=30% height=30%><img src="https://github.com/Zorglupy/mpy-DojoBoy/blob/main/making/PCB/PCB_PCB_DojoBoy-Model-A-Keyboard_2024-03-18.png" width=30% height=30%>

# Software

See Cheat Sheet file in Doc folder... 


Sources and inspirations :

- https://gist.github.com/samneggs
- https://github.com/harlepengren/PicoGame
- https://github.com/YouMakeTech/Pi-Pico-Game-Boy
- https://github.com/HalloSpaceBoy5/PicoBoy
- https://github.com/MLXXXp/Arduboy2
- https://github.com/peterhinch
- https://github.com/mchobby
- and more....
