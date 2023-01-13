import pygame
import asyncio
import main

async def TestDisplay():
    # Initialize Pygame
    pygame.init()

    # Create a window with a specific size
    screen = pygame.display.set_mode((800, 600))

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Clear the screen
        screen.fill((255, 255, 255))
        #update FrameNumber variable
        FrameNumber = "FrameNumber : " +str(main.get_frame_number())
        # Update the screen
        pygame.display.update()
        pygame.event.pump()
        await asyncio.sleep(0)
    # Quit Pygame
    pygame.quit()