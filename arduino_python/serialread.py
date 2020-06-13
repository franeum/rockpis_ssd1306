#!/usr/bin/env python3

import serial
import time
import liblo 
from rock_potentiometer import Pot

"""#!/usr/bin/env python3"""
"""#!/home/neum/anaconda3/bin/python3"""
"""def send_msg(target, label: int, value: int):
    liblo.send(target, "/hw_controller", label, value)
    return None"""

def decode_bytes(packed): 
    label = packed >> 8
    value = packed & 255
    return label, value

def main():
    arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
    pot = [Pot(label=x) for x in range(8)]
    print(pot[0])

    while True:
        try:
            datum = int.from_bytes(arduino.read(2), byteorder='big')
            """if datum != previous_val:
                label, value = decode_bytes(datum)
                #print(f"controller {label}: {value}")
                send_msg(target_address, label, value)
                previous_val = datum """
            label, value = decode_bytes(datum)
            pot[label].check_value(value) 
            time.sleep(0.01)
        except KeyboardInterrupt:
            exit()

if __name__ == "__main__":
    main()
