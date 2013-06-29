#!/usr/bin/python
import pygame
import spritesheet
import level
from pygame.locals import *
import math
from input import keyboard


#init
pygame.init()
clock = pygame.time.Clock()
FPS = 30	#Frames per second
deltat = clock.tick(FPS)
screen = pygame.display.set_mode((16*40, 16*30),DOUBLEBUF)

print "Loading..."
#tiles = spritesheet.loadTileSheet('SMB-Tiles.png',16,16,1,1)
mar = spritesheet.loadSpriteSheet('Mario.png')
print "Done!"
l0 = level.parseLevel('test.csv');
print "l0 is type:"
print type(l0);
l0s = l0.getSurf()
while True:
	clock.tick(30)
	keyboard.getInput()
#	if (keyboard.up): print "Up"
#	if (keyboard.down): print "Down"
#	if (keyboard.left): print "Left"
#	if (keyboard.right): print "Right"
	screen.blit(l0s,(0,0))
	for i in range(len(mar)):
		screen.blit(mar[i],((18*i)%640,18*(18*math.floor(i/640))))
	pygame.display.flip()
