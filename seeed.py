#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from PySide import QtCore, QtGui
import random
from joystick import Communicate,JoyStick
from Gesture import Gesture
from TakePhoto import photo
import json
import wakeup 
import os

# Custom Dictionary according to detail situation
Custom_Dict = {
	2:   "Idea",
	4:   "Design ",
	8:   "Make",
	16:  "Prototype ",
    32:  "Seeed",
	64:	 "Improve ",
	128: "Sample",
	256: "Product",
	512: "Promote",
	1024: "Market",
	2048: "Success",
}

class Tile:
    def __init__(self, value):
        self.value = value
         
class Game2048(QtGui.QWidget):
    def __init__(self, parent, width=340, gridSize=2):
        QtGui.QWidget.__init__(self, parent)
        self.gameRunning = False
        self.panelHeight = 00
        self.file_path = os.path.dirname(os.path.realpath(__file__))
        self.width = width
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        f = open(self.file_path+'/rank.json','rb')
        data_json = f.read()
        f.close()
        data = json.loads(data_json)
        self.initRank(data)
        
        self.backgroundBrush = QtGui.QBrush(QtGui.QColor(0xbbada0))
        self.gridSize = gridSize
        self.tileMargin = 16
        self.gridOffsetX = self.tileMargin
        self.gridOffsetY = self.panelHeight + self.tileMargin
        self.brushes = {
        0: QtGui.QBrush(QtGui.QColor(0xcdc1b4)), 
        1: QtGui.QBrush(QtGui.QColor(0x999999)),
        2: QtGui.QBrush(QtGui.QColor(0xeee4da)), 
        4: QtGui.QBrush(QtGui.QColor(0xede0c8)),
        8: QtGui.QBrush(QtGui.QColor(0xf2b179)), 
        16: QtGui.QBrush(QtGui.QColor(0xf59563)),
        32: QtGui.QBrush(QtGui.QColor(0xf67c5f)), 
        64: QtGui.QBrush(QtGui.QColor(0xf65e3b)),
        128: QtGui.QBrush(QtGui.QColor(0xedcf72)), 
        256: QtGui.QBrush(QtGui.QColor(0xedcc61)),
        512: QtGui.QBrush(QtGui.QColor(0xedc850)), 
        1024: QtGui.QBrush(QtGui.QColor(0xedc53f)),
        2048: QtGui.QBrush(QtGui.QColor(0xedc22e)),
        }
        self.lightPen = QtGui.QPen(QtGui.QColor(0xf9f6f2))
        self.darkPen = QtGui.QPen(QtGui.QColor(0x776e65))

        self.hiScore = 0
        self.lastPoint = None
        
        
        self.resize(QtCore.QSize(width, width + self.panelHeight))
        # self.resize(QtCore.QSize(self.screen.width(), self.screen.width() + self.panelHeight))
        self.setGeometry(0, 0, self.screen.width(), self.screen.height())
        self.reset_game()
        
        self.SuccessCallBack = None
        self.SuccessCallBackFlag = False
        self.win = False
        # self.phRect[10] = None
        
        

    def resizeEvent(self, e):
        width = min(e.size().width(), e.size().height() - self.panelHeight)
        self.tileSize = (width - self.tileMargin * (self.gridSize + 1)) / self.gridSize
        self.font = QtGui.QFont('Arial', self.tileSize / 4)
        self.width = width

    def changeGridSize(self, x):
        self.gridSize = x
        self.reset_game()

    def reset_game(self):
        # The Falg of the success call back fun, if the function run once, don't run again
        # False stands for no run  True stands for run once 
        self.SuccessCallBackFlag = False
        # 矩阵瓦块
        self.tiles = [[None for i in range(0, self.gridSize)] for i in range(0, self.gridSize)]
        self.availableSpots = range(0, self.gridSize * self.gridSize)
        self.score = 0
        self.addTile()
        self.addTile()
        self.gameRunning = True
        self.update()
        

    def addTile(self):
        if len(self.availableSpots) > 0:
            v = 2 if random.random() < 0.9 else 4
            i = self.availableSpots.pop(int(random.random() * len(self.availableSpots)))
            gridX = i % self.gridSize
            gridY = i / self.gridSize
            # self.tiles[gridX][gridY]=KeyWord(Tile(v).value)
            self.tiles[gridX][gridY] = Tile(v)

    def up(self):
        moved = False
        for gridX in range(0, self.gridSize):
            for gridY in range(1, self.gridSize):
                if self.tiles[gridX][gridY] is not None:
                    i = gridY
                    while i - 1 >= 0 and self.tiles[gridX][i - 1] is None:
                        i -= 1
                    if i - 1 >= 0 and self.tiles[gridX][i - 1].value == self.tiles[gridX][gridY].value:
                        self.score += self.tiles[gridX][gridY].value * 2
                        self.tiles[gridX][i - 1].value *= 2
                        self.tiles[gridX][gridY] = None
                        moved = True
                    elif i < gridY:
                        self.tiles[gridX][i] = self.tiles[gridX][gridY]
                        self.tiles[gridX][gridY] = None
                        moved = True
        if moved:
            self.updateTiles()

    def down(self):
        moved = False
        for gridX in range(0, self.gridSize):
            for gridY in range(self.gridSize - 2, -1, -1):
                if self.tiles[gridX][gridY] is not None:
                    i = gridY
                    while i + 1 < self.gridSize and self.tiles[gridX][i + 1] is None:
                        i += 1
                    if i + 1 < self.gridSize and self.tiles[gridX][i + 1].value == self.tiles[gridX][gridY].value:
                        self.score += self.tiles[gridX][gridY].value * 2
                        self.tiles[gridX][i + 1].value *= 2
                        self.tiles[gridX][gridY] = None
                        moved = True
                    elif i > gridY:
                        self.tiles[gridX][i] = self.tiles[gridX][gridY]
                        self.tiles[gridX][gridY] = None
                        moved = True
        if moved:
            self.updateTiles()

    def left(self):
        moved = False
        for gridX in range(1, self.gridSize):
            for gridY in range(0, self.gridSize):
                if self.tiles[gridX][gridY] is not None:
                    i = gridX
                    while i - 1 >= 0 and self.tiles[i - 1][gridY] is None:
                        i -= 1
                    if i - 1 >= 0 and self.tiles[i - 1][gridY].value == self.tiles[gridX][gridY].value:
                        self.score += self.tiles[gridX][gridY].value * 2
                        self.tiles[i - 1][gridY].value *= 2
                        self.tiles[gridX][gridY] = None
                        moved = True
                    elif i < gridX:
                        self.tiles[i][gridY] = self.tiles[gridX][gridY]
                        self.tiles[gridX][gridY] = None
                        moved = True
        if moved:
            self.updateTiles()

    def right(self):
        moved = False
        for gridX in range(self.gridSize - 2, -1, -1):
            for gridY in range(0, self.gridSize):
                if self.tiles[gridX][gridY] is not None:
                    i = gridX
                    while i + 1 < self.gridSize and self.tiles[i + 1][gridY] is None:
                        i += 1
                    if i + 1 < self.gridSize and self.tiles[i + 1][gridY].value == self.tiles[gridX][gridY].value:
                        self.score += self.tiles[gridX][gridY].value * 2
                        self.tiles[i + 1][gridY].value *= 2
                        self.tiles[gridX][gridY] = None
                        moved = True
                    elif i > gridX:
                        self.tiles[i][gridY] = self.tiles[gridX][gridY]
                        self.tiles[gridX][gridY] = None
                        moved = True
        if moved:
            self.updateTiles()

    def updateTiles(self):
        self.availableSpots = []
        for i in range(0, self.gridSize):
            for j in range(0, self.gridSize):
                if self.tiles[i][j] is None:
                    self.availableSpots.append(i + j * self.gridSize)
        self.addTile()
        self.hiScore = max(self.score, self.hiScore)
        self.update()
        if not self.movesAvailable():
            # QtGui.QMessageBox.information(self, '', 'Game Over')
            self.gameRunning = False
            self.update()

    def movesAvailable(self):
        if not len(self.availableSpots) == 0:
            return True
        for i in range(0, self.gridSize):
            for j in range(0, self.gridSize):
                if i < self.gridSize - 1 and self.tiles[i][j].value == self.tiles[i + 1][j].value:
                    return True
                if j < self.gridSize - 1 and self.tiles[i][j].value == self.tiles[i][j + 1].value:
                    return True
        return False

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.reset_game()
        if not self.gameRunning:
            return

        if e.key() == QtCore.Qt.Key_Up:
            self.up()
        elif e.key() == QtCore.Qt.Key_Down:
            self.down()
        elif e.key() == QtCore.Qt.Key_Left:
            self.left()
        elif e.key() == QtCore.Qt.Key_Right:
            self.right()   
            
    def DirectionEvent(self, value):
        #      # use this function to wakeup the screen 
        if value == "click":
            self.reset_game()
            wakeup.wakeup()
        if not self.gameRunning:
            wakeup.wakeup()
            return
        if value == "up":
            self.up()
        elif value == "down":
	    wakeup.wakeup()
            self.down()
        elif value == "left":
            self.left()
        elif value == "right":
            self.right()
    def GestureEvent(self, value):

        if value == "click":
            self.reset_game()
        if not self.gameRunning:
            return
        if value == "up":
            self.up()
        elif value == "down":
            self.down()
        elif value == "left":
            self.left()
        elif value == "right":
            self.right()
    def SetSuccessCallBack(self,callFun):
        self.SuccessCallBack = callFun


    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.backgroundBrush)
        painter.drawRect(self.rect())
        painter.setBrush(self.brushes[1])

        # Init the rank list 
        self.phwidth = self.width+25                 
        self.phmargin = 125
        painter.setFont(QtGui.QFont('Arial',self.phwidth/17))
        phRect = []
        for i in range(0,10):
            if i % 2 == 0:
                phRect.append(QtCore.QRect(self.phwidth,125+(i/2)*self.phmargin,40, 50))
            else:
                phRect.append(QtCore.QRect(self.phwidth+300,125+(i/2)*self.phmargin,70,50))
            
            painter.setPen(QtGui.QColor(255-20*i,10*i,0))
            painter.drawText(phRect[i],str(i+1),QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        

        
        for gridX in range(0, self.gridSize):
            # for gridX in range(0,4):
            for gridY in range(0, self.gridSize):
                # for gridY in range(0,4):
                tile = self.tiles[gridX][gridY]
                if tile is None:
                    painter.setBrush(self.brushes[0])
                else:
                    painter.setBrush(self.brushes[tile.value])
                rect = QtCore.QRectF(self.gridOffsetX + gridX * (self.tileSize + self.tileMargin),
                                     self.gridOffsetY + gridY * (self.tileSize + self.tileMargin), self.tileSize,
                                     self.tileSize)
                painter.setPen(QtCore.Qt.NoPen)
                painter.drawRoundedRect(rect, 10.0, 10.0)
                if tile is not None:
                    painter.setPen(self.darkPen if tile.value < 16 else self.lightPen)

                    if len(Custom_Dict[tile.value])> 10:
                        self.font = QtGui.QFont('Arial',self.tileSize / 9)
                    elif len(Custom_Dict[tile.value]) > 6:
                        self.font = QtGui.QFont('Arial', self.tileSize / 6)
                    else:
                        self.font = QtGui.QFont('Arial',self.tileSize / 5)
                    painter.setFont(self.font)

                    painter.drawText(rect, str(Custom_Dict[tile.value]),
                                     QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
                                     
                    # When someone is finished the game, call back the following function
                    if tile.value == 1024 and self.SuccessCallBack != None and self.SuccessCallBackFlag == False:
                        self.filename = self.SuccessCallBack()
                        self.SuccessCallBackFlag = True
                        
                        # deal with the winner photo    
                        try:
                            f = open(self.file_path+'/rank.json','rb')
                            data_json = f.read()
                            data = json.loads(data_json)
                            f.close()
                            for i in range(9,0,-1):
                                data[str(i)] = data[str(i-1)]
                            data['0'] = self.filename
                            f = open(self.file_path+'/rank.json','wb')
                            data_json = json.dumps(data)
                            f.write(data_json)
                            f.close()
                            self.initRank(data)
                        except Exception,e:
                            print(Exception,e)
                    if tile.value == 2048:
                        self.win = True    
                        
        TitleRect = QtCore.QRect(self.screen.width()/4*3-100, 0, self.screen.width()/5, self.screen.width()/15)    
        painter.setPen(QtGui.QColor(255,215,0))
        painter.setFont(QtGui.QFont('Arial',self.width/16))
        painter.drawText(TitleRect,QtCore.Qt.AlignCenter,u'Ranklist')   
        
        if self.gameRunning == False and self.win != True:
            painter.setPen(QtGui.QColor(255,0,0))
            painter.setFont(QtGui.QFont('Arial',self.width/4))
            painter.drawText(event.rect(),QtCore.Qt.AlignLeft,u'GAME\nOVER')

        
        if self.win == True:
            TitleRect = QtCore.QRect(110,180, self.screen.width()/2, self.screen.width()/2)
            painter.setPen(QtGui.QColor(255,0,0))
            painter.setFont(QtGui.QFont('Arial',self.width/4))
                        # painter.drawText(event.rect(),QtCore.Qt.AlignLeft,u'WIN')   
            painter.drawText(TitleRect,QtCore.Qt.AlignLeft,u'WIN')   
            self.win = False
            self.gameRunning = False
    def initRank(self,data):

        width = (self.screen.width() - self.width -10)/2
        pictureX = self.width + 100
        width = self.width/3.84
        rankmargin = 125
        for i in range(0,10):
            pixmap = QtGui.QImage(data[str(i)])
            pixmap = pixmap.scaledToWidth(width)
            lbl = QtGui.QLabel(self)
            lbl.setPixmap(QtGui.QPixmap.fromImage(pixmap))
            if i%2 == 0:
                lbl.move(pictureX,100 + (i/2)*rankmargin)
            else:
                lbl.move(pictureX+300,100 + (i/2)*rankmargin)
                
            lbl.show()
if __name__ == '__main__':
    app = QtGui.QApplication([])
    g = Game2048(None, 768, 4)
    g.move(0, 0)

    g.changeGridSize(4)
    g.setWindowTitle(u'Maker Road')
    
    # configure the joystick
    signal = Communicate()
    signal.direction[str].connect(g.DirectionEvent)
    joystickapp = JoyStick(signal)
    joystickapp.runloop(.01)
    
    # configure the gesture
    # gesture_signal = Gesture.GestureCommunicate()
    # gesture_signal.direction[str].connect(g.GestureEvent)
    # gesture_app = Gesture.Gesture(gesture_signal)
    # gesture_app.runloop(0)
    
    # configure the photo printer
    path = g.file_path+"/photo/"
    ph = photo.TakePhoto(path)
    g.SetSuccessCallBack(ph.take_photo)

    g.show()
    try:
        app.exec_()
    except Exception,e:
        print(Exception,e)

