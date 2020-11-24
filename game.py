import pygame
import random

pygame.init()
disx = 400
disy = 300
dis = pygame.display.set_mode((disx,disy))
pygame.display.set_caption('Snake AI Bro')

red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)


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


def snake_play():
    game_over = False #Closes the window if true
    game_continue = False #Gives option to continue playing
    snake_length = 1  # used for score
    snake_list = []  # to keep track of the positions of each block of the snake

    # Starting pos for snake
    x1 = disx / 2
    y1 = disy / 2

    # Randomly place food
    x2 = round(random.randrange(0, disx - 10) / 10.0) * 10.0
    y2 = round(random.randrange(0, disy - 10) / 10.0) * 10.0

    # to move the snake on key press
    x_change = 0
    y_change = 0

    while not game_over:
        while game_continue == True:
            dis.fill(black)
            message("Game over! Press P to play again or Q to quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        snake_play()
                    if event.key == pygame.K_q:
                        game_over = True
                        game_continue = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
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

        #Out of Bounds
        if x1 >= disx or x1 < 0:
            game_continue = True
        if y1 >= disy or y1 < 0:
            game_continue = True

        x1 += x_change
        y1 += y_change
        dis.fill(white)
        pygame.draw.rect(dis,black, [x2, y2, 10, 10])
        snake_head = [] #keeps track of the head of the snake
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        #So we only draw the correct number of blocks
        if len(snake_list) > snake_length:
            del snake_list[0]

        #End game if snake collides with itself
        for x in snake_list[:-1]:
            if x == snake_head:
                game_continue = True

        draw_snake(snake_list)
        score(snake_length - 1)
        pygame.display.update()

        #Eat food and increase snake size. Place new food
        if x1 == x2 and y1 == y2:
            print("Munch")
            x2 = round(random.randrange(0, disx - 10) / 10.0) * 10.0
            y2 = round(random.randrange(0, disy - 10) / 10.0) * 10.0
            snake_length = snake_length + 1

        clock.tick(20)
    pygame.quit()
    quit()

snake_play()