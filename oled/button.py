#!/usr/bin/env python3

import mraa
import time

class Push:
    def __init__(self, gpio=None):
        self.gpio = gpio 
        self.push = mraa.gpio(gpio)
        self.push.dir(mraa.DIR_IN)
        self.prev = 1

    def read_value(self):
        value = self.push.read()
        if value != self.prev:
            self.prev = value 
            print(f"pushed {self.gpio}")


if __name__ == "__main__":
    PUSH1 = Push(3)
    PUSH2 = Push(5)

    while True:
        PUSH1.read_value()
        PUSH2.read_value()
        
