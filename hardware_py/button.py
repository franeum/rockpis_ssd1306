#!/usr/bin/env python3

import mraa 
import time 

class Push:
    counter = 0
    counter_max = 1000

    __FUNCTIONS = {
        -1: Push.subtract, 
        0: Push.oneshot,
        1: Push.add
    }

    def __init__(self, gpio=None, func=0):
        self.gpio = gpio 
        self.push = mraa.Gpio(gpio)
        self.push.dir(mraa.DIR_IN)
        self.prev = 1
        self.a_func = Push.__FUNCTIONS[func]

    def get_val(self):
        value = self.push.read()

        if value != self.prev:
            self.prev = value 
            if value == 0:
                self.a_func()
    
    @staticmethod
    def add(c):
        Push.counter = min([Push.counter_max, Push.counter + 1])
        return Push.counter

    @staticmethod
    def subtract(c):
        Push.counter = max([0, Push.counter - 1])
        return Push.counter

    @staticmethod
    def oneshot():
        print(1)
        return 1
