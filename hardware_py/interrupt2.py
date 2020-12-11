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

# constants

MAX_TIME    = 3
PIN         = 24


@dataclass
class Counter:
    c: int          = 0
    start: float    = 0
    past: float     = 0
    flag: bool      = False   
    exit_flag: int  = 0 
    points: str     = '.'

c = Counter()

# inside a python interrupt you cannot use 'basic' types so you'll need to use
# objects
def press(gpio, cl):
    """interrupt handler"""
    
    if gpio.read() == 0:
        cl.flag = True 
        cl.start = time.time()
        print("pressed")

    elif gpio.read() == 1:
        cl.flag = False 
        cl.past = time.time() - c.start
        if c.past >= MAX_TIME:
            print(1)
        else:
            cl.points = '.'
            print("piu tempo per cortesia")


def configure_pin(pin, func, cls):
    configured_pin = mraa.Gpio(pin)
    print("Starting ISR for pin " + repr(pin))
    configured_pin.dir(mraa.DIR_IN)
    configured_pin.isr(mraa.EDGE_BOTH, func, (configured_pin, cls))
    return configured_pin


def main():
    try:
        # initialise GPIO
        x = configure_pin(PIN, press)

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

            time.sleep(0.1) 

        var = input("Press ENTER to stop")
        x.isrExit()

    except ValueError as e:
        print(e)

    
if __name__ == "__main__":
    main()
