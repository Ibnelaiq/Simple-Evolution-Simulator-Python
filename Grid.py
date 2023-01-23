import pygame
import numpy as np

def createGrid(_x,_y,grid_square_size,screen):
    # Square size of grid rect

    array = []
    for x in range(_x): 
        
        grid_y = np.zeros(int(_y))

        array.append(grid_y)

        for y in range(_y): 
            rect = pygame.Rect(x*grid_square_size,y*grid_square_size,grid_square_size,grid_square_size)
            pygame.draw.rect(screen, (200, 204, 201), rect,1)


    pygame.display.update()
    
    return array



