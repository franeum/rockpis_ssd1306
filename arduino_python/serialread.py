#!/usr/bin/env python3

import serial
import time
import liblo 

def send_msg(target, label: int, value: int):
    liblo.send(target, "/hw_controller", label, value)
    return None

def decode_bytes(packed): 
    label = packed >> 8
    value = packed & 255
    return label, value

def main():
    arduino = serial.Serial('/dev/ttyS0', 9600, timeout=None)
    target_address = liblo.Address(9000)
    previous_val = 0

    while True:
        try:
            datum = int.from_bytes(arduino.read(2), byteorder='big')
            if datum != previous_val:
                label, value = decode_bytes(datum)
                #print(f"controller {label}: {value}")
                send_msg(target_address, label, value)
                previous_val = datum 
            time.sleep(0.01)
        except KeyboardInterrupt:
            exit()

if __name__ == "__main__":
    main()
