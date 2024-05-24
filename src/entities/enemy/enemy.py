import pygame
import os
import random
from globals import *

# put "Enemy" Classes and functions
class Enemy(pygame.sprite.Sprite):
    def __init__(self, worldx, worldy, color, patrol_points, speed=1, chase_distance=100, enemy_number=1):
        super().__init__()
        self.images = {'up': [], 'down': [], 'left': [], 'right': []} 
        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            for i in range(1, 4):
                img = pygame.image.load(os.path.join('src', 'assets','images', 'enemies', f'enemy_{enemy_number}', f'enemy_{direction}', f'sprite{i}.png')).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                img.set_colorkey(color)
                self.images[direction].append(img)
                
        self.direction = 'down' # Dirección inicial
        self.image = self.images[self.direction][0] # Imagen inicial
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, worldx - self.rect.width)
        self.rect.y = random.randint(0, worldy - self.rect.height)
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y
        self.patrol_points = patrol_points
        self.patrol_index = 0
        self.speed = speed
        self.chase_distance = chase_distance
        self.chasing = False
        self.frame = 0
        self.hitbox = self.rect

    def patrol(self):
        target_point = self.patrol_points[self.patrol_index]
        if self.rect.x < target_point[0]:
            self.rect.x += self.speed
        elif self.rect.x > target_point[0]:
            self.rect.x -= self.speed

        if self.rect.y < target_point[1]:
            self.rect.y += self.speed
        elif self.rect.y > target_point[1]:
            self.rect.y -= self.speed

        if self.rect.x == target_point[0] and self.rect.y == target_point[1]:
            self.patrol_index = (self.patrol_index + 1) % len(self.patrol_points)

        # Boundary check
        if self.rect.right > worldx:
            self.rect.right = worldx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > worldy:
            self.rect.bottom = worldy
        if self.rect.top < 0:
            self.rect.top = 0

    def update(self, player):
        distance_to_player = ((self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2) ** 0.5
        if distance_to_player < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False

        if self.chasing:
            self.chase(player)
        else:
            self.patrol()

        if self.rect.x < self.prev_x:
            self.direction = 'left'
        elif self.rect.x > self.prev_x:
            self.direction = 'right'
        elif self.rect.y < self.prev_y:
            self.direction = 'up'
        elif self.rect.y > self.prev_y:
            self.direction = 'down'
        
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y
        
        self.image = self.images[self.direction][self.frame]


        # Incrementar el frame para la animación
        self.frame += 1
        if self.frame >= 3: # Hay 3 imágenes por dirección
            self.frame = 0

    def chase(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed