import pygame
from src.entities.player.player import Player
from src.entities.enemy.enemy import Enemy
from src.utils.helpers import draw_health_bar
from src.utils.helpers import draw_menu

class Game:
    def __init__(self):
        self.worldx = 360
        self.worldy = 360
        self.fps = 60
        self.main = True
        self.clock = pygame.time.Clock()
        self.backdrop = pygame.image.load("src/assets/images/stage.png")
        self.backdropbox = self.backdrop.get_rect()
        self.player = Player()
        self.enemy_list = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.player_list.add(self.player)
        self.all_sprites.add(self.player)
        self.steps = 2
        self.menu = True
        self.gameOver = False
        self.font = pygame.font.Font(None, 36)
        self.start_button = pygame.Rect(self.worldx // 2 - 50, self.worldy // 2 - 25, 100, 50)

        patrol_points = [(50, 50), (300, 50), (300, 300), (50, 300)]
        for index in range(2):
            enemy = Enemy(self.worldx, self.worldy, patrol_points, enemy_number=(index + 1))
            self.all_sprites.add(enemy)
            self.enemy_list.add(enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    self.menu = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.player.control(-self.steps, 0)
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.player.control(self.steps, 0)
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    self.player.control(0, -self.steps)
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.player.control(0, self.steps)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    self.player.control(self.steps, 0)
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    self.player.control(-self.steps, 0)
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    self.player.control(0, self.steps)
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    self.player.control(0, -self.steps)
                elif event.key == ord('q'):
                    self.main = False

    def run(self):
        while self.main:
            if self.gameOver:
                self.game_over()
            else:
                if self.menu:
                    self.handle_events()
                    draw_menu(self)
                else:
                    self.handle_events()
                    self.update()
                    self.draw()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def update(self):
        self.all_sprites.update()
        for enemy in self.enemy_list:
            if self.player.hitbox.colliderect(enemy.hitbox):
                self.player.hp -= 1
                if enemy.rect.x < self.player.rect.x:
                    self.player.rect.x += 10
                    enemy.rect.x -= 10
                elif enemy.rect.x > self.player.rect.x:
                    self.player.rect.x -= 10
                    enemy.rect.x += 10
                if enemy.rect.y < self.player.rect.y:
                    self.player.rect.y += 10
                    enemy.rect.y -= 10
                elif enemy.rect.y > self.player.rect.y:
                    self.player.rect.y -= 10
                    enemy.rect.y += 10
        if self.player.hp <= 0:
            self.gameOver = True

    def draw(self):
        self.player_list.draw(self.world)
        self.enemy_list.draw(self.world)
        draw_health_bar(self.world, 10, 10, self.player.hp, self.player.max_hp)