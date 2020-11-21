import pygame

pygame.init()
dis = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Snake AI Bro')

red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# Starting pos
x1 = 200
y1 = 150

#to move the snake on key press
x_change = 0
y_change = 0

clock = pygame.time.Clock()

game_over = False
while not game_over:
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
    x1 += x_change
    y1 += y_change
    dis.fill(black)
    pygame.draw.rect(dis,red, [x1, y1, 10, 10])
    pygame.display.update();
    clock.tick(30)
pygame.quit()
quit()
