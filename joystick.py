#!/usr/bin/env python
#-*-coding: utf-8 -*-
import sys
import time
import grovepi
import threading
from PySide import QtGui,QtCore


# The Grove Thumb Joystick is an analog device that outputs analog signal ranging from 0 to 1023
# The X and Y axes are two ~10k potentiometers and a momentary push button which shorts the x axis

# My joystick produces slightly different results to the specifications found on the url above
# I've listed both here:

# Specifications
#     Min  Typ  Max  Click
#  X  206  516  798  1023
#  Y  203  507  797

# My Joystick
#     Min  Typ  Max  Click
#  X  253  513  766  1020-1023
#  Y  250  505  769

class Communicate(QtCore.QObject):
    direction = QtCore.Signal(str)

class JoyStick(threading.Thread):
    def __init__(self,signal = None):
        threading.Thread.__init__(self)
        self._running = True
        
        self.signal = signal
        
        self.xPin     = 0
        self.yPin     = 1
        grovepi.pinMode(self.xPin,"INPUT")
        grovepi.pinMode(self.yPin,"INPUT")
        
        self.min      = 8
        self.max      = 15

    def terminate(self):
        self._running = False
    def runloop(self,TimeInterval):
        self._running = True 
        def TargetFun(self, _TimeInterval):
            while self._running:
                result = self.Direction()
                if self.signal != None and result != None:
                    self.signal.direction.emit(result)
                    # print("button pressed",result)
                    time.sleep(.2)
                    
                time.sleep(_TimeInterval)
        self.subthread = threading.Thread(target=TargetFun,args=(self, TimeInterval,))
        self.subthread.start()
    def isRunning(self):
        if self.subthread.is_alive():
            return True
        else:
            return False
    def Direction(self):
        try:
            x = grovepi.analogRead(self.xPin)
            y = grovepi.analogRead(self.yPin)
        
            Rx = (1023 - x) * 10 / x
            Ry = (1023 - y) * 10 / y

                # Was a click detected on the X axis?
            click = 1 if x >= 1020 else 0

            # print("x =", x, " y =", y, " Rx =", Rx, " Ry =", Ry, " click =", click)
            if click == 1:
                # print("click")
                result = "click"
            elif Rx < self.min:
                # print("down")
                result = "down"
            elif Rx > self.max:
                # print("up")
                result = "up"
            elif Ry < self.min:
                # print("right")
                result = "right"
            elif Ry > self.max:
                # print("left")
                result = "left"
            else:
                # print("None")
                result = None
        except IOError:
            # print("Error")
            result = None
        return result
        
def callback(value):
    print("callback",value)
    
    
if __name__ == "__main__":
    signal = Communicate()
    signal.direction[str].connect(callback)
    app = JoyStick(signal)
    app.runloop(.01)
    app1 = QtGui.QApplication(sys.argv)
    sys.exit(app1.exec_())


