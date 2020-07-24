#!/usr/bin/env python

import time
import blinkt
import os

dir = "/home/pi/pixels/"
BRIGHTNESS = os.environ["BRIGHTNESS"]
CLEAR_SLEEP = os.environ["CLEAR_SLEEP"]

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
    time.sleep(float(CLEAR_SLEEP))

    if no_pixels == 0:
        for i in range(0,8):
            blinkt.clear()
            blinkt.set_pixel(i, 0, 0, 0)
        blinkt.show()
