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


def foom (OO0OOO000OO0O000O ,O0O000OOOOOOO0O0O ,func =lambda O0OO0OOO00000OO0O :O0OO0OOO00000OO0O ):#line:1
	for OO00O0OOO0O0O0OO0 in xrange (len (O0O000OOOOOOO0O0O )):#line:2
		if func (OO0OOO000OO0O000O )<func (O0O000OOOOOOO0O0O [OO00O0OOO0O0O0OO0 ]):#line:3
			O0O000OOOOOOO0O0O .insert (OO00O0OOO0O0O0OO0 ,OO0OOO000OO0O000O )#line:4
			return O0O000OOOOOOO0O0O #line:5
	O0O000OOOOOOO0O0O .append (OO0OOO000OO0O000O )#line:6
	return O0O000OOOOOOO0O0O #line:7
def astar (O0O00O000OO0O0OO0 ,O0OO0OOOOOO0OO0OO ,O00000O0OOO0OOOO0 ):#line:10
	O0OOO0OOOOO0O00OO =[]#line:11
	O0000OO00O0OOO0OO =[]#line:12
	OOO0O0O0OO0OOO00O =[]#line:13
	O0O00O000OO0O0OO0 =(O0O00O000OO0O0OO0 ,0 ,distance (O0O00O000OO0O0OO0 ,O0OO0OOOOOO0OO0OO ),None )#line:16
	OOO0O0O0OO0OOO00O =set ()#line:17
	OO00O0000OO000O00 =set ()#line:18
	O0000OO00O0OOO0OO =[O0O00O000OO0O0OO0 ]#line:19
	O00OO0OOOO00000OO =O0O00O000OO0O0OO0 #line:20
	while O00OO0OOOO00000OO is not None and O00OO0OOOO00000OO [0 ]!=O0OO0OOOOOO0OO0OO and len (O0000OO00O0OOO0OO )>0 :#line:23
		OOO0O0O0OO0OOO00O .add (O00OO0OOOO00000OO [0 ])#line:24
		OO00O0000OO000O00 .add (O00OO0OOOO00000OO )#line:25
		O0000OO00O0OOO0OO .pop (0 )#line:26
		O0O00O0000OOO0OOO =fooz (O00OO0OOOO00000OO ,O00000O0OOO0OOOO0 ,O0OO0OOOOOO0OO0OO )#line:28
		for OO000O00O0000O0OO in O0O00O0000OOO0OOO :#line:30
			if OO000O00O0000O0OO [0 ]not in OOO0O0O0OO0OOO00O :#line:31
				foom (OO000O00O0000O0OO ,O0000OO00O0OOO0OO ,lambda O0OO0O0O000OO00O0 :O0OO0O0O000OO00O0 [1 ]+O0OO0O0O000OO00O0 [2 ])#line:32
		if len (O0000OO00O0OOO0OO )>0 :#line:34
			O00OO0OOOO00000OO =O0000OO00O0OOO0OO [0 ]#line:35
		else :#line:36
			O00OO0OOOO00000OO =None #line:37
	if O00OO0OOOO00000OO is not None :#line:40
		while O00OO0OOOO00000OO [3 ]is not None :#line:41
			O0OOO0OOOOO0O00OO .append (O00OO0OOOO00000OO [0 ])#line:42
			O00O0O000O000OOO0 =O00OO0OOOO00000OO [3 ]#line:43
			for OO00O0O000O000O0O in list (OO00O0000OO000O00 ):#line:44
				if O00O0O000O000OOO0 ==OO00O0O000O000O0O [0 ]:#line:45
					O00OO0OOOO00000OO =OO00O0O000O000O0O #line:46
					break #line:47
		O0OOO0OOOOO0O00OO .append (O00OO0OOOO00000OO [0 ])#line:48
		O0OOO0OOOOO0O00OO .reverse ()#line:49
	OOO0O0O0OO0OOO00O =list (OOO0O0O0OO0OOO00O )#line:50
	return O0OOO0OOOOO0O00OO ,OOO0O0O0OO0OOO00O #line:52
def fooz (OO0OOOOOOO00O0O0O ,OOOOOO0OOOOOOO000 ,OO00O0O000O0OOO0O ):#line:55
	OO0OOOO0O0O0OOOOO =[]#line:56
	for OO0O00O0OO00OOO00 in OOOOOO0OOOOOOO000 :#line:57
		if OO0O00O0OO00OOO00 [0 ]==OO0OOOOOOO00O0O0O [0 ]:#line:58
			OO0OOOO0O0O0OOOOO .append ((OO0O00O0OO00OOO00 [1 ],OO0OOOOOOO00O0O0O [1 ]+distance (OO0O00O0OO00OOO00 [0 ],OO0O00O0OO00OOO00 [1 ]),distance (OO0O00O0OO00OOO00 [1 ],OO00O0O000O0OOO0O ),OO0OOOOOOO00O0O0O [0 ]))#line:59
		elif OO0O00O0OO00OOO00 [1 ]==OO0OOOOOOO00O0O0O [0 ]:#line:60
			OO0OOOO0O0O0OOOOO .append ((OO0O00O0OO00OOO00 [0 ],OO0OOOOOOO00O0O0O [1 ]+distance (OO0O00O0OO00OOO00 [0 ],OO0O00O0OO00OOO00 [1 ]),distance (OO0O00O0OO00OOO00 [0 ],OO00O0O000O0OOO0O ),OO0OOOOOOO00O0O0O [0 ]))#line:61
	return OO0OOOO0O0O0OOOOO #line:62


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
                    if i <= len(nav.path)-3:
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


