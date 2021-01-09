import busio
import adafruit_ssd1306
from board import SCL3, SDA3
from PIL import Image, ImageDraw, ImageFont


WIDTH   = 128
HEIGHT  = 64
I2C     = busio.I2C(SCL3, SDA3)
OLED    = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, I2C)
IMAGE   = Image.new("1", (width, height))
FONT    = ImageFont.FreeTyoeFont("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", size=10)

class Oled64:
    def __init__(self):
        self.draw = ImageDraw.Draw(IMAGE)

    def write(self, txt=None, row=1, newline=True):
        
        if newline:
            self.clear_rect()

        line = row * (row - 1) * int(HEIGHT / 4)
        self.draw.text((WIDTH, 0 + line), txt, font=font, fill=255)

    def clear_rect(self):
        self.draw.rectangle((0, 0, width, height), outline=0, fill=0)