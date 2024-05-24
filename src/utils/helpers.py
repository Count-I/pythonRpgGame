import pygame
import sys
import os
from globals import *
import random
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
    def draw_menu(over=False):
        if(over):
            Helper.draw_text("Game over", (worldx // 2, worldy // 2 - 100), (255, 255, 255))
            pygame.draw.rect(world, (25, 25, 200), start_again_button)
            Helper.draw_text("Start again", (worldx // 2, worldy // 2), (255, 255, 255))

        else:
            Helper.draw_text("Menu", (worldx // 2, worldy // 2 - 100), (255, 255, 255))
            pygame.draw.rect(world, (25, 25, 200), start_button)
            Helper.draw_text("Start", (worldx // 2, worldy // 2 ), (255, 255, 255))

    @staticmethod
    def game_over():
        Helper.draw_menu()
        Helper.draw_text("Game Over", (worldx // 2 - 30, worldy // 2 - 50), (255, 255, 255))
        Helper.draw_text("Start Again", (worldx // 2 - 30, worldy // 2), (255, 255, 255))
        
    @staticmethod
    def draw_text(text, position, color):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(position[0], position[1]))
        world.blit(text_surface, text_rect)
    
    @staticmethod 
    def reset_game(player, enemy_list):
        global gameOver, paused
        # Reset game variables to initial state
        gameOver = False
        paused = False
        Helper.reset_player(player)
        Helper.reset_enemies(enemy_list)
        
    @staticmethod 
    def reset_player(player):
        # Reset player position
        player.rect.x = 160
        player.rect.y = 260
        # Reset player health
        player.hp = player.max_hp
        player.movex = 0
        player.movey = 0

    def reset_enemies(enemy_list):
        for enemy in enemy_list:
            Helper.reset_enemy(enemy)
            
    def reset_enemy(enemy):
        enemy.rect.x = random.randint(0, worldx - enemy.rect.width)
        enemy.rect.y = random.randint(0, worldy - enemy.rect.height)
        enemy.prev_x = enemy.rect.x
        enemy.prev_y = enemy.rect.y
        enemy.patrol_index = 0