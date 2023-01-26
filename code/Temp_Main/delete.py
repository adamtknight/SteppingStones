    pygame.event.pump()  # Process any events that have occurred
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            asyncio.get_event_loop().stop()
    # clear the screen
    screen.fill((255, 255, 255))
    color = (255, 0 ,205)
    #add new stones
    if(prev_stone.x > step_length):
        if side == "left" : side = "right"
        else: side = "left"
        stones.append(Stone(1, side, stone_counter))
        stone_counter+=1
        prev_stone = stones[len(stones) - 1]
    # get time since last frame in seconds
    time_since_last_frame = clock.tick() / 1000 
    # calculate distance to move
    distance_to_move = vel * time_since_last_frame 
    # for marker in markers:
    #     if marker.x > 250 and marker.x < 500 and marker.y > -550 and marker.y < 1500:
    #         color=(255,0,0)
    #         save_marker = marker.y
    #         break
    #     else: save_marker = 0
    # update the position of stones
    for stone in stones:
        if stone.x < screen_width and stone.x > 0:
            stone.x = stone.x + distance_to_move
            stone.draw(screen, 0x00ffff)
            # Save the stone's pixel coordinates and the current frame number to a CSV file
            # with open("stones.csv", "a", newline="") as f:
            #     with open("stones.csv", "a", newline="") as f:
            #         writer = csv.DictWriter(f, fieldnames=["Frame Number", "Stone ID", "X", "Y", "Side", "Marker Loc"])
            #         height = right_stone_y if stone.side == "right" else left_stone_y
            #         writer.writerow({"Frame Number": frame_number, "Stone ID": stone.id, "X": stone.x, "Y": height, "Side": stone.side, "Marker Loc": save_marker})
            
        else:
            del_stone = stones.pop(stones.index(stone))
            del del_stone
    for stone in stones:
        print(stone.id)   
    
    # display the frame number
    font = pygame.font.Font(None, 30)
    # text = font.render("Frame number: {}".format(frame_number), True, (0, 0, 0))
    screen.blit(text, (10, 10))

    
    # update the display
    pygame.display.flip()
    #await asyncio.sleep(0.01)
    # if frame_number == COLLECTION_TIME * FREQUENCY:
    #     pygame.quit()
    #     running = False