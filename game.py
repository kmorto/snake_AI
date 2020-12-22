import pygame
import random
from snake import *
from food import *
from ai import SnakeAI

pygame.init()
disx = 600
disy = 400
dis = pygame.display.set_mode((disx,disy))
pygame.display.set_caption('Snake AI Bro')

red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)

snake = Snake(10)
ai = SnakeAI(disx, disy)
global foodPos
food = Food(disx, disy)
font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()


def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, red, [x[0], x[1], 10, 10]) #draws at the x and y with size 10 10


#Displays end game message on screen
def message (msg, color):
    render = font.render(msg, True, color)
    dis.blit(render, [disx/20, disy/2])

#Displays score on screen
def score (value):
    msg = font.render("Score: " + str(value), True, blue)
    dis.blit(msg, [0,0])

def update(ai, action):
    if action == 'up':
        ai.moveUp()
    if action == 'down':
        ai.moveDown()
    if action == 'left':
        ai.moveLeft()
    if action == 'right':
        ai.moveRight()


def snake_play():
    game_over = False #Closes the window if true
    game_continue = False #Gives option to continue playing
    game_human = False #option to let user control snake
    game_ai = True
    mode = False
    game_speed = 60
    reason = None #for AI


    snake_length = 1  # used for score
    snake_list = []  # to keep track of the positions of each block of the snake

    # Starting pos for snake
    x1 = disx / 2
    y1 = disy / 2

    # Randomly place food
    foodPos = food.getPos()
    x2 = foodPos[0]
    y2 = foodPos[1]

    # to move the snake on key press
    x_change = 0
    y_change = 0

    #Ask if AI or Human is playing
    while mode == True:
        dis.fill(black)
        message("Press 1 to play or Press 2 for AI", red)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_human = True
                    game_over = False
                    mode = False
                if event.key == pygame.K_2:
                    game_ai = True
                    game_over = False
                    mode = False

    while not game_over:
        while game_continue == True:
            if(game_ai):
                ai.evolve()
                game_continue == False
                mode = False
                snake_play()
            dis.fill(black)
            message("Game over! Press P to play again or Q to quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_continue = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        snake_play()
                    if event.key == pygame.K_q:
                        game_over = True
                        game_continue = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if (game_human):
                if event.type == pygame.KEYDOWN: #Moves the snake UP DOWN LEFT or RIGHT on key press
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        x_change = -10
                        y_change = 0
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        x_change = 10
                        y_change = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        y_change = -10
                        x_change = 0
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        y_change = 10
                        x_change = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_speed = 30
                if event.key == pygame.K_e:
                    game_speed = 50000
        if(game_ai):
            if(ai.moveCount > ai.maxMoves):
                reason = "Move Count"
                game_over = True

            action = ai.move(ai.snake, food)
            update(ai, action)
            x1 = ai.snake.x
            y1 = ai.snake.y



        #Out of Bounds
        if x1 >= disx or x1 < 0:
            if(game_ai):
                reason = 'Screen'
                game_over = True
            else:
                game_continue = True
        if y1 >= disy or y1 < 0:
            if(game_ai):
                reason = 'Screen'
                game_over = True
            else:
                game_continue = True

        x1 += x_change
        y1 += y_change
        dis.fill(white)
        pygame.draw.rect(dis,black, [x2, y2, 10, 10])
        snake_head = [] #keeps track of the head of the snake
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if (game_ai):
            ai.snake.snakeList.append(snake_head)

        #So we only draw the correct number of blocks
        if len(snake_list) > snake_length:
            del snake_list[0]
        if (game_ai):
            if len(ai.snake.snakeList) > ai.snake.snakeLength:
                del ai.snake.snakeList[0]

        #End game if snake collides with itself
        for x in snake_list[:-1]:
            if x == snake_head:
                if(game_ai):
                    reason = 'Tail'
                    game_over = True
                else:
                    game_continue = True
        if(game_ai):
            draw_snake(ai.snake.snakeList)
            score(ai.snake.snakeLength - 1)
        else:
            draw_snake(snake_list)
            score(snake_length - 1)
        pygame.display.update()

        #Eat food and increase snake size. Place new food
        if x1 == x2 and y1 == y2:
            food.newPos()
            foodPos = food.getPos()
            x2 = foodPos[0]
            y2 = foodPos[1]
            snake_length = snake_length + 1
            ai.snake.snakeLength += 1

        ai.updateQValues(reason)
        clock.tick(game_speed)
    return ai.snake.length() - 1, reason

while True:
    ai.evolve()
    points, reason = snake_play()
    print(f"Games: {ai.generation}; Score: {points}; Reason: {reason}") # Output results of each game to console to monitor as agent is training
