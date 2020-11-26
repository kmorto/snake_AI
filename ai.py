# q my learning
import numpy as np
import random


class SnakeAI:

      qtable = {}
      learningRate = 0.70
      discountFactor = 0.9

      moves = ['up', 'down', 'left', 'right']
      maxMoves = 1000 #Limit to 100 moves per loop to avoid infinite loops



