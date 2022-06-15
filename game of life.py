import numpy as np
import time
import pygame
import random


##color values
Color_BG=(60,60,60)
Color_Grid = (90,90,90)
#Color_Die_Next =(150,50,50) #color of cells that die the next generation  
Color_alive_next =(175,75,75) # color of cells that turn alive next generation
Color_immune = (100,160,160) #color of immune cells
Color_dead = (5,5,5)
Color_text = (50,255,50)

#_______________________________________________________________________________________________________________________________
#SIMULATION VARIABLES: Change these to tweak infection probabilities and initial conditions                                     |
ppi_chance = 0.01       #chance that each infected neighbor adds to a cell's probability of infection EACH STEP. 1 = 100%       |
infection_length = 20     #number of steps that an infection lasts, on average                                                  |
infection_dev = 1        #std. deviation in number of steps an infection lasts                                                  |
death_chance = 0.1       #chance that an infected cell dies after infection.                                                    |
immunity_strength = 0.90 #Strength of immunity, 1 means impossible to reinfect.                                                 |
immunization_chance = 0.0001    #Chance that a random uninfected cell will immunize itself (analagous to vaccine availability)  |                                                                           
#_______________________________________________________________________________________________________________________________|

def infect (row, col, return_matrix): #infects a target cell using the infection counter and updates it to the return matrix
    return_matrix[row,col] = round(random.gauss(infection_length, infection_dev)) #decides how long the infection lasts, adds to progress matrix. Gaussian distribution.
    pass

def update (screen, cells, size, cell_infprogress, c, with_progress=False, is_running=True): # rules and stuff to update
    updated_cells = np.zeros((cells.shape[0],cells.shape[1]))
    updated_infprogress = cell_infprogress
    #goes through each cell and updates the state
    for row, col in np.ndindex(cells.shape):
        alive = np.sum(np.mod(cells[row-1:row+2, col-1:col+2], 2)) - cells[row,col] % 2 # checks cells around the cell. The modulo operator makes sure immune cells aren't counted.
        if cells[row, col] == 0:
            color = Color_BG
        elif cells[row, col] == 2:
            color = Color_immune
        elif cells[row, col] == 4: #death state is 4 because making it 3 would screw up the modulo. The 'alive' counter will only count ones with odd numbers.
            color = Color_dead #Note: words alive/dead frequently interchangeable with infected/uninfected. Should fix that sometime for clarity.
        else:
            color = Color_alive_next

        if cells [row,col] == 1: #if the cell is infected do the following
            if cell_infprogress[row, col] == 0:
                if random.random() > death_chance:
                    updated_cells[row,col] = 2
                    if with_progress:
                        color = Color_immune
                else:
                    updated_cells[row,col] = 4
                    if with_progress:
                        color = Color_dead
            elif cell_infprogress[row, col] > 0: #stays infected if progress matrix still has time left
                updated_cells[row,col] = 1
                if is_running:
                    updated_infprogress[row,col]-=1
                if with_progress: 
                    color = Color_alive_next
        elif cells[row,col] == 0: # if cell is uninfected do the following
            if random.random() <= alive * ppi_chance: #higher number of active neighbors = higher chance of infection
                updated_cells[row,col] = 1
                infect(row,col,updated_infprogress) #infects cell to progress matrix
                if with_progress:
                    color= Color_alive_next
            else:
                if random.random() <= immunization_chance:
                    updated_cells[row, col] = 2
                    if with_progress:
                        color= Color_immune
        elif cells[row,col] == 2: #if cell is immune do the following
            if random.random() <= (1-immunity_strength) * alive * ppi_chance: #small chance that immunized cells can be reinfected
                updated_cells[row,col] = 1
                infect(row,col,updated_infprogress) #infects cell to progress matrix
                if with_progress:
                    color= Color_alive_next
            else:
                updated_cells[row,col] = 2
                if with_progress:
                    color= Color_immune
        else:
            updated_cells[row,col] = 4 #Dead cells stay dead. Also, deals with any weird values that might somehow pop up in the array by killing them.
            if with_progress:
                color = Color_dead
        pygame.draw.rect(screen,color,(col*size,row*size, size-1, size-1)) # makes a grid the size of a matrix
    w, h = pygame.display.get_surface().get_size()
    text_inf = pygame.font.SysFont(None, 30).render("Infected: "+str(np.count_nonzero(cells == 1)).center(6), True, Color_text) #all of this displays text counter
    text_inf_rect = text_inf.get_rect(center=(round(w*0.9), round(h*0.06)))
    screen.blit(text_inf, text_inf_rect)
    text_imm = pygame.font.SysFont(None, 30).render("Immune:   "+str(np.count_nonzero(cells == 2)).center(6), True, Color_text)
    text_imm_rect = text_imm.get_rect(center=(round(w*0.9), round(h*0.09)))
    screen.blit(text_inf, text_inf_rect)
    text_dead = pygame.font.SysFont(None, 30).render("Dead:     "+str(np.count_nonzero(cells == 4)).center(6), True, Color_text)
    text_dead_rect = text_dead.get_rect(center=(round(w*0.9), round(h*0.12)))
    text_c = pygame.font.SysFont(None, 30).render("Step:     "+str(c).center(6), True, Color_text) #all of this displays text counter
    text_c_rect = text_c.get_rect(center=(round(w*0.1), round(h*0.94)))
    screen.blit(text_c, text_c_rect)
    screen.blit(text_inf, text_inf_rect)
    screen.blit(text_imm, text_imm_rect)
    screen.blit(text_dead, text_dead_rect)
    return updated_cells,updated_infprogress


