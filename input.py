import pygame
from pygame.locals import *
class keyboard:
	right = False
	left = False
	up = False
	down = False
	@classmethod
	def getInput(cls):
		for event in pygame.event.get():
			if not hasattr(event, 'key'): continue
			down = event.type == KEYDOWN     # key down or up?
			if event.key == K_RIGHT: cls.right = down
			elif event.key == K_LEFT:cls.left = down
			elif event.key == K_UP: cls.up = down
			elif event.key == K_DOWN: cls.down = down
			elif event.key == K_ESCAPE: exit()     # quit the game

