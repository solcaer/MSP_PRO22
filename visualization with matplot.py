
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
import numpy as np
from numpy import newaxis


def update (cells):
    updated_cells = np.zeros((cells.shape[0],cells.shape[1]))
    #goes through each cell and updates the state
    for row, col in np.ndindex(cells.shape):
           alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells [row,col]
           

           if cells [row,col] == 1:
               if alive < 2 or alive > 3:
                 updated_cells [row,col] == 0
               elif 2<= alive or alive<=3:
                    updated_cells[row,col] = 1
                    
           else:
               if alive == 3:
                   updated_cells[row,col] = 1
                   
           
    return updated_cells

#size:
w=50
h=50
p=0.5
cells = np.random.choice([1,0], h*w, p=[p, 1-p]).reshape(w, h)

def count(array):

    infected = np.count_nonzero((array == 2) | (array == 3)) # if multiple stats
    recovered = np.count_nonzero(array == 1)
    susceptible = (array.shape[0] * array.shape[1])- (infected+recovered)

    return list(infected,recovered, susceptible)

def get_graphable_data():
    data = []
    for i in arraylist:
        count (i)
        data = np.append(data, count (i))
    return data

print ('enter number of timesteps')
timesteps =28 # int(input())
arraylist = arraylist = cells[:, :,newaxis]
n_1= cells
c=0

while timesteps > 0:
    n_1= update (n_1)
    d= n_1[:,:,newaxis]
    arraylist = np.concatenate((arraylist,d),2)
    timesteps -=1
    c+=1

print (arraylist.shape)

'''for i in range (c):
    print ("Array  {x}:", i)
    print (arraylist[i])
'''
fig, ax = pyplot.subplots()

def update(frames):
    
    pyplot.imshow(arraylist [:,:,frames])
    

anim = FuncAnimation(fig, update, frames=15, interval=50)

pyplot.show()
'''
n= arraylist [c-1]
for i in arraylist:
    pyplot.matshow(i)
    pyplot.pause(0.1)'''

