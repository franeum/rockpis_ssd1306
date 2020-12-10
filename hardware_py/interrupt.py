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

class Counter:
    def __init__(self):
        self.c = 0
        self.start = 0
        self.now = 0
        self.past = 0
        self.flag = True   

c = Counter()

# inside a python interrupt you cannot use 'basic' types so you'll need to use
# objects
def press(gpio):

    if gpio.read() == 0:
        c.flag = True 
        print("pressed")
        c.start = time.time()

    if gpio.read() == 1:
        self.flag = False 
        c.past = time.time() - c.start
        print(repr(c.past))
        print_some()



def print_some():
    print("non abbastanza tempo")

# GPIO
pin = 24;

try:
    # initialise GPIO
    x = mraa.Gpio(pin)

    print("Starting ISR for pin " + repr(pin))

    # set direction and edge types for interrupt
    x.dir(mraa.DIR_IN)
    x.isr(mraa.EDGE_BOTH, press, x)
    
    while c.flag:

        if (time.time() - c.start) <= 3.0:
            time.sleep(0.1)
        else:

        # wait until ENTER is pressed
        # var = input("Press ENTER to stop")
            print("ben fatto, più di 3 secondi")
            break 

    var = input("Press ENTER to stop")
    x.isrExit()

except ValueError as e:
    print(e)
