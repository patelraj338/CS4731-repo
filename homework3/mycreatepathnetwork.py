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

def constructEdges(pathnodes, world, polys, agent = None):
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

            if not rayTraceWorld(pathnodes[i], pathnodes[j], world.getLines()[4:]):
                hitboxFlag = False
                # for obstacle in world.getObstacles():
                for pt in world.getPoints():
                    if pointInsidePolygonPoints(pt, xShiftedPolygon):
                        hitboxFlag = True
                    if pointInsidePolygonPoints(pt, yShiftedPolygon):
                        hitboxFlag = True

                if rayTraceWorld(xShiftedPolygon[0], xShiftedPolygon[1], world.getLines()[4:]) or \
                    rayTraceWorld(xShiftedPolygon[1], xShiftedPolygon[2], world.getLines()[4:]) or \
                    rayTraceWorld(xShiftedPolygon[2], xShiftedPolygon[3], world.getLines()[4:]) or \
                    rayTraceWorld(xShiftedPolygon[0], xShiftedPolygon[3], world.getLines()[4:]):
                    hitboxFlag = True
                if rayTraceWorld(yShiftedPolygon[0], yShiftedPolygon[1], world.getLines()[4:]) or \
                    rayTraceWorld(yShiftedPolygon[1], yShiftedPolygon[2], world.getLines()[4:]) or \
                    rayTraceWorld(yShiftedPolygon[2], yShiftedPolygon[3], world.getLines()[4:]) or \
                    rayTraceWorld(yShiftedPolygon[0], yShiftedPolygon[3], world.getLines()[4:]):
                    hitboxFlag = True

                if not hitboxFlag:
                    # appendLineNoDuplicates(tempLine, lines)
                    for polygon in polys:
                        if pointOnPolygon(pathnodes[i], polygon) and pointOnPolygon(pathnodes[j], polygon):
                            appendLineNoDuplicates(tempLine, lines)

    return lines

def checkPolygonValidity (poly,  world, polyList):
    if isConvex(poly) == False:
        return False
    polyListCopy = polyList[:]
    realPolygonLines = []
    invertedPolygonLines = []
    last = None
    for p in poly:
        if last != None:
            realPolygonLines.append((last, p))
            invertedPolygonLines.append((p, last))
        last = p
    realPolygonLines.append((poly[len(poly)-1], poly[0]))
    invertedPolygonLines.append((poly[0], poly[len(poly)-1]))

    for line in realPolygonLines:
        while line in polyListCopy:
            polyListCopy.remove(line)

    for line in invertedPolygonLines:
        while line in polyListCopy:
            polyListCopy.remove(line)

    worldlines = world.getLines()[4:]
    for line in realPolygonLines:
        while line in worldlines:
            worldlines.remove(line)

    for line in invertedPolygonLines:
        while line in worldlines:
            worldlines.remove(line)

    last = None
    for p in poly:
        if last != None:
            if rayTraceWorldNoEndPoints(last, p, polyListCopy) != None:
                return False
        last = p
    if rayTraceWorldNoEndPoints(poly[len(poly)-1], poly[0], polyListCopy) != None:
        return False

    last = None
    for p in poly:
        if last != None:
            if rayTraceWorldNoEndPoints(last, p, worldlines) != None:
                return False
        last = p
    if rayTraceWorldNoEndPoints(poly[len(poly)-1], poly[0], worldlines) != None:
        return False

    for obstacle in world.getObstacles():
        partOfObstacle = []
        for point in poly:
            partOfObstacle.append(pointOnPolygon(point, obstacle.getPoints()))
        if False not in partOfObstacle:
            return False
        for point in obstacle.getPoints():
            if pointInsidePolygonPoints(point, poly) and pointOnPolygon(point, poly) == False:
                return False

    return True

def combinePolygons3To4(polygons):
    quadPolygons = []
    availableTriangle = polygons[:]
    for polygon1 in polygons:
        for polygon2 in polygons:
            if polygon1 in availableTriangle and polygon2 in availableTriangle and \
                polygonsAdjacent(polygon1, polygon2):
                common = commonPoints(polygon1, polygon2)
                for p in polygon2:
                    if p not in common:
                        common.insert(1, p)
                for p in polygon1:
                    if p not in common:
                        common.append(p)
                if isConvex(common):
                    quadPolygons.append(tuple(common))
                    try:
                        availableTriangle.remove(polygon1)
                    except ValueError:
                        pass
                    try:
                        availableTriangle.remove(polygon2)
                    except ValueError:
                        pass

    return (availableTriangle + quadPolygons)


# Creates a path node network that connects the midpoints of each nav mesh together
def myCreatePathNetwork(world, agent = None):
	nodes = []
	edges = []
	polys = []
	### YOUR CODE GOES BELOW HERE ###
        polyLines = []
        for pointA in world.getPoints():
            for pointB in world.getPoints():
                for pointC in world.getPoints():

                    ## Filter system
                    if pointA != pointB and pointB != pointC and pointA != pointC and \
                        isConvex((pointA, pointB, pointC)) and \
                        checkPolygonValidity((pointA, pointB, pointC), world, polyLines) == True:

                        newPoly = (pointA, pointB, pointC)
                    	last = None
                    	for p in newPoly:
                    		if last != None and (last,p) not in polyLines and (p, last) not in polyLines:
                    			polyLines.append((last, p))
                    		last = p
                    	polyLines.append((newPoly[len(newPoly)-1], newPoly[0]))

                        polys.append(newPoly)
                        # drawPolygon(newPoly, world.debug, (0,255,0))

        polys = combinePolygons3To4(polys)
        polys = combinePolygons3To4(polys)
        polyLines = []
        for pol in polys:
            last = None
            for p in pol:
                if last != None and (last,p) not in polyLines and (p, last) not in polyLines:
                    polyLines.append((last, p))
                last = p
            polyLines.append((newPoly[len(newPoly)-1], newPoly[0]))

        for line in polyLines:
            lineMidX = (line[0][0] + line[1][0])/2.0
            lineMidY = (line[0][1] + line[1][1])/2.0
            nodes.append((lineMidX, lineMidY))
            # drawCross(world.debug, (lineMidX, lineMidY), (255, 0, 0))
        worldEdgeNodes = world.getPoints()[:4]
        node = nodes + worldEdgeNodes

        edges = constructEdges(nodes, world,polys, agent)

	### YOUR CODE GOES ABOVE HERE ###
	return nodes, edges, polys
