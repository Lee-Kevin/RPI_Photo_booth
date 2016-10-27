#!/usr/bin/env python
#-*- coding: utf-8 -*-
import cups
import logging
import threading

logging.basicConfig(level='INFO')
my_print_name = "Canon_SELPHY_CP1200"

class Printer(threading.Thread):
    def __init__(self,):
        super(Printer,self).__init__()
        
        self.filename = None
        self.flag     = False
        self.printname= None
        
        self.conn = cups.Connection()
        
# check if the printer is done
# return 1, printer is done
# return 0, cann't find the printer

    def checkprinter(self):
        self.printers = self.conn.getPrinters()
        for self.printname in self.printers.keys():
            if my_print_name == self.printname:
                break
        if my_print_name == self.printname:
            return True
        else:
            return False
# Print the file 
# input: filename
# return: True, print done
# return: False, There is some wrong with printer        
    def printFile(self,filename):
        self.filename = filename
        self.flag     = True
        if True == self.checkprinter():
            try:
                self.conn.printFile(self.printname,self.filename,"TITLE",{})
                return True
            except Exception,e:
                logging.info(e)
                return False
        else:
            return False
           
if __name__ == "__main__":
    myprint = Printer()
    print myprint.checkprinter()
    # 打印一个测试照片
    myprint.printFile("test.jpg")
    print "printing done"