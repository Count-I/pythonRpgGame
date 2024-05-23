import pygame

gameOver = False
worldx = 360
worldy = 360
fps = 60  # frame rate
ani = 4   # animation cycles
main = True
world = pygame.display.set_mode([worldx, worldy])
BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
GREEN = (0, 255, 0)

start_button = pygame.Rect(worldx//2 - 50, worldy//2 - 25, 100, 50)
    