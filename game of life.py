import numpy as np
import time
import pygame
##color values
Color_BG=(10,10,10)
Color_Grid = (40,40,40)
Color_Die_Next =(170,170,170)
Color_alive_next =(255,255,255)

def update (screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0],cells.shape[1]))
    #goes through each cell and updates the state
    for row, col in np.ndindex(cells.shape):
           alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells [row,col]
           color = Color_BG if cells[row, col] == 0 else Color_alive_next

           if cells [row,col] == 1:
               if alive < 2 or alive > 3:
                   if with_progress:
                       color = Color_Die_Next
               elif 2<= alive or alive<=3:
                    updated_cells[row,col] = 1
                    if with_progress: 
                        color = Color_alive_next
           else:
               if alive == 3:
                   updated_cells[row,col] = 1
                   if with_progress:
                       color= Color_alive_next
           pygame.draw.rect(screen,color,(col*size,row*size, size-1, size-1))
    return updated_cells

def main ():
    pygame.init()
    screen = pygame.display.set_mode((1000,800))

    #cells = np.zeros((80,100))
    cells = np.random.choice([1,0], 80*100, p=[0.15, 1-0.15]).reshape(80, 100)
    screen.fill(Color_Grid)
    update(screen,cells,10)

    pygame.display.flip()
    pygame.display.update()

    running = False
    #loop that runs all the time updating it without a pause
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update (screen, cells, 10)
                    pygame.display.update()

               #when you click on a cell turns it into the opposite state
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if cells [pos[1]//10,pos[0]//10]==1:
                    cells [pos[1]//10,pos[0]//10]=0
                    update (screen,cells,10)
                    pygame.display.update()
                else: 
                    cells [pos[1]//10,pos[0]//10]=1
                    update (screen,cells,10)
                    pygame.display.update()
               #resets matrix and fills random spots with one, when pressing esc 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    cells = np.random.choice([1,0], 80*100, p=[0.15, 1-0.15]).reshape(80, 100)
                    update (screen, cells, 10)
                    pygame.display.update()
                #resets whole matrix to 0 when pressing R
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_R:
                    running = False
                    cells = cells = np.zeros((80,100))
                    update (screen, cells, 10)
                    pygame.display.update()
        screen.fill(Color_Grid)
        if running:
            cells= update (screen, cells,10, with_progress=True)
            pygame.display.update()

        time.sleep(0.05)
if __name__== '__main__':
    main()
