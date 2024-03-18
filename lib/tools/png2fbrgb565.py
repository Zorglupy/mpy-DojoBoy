#!/usr/bin/python

# Converts an RGB image to a framebuffer for LCD display
# LCD display expects 16 bits (2 bytes) per pixel
# encoded in RGB565 format (Least Significant Bit first).
#
# png2fbrgb565.py inputfile [outputfile]

import sys

try: 
  from PIL import Image
except:
  print("The PILlow module is not installed.")
  print("type 'python -m pip install pillow' on commandline to install")
  sys.exit()
  
a_r = 1
a_g = 1
a_b = 1

def color(r, g, b):
    """
    color(r,g,b) returns a 16 bits integer color code for the ST7789 display
    where:
        r (int): Red value between 0 and 255
        g (int): Green value between 0 and 255
        b (int): Blue value between 0 and 255
    """
    # rgb (24 bits) -> rgb565 conversion (16 bits)
    # rgb = r(8 bits) + g(8 bits) + b(8 bits) = 24 bits
    # rgb565 = r(5 bits) + g(6 bits) + b(5 bits) = 16 bits
    r5 = (r & 0b11111000) >> 3
    g6 = (g & 0b11111100) >> 2
    b5 = (b & 0b11111000) >> 3
    rgb565 = (r5 << 11) | (g6 << 5) | b5
    
    # swap LSB and MSB bytes before sending to the screen
    # This is needed because MicroPython does not have an
    # SPI.write16() method and only write byte-by-byte
    lsb = (rgb565 & 0b0000000011111111)
    msb = (rgb565 & 0b1111111100000000) >> 8
    
    return ((lsb << 8) | msb)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        inputFilename = sys.argv[1]   # e.g. corner_12x12.png
        outputFilename = sys.argv[2]  # e.g. corner_12x12.bin
    elif len(sys.argv) == 2:
        inputFilename = sys.argv[1]
        outputFilename = ''
    else:
        print("png2fbrgb565.py inputfile [outputfile]")
        print('Converts an RGB image to a framebuffer RGB565 bytearray.')
        print('')
        print(' pip install pillow')
        print(' python png2fbrgb565.py corner_12x12.png')
        print(' python png2fbrgb565.py corner_12x12.png corner_12x12.bin')
        print('')
        sys.exit('ERROR: No input file parameter !')

    print('Opening image '+ inputFilename)
    inputImage = Image.open(inputFilename)

    #if inputImage.mode != 'RGB':
    #    sys.exit('ERROR: Not supported pixel mode (' + inputImage.mode + '): Supports only RGB')

    if inputImage.mode == 'RGBA':
        print('PNG Input file with alpha channel !')
        print('Conversion of alpha channel color with RGB('+str(a_r)+','+str(a_g)+','+str(a_b)+') color...')
        
        inputImage.load() # required for inputImage.split()

        newImage = Image.new("RGB", inputImage.size, (a_r, a_g, a_b))
        newImage.paste(inputImage, mask=inputImage.split()[3]) # 3 is the alpha channel

        newImage.save('RGB-'+inputFilename, 'PNG', quality=100)
    else:
        newImage = inputImage
    
    print('Image Size :',newImage.size)

    pixelSize = 3 # 3 bytes per pixel for RGB
    pixelsIn = newImage.tobytes()
    pixelsOut = bytearray(int(2*len(pixelsIn)/pixelSize))
    
    for i in range(0,len(pixelsIn)-1,pixelSize):
        r = pixelsIn[i]
        g = pixelsIn[i+1]
        b = pixelsIn[i+2]
        c = color(r,g,b)
        lsb = c & 0b0000000011111111
        msb = (c & 0b1111111100000000) >> 8
        pixelsOut[int(i/pixelSize)*2] = lsb
        pixelsOut[int(i/pixelSize)*2+1] = msb
    
    if outputFilename == '':
        print('')
        print(pixelsOut)
    else:
        print('Writing image '+outputFilename)
        outputImage = open(outputFilename,'wb')
        outputImage.write(pixelsOut)
        outputImage.close()
