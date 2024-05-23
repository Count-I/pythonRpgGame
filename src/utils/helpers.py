import pygame
import sys
import os
from globals import *

class Helper():
    @staticmethod
    def draw_health_bar(surface, x, y, health, max_health):
        # Calcula el ancho de la barra de vida en función de la cantidad actual de puntos de vida
        bar_width = int(100 * health / max_health)
        # Dibuja el contorno de la barra de vida
        pygame.draw.rect(surface, (254, 254, 254), (x, y, 100, 20), 2)
        # Dibuja la barra de vida propiamente dicha
        pygame.draw.rect(surface, (0, 255, 0), (x, y, bar_width, 20))

    @staticmethod
    def draw_menu():
        Helper.draw_text("Menu", (worldx // 2 - 30, worldy // 2 - 100), (255, 255, 255))
        pygame.draw.rect(world, (25, 25, 200), start_button)
        Helper.draw_text("Start", (worldx // 2 - 25, worldy // 2 - 15), (255, 255, 255))

    @staticmethod
    def game_over():
        Helper.draw_menu()
        Helper.draw_text("Game Over", (worldx // 2 - 30, worldy // 2 - 50), (255, 255, 255))
        Helper.draw_text("Start Again", (worldx // 2 - 30, worldy // 2), (255, 255, 255))
        
    @staticmethod
    def draw_text(text, position, color):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, color)
        world.blit(text_surface, position)