#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
from PySide import QtCore, QtGui
import random
from joystick import Communicate,JoyStick
from TakePhoto import photo

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
        self.panelHeight = 80
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
        self.scoreRect = QtCore.QRect(10, 10, 80, self.panelHeight - 20)
        self.hiScoreRect = QtCore.QRect(100, 10, 80, self.panelHeight - 20)
        self.resetRect = QtCore.QRectF(190, 10, 80, self.panelHeight - 20)
        self.scoreLabel = QtCore.QRectF(10, 25, 80, self.panelHeight - 30)
        self.hiScoreLabel = QtCore.QRectF(100, 25, 80, self.panelHeight - 30)
        self.hiScore = 0
        self.lastPoint = None
        
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.resize(QtCore.QSize(width, width + self.panelHeight))
        # self.resize(QtCore.QSize(self.screen.width(), self.screen.width() + self.panelHeight))
        self.setGeometry(0, 0, self.screen.width(), self.screen.height())
        self.reset_game()
        self.width = width
        
        self.SuccessCallBack = None
        self.SuccessCallBackFlag = False

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
        if not self.gameRunning:
            return
        if e.key() == QtCore.Qt.Key_Escape:
            self.reset_game()
        elif e.key() == QtCore.Qt.Key_Up:
            self.up()
        elif e.key() == QtCore.Qt.Key_Down:
            self.down()
        elif e.key() == QtCore.Qt.Key_Left:
            self.left()
        elif e.key() == QtCore.Qt.Key_Right:
            self.right()   
            
    def DirectionEvent(self, value):

        if value == "click":
            self.reset_game()
        elif value == "up":
            self.up()
        elif value == "down":
            self.down()
        elif value == "left":
            self.left()
        elif value == "right":
            self.right()
    def SetSuccessCallBack(self,callFun):
        self.SuccessCallBack = callFun
            

    # def mousePressEvent(self, e):
        # self.lastPoint = e.pos()

    # def mouseReleaseEvent(self, e):
        # if self.resetRect.contains(self.lastPoint.x(), self.lastPoint.y()) and self.resetRect.contains(e.pos().x(),
                                                                                                       # e.pos().y()):
            # if QtGui.QMessageBox.question(self, '', 'Are you sure you want to start a new game?', QtGui.QMessageBox.Yes,
                                          # QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
                # self.reset_game()
        # elif self.gameRunning and self.lastPoint is not None:
            # dx = e.pos().x() - self.lastPoint.x()
            # dy = e.pos().y() - self.lastPoint.y()
            # if abs(dx) > abs(dy) and abs(dx) > 10:
                # if dx > 0:
                    # self.right()
                # else:
                    # self.left()
            # elif abs(dy) > 10:
                # if dy > 0:
                    # self.down()
                # else:
                    # self.up()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.backgroundBrush)
        painter.drawRect(self.rect())
        painter.setBrush(self.brushes[1])
        painter.drawRoundedRect(self.scoreRect, 10.0, 10.0)
        painter.drawRoundedRect(self.hiScoreRect, 10.0, 10.0)
        painter.drawRoundedRect(self.resetRect, 10.0, 10.0)
        painter.setFont(QtGui.QFont('Arial', 9))
        painter.setPen(self.darkPen)
        painter.drawText(QtCore.QRectF(10, 15, 80, 20), 'SCORE',
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.drawText(QtCore.QRectF(100, 15, 80, 20), 'HIGHSCORE',
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.setFont(QtGui.QFont('Arial', 15))
        painter.setPen(self.lightPen)
        painter.drawText(self.resetRect, 'RESET', QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.setFont(QtGui.QFont('Arial', 12))
        painter.setPen(self.lightPen)
        painter.drawText(self.scoreLabel, str(self.score),
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.drawText(self.hiScoreLabel, str(self.hiScore),
                         QtGui.QTextOption(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter))
        painter.setFont(self.font)
        
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
                    if tile.value == 8 and self.SuccessCallBack != None and self.SuccessCallBackFlag == False:
                        self.SuccessCallBack()
                        self.SuccessCallBackFlag = True
        if not self.gameRunning:
            painter.setPen(QtGui.QColor(255,0,0))
            painter.setFont(QtGui.QFont('Arial',self.width/4))
            painter.drawText(event.rect(),QtCore.Qt.AlignCenter,u'GAME\nOVER')

def callback():
    print("I have finished the game")
if __name__ == '__main__':
    app = QtGui.QApplication([])
    g = Game2048(None, 600, 4)
    g.move(0, 0)

    g.changeGridSize(3)
    g.setWindowTitle(u'创客养成记')
    
    # configure the joystick
    signal = Communicate()
    signal.direction[str].connect(g.DirectionEvent)
    joystickapp = JoyStick(signal)
    joystickapp.runloop(.01)
    
    # configure the photo printer
    ph = photo.TakePhoto()
    g.SetSuccessCallBack(ph.take_photo)
    
    
    g.show()
    app.exec_()

