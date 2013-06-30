#!/usr/bin/python
import pygame
import spritesheet
import level
from pygame.locals import *
import math
from input import Keyboard


#pygamey-ness - have group for items, group for enemies, group for player
#pygame is optimized to use groups - ie, an enemy sprite could use store a group of 'targets'
#when the group is empty, bumble abount, when the group has members, pursue them.  etc.
#associating/disassociating from groups is a very fast operation so make use of it!!
class GameObj(pygame.sprite.Sprite):
	def __init__(self,fs=None,r=None):
		pygame.sprite.Sprite.__init__(self)
		frames=fs
		rect=r
		animation=idleAnimation
		#store all frames in here for every animation - have each animation just index into this
		frames=None	#frames for animation

	#override this, otherwise just first frame
	def idleAnimation:
		#TODO default animation	
		while True:
			self.image = frames[0]
			yield None
	
class Player(GameObj,frames):
	#player states
	(PSTATE_SMALL,PSTATE_BIG,PSTATE_FIRE) = range(3)
	#motion states
	(MSTATE_STAND,MSTATE_WALK,MSTATE_RUN,MSTATE_JUMSTATEP,MSTATE_SWIMSTATE) = range(5)
	def __init__(self):
		GameObj.__init__(self,fs=frames)
		motionState = M_STAND
		playerState = PSTATE_SMALL
	def walkAnimation(self):
		while True:
			#have 3 states to contend with - whats a pythonic swtich case?
			self.image = (self.playerState==Player.) : ?frames[1]
			yield None
			self.image = frames[2]
			yield None
			self.image = frames[3]
			yield None
			self.image = frames[2]
			yield None
				
class Enemy(GameObj):
	def __init__(self):
		GameObj.__init__(self)

class Item(GameObj):
	def __init__(self):
		GameObj.__init__(self)

class App:
	def __init__(self):
		#init
		pygame.init()
		self.clock = pygame.time.Clock()
		self.FPS = 30	#Frames per second
		self.deltat = self.clock.tick(self.FPS)
		self.screen = pygame.display.set_mode((16*40, 16*30),DOUBLEBUF)
		pygame.display.set_caption("Shitty Mario")
		self.keyboard = Keyboard()
		print "Loading..."
		#tiles = spritesheet.loadTileSheet('SMB-Tiles.png',16,16,1,1)
		#mar = spritesheet.loadSpriteSheet('Mario.png')
		print "Done!"
		self.l0 = level.parseLevel('test.csv');
		self.l0s = self.l0.getSurf()
		while True:
			self.clock.tick(30)
			self.keyboard.getInput()
			if (self.keyboard.up): print "Up"
			if (self.keyboard.down): print "Down"
			if (self.keyboard.left): print "Left"
			if (self.keyboard.right): print "Right"
			self.screen.blit(self.l0s,(0,0))
			#for i in range(len(mar)):
			#	screen.blit(mar[i],((18*i)%640,18*(18*math.floor(i/640))))
			pygame.display.flip()

if __name__=="__main__":
	app = App()
