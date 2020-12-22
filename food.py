import random

class Food:
    disx = 0
    disy = 0
    def __init__(self, disx, disy):
        self.x = round(random.randrange(0, disx - 10) / 10.0) * 10.0
        self.y = round(random.randrange(0, disy - 10) / 10.0) * 10.0
        self.disx = disx
        self.disy = disy

    def newPos(self):
        self.x = round(random.randrange(0, self.disx - 10) / 10.0) * 10.0
        self.y = round(random.randrange(0, self.disy - 10) / 10.0) * 10.0

    def getPos(self):
        return [self.x, self.y]

