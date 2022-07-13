import numpy as np
from numpy.random import default_rng
#from Game1 import Game as Game1
from typing import Tuple            
            

rng = np.random.default_rng()

#model: np.ndarray

emptyArr = np.zeros((10,10), dtype = int)

# grid of randomly placed 0's and 1's
randomGrid = rng.choice(2, (10, 10))

# grid with every value of 255
full255Grid = np.full((10, 10), 255)

# essentially a mask to create a grid of randomly placed values
# of 0 and 255
orig = randomGrid * full255Grid

# count living cells from initial frame
#self.livingCells += np.count_nonzero(grid == 255)
            
#####print(orig)

emptyArr[:, :] = 0

#Diag
emptyArr[1:, :-1] += orig[:-1, 1:]
emptyArr[1:, 1:] += orig[:-1, :-1] 
emptyArr[:-1, :-1] += orig[1:, 1:] 
emptyArr[:-1, 1:] += orig[1:, :-1] 
emptyArr[-1, :] += orig[0, :] 
emptyArr[0, :] += orig[-1, :] 
emptyArr[:, -1] += orig[:, 0] 
emptyArr[:, 0] += orig[:, -1] 

#vertical/horizontal
emptyArr[:-1, :] += orig[1:, :]
emptyArr[1:, :] += orig[:-1, :] 
emptyArr[:, :-1] += orig[:, 1:] 
emptyArr[:, 1:] += orig[:, :-1] 

#rules
x = (orig == 255) & ((emptyArr == 510) | (emptyArr == 765))
y = (orig == 0) & (emptyArr == 765)
orig = x + y  
#####print(orig) 