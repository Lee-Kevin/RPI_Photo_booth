#!/usr/bin/env python
#-*-coding: utf-8 -*-
#
# This is the demo code by Kevin Lee
#
#

import picamera
import time
import itertools
import printer 

import threading
import logging
from datetime import datetime
import os

logging.basicConfig(level='INFO')
TAKEPHOTO = False

class TakePhoto():
    def __init__(self,path):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1366, 768)
        self.camera.framerate = 24       
        self.myprint = printer.Printer()
        self.photo_path = path
        
    def take_photo(self):
        self.camera.start_preview()
        count_down = '54321'
        self.camera.annotate_text_size = 160
        for c in count_down:
            self.camera.annotate_text = "\n"+c
            time.sleep(1)
        self.camera.annotate_text = ''
        datetime.now()
        self.filename = datetime.now().strftime("20%y-%m-%d-%H-%M-%S")+'.jpg'
        try:
            self.camera.capture(self.photo_path + self.filename)
        except Exception,e:
            logging.info(e)
            
        self.print_photo()
        self.camera.stop_preview()
        return self.photo_path+self.filename
            
    def print_photo(self):
        self.camera.annotate_text = "\nPrinting..."
        print("print the photo")
        
        # If the mypin 3 is low the printer will not print the photo
        if True == self.myprint.printFile(self.photo_path+self.filename):
            logging.info("print the photo")
            time.sleep(8)
if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__))
    path = path + "/"
    app = TakePhoto(path)
    filename = app.take_photo()
    print(filename)
