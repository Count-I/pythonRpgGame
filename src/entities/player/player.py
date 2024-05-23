import pygame
import os

# put Python classes and functions here

class Player(pygame.sprite.Sprite):
    '''
    Spawn new player
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 10 # player health points
        self.max_hp = 10 # player max health
        self.speed = 2 # default player speed
        self.movex = 0 # x position from origin
        self.movey = 0 # y position from origin
        self.frame = 0 # current player frame 
        self.images = {'up': [], 'down': [], 'left': [], 'right': []} 
        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            for i in range(1, 4):
                img = pygame.image.load(os.path.join('src', 'assets','images', 'hero', 'hero_' + direction, 'sprite' + str(i) + '.png')).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                self.images[direction].append(img)
        self.direction = 'down' # Dirección inicial
        self.image = self.images[self.direction][0] # Imagen inicial
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        
        
    def control(self, x, y):
        """
        control player movement
        """
        self.movex += x * self.speed	 
        self.movey += y * self.speed	
    
    def update(self):
        """
        Update sprite position
        """
        
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        
        if self.movex < 0:
            self.direction = 'left'
        elif self.movex > 0:
            self.direction = 'right'
        elif self.movey < 0:
            self.direction = 'up'
        elif self.movey > 0:
            self.direction = 'down'
            
        self.image = self.images[self.direction][self.frame]

        # Incrementar el frame para la animación
        self.frame += 1
        if self.frame >= 3: # Hay 3 imágenes por dirección
            self.frame = 0