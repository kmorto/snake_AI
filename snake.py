class Snake:

    def __init__(self, tileSize):
        self.snakeList = {'x': 0, 'y': 0}
        self.snakeTile = tileSize
        self.snakeLength = 1
        self.snakeSpeed = 30

    def head_x(self):
        return self.snakeList['x']

    def head_y(self):
        return self.snakeList['y']

    def newheadx(self, newX):
        self.snakeList['x'] = newX

    def newheady(self, newY):
        self.snakeList['y'] = newY

    def length(self):
        return self.snakeLength

    def newlength(self, value):
        self.snakeLength = value

    def changesize(self, value):
        self.snakeTile = value

    def changespeed(self, value):
        self.snakeSpeed = value