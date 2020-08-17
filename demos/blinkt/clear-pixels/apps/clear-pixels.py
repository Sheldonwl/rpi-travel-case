#!/usr/bin/env python

import blinkt
import os

dir = "/home/pi/pixels/"

for i in range(0,8):
    if os.path.isfile(dir + str(i)):
        os.remove(dir + str(i))

for i in range(0,8):
    blinkt.set_pixel(i, 0, 0, 0)
    blinkt.clear()
    blinkt.show()
