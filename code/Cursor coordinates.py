import os
import pygame

# Initialize Pygame and create the screen
pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "0,365"
screen = pygame.display.set_mode((1250, 400))
pygame.display.set_caption("Cursor Coordinates")

# Create a font object to use for displaying the coordinates
font = pygame.font.Font(None, 30)

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
    screen.blit(text, (10, 10))
    # Update the display
    pygame.display.update()

pygame.quit()
