#!/usr/bin/env python
#-*-coding: utf-8 -*-
import grove_gesture_sensor
import time
import threading
import sys
from PySide import QtGui,QtCore


class GestureCommunicate(QtCore.QObject):
    direction = QtCore.Signal(str)

class Gesture(threading.Thread):
    def __init__(self,signal = None):
        threading.Thread.__init__(self)
        self._running = True
        
        self.signal = signal
        try:
            self.g=grove_gesture_sensor.gesture()
            self.g.init()
        except Exception,e:
            print(Exception,e)
    def terminate(self):
        self._running = False
    def runloop(self,TimeInterval):
        self._running = True 
        def TargetFun(self, _TimeInterval):
            while self._running:
                gest=self.g.return_gesture()
                if gest==self.g.RIGHT:
                    result = 'right'
                    print("RIGHT")
                elif gest==self.g.LEFT:
                    result = 'left'
                    print("LEFT")
                elif gest==self.g.UP:
                    result = 'up'
                    print("UP")
                elif gest==self.g.DOWN:
                    result = 'down'
                    print("DOWN")
                elif gest==self.g.CLOCKWISE:
                    result = 'click'
                    print("CLOCKWISE")
                elif gest==self.g.ANTI_CLOCKWISE:
                    result = 'click'
                    print("ANTI_CLOCKWISE")
                else:
                    result = None

                if self.signal != None and result != None:
                    self.signal.direction.emit(result)
                    time.sleep(.2)
                    
                time.sleep(_TimeInterval)
        self.subthread = threading.Thread(target=TargetFun,args=(self, TimeInterval,))
        self.subthread.start()
    def isRunning(self):
        if self.subthread.is_alive():
            return True
        else:
            return False  
def callback(value):
    print("callback",value)
    
    
if __name__ == "__main__":
    signal = GestureCommunicate()
    signal.direction[str].connect(callback)
    app = Gesture(signal)
    app.runloop(0)
    app1 = QtGui.QApplication(sys.argv)
    sys.exit(app1.exec_())



