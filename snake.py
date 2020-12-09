
class Snake:

    def __init__(self, tileSize):
        self.x = 0; #For head pos
        self.y = 0;
        self.snakeList = []
        self.snakeTile = tileSize
        self.snakeLength = 1
        self.snakeSpeed = 30

    def head_x(self):
        return self.x

    def head_y(self):
        return self.y

    def newheadx(self, newX):
        self.x = newX

    def newheady(self, newY):
        self.y = newY

    def length(self):
        return self.snakeLength

    def newlength(self, value):
        self.snakeLength = value

    def changesize(self, value):
        self.snakeTile = value

    def changespeed(self, value):
        self.snakeSpeed = value