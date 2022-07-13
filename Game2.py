import numpy as np
from numpy.random import default_rng
from Game1 import Game as Game1
from typing import Tuple

class Game(Game1):
    rng = default_rng()

    model: np.ndarray
    def __init__(self):
        super().__init__()

    def generateModel(self, option: int) -> np.ndarray:
        if option == "random":
            """
            Generating initial randomly placed living cells grid and
            incrementing Game.livingCells value with the # of created
            living cells.
            """

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
        else:
            """
            Creates a full grid of 0, sets the coordinates of the
            initial living cells based on user's option, and returns that grid.
            """
            return self.generateInitialStateCoords(option)

    def generateInitialStateCoords(self, option: int):
        # create gridSize x gridSize grid of all 0's
        grid = np.full((self.gridSize, self.gridSize), 0)

        # get the center coordinate of the grid
        center = self.getCenterCoord()

        # set cell coordinates to be alive based on option
        if option == "blip":
            #               X coord     Y coord
            grid.itemset( (center - 1, center), 255)
            grid.itemset( (center,     center), 255)
            grid.itemset( (center + 1, center), 255)
            self.livingCells += 3
        elif option == "glider":
            grid.itemset( (center + 1, center - 1), 255)
            grid.itemset( (center - 1, center),     255)
            grid.itemset( (center + 1, center),     255)
            grid.itemset( (center,     center + 1), 255)
            grid.itemset( (center + 1, center + 1), 255)
            self.livingCells += 5
        elif option == "pentomino":
            grid.itemset( (center,     center - 1), 255)
            grid.itemset( (center + 1, center - 1), 255)
            grid.itemset( (center - 1, center),     255)
            grid.itemset( (center,     center),     255)
            grid.itemset( (center, center + 1),     255)
            self.livingCells += 5
        
        return grid


    #def assnm3_ncheck(emptyArr, orig);

        #emptyArr[:, :] = 0

        #Diag
        #emptyArr[1:, :-1] += orig[:-1, 1:]
        #emptyArr[1:, 1:] += orig[:-1, :-1] 
        #emptyArr[:-1, :-1] += orig[1:, 1:] 
        #emptyArr[:-1, 1:] += orig[1:, :-1] 
        #emptyArr[-1, :] += orig[0, :] 
        #emptyArr[0, :] += orig[-1, :] 
        #emptyArr[:, -1] += orig[:, 0] 
        #emptyArr[:, 0] += orig[:, -1] 

        #vertical/horizontal
        #emptyArr[:-1, :] += orig[1:, :]
        #emptyArr[1:, :] += orig[:-1, :] 
        #emptyArr[:, :-1] += orig[:, 1:] 
        #emptyArr[:, 1:] += orig[:, :-1] 

        #rules
        #x = (orig == 255) & ((emptyArr == 510) | (emptyArr == 765))
        #y = (orig = 0) & (emptyArr == 765)
        #orig = x + y
        

    def getNeighborCount(self, coord: Tuple[int, int]) -> int:
        count = 0

        xRange = ((coord[0] - 1), (coord[0] + 2))
        yRange = ((coord[1] - 1), (coord[1] + 2))

        x = xRange[0]
        y = yRange[0]



        # loop through a 3x3 portion of the matrix
        for y in range(yRange[0], yRange[1]):
            for x in range(xRange[0], xRange[1]):
                if (
                    # x position does not exist on board
                    x < 0
                    or x > (self.gridSize - 1)
                    # y position does not exist on board
                    or y < 0
                    or y > (self.gridSize - 1)
                    # if the current (x, y) is the given coordinate
                    # we want to count the coord's neighbors, not itself,
                    # so we continue to the next iteration of the loop
                    or (x, y) == coord):
                    continue
                elif self.model[y][x] == 255: # a cell within the neighboring area is alive
                    count += 1


        return count
