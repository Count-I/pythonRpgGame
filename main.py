import pygame
import sys
import os
import random
from globals import *
from src.entities.player.player import Player
from src.entities.enemy.enemy import Enemy
from src.utils.helpers import Helper

'''
Variables
'''
'''
Objects
'''

'''
Setup
'''

#all_sprites 
all_sprites = pygame.sprite.Group()

backdrop =  pygame.image.load(os.path.join('src', 'assets','images','stage.png'))
clock = pygame.time.Clock()
pygame.init()
world = pygame.display.set_mode([worldx, worldy])
backdropbox = world.get_rect()

player = Player()   # spawn player
player.rect.x = 160   # send player to x cordenate
player.rect.y = 260   #send player to y cordenate
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 2
all_sprites.add(player)

# Setup Enemy

enemy_list = pygame.sprite.Group()

patrol_points = [(50, 50), (300, 50), (300, 300), (50, 300)]

for index in range(2):
    enemy = Enemy(worldx, worldy, BLACK, patrol_points, enemy_number=(index+1))
    all_sprites.add(enemy)
    enemy_list.add(enemy)


menu = True #Initial menu
font = pygame.font.Font(None, 36)



start_button = pygame.Rect(worldx//2 - 50, worldy//2 - 25, 100, 50)

'''
Main Loop
'''
while main:
        if menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    try:
                        sys.exit()
                    finally:
                        main = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        menu = False
            
            world.blit(backdrop, backdropbox)
            Helper.draw_menu()
            pygame.draw.rect(world, BLUE, start_button)
            Helper.draw_menu()
            
            pygame.display.flip()
            clock.tick(fps)
        else:
            if gameOver:
                menu = True
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    try:
                        sys.exit()
                    finally:
                        main = False
        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        player.control(-steps, 0)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        player.control(steps, 0)
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        player.control(0, -steps)
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        player.control(0, steps)
        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        player.control(steps, 0)
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        player.control(-steps, 0)
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        player.control(0, steps)
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        player.control(0, -steps)
                    if event.key == ord('q'):
                        pygame.quit()
                        sys.exit()
                        main = False  
        
            world.blit(backdrop, backdropbox)
            player.update()
            for enemy in enemy_list:
                enemy.update(player)
                if player.hitbox.colliderect(enemy.hitbox):
                    player.hp -= 1
                    if enemy.rect.x < player.rect.x:   
                        player.rect.x += 10                
                        enemy.rect.x -= 10
                    elif enemy.rect.x > player.rect.x:
                        player.rect.x -= 10
                        enemy.rect.x += 10
                    if enemy.rect.y < player.rect.y:  
                        player.rect.y += 10    
                        enemy.rect.y -= 10
                    elif enemy.rect.y > player.rect.y:
                        player.rect.y -= 10
                        enemy.rect.y += 10
                        
                    
            if(player.hp == 0):
                gameOver = True      
            player_list.draw(world)
            enemy_list.draw(world)
            Helper.draw_health_bar(world, 10, 10, player.hp, player.max_hp)
            pygame.display.flip()
            clock.tick(fps)