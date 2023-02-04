import pygame
import sys

def run_other_file():
    # code to run the other Python file goes here
    pass

# initialize Pygame
pygame.init()

# set the window size
window_size = (400, 400)

# create the window
screen = pygame.display.set_mode(window_size)

# set the title of the window
pygame.display.set_caption("Pygame Parameters")

# define the colors
black = (0, 0, 0)
white = (255, 255, 255)

# set the default values for the parameters
TREADMILL_SPEED_RIGHT = 1.25
TREADMILL_SPEED_LEFT = 1.25
STEP_LENGTH_RIGHT = 0.67
STEP_LENGTH_LEFT = 0.67
STEP_WIDTH = 0.3
STONE_WIDTH = 0.3
STONE_HEIGHT = 0.15
COLLECTION_TIME = 5
FREQUENCY = 100
RIGHT_SHIFT_BACK_DIST = 0.1
RIGHT_SHIFT_FORWARD_DIST = 0.1
RIGHT_SHIFT_RIGHT_DIST = 0.15
RIGHT_SHIFT_LEFT_DIST = 0.15
LEFT_SHIFT_BACK_DIST = 0.1
LEFT_SHIFT_FORWARD_DIST = 0.1
LEFT_SHIFT_RIGHT_DIST = 0.15
LEFT_SHIFT_LEFT_DIST = 0.15
FILEPATH_TO_STEPPATH = "C:/Users/Neurolab/Documents/Projects/Knight/SteppingStones/code/Temp_Main/TEST"

# create the font for the text
font = pygame.font.Font(None, 30)

# flag to indicate if the program should run
running = True

# main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # clear the screen
    screen.fill(black)

    # display the text for each parameter
    text = font.render("TREADMILL_SPEED_RIGHT: " + str(TREADMILL_SPEED_RIGHT), True, white)
    screen.blit(text, (50, 50))
    text = font.render("TREADMILL_SPEED_LEFT: " + str(TREADMILL_SPEED_LEFT), True, white)
    screen.blit(text, (50, 100))
    text = font.render("STEP_LENGTH_RIGHT: " + str(STEP_LENGTH_RIGHT), True, white)
    screen.blit(text, (50, 150))
    text = font.render("STEP_LENGTH_LEFT: " + str(STEP_LENGTH_LEFT), True, white)
    screen.blit(text, (50, 200))
    text = font.render("STEP_WIDTH: " + str(STEP_WIDTH), True, white)
    screen.blit(text, (50, 200))
    text = font.render("STONE_WIDTH: " + str(STONE_WIDTH), True, white)
    screen.blit(text, (50, 250))
    text = font.render("STONE_HEIGHT: " + str(STONE_HEIGHT), True, white)
    screen.blit(text, (50, 300))
    text = font.render("COLLECTION_TIME: " + str(COLLECTION_TIME), True, white)
    screen.blit(text, (50, 350))
    text = font.render("FREQUENCY: " + str(FREQUENCY), True, white)
    screen.blit(text, (200, 50))
    text = font.render("RIGHT_SHIFT_BACK_DIST: " + str(RIGHT_SHIFT_BACK_DIST), True, white)
    screen.blit(text, (200, 100))
    text = font.render("RIGHT_SHIFT_FORWARD_DIST: " + str(RIGHT_SHIFT_FORWARD_DIST), True, white)
    screen.blit(text, (200, 150))
    text = font.render("RIGHT_SHIFT_RIGHT_DIST: " + str(RIGHT_SHIFT_RIGHT_DIST), True, white)
    screen.blit(text, (200, 200))
    text = font.render("RIGHT_SHIFT_LEFT_DIST: " + str(RIGHT_SHIFT_LEFT_DIST), True, white)
    screen.blit(text, (200, 250))
    text = font.render("LEFT_SHIFT_BACK_DIST: " + str(LEFT_SHIFT_BACK_DIST), True, white)
    screen.blit(text, (200, 300))
    text = font.render("LEFT_SHIFT_FORWARD_DIST: " + str(LEFT_SHIFT_FORWARD_DIST), True, white)
    screen.blit(text, (200, 350))
    text = font.render("LEFT_SHIFT_RIGHT_DIST: " + str(LEFT_SHIFT_RIGHT_DIST), True, white)
    screen.blit(text, (350, 50))
    text = font.render("LEFT_SHIFT_LEFT_DIST: " + str(LEFT_SHIFT_LEFT_DIST), True, white)
    screen.blit(text, (350, 100))
    text = font.render("FILEPATH_TO_STEPPATH: " + str(FILEPATH_TO_STEPPATH), True, white)
    screen.blit(text, (350, 150))
    # create the "GO" button
    go_button = pygame.Rect(150, 300, 100, 50)
    pygame.draw.rect(screen, white, go_button)
    text = font.render("GO", True, black)
    screen.blit(text, (185, 320))

    # check if the "GO" button was clicked
    mouse_pos = pygame.mouse.get_pos()
    if go_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
        run_other_file()
    # update the display
    pygame.display.update()
    

