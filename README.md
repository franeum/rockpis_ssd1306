# rockpis_ssd1306

python module to drive oled ssd1306

## Connections

| ROCKPIS          | SSD1306 |
| ---------------- | ------- |
| 11 (I2C3_SDA_M0) | SDA     |
| 13 (I2C3_SCL_M0) | SCL     |
| 17 (+3.3V)       | VCC     |
| 20 (GND)         | GND     |

**N.B. check power, perhaps is better +5V**

## Rockpis configuration

In `/boot/uEnv.txt` add this code to the line beginning with `overlay`:

**rk3308-i2c3**

so the line now could be:

```bash
overlay=rk3308-console-on-uart0 rk3308-uart2 rk3308-i2c3
```

## package to manage SSD1306

[https://github.com/adafruit/Adafruit_CircuitPython_SSD1306](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306)

## example to use

```python
# Basic example of clearing and drawing pixels on a SSD1306 OLED display.
# This example and library is meant to work with Adafruit CircuitPython API.
# Author: Tony DiCola
# License: Public Domain

# Import all board pins.
from board import SCL, SDA
import busio

# Import the SSD1306 module.
import adafruit_ssd1306


# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
# Alternatively you can change the I2C address of the device with an addr parameter:
# display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x31)

# Clear the display.  Always call show after changing pixels to make the display
# update visible!
display.fill(0)
display.show()

# Set a pixel in the origin 0,0 position.
display.pixel(0, 0, 1)
# Set a pixel in the middle 64, 16 position.
display.pixel(64, 16, 1)
# Set a pixel in the opposite 127, 31 position.
display.pixel(127, 31, 1)
display.show()
```
