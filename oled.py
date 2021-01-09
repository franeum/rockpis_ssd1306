import busio
import adafruit_ssd1306
from board import SCL3, SDA3
from PIL import Image, ImageDraw, ImageFont


WIDTH   = 128
HEIGHT  = 64
I2C     = busio.I2C(SCL3, SDA3)
OLED    = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, I2C)
image   = Image.new("1", (width, height))


class Oled64:
    def __init__(self):
        pass 
