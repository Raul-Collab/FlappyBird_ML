import pygame
import matplotlib.pyplot as plt
import numpy as np
import random
from Sprites import BG, birdSprite
from Settings import *
import Components
import Population


#Classes
class Game:
    #Variables
    running = True
    speed = 0
    score = 0
    GameOver = False
    running = True
    x = []
    y = []

    # Constants
    GRAVITY = 0.5  
    JUMP_STRENGTH = -10  
    Pipes = []
    height = Window_Height
    width = Window_Width
    FPS = Frames
    
    def __init__(self, top_player = False):
        pygame.init()
        pygame.font.init()

        self.birds = []
        self.radius = 20
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        if not top_player:
            self.birdAmount = 250
        else:
            self.birdAmount = 0

        bg_height = pygame.image.load('./Sprites/bg.png').get_height()
        self.scaleFactor = Window_Height / bg_height
        self.allSprites = pygame.sprite.Group()

        self.top_player = top_player

        BG(self.allSprites, self.scaleFactor)
        self.population = Population.Population(self.birds, self)

        for i in range(0, self.birdAmount):
            self.birds.append(Components.Bird(self.screen, self, self.radius))

        if top_player:
            self.birds.append(Components.Bird(self.screen, self, self.radius, top_player=True))
    
    def extinct(self):
        extinct = True
        for b in self.birds:
            if b.alive:
                extinct = False
        return extinct

    def update_birds(self):
        if not self.extinct():
            for b in self.birds:
                if b.alive == True:
                    b.drawBird()
                    if self.Pipes:
                        b.look()
                    b.think()
                    b.birdMove()
                    b.lifespan += 1 

        else:
            self.Pipes.clear()
            if not self.top_player:
                self.population.natural_selection()

    def update_Pipes(self):
        if self.Pipes:
            for pipe in self.Pipes:
                pipe.spawnPipe(self.screen)
                pipe.exterminate()
                for b in self.birds:
                    pipe.collision(b) 
                    pipe.isPassed(b)
                pipe.movePipe()
        else:
            self.Pipes.append(Components.Pipe(self.screen, self, self.radius))

        if self.Pipes:
            if self.Pipes[-1].xPosition <= 1000:
                    if len(self.Pipes) < 8:
                        self.Pipes.append(Components.Pipe(self.screen, self, self.radius))

    def update_score(self):
        score_text = self.font.render('Generation: ' + str(self.population.generation), True, 'white')
        self.screen.blit(score_text, (self.screen.get_width()/2 - 50, 0))

        # X axis values:
        x = [2,3,7,29,8,5,13,11,22,33]
        # Y axis values:
        y = [4,7,55,43,2,4,11,22,33,44]
        # Create scatter plot:
        plt.scatter(x, y)
        plt.show()

    def update_sprites(self):
        self.allSprites.draw(self.screen)
        if not self.GameOver:
            self.allSprites.update()

    def mainLoop(self):

        while self.running:
            self.clock.tick(self.FPS)
            self.screen.fill("black")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            
            self.update_sprites()
            self.update_Pipes()
            self.update_birds()
            self.update_score()


            pygame.display.flip()

    pygame.quit() 



    
 



