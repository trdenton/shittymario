#!/usr/bin/python
import pygame
import spritesheet
import level
from pygame.locals import *
import math
from input import Keyboard

class App:
	def __init__(self):
		#init
		pygame.init()
		self.clock = pygame.time.Clock()
		self.FPS = 30	#Frames per second
		self.deltat = self.clock.tick(self.FPS)
		self.screen = pygame.display.set_mode((16*40, 16*30),DOUBLEBUF)
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
