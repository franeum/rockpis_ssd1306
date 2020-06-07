#!/home/neum/anaconda3/bin/python

import serial
import time
import struct

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

while True:
    try:
        datum = arduino.read(1)
        val = int.from_bytes(datum, byteorder='big')
        print(val, end=' ')
        time.sleep(0.01)
    except KeyboardInterrupt:
        exit()