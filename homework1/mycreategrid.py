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

        #j is row(y) and i is column(x)
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                topLeftCornX = i * cellsize
                topLeftCornY = j * cellsize
                topLeftPoint = (topLeftCornX, topLeftCornY)

                if topLeftCornX + cellsize >= world.getDimensions()[0] or topLeftCornY + cellsize >= world.getDimensions()[1]:
                    grid[i][j] = False
                    continue

                if rayTraceWorld(topLeftPoint, (topLeftPoint[0] + cellsize, topLeftPoint[1]), world.getLines()[4:]) or \
                    rayTraceWorld(topLeftPoint, (topLeftPoint[0] , topLeftPoint[1]+cellsize), world.getLines()[4:]) or \
                    rayTraceWorld((topLeftPoint[0] , topLeftPoint[1]+cellsize), (topLeftPoint[0] + cellsize, topLeftPoint[1]+cellsize), world.getLines()[4:]) or \
                    rayTraceWorld((topLeftPoint[0] + cellsize , topLeftPoint[1]), (topLeftPoint[0] + cellsize, topLeftPoint[1]+cellsize), world.getLines()[4:]):
                    grid[i][j] = False
                    continue

                for obstacle in world.getObstacles():
                    if pointInsidePolygonPoints(topLeftPoint, obstacle.getPoints()) or \
                        pointInsidePolygonPoints((topLeftPoint[0] + cellsize, topLeftPoint[1]), obstacle.getPoints()) or \
                        pointInsidePolygonPoints((topLeftPoint[0], topLeftPoint[1]+ cellsize), obstacle.getPoints()) or \
                        pointInsidePolygonPoints((topLeftPoint[0] + cellsize, topLeftPoint[1] + cellsize), obstacle.getPoints()):
                        grid[i][j] = False

	### YOUR CODE GOES ABOVE HERE ###
	return grid, dimensions
