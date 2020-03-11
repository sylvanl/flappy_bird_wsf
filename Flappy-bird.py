"""This is an independant python game created specially for the Web School Factory students to have fun with."""
import random
import pygame
from pygame.locals import *
pygame.init()

# Window size
GAME_HEIGHT = 600
FLOOR_HEIGHT = 100
WINDOW_WIDTH = 600

# Settings
FRAME_RATE = 1
PIPE_WIDTH = 60
MIN_WHOLE_HEIGHT = 100
HOLE_SIZE = 120
SPEED = 2
BIRD_UPDATE_TIME = 20
GRAVITY = 8
FLEIGHT_TIME = 10
FLIGHT_HEIGHT = 5

# Display creation
DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, GAME_HEIGHT + FLOOR_HEIGHT))
pygame.display.set_caption('Flappy WSF')

# Import images
BACKGROUND_IMAGE = pygame.image.load("bg.png")
FLOOR = pygame.image.load("ground.png")
PIPE_BODY = pygame.image.load("pipe_body.png")
PIPE_END = pygame.image.load("pipe_end.png")
BIRD_UP = pygame.image.load("bird_wing_up.png")
BIRD_DOWN = pygame.image.load("bird_wing_down.png")


# Pipe pairs
def pipe_pair(pipe_position, top_height, bottom_height):
    """This function represents a pair of pipes."""

    # Convert arguments into int format
    pipe_position = int(pipe_position)
    top_height = int(top_height)
    bottom_height = int(bottom_height)

    # Top Pipe
    DISPLAY.blit(pygame.transform.scale(PIPE_BODY, (PIPE_WIDTH, top_height)), (pipe_position, 0))
    DISPLAY.blit(pygame.transform.scale(PIPE_END, (PIPE_WIDTH, 30)), (pipe_position, top_height - 30))

    # Bottom Pipe
    DISPLAY.blit(pygame.transform.scale(PIPE_BODY, (PIPE_WIDTH, bottom_height)), (pipe_position, GAME_HEIGHT - bottom_height))
    DISPLAY.blit(pygame.transform.scale(PIPE_END, (PIPE_WIDTH, 30)), (pipe_position, GAME_HEIGHT - bottom_height))


def floor(floor_position, top_height, bottom_height):
    """This function generates the floor."""

    # Convert arguments into int format
    floor_position = int(floor_position)
    top_height = int(top_height)
    bottom_height = int(bottom_height)

    # Display floor
    DISPLAY.blit(pygame.transform.scale(FLOOR, (WINDOW_WIDTH, top_height)), (floor_position, 0))


class Bird(pygame.sprite.Sprite):
    """Class representing the player :
    - It's position
    - it's flying capabilities
    - It's illustration"""

    def __init__(self, climb_time, up_image, down_image):
        """Player constructor"""
        self.x_position = WINDOW_WIDTH / 4
        self.y_position = GAME_HEIGHT / 2
        self.climb_time = climb_time
        self.up_image = up_image
        self.down_image = down_image
        # Shows player once generated
        self.update()

    def update(self):
        """Player position update function"""
        DISPLAY.blit(pygame.transform.scale(self.up_image, (60, 60)), (self.x_position, self.y_position))

    def gravity(self):
        """Gravity effects on player function"""
        # pygame.transform.rotate(self.up_image.convert(), 100)
        self.up_image = pygame.transform.rotate(BIRD_UP, -30)
        self.y_position += GRAVITY
        self.update()

    def fly(self):
        """Player flight function"""
        self.up_image = pygame.transform.rotate(BIRD_UP, 15)
        self.y_position -= FLIGHT_HEIGHT
        self.update()


# This timer is set to 1 ms, it is used to move the pipes
UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(UPDATE, FRAME_RATE)

# This timer is set to 10 ms, it is used to create gravity
UPDATE_BIRD = pygame.USEREVENT + 2
pygame.time.set_timer(UPDATE_BIRD, BIRD_UPDATE_TIME)


def main():
    """This function contains the events."""

    # position = WINDOW_WIDTH
    once = 0
    pause = True
    flying = 0
    pipe_position_a = WINDOW_WIDTH
    pipe_position_b = WINDOW_WIDTH + ((WINDOW_WIDTH + PIPE_WIDTH) / 2)

    player = Bird(5, BIRD_UP, BIRD_DOWN)
    
    # Event loop
    while True:
        # Game background
        if GAME_HEIGHT > WINDOW_WIDTH:
            DISPLAY.blit(pygame.transform.scale(BACKGROUND_IMAGE, (GAME_HEIGHT, GAME_HEIGHT)), (0, 0))
        else:
            DISPLAY.blit(pygame.transform.scale(BACKGROUND_IMAGE, (WINDOW_WIDTH, WINDOW_WIDTH)), (0, 0))

        DISPLAY.blit(pygame.transform.scale(FLOOR, (WINDOW_WIDTH, FLOOR_HEIGHT)), (0, GAME_HEIGHT))

        # Game events
        for event in pygame.event.get():

            # Quit game
            if event.type == QUIT:
                pygame.quit()
                quit()
            
            elif event.type == pygame.KEYDOWN:
                pause = False
                flying = FLEIGHT_TIME                

            elif pause == False:
                
                # Player generation and mouvment
                if event.type == UPDATE_BIRD:
                    if flying > 0:
                        flying -= 1
                        player.fly()
                    else:
                        player.gravity()
                    

                # Pipe generation and movement
                elif event.type == UPDATE:
                    if once == 0:
                        once = 1
                        top_height_a = random.randint(MIN_WHOLE_HEIGHT, GAME_HEIGHT - MIN_WHOLE_HEIGHT - HOLE_SIZE)
                        bottom_height_a = GAME_HEIGHT - top_height_a - HOLE_SIZE
                        top_height_b = random.randint(MIN_WHOLE_HEIGHT, GAME_HEIGHT - MIN_WHOLE_HEIGHT - HOLE_SIZE)
                        bottom_height_b = GAME_HEIGHT - top_height_b - HOLE_SIZE

                    elif pipe_position_a <= 0 - PIPE_WIDTH:
                        top_height_a = random.randint(MIN_WHOLE_HEIGHT, GAME_HEIGHT - MIN_WHOLE_HEIGHT - HOLE_SIZE)
                        bottom_height_a = GAME_HEIGHT - top_height_a - HOLE_SIZE
                        pipe_position_a = WINDOW_WIDTH

                    elif pipe_position_b <= 0 - PIPE_WIDTH:
                        top_height_b = random.randint(MIN_WHOLE_HEIGHT, GAME_HEIGHT - MIN_WHOLE_HEIGHT - HOLE_SIZE)
                        bottom_height_b = GAME_HEIGHT - top_height_b - HOLE_SIZE
                        pipe_position_b = WINDOW_WIDTH

                    # Add pipe visualls
                    pipe_pair(pipe_position_a, top_height_a, bottom_height_a)
                    pipe_pair(pipe_position_b, top_height_b, bottom_height_b)

                    # Move pipe
                    pipe_position_a -= SPEED
                    pipe_position_b -= SPEED

                    # Add collision elements

                    # collisions = []

            player.update()
            pygame.display.update()

if __name__ == '__main__':
    main()
