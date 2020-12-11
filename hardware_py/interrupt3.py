#!/usr/bin/env python3

import mraa
import time
import sys
import os 
import threading 
from dataclasses import dataclass

# constants

MAX_TIME    = 3


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
        self.x.edge(mraa.EDGE_BOTH)

    def on_press(self, func, *args):
        self.x.isr(mraa.EDGE_BOTH, func, self)

    def perform_exit(self):
        self.x.isrExit()


def callback(gpio):
    if gpio.x.read() == 0:
        print("pressed")
        gpio.start = time.time()
        gpio.flag = True

    elif gpio.x.read() == 1:
        print("released")
        gpio.flag = False 


def timing(cls):
    while True:
        if cls.flag:
            print("premuto")
        else:
            print("non premuto")
        time.sleep(0.25)

def main():
    try:
        c = Counter()

        t1 = threading.Thread(target=c.on_press, args=(callback, c))
        t1.start()
        t1.join() 
        
        t2 = threading.Thread(target=timing, args=(c,))
        t2.start() 
        t2.join()

        var = input("Press ENTER to stop")
        c.perform_exit()
    except ValueError as e:
        print(e)

    
if __name__ == "__main__":
    main()
