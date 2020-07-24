#!/usr/bin/env python

import time
import blinkt
import os

dir = "/home/pi/pixels/"
BRIGHTNESS = os.environ["BRIGHTNESS"]
CLEAR_SLEEP = os.environ["CLEAR_SLEEP"]

while True:
    if os.path.isfile(dir + str(0)):        # Pixel 0
        blinkt.set_pixel(0, 0, 0, int(BRIGHTNESS))
    else: 
        blinkt.set_pixel(0, 0, 0, 0)
    if os.path.isfile(dir + str(1)):        # Pixel 1
        blinkt.set_pixel(1, 0, 0, int(BRIGHTNESS))
    else: 
        blinkt.set_pixel(1, 0, 0, 0)
    if os.path.isfile(dir + str(2)):        # Pixel 2
        blinkt.set_pixel(2, 0, 0, int(BRIGHTNESS))
    else: 
        blinkt.set_pixel(2, 0, 0, 0)
    if os.path.isfile(dir + str(3)):        # Pixel 3
        blinkt.set_pixel(3, 0, 0, int(BRIGHTNESS))
    else: 
        blinkt.set_pixel(3, 0, 0, 0)
    if os.path.isfile(dir + str(4)):        # Pixel 4
        blinkt.set_pixel(4, 0, 0, int(BRIGHTNESS))
    else: 
        blinkt.set_pixel(4, 0, 0, 0)
    if os.path.isfile(dir + str(5)):        # Pixel 5
        blinkt.set_pixel(5, 0, 0, int(BRIGHTNESS))
    else: 
        blinkt.set_pixel(5, 0, 0, 0)
    if os.path.isfile(dir + str(6)):        # Pixel 6
        blinkt.set_pixel(6, 0, 0, int(BRIGHTNESS))
    else: 
        blinkt.set_pixel(6, 0, 0, 0)
    if os.path.isfile(dir + str(7)):        # Pixel 7
        blinkt.set_pixel(7, 0, 0, int(BRIGHTNESS))
    else: 
        blinkt.set_pixel(7, 0, 0, 0)
    
    blinkt.show()
    time.sleep(float(CLEAR_SLEEP))

    blinkt.clear()
    blinkt.set_pixel(0, 0, 0, 0)
    blinkt.set_pixel(1, 0, 0, 0)
    blinkt.set_pixel(2, 0, 0, 0)
    blinkt.set_pixel(3, 0, 0, 0)
    blinkt.set_pixel(4, 0, 0, 0)
    blinkt.set_pixel(5, 0, 0, 0)
    blinkt.set_pixel(6, 0, 0, 0)
    blinkt.set_pixel(7, 0, 0, 0)
    blinkt.show()
