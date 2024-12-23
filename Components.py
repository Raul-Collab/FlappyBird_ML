import pygame
import random
import Brain
import math

class Bird:
    def __init__(self, screen, game, radius, top_player = False):
        self.xPos = screen.get_width()/2 - 100
        self.yPos = screen.get_height()/2
        self.speed = 0
        self.screen = screen
        self.game = game
        self.radius = radius
        self.alive = True
        self.lifespan = 0

        #AI
        self.decision = None
        self.vision = [0.5, 1, 0, 10, 0]
        self.inputs = 4
        self.fitness = 0
        self.weigths =  [-0.5144294811028977, -0.5897756793720694, -1, 0.07409413920364102, -0.26125064615517546]

        if not top_player:
            self.brain = Brain.Brain(self.inputs)
        if top_player:
            self.brain = Brain.Brain(self.inputs, top_player=True, weights=self.weigths)
            
        self.brain.generate_net()

    def drawBird(self):
        pygame.draw.circle(self.screen, "red", (self.xPos, self.yPos), self.radius)

    def birdMove(self):
        self.speed += self.game.GRAVITY
        self.yPos += self.speed

        if self.yPos + self.radius > self.screen.get_height():
            self.alive = False
        if self.yPos + self.radius < 0:
            self.alive = False

    def closest_pipe(self):
        if self.game.Pipes:
            for p in self.game.Pipes:
                if not p.passed:
                    return p
            
    #AI functions
    def look(self):
        if self.closest_pipe() is not None:
            diff_x = self.closest_pipe().xPosition - self.xPos
            top_diff_y = self.closest_pipe().yPosition - self.yPos
            bot_diff_y = self.closest_pipe().yPosition + self.closest_pipe().gap - self.yPos

            max_distance = math.sqrt(self.screen.get_width() ** 2 + self.screen.get_height() ** 2)
            
            self.vision[0] = min(1, diff_x / self.screen.get_width())
            self.vision[1] =  top_diff_y / self.screen.get_height()
            self.vision[2] =  bot_diff_y / self.screen.get_height()
            self.vision[3] = self.speed / 10 
            self.vision[4] = abs(self.screen.get_height() - self.yPos) / self.screen.get_height()

            # print("Vision: ", self.vision)

            # pygame.draw.line(self.game.screen, 
            #                 "green", 
            #                 (self.xPos, self.yPos), 
            #                 (self.closest_pipe().xPosition, self.closest_pipe().yPosition))
            
            # pygame.draw.line(self.game.screen, 
            #                 "green", 
            #                 (self.xPos, self.yPos), 
            #                 (self.closest_pipe().xPosition, self.closest_pipe().yPosition + self.closest_pipe().gap))
        
    def think(self):
        self.decision = self.brain.feed_forward(self.vision)
        if self.decision > 0.5:
            if not self.game.GameOver:
                self.speed = self.game.JUMP_STRENGTH

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Bird(self.screen, self.game, self.radius)
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_net()
        return clone

class Pipe:
    def __init__(self, screen, game, birdRadius):
        self.xPosition = 1400
        self.yPosition = random.randint(20, int(game.height) - 200)
        self.width = 70
        self.gap = 200
        self.screen = screen
        self.game = game
        self.birdRadius = birdRadius
        self.passed = False

    def spawnPipe(self, screen):
        topRect = pygame.draw.rect(screen, "green", [self.xPosition, 0, self.width, self.yPosition])
        botRect = pygame.draw.rect(screen, "green", [self.xPosition, self.yPosition + self.gap, self.width, self.game.height])

    def movePipe(self):
        self.xPosition -= 7

    def exterminate(self):
        if self.xPosition < -700:
            self.game.Pipes.remove(self)
    
    def isPassed(self, bird):
        if not self.passed:
            if self.xPosition < bird.xPos:
                self.game.score += 1
                self.passed = True 
    
    def collision(self, bird):
        if (bird.xPos + self.birdRadius >= self.xPosition and bird.xPos <= self.xPosition + self.width):
            if (bird.yPos <= self.yPosition or bird.yPos + self.birdRadius >= self.yPosition + self.gap):
                bird.alive = False