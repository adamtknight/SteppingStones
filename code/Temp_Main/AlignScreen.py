import pygame
import os
import sys
import SteppingStonesFullControlMain as m

# Initialize pygame library and center the screen
pygame.init()
os.environ["SDL_VIDEO_WINDOW_POS"] = "0,365"

# Create the screen and set the caption
screen = pygame.display.set_mode((m.screen_width, m.screen_height))
pygame.display.set_caption("Stepping Stones")
# clear the screen
screen.fill((255, 255, 255))
# Draw the 4 circles at the corners of the screen
pygame.draw.circle(screen, (255, 0, 0), (m.TL_x, m.TL_y), 1)
pygame.draw.circle(screen, (255, 0, 0), (m.TR_x, m.TR_y), 1)
pygame.draw.circle(screen, (255, 0, 0), (m.BL_x, m.BL_y), 1)
pygame.draw.circle(screen, (255, 0, 0), (m.BR_x, m.BR_y), 1)

# Draw the text message asking the user to press enter to start
font = pygame.font.Font(None, 30)
text = font.render("Ensure all red circles are aligned with marked bolts! Press enter to start...", True, (0, 0, 0))
text_rect = text.get_rect()
text_rect.center = (m.screen_width // 2, m.screen_height // 2)
screen.blit(text, text_rect)    
    
