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
from moba import *

class MyMinion(Minion):

	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
		self.states = [Idle, Move, AttackTower, AttackBase, AttackEnemyMinion, AttackEnemyHero]
		### Add your states to self.states (but don't remove Idle)
		### YOUR CODE GOES BELOW HERE ###

		### YOUR CODE GOES ABOVE HERE ###

	def start(self):
		Minion.start(self)
		self.changeState(Idle)





############################
### Idle
###
### This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):

	def enter(self, oldstate):
		State.enter(self, oldstate)
		# stop moving
		self.agent.stopMoving()

	def execute(self, delta = 0):
		State.execute(self, delta)
		### YOUR CODE GOES BELOW HERE ###
                # print self.agent.getPossibleDestinations()
                # print self.agent.world.getEnemyTowers(self.agent.getTeam())
                self.agent.changeState(Move)
		### YOUR CODE GOES ABOVE HERE ###
		return None

##############################
### Taunt
###
### This is a state given as an example of how to pass arbitrary parameters into a State.
### To taunt someome, Agent.changeState(Taunt, enemyagent)

class Taunt(State):

	def parseArgs(self, args):
		self.victim = args[0]

	def execute(self, delta = 0):
		if self.victim is not None:
			print "Hey " + str(self.victim) + ", I don't like you!"
		self.agent.changeState(Idle)

##############################
### YOUR STATES GO HERE:


class Move(State):
    def enter(self, oldstate):
        if self.agent.world.getBaseForTeam(self.agent.getTeam()) != None:
            print self.agent.world.getBaseForTeam(self.agent.getTeam()).numSpawned
        self.enemyTowers = self.agent.world.getEnemyTowers(self.agent.getTeam())
        self.enemyNPC = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        self.enemyBases = self.agent.world.getEnemyBases(self.agent.getTeam())
        self.enemyTowerLocations = []
        for tower in self.enemyTowers:
            self.enemyTowerLocations.append(tower.position)

        if len(self.enemyTowerLocations) > 0:
            self.agent.navigateTo(self.enemyTowerLocations[0])
            self.TARGET = "tower"
        elif len(self.enemyBases) > 0 and len(self.enemyTowerLocations) == 0:
            self.agent.navigateTo(self.enemyBases[0].position)
            self.TARGET = "base"

    def execute(self, delta = 0):
        # if distance()
        if len(self.enemyBases) > 0:
            if len(self.enemyNPC) > 0 and distance(self.agent.position, self.enemyBases[0].getLocation()) > 400:
                for enemy in self.enemyNPC:
                    if distance(enemy.getLocation(), self.agent.getLocation()) < 150:
                        self.agent.stopMoving()
                        self.agent.changeState(AttackEnemyMinion, enemy)
                        return None

        if len(self.enemyTowerLocations) > 0 and self.TARGET == "tower":
            if self.agent.moveTarget == None and len(self.enemyTowerLocations) > 0 and not self.agent.isMoving():
                self.agent.navigateTo(self.enemyTowerLocations[0])

            if distance(self.agent.position, self.enemyTowerLocations[0]) < 150:
                self.agent.stopMoving()
                self.agent.changeState(AttackTower, self.enemyTowers[0])
        elif len(self.enemyTowerLocations) == 0 and len(self.enemyBases) > 0 and self.TARGET == "base":
            if self.agent.moveTarget == None and len(self.enemyBases) > 0 and not self.agent.isMoving():
                self.agent.navigateTo(self.enemyBases[0].getLocation())

            if distance(self.agent.position, self.enemyBases[0].getLocation()) < 150:
                self.agent.stopMoving()
                self.agent.changeState(AttackBase, self.enemyBases[0])
        # else:
        #     self.agent.stopMoving()


class AttackTower(State):
    def parseArgs(self, args):
		self.attackTarget = args[0]
    def enter(self, oldstate):
        pass

    def execute(self, delta = 0):
        if self.attackTarget.getHitpoints() > 0:
            self.agent.turnToFace(self.attackTarget.getLocation())
            self.agent.shoot()
        else:
            self.agent.changeState(Idle)

class AttackBase(State):
    def parseArgs(self, args):
        self.attackTarget = args[0]
    def enter(self, oldstate):
        pass

    def execute(self, delta = 0):
        # print self.attackTarget.getHitpoints()
        if self.attackTarget.getHitpoints() > 0:
            self.agent.turnToFace(self.attackTarget.getLocation())
            self.agent.shoot()
        else:
            self.agent.changeState(Idle)

class AttackEnemyMinion(State):
    def parseArgs(self, args):
        self.attackTarget = args[0]
    def enter(self, oldstate):
        pass

    def execute(self, delta = 0):
        if distance(self.attackTarget.getLocation(), self.agent.getLocation()) < 150 and self.attackTarget.getHitpoints() > 0:
            self.agent.turnToFace(self.attackTarget.getLocation())
            self.agent.shoot()
        else:
            self.agent.changeState(Move)

class AttackEnemyHero(State):
    pass
