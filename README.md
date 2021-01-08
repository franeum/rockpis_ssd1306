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
