#!/usr/bin/env python3

import mraa
import time

class Push:
    def __init__(self, gpio=None):
        self.gpio = gpio 
        self.push = mraa.Gpio(gpio)
        self.push.dir(mraa.DIR_IN)
        self.prev = 1
        self.counter = 0

    def read_value(self):
        value = self.push.read()
        if (value != self.prev) and (value == 0):
            self.prev = value 
            self.counter += 1
            print(f"pushed {self.gpio}: {self.counter}")

if __name__ == "__main__":
    #PUSH1 = Push(3)
    PUSH2 = Push(5)

    while True:
        #PUSH1.read_value()
        PUSH2.read_value()
        
