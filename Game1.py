## Nick Persinger and Riley Price-Welte

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
from numpy.random import default_rng




class Game:
    model = []
    frames = 0 
    livingCells = 0
    deadCells = 0
    currentLivingCells = 0
    currentDeadCells = 0
    i = 1
    fullGrid = 0
    livingCellList = []
    deadCellList = []
    boardSizeList = []
    timeList = []
    increment1 = 0
    increment2 = 5
    graphing = False

    # 0-100 probability for random initial state
    RANDOM_PROBABILITY = 50

    
    def __init__(self):


        ## Arguments for execution
        ## --start requires one of the initial starting states: 'blip','glider', 'random', 'pentomino
        ## --animate decides to run the visualization
        ## --graph creates a graph of living and dead cells through each step of execution
        ## --gridsize is a single int arguement that creates NxN matrix
        ## -- steps is number of steps to be executed
        
        parser = argparse.ArgumentParser(description="Conway Game of Life")
        parser.add_argument('--start', choices=['blip', 'glider', 'random', 'pentomino'], required='True', help="Generates starting coordinates for simulation")
        parser.add_argument('--animate', action='store_true', help="Animates the simulation")
        parser.add_argument('--graph', action='store_true', help="Graphs living and dead cells")
        parser.add_argument('--timegraph', action='store_true', help="Graphs time steps per millisecond")
        parser.add_argument('--gridsize', type=int, required='True', help="Value to choose grid size")
        parser.add_argument('--steps', type=int, required='True', help="Value to choose number of steps to simulate")
        args = parser.parse_args()


        initialStateOption = args.start
        self.gridSize = args.gridsize
        self.model = self.generateModel(initialStateOption)
        self.steps = args.steps
        self.startTime = time.time()
        self.animate = args.animate
        self.fullGrid = args.gridsize * args.gridsize
        self.graph = args.graph
        self.timegraph = args.timegraph
        
    def makeGraph(self):
        plt.close()
        plt.xlabel("Board Size: 1 = 100")
        plt.ylabel("Steps per ms")
        plt.bar(self.boardSizeList, self.timeList)    
        plt.show() 

################################################################################################################
    ######################## Methods to run simulation without visualization ##############################
################################################################################################################
    
    def conway_assignment_two(self):
        fig, ax = plt.subplots()
        #stores each matrix representation for each step
        storedSteps = []
        self.frame = ax.matshow(self.model)
        
        for i in range (0, self.steps+1):
            self.updateView3(self.steps, storedSteps)
       

    def updateView3(self, frameCount, storedSteps):
        cellCount = [self.livingCells, self.deadCells]
        
        # end condition 
        if self.frames == self.steps:
            endTime = time.time()
            
            msElapsed = (endTime - self.startTime) * 1000 # multiply 1000 for ms
            
            print("===================================================")
            print("                    Statistics                     ")
            print("===================================================")
            print("")
            print("Start Date/Time:        ", datetime.datetime.fromtimestamp(self.startTime))
            print("End Date/Time:          ", datetime.datetime.fromtimestamp(endTime))
            print('Milliseconds elapsed:    {0}ms'.format(msElapsed))
            print("")
            print("# of Cells Born:        ", self.livingCells)
            print("# of Deceased Cells:    ", self.deadCells)
            print("")
            print("Frames Processed:       ", self.frames)
            print("")
            print("Steps per millisecond:  ", (self.steps/msElapsed))
            print("")
            print("Stored a list of board states with length: " , len(storedSteps))
       

        # "while" processed frames < frames to process
        if self.frames < self.steps:            
            self.frames += 1
        # stores current matrix into list storedSteps
            
            # calculate and set the model to be the next frame's
            self.updateModel()
            storedSteps.append(self.model)
            # set the current frame to use the new matrix model from the line above
            self.frame.set_data(self.model)      
            
        return [self.frame], cellCount



################################################################################################################
     ######################## Methods to graph time steps per millisecond ##############################
