# q my learning
import random
import pygame
from snake import *
from food import *
import dataclasses
import json

@dataclasses.dataclass
class GameState:
    distance: tuple  # Returns how far the snake is from the food in x and y
    position: tuple #list that gives the poisiton of the food in respect to snake
    surroundings: tuple  # 4 number list that gives surroundings
    food: tuple  # Returns the x and y position of the food
    obstacle: tuple



# Need to keep track of the number of generations for GUI
class SnakeAI:

    def __init__(self, disx, disy):
        self.snake = Snake(10)
        self.qtable = self.LoadQvalues()
        self.history = []
        self.learningRate = 0.70
        self.discountFactor = 0.5
        self.epsilon = 0.1
        self.snake.x = disx / 2
        self.snake.y = disy / 2
        self.maxMoves = 1000
        self.initX = disx / 2
        self.initY = disy / 2
        self.reward = 10
        self.penalty = -10
        self.disX = disx
        self.disY = disy
        self.moveCount = 0
        self.direction = 3
        self.points = 0
        self.food = Food(disx, disy)
        self.generation = 1
        self.gameCount = 1

        self.actions = {
            0: 'up',
            1: 'down',
            2: 'left',
            3: 'right'
        }

    def LoadQvalues(self, path="qvalues.json"):
        with open(path, "r") as f:
            qvalues = json.load(f)
        return qvalues

    def SaveQvalues(self, path="qvalues.json"):
        with open(path, "w") as f:
            json.dump(self.qtable, f)

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
        self.history = []
        self.generation += 1

        if self.gameCount > 100:
            self.epsilon = 0
        else:
            self.epsilon = .1
        self.gameCount += 1
        if self.gameCount % 100 == 0:  # Save qvalues every qvalue_dump_n games
            print("Save Qvals")
            self.SaveQvalues()

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

    def gameOver(self, snake):
        if (snake.x > self.disX or self.snake.y > self.disY or snake.x < 0 or snake.y < 0):
            return True
        for x in snake.snakeList[:-1]:
            if x == snake.snakeList[-1]:
                return True

    def move(self, snake, food):
        state = self.getState(snake, food)
        # Epsilon Greedy
        rand = random.uniform(0, 1)
        if rand < self.epsilon:
            action = random.choices(list(self.actions.keys()))[0]
        else:
            state_score = self.qtable[self.getStateStr(state)]
            action = state_score.index(max(state_score))
        action_val = self.actions[action]


        self.history.append({
            'state': state,
            'action': action
        })

        return action_val

    def updateQValues(self, reason):
        history = self.history[::-1]
        for i, h in enumerate(history[:-1]):
            if reason:  # Snake died
                sN = history[0]['state']
                aN = history[0]['action']
                reward = -100
                state_str = self.getStateStr(sN)
                self.qtable[state_str][aN] = (1 - self.learningRate) * self.qtable[state_str][aN] + self.learningRate * reward
                reason = None
            else:
                s1 = h['state']  # current state
                s0 = history[i + 1]['state']  # previous state
                a0 = history[i + 1]['action']  # previous action

                x1 = s0.distance[0]
                y1 = s0.distance[1]

                x2 = s1.distance[0]
                y2 = s1.distance[1]

                if s0.food != s1.food:  # Snake ate a food, positive reward
                    reward = 10
                elif (abs(x1) > abs(x2) or abs(y1) > abs(y2)):  # Snake is closer to the food, positive reward
                    reward = 1
                else:
                    reward = -1.5  # Snake is further from the food, negative reward

                state_str = self.getStateStr(s0)
                new_state_str = self.getStateStr(s1)
                self.qtable[state_str][a0] = (1 - self.learningRate) * (
                    self.qtable[state_str][a0]) + self.learningRate * (
                        reward + self.discountFactor * max(self.qtable[new_state_str]))

    def getState(self, snake, food):
        sqs = [
            (snake.x - 10, snake.y),
            (snake.x + 10, snake.y),
            (snake.x, snake.y - 10),
            (snake.x, snake.y + 10)
        ]
        surrounding_list = []
        for sq in sqs:
            if sq[0] < 0 or sq[1] < 0:  # off screen left or top
                surrounding_list.append('1')
            elif sq[0] >= self.disX or sq[1] >= self.disY:  # off screen right or bottom
                surrounding_list.append('1')
            elif sq in snake.snakeList[:-1]:  # part of tail
                surrounding_list.append('1')
            else:
                surrounding_list.append('0')
        surroundings = ''.join(surrounding_list)




        foodPos = food.getPos()
        dis_x = foodPos[0] - snake.x
        dis_y = foodPos[1] - snake.y

        if dis_x > 0:
            pos_x = '1' # Food is to the right of the snake
        elif dis_x < 0:
            pos_x = '0' # Food is to the left of the snake
        else:
            pos_x = 'NA' # Food and snake are on the same X file

        if dis_y > 0:
            pos_y = '3' # Food is below snake
        elif dis_y < 0:
            pos_y = '2' # Food is above snake
        else:
            pos_y = 'NA' # Food and snake are on the same Y file

        return GameState((dis_x, dis_y), (pos_x, pos_y), surroundings, (foodPos[0], foodPos[1]))

    def getStateStr(self, state):
        return str((state.position[0], state.position[1], state.surroundings))

    def obstacleCheck(self, snake):
        test = Snake(10)
        test.x = snake.x
        test.y = snake.y
        test.snakeList = snake.snakeList



