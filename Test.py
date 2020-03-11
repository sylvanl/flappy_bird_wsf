# import pygame, sys
# from pygame.locals import *
# pygame.init()
import random
import pygame
from pygame.locals import *
pygame.init() 

# Window size 
gameHeight = 600
floorHeight = 50
windowWidth = 400

# Settings
minHoleHeight = 100
holeSize = 80

# Display creation
display = pygame.display.set_mode((windowWidth, gameHeight + floorHeight)) 
pygame.display.set_caption('Flappy WSF') 

# Import images 
background = pygame.image.load("bg.png") 
floor = pygame.image.load("ground.png") 
pipeBody = pygame.image.load("pipe_body.png") 
pipeEnd = pygame.image.load("pipe_end.png")


def pipeGeneration(pipePosition) :
    topHeight = random.randint(minHoleHeight, gameHeight - minHoleHeight - holeSize)
    bottomHeight = gameHeight - topHeight - holeSize
    
    # Top Pipe
    display.blit(pygame.transform.scale(pipeBody, (60, topHeight)), (pipePosition, 0))
    display.blit(pygame.transform.scale(pipeEnd, (60, 30)), (pipePosition, topHeight - 30))

    # Bottom Pipe
    display.blit(pygame.transform.scale(pipeBody, (60, bottomHeight)), (pipePosition, gameHeight - bottomHeight))
    display.blit(pygame.transform.scale(pipeEnd, (60, 30)), (pipePosition, gameHeight - bottomHeight))


class Pipe(pygame.sprite.Sprite):
    """Pipe obstacle
    """

    WIDTH = 80
    HEIGHT = 32
    INTERVAL = 3000

    # Define a new random pipe
    def __init__(self, pipe):
        
        self.gameHeight = float(gameHeight - 1)
        self.score_count = 0

        # random = int(input ("Devinez le nombre (entre 0 & 100)"))





pipe = pygame.image.load("pipe_end.png")
newPipe = Pipe(pipe)


def main():

    # Infinite loop 
    while True : 
        # display.blit(image, (0, 0))
        display.blit(pygame.transform.scale(background, (500, gameHeight)), (0, 0))
        display.blit(pygame.transform.scale(floor, (500, floorHeight)), (0, gameHeight))
        pipeGeneration(150)
        pipeGeneration(300)

        for event in pygame.event.get() : 
    
            if event.type == pygame.QUIT : 
                pygame.quit() 
                quit() 
            pygame.display.update() 


if __name__ == "__main__":
    main()