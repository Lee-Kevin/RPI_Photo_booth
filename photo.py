#!/usr/bin/env pytho
#-*-coding: utf-8 -*-
#
# This is the demo code by Kevin Lee
#
#

import picamera
import time
import itertools
import printer 

import RPi.GPIO 
import threading
import logging
from datetime import datetime

logging.basicConfig(level='INFO')
TAKEPHOTO = False
mybutton = 2

class Button():
    def __init__(self,button = 2):
        self.button = button
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        # 按钮连接的GPIO针脚的模式设置为信号输入模式，同时默认拉高GPIO口电平，
        # 当GND没有被接通时，GPIO口处于高电平状态，取的的值为1
        # 注意到这是一个可选项，如果不在程序里面设置，通常的做法是通过一个上拉电阻连接到VCC上使之默认保持高电平
        RPi.GPIO.setup(self.button, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
        
    def attach(self,call_backFun):
        RPi.GPIO.add_event_detect(self.button, RPi.GPIO.RISING, callback=call_backFun, bouncetime=200)
        
    def detach(self):
        RPi.GPIO.remove_event_detect(self.button)
        
    def terminate(self):
        RPi.GPIO.cleanup()
        
def takephoto(mybutton):
    global TAKEPHOTO
    TAKEPHOTO = True
    print("button pressed")

 
class TakePhoto():
    def __init__(self):
        self.s = " Say 'ReSpeaker' to take a photo "
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1366, 768)
        self.camera.framerate = 24
        
        self.camera.start_preview()
        self.camera.annotate_text = ' ' * 25
        self.camera.annotate_text_size = 28

        
        # init the photo printer
        self.myprint = printer.Printer()
        
        self._running = True
    def runloop(self):
        global TAKEPHOTO
        while self._running:
            for c in itertools.cycle(self.s):
                self.camera.annotate_text = self.camera.annotate_text[1:25] + c
                time.sleep(0.1)
                if TAKEPHOTO:
                    self.take_photo()
                    self.print_photo()
                    
                    TAKEPHOTO = False
            
    def take_photo(self):
        count_down = '54321'
        self.camera.annotate_text_size = 160
        for c in count_down:
            self.camera.annotate_text = c
            time.sleep(1)
        self.camera.annotate_text = ''
        datetime.now()
        self.filename = datetime.now().strftime("%d-%H-%M-%S")+'.jpg'
        try:
            self.camera.capture(self.filename)
        except Exception,e:
            logging.info(e)
            
    def print_photo(self):
        self.camera.annotate_text = "Printing..."
        print("print the photo")
        
        if True == self.myprint.printFile(self.filename):
            logging.info("print the photo")
            time.sleep(7)
            
        else:
            time.sleep(3)
            self.camera.annotate_text_size = 100
            self.camera.annotate_text = "Printer Error"
            time.sleep(7)
            logging.info("Printer Error")
            
        self.camera.annotate_text_size = 28
        self.camera.annotate_text = ' ' * 25
        
    def terminate(self):
        self._running = False
        self.camera.stop_preview()
    
if __name__ == "__main__":
    btn = Button(mybutton)
    btn.attach(takephoto)

    app = TakePhoto()
    app.runloop()    