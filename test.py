import os
import math
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
import matplotlib as mpl
import time
import datetime
import argparse
import numpy as np




list1 = [2, 1.5, 1, .5]
list2 = [1, 2, 3, 4]


plt.xlabel("Board Size -- 1 = 100")
plt.ylabel("Steps per ms")
plt.bar(list2, list1)
plt.show()





emptyArr = np.zeros((self.gridSize, self.gridSize), dtype = int)

            # grid of randomly placed 0's and 1's
            randomGrid = self.rng.choice(2, (self.gridSize, self.gridSize))

            # grid with every value of 255
            full255Grid = np.full((self.gridSize, self.gridSize), 255)

            # essentially a mask to create a grid of randomly placed values
            # of 0 and 255
            orig = randomGrid * full255Grid

            # count living cells from initial frame
            self.livingCells += np.count_nonzero(orig == 255)

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

            return orig