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

import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates the path network as a list of lines between all path nodes that are traversable by the agent.
def myBuildPathNetwork(pathnodes, world, agent = None):
	lines = []
	### YOUR CODE GOES BELOW HERE ###
        for i in range(len(pathnodes)):
            for j in range (i+1, len(pathnodes)):
                tempLine = (pathnodes[i], pathnodes[j])
                offset = 2

                xShiftedPolygon = [(pathnodes[i][0] + agent.getMaxRadius() + offset, pathnodes[i][1]), \
                    (pathnodes[i][0] - agent.getMaxRadius() - offset, pathnodes[i][1]), \
                    (pathnodes[j][0] - agent.getMaxRadius() - offset, pathnodes[j][1]), \
                    (pathnodes[j][0] + agent.getMaxRadius() + offset, pathnodes[j][1])]

                yShiftedPolygon = [(pathnodes[i][0], pathnodes[i][1] + agent.getMaxRadius() + offset), \
                    (pathnodes[i][0], pathnodes[i][1] - agent.getMaxRadius() - offset), \
                    (pathnodes[j][0], pathnodes[j][1] - agent.getMaxRadius() - offset), \
                    (pathnodes[j][0], pathnodes[j][1] + agent.getMaxRadius() + offset)]

                if not rayTraceWorld(pathnodes[i], pathnodes[j], world.getLines()):
                    hitboxFlag = False
                    # for obstacle in world.getObstacles():
                    for pt in world.getPoints():
                        if pointInsidePolygonPoints(pt, xShiftedPolygon):
                            hitboxFlag = True
                        if pointInsidePolygonPoints(pt, yShiftedPolygon):
                            hitboxFlag = True

                    if rayTraceWorld(xShiftedPolygon[0], xShiftedPolygon[1], world.getLines()) or \
                        rayTraceWorld(xShiftedPolygon[1], xShiftedPolygon[2], world.getLines()) or \
                        rayTraceWorld(xShiftedPolygon[2], xShiftedPolygon[3], world.getLines()) or \
                        rayTraceWorld(xShiftedPolygon[0], xShiftedPolygon[3], world.getLines()):
                        hitboxFlag = True
                    if rayTraceWorld(yShiftedPolygon[0], yShiftedPolygon[1], world.getLines()) or \
                        rayTraceWorld(yShiftedPolygon[1], yShiftedPolygon[2], world.getLines()) or \
                        rayTraceWorld(yShiftedPolygon[2], yShiftedPolygon[3], world.getLines()) or \
                        rayTraceWorld(yShiftedPolygon[0], yShiftedPolygon[3], world.getLines()):
                        hitboxFlag = True

                    if not hitboxFlag:
                        appendLineNoDuplicates(tempLine, lines)

	### YOUR CODE GOES ABOVE HERE ###
	return lines
