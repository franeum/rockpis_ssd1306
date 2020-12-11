#!/usr/bin/env python3

import time
import subprocess

from board import SCL3, SDA3
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


"""
table of conversion point -> pixel
point   C               space           2               n.of chars
5       (3, 6)          (3, 5)          (3, 5)          42
6       (4, 6)          (4, 5)          (4, 5)          32
7       (4, 7)          (4, 6)          (4, 6)          32
8       (5, 8)          (5, 7)          (5, 7)          25
9       (6, 8)          (5, 8)          (5, 8)          21
10      (6, 9)          (6, 9)          (6, 9)          21
11      (7, 10)         (7, 10)         (7, 10)         18
12      (7, 10)         (7, 10)         (7, 10)         18
13      (8, 11)         (8, 11)         (8, 11)         16
14      (8, 12)         (8, 12)         (8, 12)         16
15      (9, 13)         (9, 13)         (9, 13)         14
16      (10, 14)        (10, 14)        (10, 14)        12
17      (10, 15)        (10, 15)        (10, 15)        12
18      (11, 15)        (11, 15)        (11, 15)        11
19      (11, 16)        (11, 16)        (11, 16)        11
20      (12, 17)        (12, 17)        (12, 17)        10
"""


# Create the I2C interface.
i2c = busio.I2C(SCL3, SDA3)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2 
TOP = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
X = 0


# Load default font.
font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", size=12)
#font = ImageFont.load_default()


def write_text(txt):
    print(font.getlength(txt))
    draw.text((X, TOP + 8), txt, font=font, fill=255)
    disp.image(image)
    disp.show()


def create_scrolling_text(string, a_time=0.1):
    # 15
    for i,ch in enumerate(string):
        c = i+1
        write_text(string[:c])
        time.sleep(a_time)


if __name__ == "__main__":
    write_text("PROVA PROVA 123")
