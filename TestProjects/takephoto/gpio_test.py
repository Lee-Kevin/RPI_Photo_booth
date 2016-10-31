#!/usr/bin/env python
#-*-coding: utf-8 -*-

import RPi.GPIO
import time
import logging

logging.basicConfig(level='INFO')
mypin = 3

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(mypin, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_DOWN)

if __name__ == "__main__":
    while True:
        if RPi.GPIO.input(mypin):
            print("High")
        else:
            print("LOW")
        time.sleep(1)
    