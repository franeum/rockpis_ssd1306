#!/usr/bin/env python3

import mraa
import time

class Push:
    counter = 0

    def __init__(self, gpio=None, func=-1):
        self.gpio = gpio 
        self.push = mraa.Gpio(gpio)
        self.push.dir(mraa.DIR_IN)
        self.prev = 1
        if func == -1:
            self.a_func = self.subtract
        else:
            self.a_func = self.add

    def read_value(self):
        value = self.push.read()
        if value != self.prev:
            self.prev = value 
            if value == 0:
                Push.counter = self.a_func(Push.counter)
                print(Push.counter)

    def add(self, c):
        return c + 1

    def subtract(self, c):
        return max([0,c-1])

if __name__ == "__main__":
    PUSH1 = Push(23,-1)
    PUSH2 = Push(24,1)

    while True:
        PUSH1.read_value()
        PUSH2.read_value()
        
