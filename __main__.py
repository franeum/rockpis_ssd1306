#!/usr/bin/env python3

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import subprocess

from board import SCL3, SDA3
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


#def write_message()


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
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", size=10)

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

draw.text((x, top + 8), "Ciao Amore", font=font, fill=255)
draw.text((x, top + 16), "grazie di esistere!", font=font, fill=255)
disp.image(image)
disp.show()
time.sleep(2)
disp.fill(0)
disp.show()

import keyword
import random

for _ in range(25):
    parola = random.choice(keyword.kwlist)
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    disp.fill(0)
    disp.show()
    draw.text((x, top + 8), parola, font=font, fill=255)
    disp.image(image)
    disp.show()
    time.sleep(0.25)

disp.fill(0)
disp.show()
