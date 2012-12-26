import pygame
import spritesheet
import string

#blocks float above tiles
class Block:
	BLOCK_ITEM,BLOCK_COIN,BLOCK_HIDDEN,BLOCK_BREAK = range(4)
	def __init__(self,blockType=BLOCK_ITEM,tiledex=0,elevation=16):
		blockType = BLOCK_ITEM

#a class to represent a tile in a rivercity ransom style game
class Tile:
	#floor is walkable, float is a floating platform, wall is nonwalkable, drop makes ya fall!
	TILE_FLOOR, TILE_FLOAT, TILE_WALL, TILE_DROP = range(4)
	#type is the type of tile obviously,tiledex isthe index into the tilesheet
	#elevation - self explanatory
	#block is a list of block objects 
	def __init__(self, tileType=TILE_FLOOR,tiledex=0,elevation=0,blocks=None):
		tileType = TILE_FLOOR
		tiledex = 0
		elevation = 0

class Level:
	tilewidth = 16
	tileheight = 16
	xtiles	= 500#width of level, essentially
	ytiles = 30
	tilesheet = []	#the tilesheet!
	layout = []#2d array of tiles
	surf = None
	def __init__(self):
		self.tilesheet = spritesheet.loadTileSheet('SMB-Tiles.png',self.tilewidth,self.tileheight,1,1)	
		self.layout = []
		for i in xrange(self.xtiles):
			self.layout.append([])
			for j in xrange(self.ytiles):
				self.layout[i].append(Tile());
	#return a pygame surface representing the level
	def getSurf(self):
		if (self.surf is None):
			self.surf = pygame.Surface((self.xtiles*self.tilewidth,self.ytiles*self.tileheight)).convert()
			for i in xrange(self.xtiles):
				for j in xrange(self.ytiles):
					tdex = self.layout[i][j].tiledex
					self.surf.blit(self.tilesheet[tdex],(i*self.tilewidth,j*self.tileheight))
		return self.surf

def level0Init():
	l0 = Level();
	for i in xrange(l0.xtiles):
		for j in range(0,15):
			l0.layout[i][j].tiledex = (13*7) - 1
		for j in range(15,25):
			l0.layout[i][j].tiledex = (13*8)-1
		for j in range(25,30):
			l0.layout[i][j].tiledex = 0
	return l0


#each cell represents a tile in following format: tile index;tileType;elevation;hasBlocks
def cellParse(cell):
	ssplit = string.split(cell,';')
	t = Tile();
	

#parse a csv file that describes a level
#all levels are 30 tiles high with a variable width
#first line:	width(tiles),tilesheet (filename)
#next 30 lines describe the tiles
#each cell represents a tile in following format: tile index;tileType;elevation;hasBlocks
def levelParse(filename):
	l = Level()
	width = 500
	tileFile = None
	f = open(filename, 'r')
	lnum = 0
	for line in f:
		csplit = string.split(line,',')
		if (lnum ==0):	#read in width,tilesheet
			width = csplit[0]
			tileFile = csplit[1]	
		else if (lnum <= 31):	#now we are parsing the tiles	
			y = lnum - 1
			for x in range(len(csplit)):
				cell = csplit[x]
				l.layout[x][y]	= cellParse(cell)	
		lnum = lnum + 1
