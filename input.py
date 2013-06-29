import pygame
from pygame.locals import *
class Keyboard:
	right = False
	left = False
	up = False
	down = False
	space = False
	a = False
	z = False
	@classmethod
	def getInput(cls):
		for event in pygame.event.get():
			if not hasattr(event, 'key'): continue
			down = event.type == KEYDOWN     # key down or up?
			if event.key == K_RIGHT: cls.right = down
			elif event.key == K_LEFT:cls.left = down
			elif event.key == K_UP: cls.up = down
			elif event.key == K_DOWN: cls.down = down
			elif event.key == K_SPACE: cls.space = down
			elif event.key == K_z: cls.z = down
			elif event.key == K_a: cls.a = down
			elif event.key == K_ESCAPE: exit()     # quit the game

