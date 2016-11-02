#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os

def wakeup():
    os.system("/usr/bin/xset -dpms")
    
if __name__ == "__main__":
    wakeup()