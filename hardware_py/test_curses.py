#!/usr/bin/env python3

import curses
import time

curses.initscr()
begin_x = 0 
begin_y = 1
height = 3 
width = curses.COLS
screen = curses.newwin(height, width, begin_y, begin_x)
screen.addstr(0, 0, '_' * curses.COLS)
screen.refresh()

for i in range(curses.COLS):
    screen.addstr(0, i, '-')
    screen.refresh()
    time.sleep(0.1)

# Changes go in to the screen buffer and only get
# displayed after calling `refresh()` to update
screen.refresh()

curses.napms(100)
curses.endwin()