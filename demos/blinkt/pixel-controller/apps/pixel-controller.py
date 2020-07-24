#!/usr/bin/env python

import time
import blinkt
import os

dir = "/home/pi/pixels/"
BRIGHTNESS = 255
CLEAR_SLEEP = 0.1

while True:
    no_pixels = 8
    for i in range(0,8):
        if os.path.isfile(dir + str(i)):
            blinkt.set_pixel(i, 0, 0, int(BRIGHTNESS))
            no_pixels += 1
        else:
            blinkt.set_pixel(i, 0, 0, 0)
            no_pixels -= 1

    blinkt.show()
    time.sleep(int(CLEAR_SLEEP))

    if no_pixels == 0:
        for i in range(0,8):
            blinkt.clear()
            blinkt.set_pixel(i, 0, 0, 0)
        blinkt.show()
