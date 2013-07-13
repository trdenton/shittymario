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
	def __init__(self,frames=None,r=None):
		pygame.sprite.Sprite.__init__(self)
		self.frames=frames
		self.image=None
		self.rect=r
		self.animation=self.idleAnimation	#animation being a function
		#store all frames in here for every animation - have each animation just index into this

	#override this, otherwise just first frame
	def idleAnimation(self):
		#TODO default animation	
		while True:
			self.image = frames[0]
			yield None
	def update(self):
		self.animation()	
	
class Player(GameObj):
	#player states
	(PSTATE_SMALL,PSTATE_BIG,PSTATE_FIRE) = range(3)
	#motion states
	(MSTATE_STAND,MSTATE_WALK,MSTATE_RUN,MSTATE_JUMP,MSTATE_SWIM) = range(5)
	def __init__(self,frames=None):
		GameObj.__init__(self,frames=frames)
		self.mstate = Player.MSTATE_WALK
		self.pstate = Player.PSTATE_SMALL
		self.animation = self.motionAnimation()
		self.image=self.frames[5]
	def update(self):
		
		self.animation.next()
		self.rect = self.image.get_rect()

	def motionAnimation(self):
		while True:
			if (self.pstate == Player.PSTATE_SMALL):		
				if self.mstate == Player.MSTATE_STAND:			
					self.image = self.frames[5]	
					yield None
				elif self.mstate == Player.MSTATE_WALK or self.mstate == Player.MSTATE_RUN:
					self.image = self.frames[11]	
					yield None
					self.image = self.frames[6]	
					yield None
					self.image = self.frames[7]	
					yield None
					self.image = self.frames[6]	
					yield None
				elif self.mstate == Player.MSTATE_JUMP:			
					self.image = self.frames[5]
					yield None
				elif self.mstate == Player.MSTATE_SWIM:			
					yield None
			elif (self.pstate == Player.PSTATE_BIG):
				if self.mstate == Player.MSTATE_STAND:			
					yield None
				elif self.mstate == Player.MSTATE_WALK:			
					yield None
				elif self.mstate == Player.MSTATE_RUN:			
					yield None
				elif self.mstate == Player.MSTATE_JUMP:			
					yield None
				elif self.mstate == Player.MSTATE_SWIM:			
					yield None
			elif (self.pstate == Player.PSTATE_FIRE):
				if self.mstate == Player.MSTATE_STAND:			
					yield None
				elif self.mstate == Player.MSTATE_WALK:			
					yield None
				elif self.mstate == Player.MSTATE_RUN:			
					yield None
				elif self.mstate == Player.MSTATE_JUMP:			
					yield None
				elif self.mstate == Player.MSTATE_SWIM:			
					yield None
			else:
				self.image = self.frames[0]
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
		mar = spritesheet.loadSpriteSheet('Mario.png')
		print "Done!"
		self.l0 = level.parseLevel('test.csv');
		self.l0s = self.l0.getSurf()
		playerGroup = pygame.sprite.Group()
		player = Player(frames=mar)
		playerGroup.add(player)
		while True:
			self.clock.tick(5)
			self.keyboard.getInput()
			if (self.keyboard.up): print "Up"
			if (self.keyboard.down): print "Down"
			if (self.keyboard.left): print "Left"
			if (self.keyboard.right): print "Right"
			self.screen.blit(self.l0s,(0,0))
			playerGroup.update()
			playerGroup.draw(self.screen)
			#for i in range(len(mar)):
			#	self.screen.blit(mar[i], (((18*i)%640), i))
			pygame.display.flip()

if __name__=="__main__":
	app = App()
