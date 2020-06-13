#!/usr/bin/env python3

import serial
import time

arduino = serial.Serial('/dev/ttyS0', 9600, timeout=None)

while True:
    try:
        datum = arduino.read(2)
        packed = int.from_bytes(datum, byteorder='big')
        label = packed >> 8
        value = packed & 255
        print(f"controller {label}: {value}")
        time.sleep(0.01)
    except KeyboardInterrupt:
        exit()