################################################################################################################

    def conway_assignment_two_timegraph(self):
        fig, ax = plt.subplots()
        self.startTime = 0
        self.startTime = time.time()
        #stores each matrix representation for each step
        if self.graphing == True:
            #plt.close()
            self.gridSize += 300
            self.frames = 0
            
            self.model = self.generateModel("random")
            
        self.frame = ax.matshow(self.model)
        
        for i in range (0, self.steps+1):
            self.updateView2(self.steps)
    

    def updateView2(self, frameCount):
        cellCount = [self.livingCells, self.deadCells]
        
        # end condition 
        if self.frames == self.steps:
            
            self.endTime = time.time()
            
            msElapsed = (self.endTime - self.startTime) * 1000 # multiply 1000 for ms
            self.timeList.append(self.steps/msElapsed)
            self.boardSizeList.append(self.gridSize/100)
            plt.close()
        
            

        # "while" processed frames < frames to process
        if self.frames < self.steps:            
            self.frames += 1
            # calculate and set the model to be the next frame's
            self.updateModel()
            # set the current frame to use the new matrix model from the line above
            self.frame.set_data(self.model)      
            
        return [self.frame], cellCount


    


################################################################################################################
    #################### Methods to simulate and visualize graph of cells after simulation#################
################################################################################################################


    def conway_assignment_two_graph(self):
        fig, ax = plt.subplots()
        storedSteps = []
        
        # take the initial model generated from the constructor
        # and create the very first frame with it
        self.frame = ax.matshow(self.model)

        # https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html
        # interval can be changed to increase or decrease the speed of animation
        #ani = animation.FuncAnimation(fig, self.updateView, interval=1, frames=(self.steps - 1), blit=True, repeat=False)
        
        for i in range (0, self.steps+1):
            self.updateViewGraph(self.steps, storedSteps);
       
        #plt.show()

    def updateViewGraph(self, frameCount, storedSteps):
        cellCount = [self.livingCells, self.deadCells]
        
        # end condition 
        if self.frames == self.steps:
            endTime = time.time()
            
            msElapsed = (endTime - self.startTime) * 1000 # multiply 1000 for ms
            
            print("===================================================")
            print("                    Statistics                     ")
            print("===================================================")
            print("")
            print("Start Date/Time:        ", datetime.datetime.fromtimestamp(self.startTime))
            print("End Date/Time:          ", datetime.datetime.fromtimestamp(endTime))
            print('Milliseconds elapsed:    {0}ms'.format(msElapsed))
            print("")
            print("# of Cells Born:        ", self.livingCells)
            print("# of Deceased Cells:    ", self.deadCells)
            print("")
            print("Frames Processed:       ", self.frames)
            print("")
            print("Steps per millisecond:  ", (self.steps/msElapsed))


            plt.close()
            fig = plt.figure(figsize=(6,4))
            ax = fig.add_subplot(1,1,1)
            plt.title("Living and Dead Cells")
            x = range(len(self.livingCellList))
            rangeList = []
            livingList = []
            deadList = []

            def animate(i):
                if i == self.steps:
                    quit()
                rangeList.append(x[i])
                livingList.append(self.livingCellList[i])
                deadList.append(self.deadCellList[i])
                

                plt.plot(rangeList, livingList, scaley=True, scalex=True, label="Alive", linestyle="-", color="blue")
                plt.plot(rangeList, deadList, scaley=True, scalex=True, label="Dead", linestyle="-", color="red")
                plt.legend(['Alive', 'Dead'])
            anim = animation.FuncAnimation(fig, animate, interval=1)
            plt.show()

            
        # "while" processed frames < frames to process
        if self.frames < self.steps:            
            self.frames += 1
            
            # calculate and set the model to be the next frame's
            self.updateModel()
            # set the current frame to use the new matrix model from the line above
            self.frame.set_data(self.model)
            #self.currentDeadCells = self.fullGrid - self.currentLivingCells
            self.livingCellList.append(self.currentLivingCells)
            self.deadCellList.append(self.currentDeadCells)

            
            
        return [self.frame], cellCount


################################################################################################################
    ########################## Methods to run simulation with visualization#################################
################################################################################################################

         
    def conway_assignment_two_animate(self):
        fig, ax = plt.subplots()
        
        # take the initial model generated from the constructor
        # and create the very first frame with it
        self.frame = ax.matshow(self.model)
        
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html
        # interval can be changed to increase or decrease the speed of animation
        ani = animation.FuncAnimation(fig, self.updateView, interval=1, frames=(self.steps - 1), blit=True, repeat=False)
        
        plt.show()
        
