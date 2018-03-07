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

### Returns true if the agent can get from p1 to p2 directly without running into an obstacle.
### p1: the current location of the agent
### p2: the destination of the agent
### worldLines: all the lines in the world
### agent: the Agent object
def clearShot (OO0O0OO0000O00OOO ,O00O00O0OOO0OO00O ,O00O0O0OOO0OO0OOO ,O0OO00OO0O0OOO000 ,OOO00OOOOOO00OOOO ):#line:139
	O0O00OO000O0O00OO =OOO00OOOOOO00OOOO .getRadius ()*4.0 #line:141
	OOOO00OOO0O00OO00 =rayTraceWorld (OO0O0OO0000O00OOO ,O00O00O0OOO0OO00O ,O00O0O0OOO0OO0OOO )#line:142
	if OOOO00OOO0O00OO00 ==None :#line:143
		O00O0000O00OO0000 =False #line:144
		for OOOO00000O0O0OO0O in O0OO00OO0O0OOO000 :#line:145
			if minimumDistance ((OO0O0OO0000O00OOO ,O00O00O0OOO0OO00O ),OOOO00000O0O0OO0O )<O0O00OO000O0O00OO :#line:146
				O00O0000O00OO0000 =True #line:147
		if not O00O0000O00OO0000 :#line:148
			return True #line:149
	return False

### This function optimizes the given path and returns a new path
### source: the current position of the agent
### dest: the desired destination of the agent
### path: the path previously computed by the A* algorithm
### world: pointer to the world
def shortcutPath(source, dest, path, world, agent):
	### YOUR CODE GOES BELOW HERE ###

	### YOUR CODE GOES BELOW HERE ###
	return path


### This function changes the move target of the agent if there is an opportunity to walk a shorter path.
### This function should call nav.agent.moveToTarget() if an opportunity exists and may also need to modify nav.path.
### nav: the navigator object
### This function returns True if the moveTarget and/or path is modified and False otherwise
def mySmooth(nav):
	### YOUR CODE GOES BELOW HERE ###

	### YOUR CODE GOES ABOVE HERE ###
	return False


