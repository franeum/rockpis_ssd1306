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
        self.flag = False   
        self.exit_flag = 0 

c = Counter()

# inside a python interrupt you cannot use 'basic' types so you'll need to use
# objects
def press(gpio):

    if gpio.read() == 0:
        c.flag = True 
        print("pressed")
        c.start = time.time()

    elif gpio.read() == 1:
        c.flag = False 
        c.past = time.time() - c.start
        if c.past >= 3.0:
            print(1)
        else:
            print(0)


# GPIO
pin = 24;

try:
    # initialise GPIO
    x = mraa.Gpio(pin)

    print("Starting ISR for pin " + repr(pin))

    # set direction and edge types for interrupt
    x.dir(mraa.DIR_IN)
    x.isr(mraa.EDGE_BOTH, press, x)

    while True:
        #print("flag:", c.flag)
        if c.flag == True: 
            time_pasted = time.time() - c.start
            print('.', end='')
            if (time_pasted) >= 3.0:
                print("\nEXECUTE!!!!!!!")
                c.flag = False 
        else:
            if c.exit_flag == 0:
                print("More long please") 
                c.exit_flag = 1

        time.sleep(0.1) 

    var = input("Press ENTER to stop")
    x.isrExit()

except ValueError as e:
    print(e)
