#!/home/neum/anaconda3/bin/python

import serial
import time

arduino = serial.Serial('/dev/ttyS0', 9600, timeout=None)

while True:
    try:
        datum = arduino.read(1)
        packed = int.from_bytes(aaa, byteorder='big')
        label = packed >> 8
        value = packed & 255
        print(f"{label}: {value}")
        time.sleep(0.01)
    except KeyboardInterrupt:
        exit()