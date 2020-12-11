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

#c = Counter()

# inside a python interrupt you cannot use 'basic' types so you'll need to use
# objects
def press(gpio, *args):
    """interrupt handler"""

    if gpio.read() == 0:
        #cl.flag = True 
        #cl.start = time.time()
        print("pressed")

    elif gpio.read() == 1:
        #cl.flag = False 
        #cl.past = time.time() - cl.start
        #if cl.past >= MAX_TIME:
        #    print(1)
        #else:
        #    cl.points = '.'
        #    print("piu tempo per cortesia")
        print("released")

def configure_pin(pin, func, cls):
    configured_pin = mraa.Gpio(pin)
    print("Starting ISR for pin " + repr(pin))
    configured_pin.dir(mraa.DIR_IN)
    configured_pin.isr(mraa.EDGE_BOTH, func, (configured_pin, cls))
    return configured_pin


def main():
    try:
        c = Counter()
        # initialise GPIO
        #x = configure_pin(PIN, press, c)
        x = mraa.Gpio(PIN)
        x.dir(mraa.DIR_IN)
        x.isr(mraa.EDGE_BOTH, press, x)
        """
        while True:
            #print("flag:", c.flag)
            if c.flag == True: 
                time_pasted = time.time() - c.start
                c.points += '.'
                os.system('clear') # clear terminal
                print(c.points)
                if (time_pasted) >= MAX_TIME:
                    c.points = '.'
                    print("\nEXECUTE!!!!!!!")
                    c.flag = False 
                
            else:
                if c.exit_flag == 0:
                    points = '.'
                    print("More long please") 
                    c.exit_flag = 1

            time.sleep(0.1) """

        var = input("Press ENTER to stop")
        x.isrExit()

    except ValueError as e:
        print(e)

    
if __name__ == "__main__":
    main()
