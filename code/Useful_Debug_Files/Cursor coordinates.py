import os
import pygame

# Initialize Pygame and create the screen
# Initialize pygame library and position the screen

pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "1920, 360"


# Set some initial variables

screen_width = 1250
screen_height = 400

# Create the screen and set the caption
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Cursor Coordinates")

# Create a font object to use for displaying the coordinates
font = pygame.font.Font(None, 100)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Clear the screen
    screen.fill((255, 255, 255))
    # Get the cursor coordinates
    x, y = pygame.mouse.get_pos()
    # Create the text surface with the coordinates
    text = font.render(f"Cursor: ({x}, {y})", True, (0, 0, 0))
    # Blit the text surface on the screen
    screen.blit(text, (screen_width/2, screen_height/2))
    # Update the display
    pygame.display.update()

pygame.quit()
