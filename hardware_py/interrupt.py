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

c = Counter()

# inside a python interrupt you cannot use 'basic' types so you'll need to use
# objects
def press(gpio):
    #print("pin " + repr(gpio.getPin(True)) + " = " + repr(gpio.read()))
    
    if gpio.read() == 0:
        print(0)
        print("pressed")
        c.start = time.time()
    
    if gpio.read() == 1:
        print("released after seconds")
        c.past = time.time() - c.start
        print(repr(c.past))
        print_some()


def print_some():
    print("stocazzooooooo")

# GPIO
pin = 24;

try:
    # initialise GPIO
    x = mraa.Gpio(pin)

    print("Starting ISR for pin " + repr(pin))

    # set direction and edge types for interrupt
    x.dir(mraa.DIR_IN)
    x.isr(mraa.EDGE_BOTH, press, x)

    # wait until ENTER is pressed
    var = input("Press ENTER to stop")
    x.isrExit()
except ValueError as e:
    print(e)
