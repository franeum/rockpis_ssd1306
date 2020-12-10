#!/usr/bin/env python3

import curses
import time

curses.initscr()
curses.start_color()
curses.noecho()
curses.curs_set(False)
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
begin_x = 20 
begin_y = 20
height = 100 
width = 100
screen = curses.newwin(height, width, begin_y, begin_x)
#screen.addstr(0, 0, '_' * curses.COLS)
screen.refresh()

#symbols = ['|', '/', '-', '\\', '|', '/', '-', '\\']
symbols = [' | \n | \n | ','  /\n / \n/','   \n---\n   ','\\  \n \\ \n  \\']

screen.addstr(0, 0, "ciao", curses.color_pair(1) | curses.A_BOLD)
screen.refresh()
curses.napms(2000)
screen.clear()

for i in range(20):
    screen.addstr(0, 0, symbols[i % 4], curses.color_pair(1) | curses.A_BOLD)
    screen.refresh()
    time.sleep(0.1)

# Changes go in to the screen buffer and only get
# displayed after calling `refresh()` to update
screen.refresh()

curses.napms(100)
curses.endwin()