## Method creates the next frame to be displayed and returns that frame
    
    ## Method creates the next frame to be displayed and returns that frame
    
    def updateView(self, frameCount):
        
        # end condition 
        if self.frames == self.steps:
            endTime = time.time()
            
            msElapsed = (endTime - self.startTime) * 1000 # multiply 1000 for ms
            
            print("===================================================")
            print("                    Statistics                     ")
            print("===================================================")
            print("")
            print("Start Date/Time:        ", datetime.datetime.fromtimestamp(self.startTime))
            print("End Date/Time:          ", datetime.datetime.fromtimestamp(endTime))
            print('Milliseconds elapsed:    {0}ms'.format(msElapsed))
            print("")
            print("# of Cells Born:        ", self.livingCells)
            print("# of Deceased Cells:    ", self.deadCells)
            print("")
            print("Frames Processed:       ", self.frames)
            print("")
            print("Steps per millisecond:  ", (self.steps/msElapsed))
            print("")
            
           
        # "while" processed frames < frames to process
        if self.frames < self.steps:            
            self.frames += 1
            # calculate and set the model to be the next frame's
            self.updateModel()
            
            # set the current frame to use the new matrix model from the line above
            self.frame.set_data(self.model)
        
        return [self.frame]

        #Calculates cell position for next frame
      
    def updateModel(self):
    
##        coordsToUpdate = []
        self.currentLivingCells = 0
        self.currentDeadCells = 0
##        rng = np.random.default_rng()
##
##        #model: np.ndarray
##
        emptyArr = np.zeros((self.gridSize,self.gridSize), dtype = int)
##
##        # grid of randomly placed 0's and 1's
##        randomGrid = rng.choice(2, (10, 10))
##
##        # grid with every value of 255
##        full255Grid = np.full((10, 10), 255)
##
##        # essentially a mask to create a grid of randomly placed values
##        # of 0 and 255
##        orig = randomGrid * full255Grid
        #orig = self.model
        # count living cells from initial frame
        
                    
        #####print(orig)

        emptyArr[:, :] = 0
        orig = self.model
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
        orig = np.where(orig == True, 255,0)
        self.model = orig
        self.livingCells += np.count_nonzero(self.model == 255)
        self.deadCells += np.count_nonzero(orig == 0)
        self.currentLivingCells = np.count_nonzero(self.model == 255)
        self.currentDeadCells = np.count_nonzero(orig == 0)
        
        #print('1')
        #self.livingCells += np.count_nonzero(orig == True)
        #####print(orig) 
    
       # generates the initial model based on user input
    
    def generateModel(self, option: int):
        #grid = []
        livingCells = 0
        deadCells   = 0
        #model: np.ndarray
        rng = default_rng()
        grid = np.full((self.gridSize, self.gridSize), 0)
        center = self.getCenterCoord()
        
##        emptyArr = np.zeros((self.gridSize,self.gridSize), dtype = int)
##
##        # grid of randomly placed 0's and 1's
##        randomGrid = rng.choice(2, (self.gridSize, self.gridSize))
##
##        # grid with every value of 255
##        full255Grid = np.full((self.gridSize, self.gridSize), 255)
##
##        # essentially a mask to create a grid of randomly placed values
##        # of 0 and 255
##        orig = randomGrid * full255Grid

        # count living cells from initial frame
        #self.livingCells += np.count_nonzero(orig == 255)
        if option == "random":
            # nested forloop to create a matrix with randomly placed cells based on grid size
            emptyArr = np.zeros((self.gridSize,self.gridSize), dtype = int)
##
##        # grid of randomly placed 0's and 1's
            randomGrid = rng.choice(2, (self.gridSize, self.gridSize))
##
##        # grid with every value of 255
            full255Grid = np.full((self.gridSize, self.gridSize), 255)
##
##        # essentially a mask to create a grid of randomly placed values
##        # of 0 and 255
            orig = randomGrid * full255Grid
            self.model = orig
            return orig
                        
        
        # get the center coordinate of the grid
        

        # set cell coordinates to be alive based on option
        elif option == "blip":
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

    # finds the centerpoint of the grid for the initial starting state
    
    def getCenterCoord(self) -> int:
     
        center = math.ceil((self.gridSize / 2)) - 1
        return center


game = Game()
if game.animate == True:
    game.conway_assignment_two_animate()
elif game.graph == True:
    game.conway_assignment_two_graph()
elif game.timegraph == True:
    for z in range(0,game.increment2):
        game.conway_assignment_two_timegraph()
        game.graphing = True
        
        if z == (game.increment2-1):
            game.makeGraph()
else: game.conway_assignment_two()