def main ():
    random.seed()
    pygame.init() # initiates the visual part
    height= 1000 # some
    width = 800 # variables to determine size of our field
    size= 10
    h= int(height/size)
    w= int(width/size)
    screen = pygame.display.set_mode((height,width))

    cells = np.zeros((w,h))
    cell_infprogress = np.zeros((w,h)) #adds new array to track cell infection progress
    c=0 #counter to keep track of at what step we are
    screen.fill(Color_Grid)
    update(screen,cells,size, cell_infprogress, c)
    running = False
  
    pygame.display.update()
    #function to make a matrix with specific numbers of cells alive at random locations
    def start_with_x (num_inf,num_imm = 0):
        REPLACE_COUNT_INF = int(num_inf)
        REPLACE_COUNT_IMM = int(num_imm)
        REPLACE_WITH_INF = 1
        REPLACE_WITH_IMM = 2
        cells = np.zeros((w,h))
        cell_infprogress = np.zeros((w,h))
        cells.flat[np.random.choice((h*w), REPLACE_COUNT_INF, replace=False)] = REPLACE_WITH_INF
        if num_imm > 0:
            cells.flat[np.random.choice((h*w), REPLACE_COUNT_IMM, replace=False)] = REPLACE_WITH_IMM
        for row, col in np.ndindex(cells.shape):
            if cells[row,col] == 1:
                infect(row,col,cell_infprogress)
        return cells,cell_infprogress
    
    # the following allows us only let the game go on for a specific amount of time
    print ("please enter the number of timesteps")
    timesteps= int(input())
    x=timesteps
    running = False
    cells = np.zeros((w,h))                 #This is clearly redundant, but for some reason it prevents the program from trying to run while you assign cells.
    cell_infprogress = np.zeros((w,h))
    
    
    #game initiating loop
    while True:
        
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: #makes us able to close the game
                pygame.quit()
                return
           #pauses when pressing space, continues when pressing it again
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update (screen, cells, size, cell_infprogress, c)
                    pygame.display.update()
                    if running == True:
                        print("Beginning with " +str(np.count_nonzero(cells == 1))+" infected cells, "+str(np.count_nonzero(cells == 2))+" immune cells, and "+str(np.count_nonzero(cells == 4))+" dead cells.")
                        print ("running.")
                    elif running == False:
                        print ("paused.")
                elif event.key == pygame.K_ESCAPE: #resets matrix and fills random spots with one, when pressing esc
                    running = False
                    x = timesteps
                    c = 0
                    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                        cells = np.random.choice([2,1,0], w*h, p=[0.05, 0.15, 0.8]).reshape(w, h)#when pressing shift, 15% chance for cell to be active and 5% chance for immunized
                    else:
                        cells = np.random.choice([1,0], w*h, p=[0.15, 1-0.15]).reshape(w, h)# chance for a field to be alive is 15%
                    for row, col in np.ndindex(cells.shape):
                        if cells[row,col] == 1:
                            infect(row,col,cell_infprogress)
                    update (screen, cells, size, cell_infprogress, c)
                    pygame.display.update()
                    print("reset random start")
                elif event.key == pygame.K_r: #resets whole matrix to 0(dead) when pressing R
                    running = False
                    c=0
                    x= timesteps
                    cells = np.zeros((w,h))
                    cell_infprogress = np.zeros((w,h))
                    update(screen, cells, size, cell_infprogress)
                    pygame.display.update()
                    print("cleared field")
                if event.key == pygame.K_w:#random start with 500 cells alive
                    running = False
                    if pygame.key.get_pressed()[pygame.K_LSHIFT]: #pressing shift will do this but also randomly immunize 500 cells
                        cells, cell_infprogress = start_with_x(500,500)
                    else:
                        cells, cell_infprogress = start_with_x(500)
                    update (screen, cells, size, cell_infprogress, c)
                    pygame.display.update()  
                    print("random start with x")


               #manual cell assignment 
            if pygame.mouse.get_pressed()[0]:
                keys = pygame.key.get_pressed()
                pos = pygame.mouse.get_pos()
                if keys[pygame.K_LSHIFT]:   #Shift-left-click makes a cell immune
                    cells [pos[1]//size,pos[0]//size]=2
                    cell_infprogress[pos[1]//size,pos[0]//size]=0
                    update (screen,cells,size,cell_infprogress, c, False, False)
                    pygame.display.update()
                    
                elif keys[pygame.K_LCTRL]:     #Control-left-click kills a cell
                    cells [pos[1]//size,pos[0]//size]=4
                    cell_infprogress[pos[1]//size,pos[0]//size]=0
                    update (screen,cells,size,cell_infprogress, c, False, False)
                    pygame.display.update()
                else:   #Regular left click infects a cell
                    cells [pos[1]//size,pos[0]//size]=1
                    infect(pos[1]//size,pos[0]//size,cell_infprogress)
                    update (screen,cells,size,cell_infprogress, c, False, False)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[2]:   #Right click returns a cell to normal. 
                pos = pygame.mouse.get_pos()
                cells [pos[1]//size,pos[0]//size]=0
                cell_infprogress[pos[1]//size,pos[0]//size]=0
                update (screen,cells,size,cell_infprogress, c, False, False)
                pygame.display.update()

        if np.count_nonzero(cells == 1) ==0 and c > 1:
            x = 0
            print("There are no more infected cells.")
        screen.fill(Color_Grid)
        if running and x>0:
            x -= 1
            c+=1 #counter to keep track of at what step we are
            cells, cell_infprogress = update(screen, cells,size, cell_infprogress, c, with_progress=True)
            pygame.display.update()
        #once all timesteps done it stops so you can look at the end
        elif x == 0:
            running = False
            update (screen, cells, size, cell_infprogress, c, with_progress=True)
            pygame.display.update()
            if c == timesteps: 
                print(" total timesteps done:", c)
            elif c > timesteps:
                print ("another "+ str(timesteps) + " timesteps done")
                print(" total timesteps done:", c)
            print("stopped.")
            #loop to "stop" the thing to look at current state after time steps
            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = not running
                        update (screen, cells, size, cell_infprogress,c)
                        pygame.display.update()
                        x = timesteps
                        if running == True:
                            print ("running.")
                        elif running == False:
                            print ("paused.")
                            break
                    elif event.key == pygame.K_r:
                        running = False
                        c=0
                        x= timesteps
                        cells = np.zeros((w,h))
                        cell_infprogress = np.zeros((w,h))
                        update (screen, cells, size, cell_infprogress,c)
                        pygame.display.update()
                        print ("cleared field")
                        break
            continue
        
                    
            

        time.sleep(0.05)
       
if __name__== '__main__':
    main()
