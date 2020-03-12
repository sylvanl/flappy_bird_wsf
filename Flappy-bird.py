"""This is an independant python game created specially for the Web School Factory students to have fun with."""
import random
import pygame
import os
from pygame.locals import *
pygame.init()

# Window size
GAME_HEIGHT: int = 600
FLOOR_HEIGHT: int = 100
WINDOW_WIDTH: int = 600

# Settings
FRAME_RATE: int = 60
PIPE_WIDTH: int = 60
MIN_WHOLE_HEIGHT: int = 100
HOLE_SIZE: int = 120
SPEED: int = 2
GRAVITY: int = 2
FLEIGHT_TIME: int = 20
FLIGHT_HEIGHT: int = 2
WHITE = (255, 255, 255)
FONT = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 60)
SMALL_FONT = pygame.font.SysFont('sitkasmallsitkatextboldsitkasubheadingboldsitkaheadingboldsitkadisplayboldsitkabannerbold', 40)

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
        self.x_position: int = WINDOW_WIDTH / 4
        self.y_position: int = GAME_HEIGHT / 2
        self.climb_time: int = climb_time
        self.up_image = up_image
        self.down_image = down_image
        # Shows player once generated
        self.update()

    def update(self):
        """Player position update function"""
        # Update visual
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
    
    def x_position(self):
        """Testing"""
        return self.x_position

    def y_position(self):
        """Testing"""
        return self.y_position


# This timer is set to 1 ms, it is used to move the pipes
UPDATE = pygame.USEREVENT+1
pygame.time.set_timer(UPDATE, FRAME_RATE)
# clock = pygame.time.Clock()



