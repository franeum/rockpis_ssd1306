#!/usr/bin/env python3

# Author: Brendan Le Foll <brendan.le.foll@intel.com>
# Copyright (c) 2014 Intel Corporation.
#
# SPDX-License-Identifier: MIT
#
# Example Usage: Triggers ISR upon GPIO state change

import mraa
import time
import sys
import os 
import threading 
from dataclasses import dataclass

# constants

MAX_TIME    = 3
PIN         = 24


#@dataclass
class Counter:
    def __init__(self):
        self.c  = 0
        self.start = 0
        self.past = 0
        self.flag = False   
        self.exit_flag = 0 
        self.points = '.'
        self._pin = 24
        self.x = mraa.Gpio(24)
        self.x.dir(mraa.DIR_IN)
        #self.x.isr(mraa.EDGE_BOTH, press, self.x)

    def on_press(self, func, data):
        self.x.isr(mraa.EDGE_BOTH, func, data)

    def callback(self):
        if self.x.read() == 0:
            print("pressed")

        elif self.x.read() == 1:
            print("released")    

    def perform_exit(self):
        self.x.isrExit()

def main():
    try:
        c = Counter()
        c.on_press(c.callback(), 2)

        var = input("Press ENTER to stop")
        c.perform_exit()

    except ValueError as e:
        print(e)

    
if __name__ == "__main__":
    main()
