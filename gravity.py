import sys
import random

# Pygame
import pygame
from pygame.locals import *

# Interface
from tkinter import filedialog
from tkinter import *


pygame.init()
vec = pygame.math.Vector2

# Gravity movements
acceleration = 0.5
friction = -0.10

# Video & display
screen_width = 1280
screen_height = 720
fps = 60
fps_clock = pygame.time.Clock()

display_surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Busters")

"""
Pygame classes
"""
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((30, 30))
        self.surface.fill((128,255,40))
        self.rect = self.surface.get_rect()

        self.position = vec((100, 600))
        self.velocity = vec(0,0)
        self.acceleration = vec (0,0)
    
    def movement(self):
        self.acceleration = vec(0,0.5) #0,5 adds vertical force a.k.a gravity

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acceleration.x = -acceleration
        if pressed_keys[K_RIGHT]:
            self.acceleration.x = acceleration
        
        self.acceleration.x += self.velocity.x * friction
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        # screen edges
        if self.position.x > screen_width:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = screen_width

        self.rect.midbottom = self.position

    def update(self):
        hits = pygame.sprite.spritecollide(player1, grounds, False)
        if player1.velocity.y > 0:
            if hits:
                self.velocity.y = 0
                self.position.y = hits[0].rect.top + 1

    def jump(self):
        hits = pygame.sprite.spritecollide(self, grounds, False)
        if hits:
            self.velocity.y = -10 # jumping power


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((screen_width, 20))
        self.surface.fill((255,0,0))
        self.rect = self.surface.get_rect(
            center = (screen_width/2, screen_height - 10)
        )
    def movement(self):
        pass


player1 = Player()
ground = Ground()

sprites = pygame.sprite.Group()
sprites.add(player1, ground)

grounds = pygame.sprite.Group()
grounds.add(ground)
""
"""
The game loop that runs
the actual game
"""
while True:
       
    for event in pygame.event.get():
        # Ecit when the close window button is clicked    
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player1.jump()

    display_surface.fill((0,0,0))
    player1.update()

    for sprite in sprites:
        display_surface.blit(sprite.surface, sprite.rect)
        sprite.movement()
      
    pygame.display.update()
    fps_clock.tick(fps)