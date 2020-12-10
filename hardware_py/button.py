#!/usr/bin/env python3

import mraa 
import time 

class Push:

    def __init__(self, gpio=None):
        self.gpio = gpio 
        self.push = mraa.Gpio(gpio)
        self.push.dir(mraa.DIR_IN)
        self.prev = 1

    def get_val(self):
        value = self.push.read()

        if value != self.prev:
            self.prev = value 
            if value == 0:
                return self.oneshot()

    def oneshot(self):
        print(1)
        return 1


class PushCounter:

    def __init__(self, downer=None, upper=None, current=0):
        self._MIN = 0
        self._MAX = 1000
        self.downer = downer 
        self.upper = upper 
        self.current = current 

    def add(self):
        self.current = min([self._MAX, self.current + 1])
        return self.current

    def subtract(self):
        self.current = max([self._MIN, self.current - 1])
        return self.current 

    def next_value(self):
        if self.downer.get_val():
            return self.subtract() 
        if self.upper.get_val():
            return self.add() 

    @property
    def min(self):
        return self._MIN 

    @property
    def max(self):
        return self._MAX 

    @min.setter
    def min(self, val):
        self._MIN = val 

    @max.setter
    def min(self, val):
        self._MAX = val 