import busio
import adafruit_ssd1306
from board import SCL3, SDA3
from PIL import Image, ImageDraw, ImageFont


WIDTH   = 128
HEIGHT  = 64
I2C     = busio.I2C(SCL3, SDA3)
OLED    = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, I2C)



class Oled64:
    def __init__(self):
        #self.oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, I2C)
        self.image = Image.new("1", (WIDTH, HEIGHT))
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", size=10)
        self.draw = ImageDraw.Draw(self.image)

    def write(self, txt=None, row=1, newline=True):
        
        if newline:
            self.clear_rect()

        line = row * (row - 1) * int(HEIGHT / 4)
        self.draw.text((0, 0 + line), txt, font=self.font, fill=255)
        OLED.image(self.image)
        OLED.show()

    def clear_rect(self):
        self.draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
