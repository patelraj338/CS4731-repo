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
from mycreatepathnetwork import *
from mynavigatorhelpers import *


###############################
### AStarNavigator
###
### Creates a path node network and implements the A* algorithm to create a path to the given destination.

class AStarNavigator(NavMeshNavigator):

	def __init__(self):
		NavMeshNavigator.__init__(self)


	### Create the path node network.
	### self: the navigator object
	### world: the world object
	def createPathNetwork(self, world):
		self.pathnodes, self.pathnetwork, self.navmesh = myCreatePathNetwork(world, self.agent)
		return None

	### Finds the shortest path from the source to the destination using A*.
	### self: the navigator object
	### source: the place the agent is starting from (i.e., its current location)
	### dest: the place the agent is told to go to
	def computePath(self, source, dest):
		self.setPath(None)
		### Make sure the next and dist matrices exist
		if self.agent != None and self.world != None:
			self.source = source
			self.destination = dest
			### Step 1: If the agent has a clear path from the source to dest, then go straight there.
			###   Determine if there are no obstacles between source and destination (hint: cast rays against world.getLines(), check for clearance).
			###   Tell the agent to move to dest
			### Step 2: If there is an obstacle, create the path that will move around the obstacles.
			###   Find the path nodes closest to source and destination.
			###   Create the path by traversing the self.next matrix until the path node closest to the destination is reached
			###   Store the path by calling self.setPath()
			###   Tell the agent to move to the first node in the path (and pop the first node off the path)
			if clearShot(source, dest, self.world.getLines(), self.world.getPoints(), self.agent):
				self.agent.moveToTarget(dest)
			else:
				start = findClosestUnobstructed(source, self.pathnodes, self.world.getLinesWithoutBorders())
				end = findClosestUnobstructed(dest, self.pathnodes, self.world.getLinesWithoutBorders())
				if start != None and end != None:
					# print len(self.pathnetwork)
					newnetwork = unobstructedNetwork(self.pathnetwork, self.world.getGates())
					# print len(newnetwork)
					closedlist = []
					path, closedlist = astar(start, end, newnetwork)
					if path is not None and len(path) > 0:
						path = shortcutPath(source, dest, path, self.world, self.agent)
						self.setPath(path)
						if self.path is not None and len(self.path) > 0:
							first = self.path.pop(0)
							self.agent.moveToTarget(first)
		return None

	### Called when the agent gets to a node in the path.
	### self: the navigator object
	def checkpoint(self):
		myCheckpoint(self)
		return None

	### This function gets called by the agent to figure out if some shortcuts can be taken when traversing the path.
	### This function should update the path and return True if the path was updated.
	def smooth(self):
		return mySmooth(self)

	def update(self, delta):
		myUpdate(self, delta)


def unobstructedNetwork(network, worldLines):
	newnetwork = []
	for l in network:
		hit = rayTraceWorld(l[0], l[1], worldLines)
		if hit == None:
			newnetwork.append(l)
	return newnetwork


class AStarNode:
    def __init__ (self, point):
        self.point = point
        self.parent = None
        self.H = 0
        self.C = 0

def constructNodesList(network):
    nodeList = []
    for edge in network:
        if edge[0] not in nodeList:
            nodeList.append(edge[0])
        if edge[1] not in nodeList:
            nodeList.append(edge[1])
    return nodeList

def constructAStarNodes(nodes, goal):
    astarNodes = []
    for node in nodes:
        hscore = distance(node, goal)
        newAStarNode = AStarNode(node)
        newAStarNode.H = hscore
        astarNodes.append(newAStarNode)
    return astarNodes

def linkNodesAndAStarNodes(nodes, anodes):
    linkDict = dict()
    for node in nodes:
        for anode in anodes:
            if node == anode.point:
                linkDict[node] = anode
                break
    return linkDict

def getChildren(node, network):
    children = []
    for edge in network:
        if edge[0] == node:
            children.append(edge[1])
        elif edge[1] == node:
            children.append(edge[0])
    return children

def astar(init, goal, network):
	path = []
	open = []
	closed = []
	### YOUR CODE GOES BELOW HERE ###

        nodes = constructNodesList (network)
        astar = constructAStarNodes(nodes, goal)
        linked = linkNodesAndAStarNodes(nodes, astar)
        current = linked[init]
        open.append(current)
        while open:
            current = min(open, key = lambda o: o.H + o.C)
            if current.point == goal:
                while current.parent:
                    path.insert(0, current.point)
                    current = current.parent
                break

            open.remove(current)
            closed.append(current.point)

            children = getChildren(current.point, network)
            for node in children:
                if node in closed:
                    continue
                if linked[node] in open:
                    newCost = current.C + distance(current.point, node)
                    if linked[node].C > newCost:
                        linked[node].C = newCost
                        linked[node].parent = current
                else:
                    linked[node].C = current.C + distance(current.point, node)
                    linked[node].parent = current
                    open.append(linked[node])
	### YOUR CODE GOES ABOVE HERE ###
	return path, closed


