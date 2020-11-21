import pygame

pygame.init()
dis=pygame.display.set_mode((400,300))
pygame.display.set_caption('Snake AI Bro')
while True:
    for event in pygame.event.get():
        print(event)
pygame.quit()
quit()

