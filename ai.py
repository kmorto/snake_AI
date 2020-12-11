# q my learning
import numpy as np
import random
import pygame
from snake import *
from food import *
from game import *


# Need to keep track of the number of generations for GUI
class SnakeAI:
    snake = Snake(10)
    moveCount = 0
    initX = 0
    initY = 0
    direction = 2
    points = 0
    disX = 0
    disY = 0

    def __init__(self, disx, disy):
        self.qtable = {}
        self.learningRate = 0.70
        self.discountFactor = 0.9
        self.moves = ['up', 'down', 'left', 'right']
        self.snake.x = disx / 2
        self.snake.y = disy / 2
        self.maxMoves = 100
        self.initX = disx / 2
        self.initY = disy / 2
        self.reward = 10
        self.penalty = -10
        self.disX = disx
        self.disY = disy

    def moveUp(self):
        self.snake.y -= 10
        self.moveCount = self.moveCount + 1
        self.direction = 0

    def moveDown(self):
        self.snake.y += 10
        self.moveCount = self.moveCount + 1
        self.direction = 1

    def moveLeft(self):
        self.snake.x -= 10
        self.moveCount = self.moveCount + 1
        self.direction = 2

    def moveRight(self):
        self.snake.x += 10
        self.moveCount = self.moveCount + 1
        self.direction = 3

    # Go to next generation and reset snake to initial positions and size
    def evolve(self):
        self.snake = Snake(10)
        self.snake.x = self.initX
        self.snake.y = self.initY
        self.moveCount = 0

    # literally goes in a circle
    def circle(self):
        if (self.moveCount < self.maxMoves):
            if (self.direction == 0):  # up
                self.moveRight()
                return
            if (self.direction == 1):  # down
                self.moveLeft()
                return
            if (self.direction == 2):  # left
                self.moveUp()
                return
            if (self.direction == 3):  # right
                self.moveDown()
                return
        else:
            self.evolve()

    def gameOver(self):
        if (self.snake.x > self.disX or self.snake.y > self.disY or self.snake.x < 0 or self.snake.y < 0):
            return True
        for x in self.snake.snakeList[:-1]:
            if x == self.snakeList[-1]:
                return True

    # Checks if its surroundings are safe to move in. Returns 3 numbers for straight, left, or right (0 or 1)
    def obstacleCheck(self):
        test = self
        # Check if its safe to move straight ahead
        if (self.direction == 0):
            test.moveUp()
        if (self.direction == 1):
            test.moveDown()
        if (self.direction == 2):
            test.moveLeft()
        if (self.direction == 3):
            test.moveRight()

        if (test.gameOver()):
            straight = 0
        else:
            straight = 1

        #left check
        test = self
        if (self.direction == 0):
             test.moveLeft()
        if (self.direction == 1):
              test.moveRight()
        if (self.direction == 2):
              test.moveDown()
        if (self.direction == 3):
              test.moveUp()

        if(test.gameOver()):
              left = 0
        else:
              left = 1

        #right check
        test = self
        if (self.direction == 0):
              test.moveRight()
        if (self.direction == 1):
              test.moveLeft()
        if (self.direction == 2):
              test.moveUp()
        if (self.direction == 3):
              test.moveDown()

        if (test.gameOver()):
              right = 0
        else:
              right = 1

        return [straight, left, right]

    def foodDirection(self):
        xpos = foodPos[0]
        ypos = foodPos[1]

        #check if food is straight ahead
        if (self.direction == 0 or self.direction == 1):
            if (ypos == self.snake.y):
                straight = 1
            else:
                straight = 0
        if (self.direction == 2 or self.direction == 3):
            if (xpos == self.snake.x):
                straight = 1
            else:
                straight = 0

        #check if food is to the left
        if (self.direction == 0):
            if (xpos < self.snake.x):
                left = 1
            else:
                left = 0
        if (self.direction == 1):
            if (xpos > self.snake.x):
                left = 1
            else:
                left = 0
        if (self.direction == 2):
            if (ypos > self.snake.y):
                left = 1
            else:
                left = 0
        if (self.direction == 3):
            if (ypos < self.snake.y):
                left = 1
            else:
                left = 0

        #check if food is to the right
        if (self.direction == 0):
            if (xpos > self.snake.x):
                right = 1
            else:
                right = 0
        if (self.direction == 1):
            if (xpos < self.snake.x):
                right = 1
            else:
                right = 0
        if (self.direction == 2):
            if (ypos < self.snake.y):
                right = 1
            else:
                right = 0
        if (self.direction == 3):
            if (ypos > self.snake.y):
                right = 1
            else:
                right = 0
        return [straight, left, right]

    def move(self):
        obstacles = self.obstacleCheck()
        foodDir = self.foodDirection()
        dnn = obstacles.append(foodDir)