def myUpdate(nav, delta):
	### YOUR CODE GOES BELOW HERE ###
        if nav.agent.getLocation() != None:
            if rayTraceWorld(nav.agent.getLocation(), nav.agent.getMoveTarget(), nav.world.getGates()):
                nav.agent.navigateTo(nav.agent.getMoveTarget())
                if nav.path == None:
                    nav.agent.stopMoving()
	### YOUR CODE GOES ABOVE HERE ###
	return None

def myCheckpoint(nav):
	### YOUR CODE GOES BELOW HERE ###
        if rayTraceWorld(nav.agent.moveOrigin, nav.agent.getMoveTarget(), nav.world.getGates()):
            nav.agent.navigateTo(nav.getDestination())
            if nav.path == None:
                nav.agent.stopMoving()
                return None
        # print str(nav.path == None) + " " + str(nav.world == None)
        if nav.path != None:
            if len(nav.path) > 1:
                if rayTraceWorld(nav.agent.getMoveTarget(), nav.path[0], nav.world.getGates()):
                    nav.agent.navigateTo(nav.getDestination())
                    if nav.path == None:
                        nav.agent.stopMoving()
                        return None
                for i in range(0, len(nav.path)-1):
                    if rayTraceWorld(nav.path[i], nav.path[i+1], nav.world.getGates()):
                        nav.agent.navigateTo(nav.getDestination())
                        if nav.path == None:
                            nav.agent.stopMoving()
            elif len(nav.path)==1:
                if rayTraceWorld(nav.agent.getMoveTarget(), nav.path[0], nav.world.getGates()):
                    nav.agent.navigateTo(nav.getDestination())
                    if nav.path == None:
                        nav.agent.stopMoving()
	### YOUR CODE GOES ABOVE HERE ###
	return None


### Returns true if the agent can get from p1 to p2 directly without running into an obstacle.
### p1: the current location of the agent
### p2: the destination of the agent
### worldLines: all the lines in the world
### agent: the Agent object
def clearShot(p1, p2, worldLines, worldPoints, agent):
	### YOUR CODE GOES BELOW HERE ###
        # add extra check for obstacle in agent hitbox!
        # print vars(agent)
        radius = agent.getMaxRadius()
        offset = 2
        xShiftedPolygon = [(p1[0] + agent.getMaxRadius() + offset, p1[1]), \
                    (p1[0] - agent.getMaxRadius() - offset, p1[1]), \
                    (p2[0] - agent.getMaxRadius() - offset, p2[1]), \
                    (p2[0] + agent.getMaxRadius() + offset, p2[1])]

        yShiftedPolygon = [(p1[0], p1[1] + agent.getMaxRadius() + offset), \
            (p1[0], p1[1] - agent.getMaxRadius() - offset), \
            (p2[0], p2[1] - agent.getMaxRadius() - offset), \
            (p2[0], p2[1] + agent.getMaxRadius() + offset)]

        if rayTraceWorld(p1, p2, worldLines) == None:
            hitboxFlag = False
            for pt in worldPoints:
                if pointInsidePolygonPoints(pt, xShiftedPolygon):
                    hitboxFlag = True
                if pointInsidePolygonPoints(pt, yShiftedPolygon):
                    hitboxFlag = True

            if rayTraceWorld(xShiftedPolygon[0], xShiftedPolygon[1], worldLines) or \
                rayTraceWorld(xShiftedPolygon[1], xShiftedPolygon[2], worldLines) or \
                rayTraceWorld(xShiftedPolygon[2], xShiftedPolygon[3], worldLines) or \
                rayTraceWorld(xShiftedPolygon[0], xShiftedPolygon[3], worldLines):
                hitboxFlag = True
            if rayTraceWorld(yShiftedPolygon[0], yShiftedPolygon[1], worldLines) or \
                rayTraceWorld(yShiftedPolygon[1], yShiftedPolygon[2], worldLines) or \
                rayTraceWorld(yShiftedPolygon[2], yShiftedPolygon[3], worldLines) or \
                rayTraceWorld(yShiftedPolygon[0], yShiftedPolygon[3], worldLines):
                hitboxFlag = True

            if hitboxFlag == False:
                return True
	### YOUR CODE GOES ABOVE HERE ###
	return False