def main():
    """This function contains the events."""

    once: bool = True
    pause: bool = True
    flying: int = 0
    pipe_position_a: int = WINDOW_WIDTH
    pipe_position_b: int = WINDOW_WIDTH + ((WINDOW_WIDTH + PIPE_WIDTH) / 2)
    player = Bird(5, BIRD_UP, BIRD_DOWN)
    score = 0
    high_score = 0

    # Event loop
    while True:

        # Game background
        if GAME_HEIGHT > WINDOW_WIDTH:
            DISPLAY.blit(pygame.transform.scale(BACKGROUND_IMAGE, (GAME_HEIGHT, GAME_HEIGHT)), (0, 0))
        else:
            DISPLAY.blit(pygame.transform.scale(BACKGROUND_IMAGE, (WINDOW_WIDTH, WINDOW_WIDTH)), (0, 0))

        DISPLAY.blit(pygame.transform.scale(FLOOR, (WINDOW_WIDTH, FLOOR_HEIGHT)), (0, GAME_HEIGHT))
        player_collision = pygame.Rect(0, 0, 4, 4)


        # Screen update
        if pause == False:
                
            # Pipe generation and movement
            if once == True:
                once = False
                score = 0
                top_height_a: int = random.randint(MIN_WHOLE_HEIGHT, GAME_HEIGHT - MIN_WHOLE_HEIGHT - HOLE_SIZE)
                bottom_height_a: int = GAME_HEIGHT - top_height_a - HOLE_SIZE
                top_height_b: int = random.randint(MIN_WHOLE_HEIGHT, GAME_HEIGHT - MIN_WHOLE_HEIGHT - HOLE_SIZE)
                bottom_height_b: int = GAME_HEIGHT - top_height_b - HOLE_SIZE
                bottom_pipe_y_position_a: int = GAME_HEIGHT - bottom_height_a
                bottom_pipe_y_position_b: int = GAME_HEIGHT - bottom_height_b

            elif pipe_position_a <= 0 - PIPE_WIDTH:
                top_height_a: int = random.randint(MIN_WHOLE_HEIGHT, GAME_HEIGHT - MIN_WHOLE_HEIGHT - HOLE_SIZE)
                bottom_height_a: int = GAME_HEIGHT - top_height_a - HOLE_SIZE
                pipe_position_a: int = WINDOW_WIDTH
                bottom_pipe_y_position_a: int = GAME_HEIGHT - bottom_height_a

            elif pipe_position_b <= 0 - PIPE_WIDTH:
                top_height_b: int = random.randint(MIN_WHOLE_HEIGHT, GAME_HEIGHT - MIN_WHOLE_HEIGHT - HOLE_SIZE)
                bottom_height_b: int = GAME_HEIGHT - top_height_b - HOLE_SIZE
                pipe_position_b: int = WINDOW_WIDTH
                bottom_pipe_y_position_b: int = GAME_HEIGHT - bottom_height_b

            # Player generation and mouvment
            if flying > 0:
                flying -= 1
                player.fly()

            else:
                player.gravity()

            # Add pipe visualls
            pipe_pair(pipe_position_a, top_height_a, bottom_height_a)
            pipe_pair(pipe_position_b, top_height_b, bottom_height_b)

            # Move pipe
            pipe_position_a -= SPEED
            pipe_position_b -= SPEED

            # Add collision elements
            floor_hitbox = pygame.Rect(0, GAME_HEIGHT, WINDOW_WIDTH, FLOOR_HEIGHT)
            top_pipe_a = pygame.Rect(pipe_position_a, 0, PIPE_WIDTH, top_height_a)
            bottom_pipe_a = pygame.Rect(pipe_position_a, bottom_pipe_y_position_a, PIPE_WIDTH, bottom_height_a)
            top_pipe_b = pygame.Rect(pipe_position_b, 0, PIPE_WIDTH, top_height_b)
            bottom_pipe_b = pygame.Rect(pipe_position_b, bottom_pipe_y_position_b, PIPE_WIDTH, bottom_height_b)
            collisions = [floor_hitbox, top_pipe_a, bottom_pipe_a, top_pipe_b, bottom_pipe_b]
            player_collision = pygame.Rect(player.x_position + 15, player.y_position + 15, 30, 30)

            # Debug (show hitboxes)
            # pygame.draw.rect(DISPLAY, (255,0,255), floor_hitbox)
            # pygame.draw.rect(DISPLAY, (255,0,255), top_pipe_a)
            # pygame.draw.rect(DISPLAY, (255,0,255), bottom_pipe_a)
            # pygame.draw.rect(DISPLAY, (255,0,255), top_pipe_b)
            # pygame.draw.rect(DISPLAY, (255,0,255), bottom_pipe_b)
            # pygame.draw.rect(DISPLAY, (255,0,255), player_collision)  

            # Collision and reset
            if player_collision.collidelist(collisions) != -1:
                pause = True
                once = True
                pipe_position_a: int = WINDOW_WIDTH
                pipe_position_b: int = WINDOW_WIDTH + ((WINDOW_WIDTH + PIPE_WIDTH) / 2)
                player = Bird(5, BIRD_UP, BIRD_DOWN)
            
            # Scoring counter
            if player.x_position == pipe_position_a or player.x_position == pipe_position_b:
                score += 1
                print(score)

                if score > high_score:
                    high_score = score

            display_score = FONT.render(str(score), False, WHITE)
            DISPLAY.blit(display_score, (WINDOW_WIDTH / 2 - 20, 20))

        else:
            display_game_over = FONT.render("GAME OVER", False, WHITE)
            DISPLAY.blit(display_game_over, (WINDOW_WIDTH / 2 - 200, 60))   
            display_score = SMALL_FONT.render("Score : " + str(score), False, WHITE)
            DISPLAY.blit(display_score, (WINDOW_WIDTH / 2 - 100, 130))
            display_score = SMALL_FONT.render("High score : " + str(high_score), False, WHITE)
            DISPLAY.blit(display_score, (WINDOW_WIDTH / 2 - 160, 180))

        # Game events
        for event in pygame.event.get():

            # Quit game
            if event.type == QUIT:
                pygame.quit()
                quit()
            
            elif event.type == pygame.KEYDOWN:
                if pause == True:
                    pause = False
                else:
                    flying = FLEIGHT_TIME

            player.update()
            pygame.display.update()


if __name__ == '__main__':
    main()
