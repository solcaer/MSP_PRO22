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
    height= 1500
    width = 1200
    size= 15
    h= int(height/size)
    w= int(width/size)
    screen = pygame.display.set_mode((height,width))

    cells = np.zeros((w,h))
    #cells = np.random.choice([1,0], h*w, p=[0.15, 1-0.15]).reshape(w, h)
    screen.fill(Color_Grid)
    update(screen,cells,size)
    running = False
  
    pygame.display.update()
    #funtion to start with specific numbers of cells alive
    def start_with_x (x):
        REPLACE_COUNT = int(x)
        REPLACE_WITH = 1
        cells = np.zeros((w,h))
        cells.flat[np.random.choice((h*w), REPLACE_COUNT, replace=False)] = REPLACE_WITH
        return cells
    
    #loop that runs all the time updating it without a pause
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
           #pauses when pressing space, continues when pressing it again
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update (screen, cells, size)
                    pygame.display.update()
                    if running == True:
                        print ("running.")
                    elif running == False:
                        print ("paused.")


               #when you click on a cell turns it into the opposite state
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if cells [pos[1]//size,pos[0]//size]==1:
                    cells [pos[1]//size,pos[0]//size]=0
                    update (screen,cells,size)
                    pygame.display.update()
                    
                else: 
                    cells [pos[1]//size,pos[0]//size]=1
                    update (screen,cells,size)
                    pygame.display.update()
               #resets matrix and fills random spots with one, when pressing esc 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    cells = np.random.choice([1,0], w*h, p=[0.15, 1-0.15]).reshape(w, h)
                    update (screen, cells, size)
                    pygame.display.update()
                    print("reset random start")
                    #resets whole matrix to 0 when pressing R
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        running = False
                        cells = np.zeros((w,h))
                        update (screen, cells, size)
                        pygame.display.update()
                        print ("cleared field")
                        #random start with 500 cells alive
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            running = False
                            cells= start_with_x(500)
                            update (screen, cells, size)
                            pygame.display.update()
                            
                            print("random start with x")
        screen.fill(Color_Grid)
        if running:
            cells= update (screen, cells,size, with_progress=True)
            pygame.display.update()

        time.sleep(0.05)
if __name__== '__main__':
    main()
