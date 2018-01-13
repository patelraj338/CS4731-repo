'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates a grid as a 2D array of True/False values (True = traversable). Also returns the dimensions of the grid as a (columns, rows) list.
def myCreateGrid(world, cellsize):
	grid = None
	dimensions = (0, 0)
	### YOUR CODE GOES BELOW HERE ###
        dimensions = (int(math.ceil(world.getDimensions()[0]/cellsize)), int(math.ceil(world.getDimensions()[1]/cellsize)))
        grid = [[True]*dimensions[1] for _ in range(dimensions[0])]

        for obstacle in world.getObstacles():
            minX = obstacle.getPoints()[0][0]
            minY = obstacle.getPoints()[0][1]
            maxX = obstacle.getPoints()[0][0]
            maxY = obstacle.getPoints()[0][1]
            for i in range(1, len(obstacle.getPoints())):
                minX = obstacle.getPoints()[i][0] if obstacle.getPoints()[i][0] < minX else minX
                maxX = obstacle.getPoints()[i][0] if obstacle.getPoints()[i][0] > maxX else maxX
                minY = obstacle.getPoints()[i][1] if obstacle.getPoints()[i][1] < minY else minY
                maxY = obstacle.getPoints()[i][1] if obstacle.getPoints()[i][1] > maxY else maxY

            for i in range(int(minX-0.5), int(maxX+0.5)):
                for j in range(int(minY-0.5), int(maxY+0.5)):
                    if grid[int(i/cellsize)][int(j/cellsize)]:
                        grid[int(i/cellsize)][int(j/cellsize)] = False

	### YOUR CODE GOES ABOVE HERE ###
	return grid, dimensions
