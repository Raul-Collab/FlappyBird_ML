from typing import Any
import pygame

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor):
        super().__init__(groups)
        bg_image = pygame.image.load('./Sprites/bg.png').convert()    

        full_width = bg_image.get_width() *scaleFactor
        full_height = bg_image.get_height() * scaleFactor
        full_sized_image = pygame.transform.scale(bg_image, (full_width, full_height)) 

        self.image = pygame.Surface((full_width *2, full_height)) 
        self.image.blit(full_sized_image, (0,0))
        self.image.blit(full_sized_image, (full_width,0))

        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)
    
    def update(self):
        self.pos.x -= 2
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class birdSprite(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor):
        super().__init__(groups)
        playerSprite = pygame.image.load('./Sprites/bird.png').convert()  

        self.image = playerSprite
        self.rect = self.image.get_rect(topleft = (0,0))  