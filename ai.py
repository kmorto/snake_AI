# q my learning
import numpy as np
import random
import pygame
from snake import *

#Need to keep track of the number of generations for GUI
class SnakeAI:
      snake = Snake(10)
      maxMoves = 1000
      moveCount = 0
      direction = 2
      def __init__(self, disx, disy):
            self.qtable = {}
            self.learningRate = 0.70
            self.discountFactor = 0.9
            self.moves = ['up', 'down', 'left', 'right']
            self.snake.x = disx / 2
            self.snake.y = disy / 2

      def moveUp(self):
          self.snake.y -= 10
          self.moveCount + 1
          self.direction = 0

      def moveDown(self):
            self.snake.y += 10
            self.moveCount + 1
            self.direction = 1

      def moveLeft(self):
            self.snake.x -= 10
            self.moveCount + 1
            self.direction = 2

      def moveRight(self):
            self.snake.x += 10
            self.moveCount + 1
            self.direction = 3

      def circle(self):
            if(self.direction == 0): #up
                  self.moveRight()
                  return
            if(self.direction == 1): #down
                  self.moveLeft()
                  return
            if(self.direction == 2): #left
                  self.moveUp()
                  return
            if(self.direction == 3): #right
                  self.moveDown()
                  return






