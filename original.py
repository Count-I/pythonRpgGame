import pygame
import sys
import os
import random

'''
Variables
'''
gameOver = False
worldx = 360
worldy = 360
fps = 60  # frame rate
ani = 4   # animation cycles
main = True

BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
GREEN = (0, 255, 0)

'''
Functions
'''

def draw_health_bar(surface, x, y, health, max_health):
    # Calcula el ancho de la barra de vida en función de la cantidad actual de puntos de vida
    bar_width = int(100 * health / max_health)
    # Dibuja el contorno de la barra de vida
    pygame.draw.rect(surface, WHITE, (x, y, 100, 20), 2)
    # Dibuja la barra de vida propiamente dicha
    pygame.draw.rect(surface, GREEN, (x, y, bar_width, 20))

def game_over():
    draw_menu(world, "Game over", (worldx//2 - 30, worldy//2 - 100), WHITE)
    draw_menu(world, "Start again", (worldx//2 - 30, worldy//2 - 100), WHITE)
    
def draw_menu(surface, title, position, color):
    text_surface = font.render(title, True, color)
    surface.blit(text_surface, position)
'''
Objects
'''

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
                img = pygame.image.load(os.path.join('images', 'hero', 'hero_' + direction, 'sprite' + str(i) + '.png')).convert_alpha()
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
        
# put "Enemy" Classes and functions
class Enemy(pygame.sprite.Sprite):
    def __init__(self, patrol_points, speed=1, chase_distance=100, enemy_number=1):
        super().__init__()
        self.images = {'up': [], 'down': [], 'left': [], 'right': []} 
        directions = ['up', 'down', 'left', 'right']
        for direction in directions:
            for i in range(1, 4):
                img = pygame.image.load(os.path.join('images', 'enemies', f'enemy_{enemy_number}', f'enemy_{direction}', f'sprite{i}.png')).convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
                img.set_colorkey(BLACK)
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

'''
Setup
'''

#all_sprites 
all_sprites = pygame.sprite.Group()

backdrop =  pygame.image.load(os.path.join('images','stage.png'))
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

patrol_points = [(50, 50), (300, 50), (300, 300), (50, 300)];

for index in range(2):
    enemy = Enemy(patrol_points, enemy_number=(index+1))
    all_sprites.add(enemy)
    enemy_list.add(enemy)


menu = True #Initial menu
font = pygame.font.Font(None, 36);



start_button = pygame.Rect(worldx//2 - 50, worldy//2 - 25, 100, 50)

'''
Main Loop
'''
while main:
    if gameOver:
        game_over()
    else:   
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
            draw_menu(world, "Menu", (worldx//2 - 30, worldy//2 - 100), WHITE)
            pygame.draw.rect(world, BLUE, start_button)
            draw_menu(world, "Start", (worldx//2 - 25, worldy//2 - 15), WHITE)
            
            pygame.display.flip()
            clock.tick(fps)
        else:
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
            draw_health_bar(world, 10, 10, player.hp, player.max_hp)
            pygame.display.flip()
            clock.tick(fps)