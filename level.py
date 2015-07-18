import pygame
import spritesheet
import string
import sys

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
		self.tileType = Tile.TILE_FLOOR
		self.tiledex = 0
		self.elevation = 0
		self.blocks=blocks
		#only used in level editor
		self.img = None


	'''
	write out tile particulars
	'''
	#format: tile index;tileType;elevation;hasBlocks
	def write(self,fhandle):
		hasBlocks=0
		if self.blocks is not None:
			hsaBlocks=1
		fhandle.write( "%d;%d;%d;%d" % (self.tiledex,self.tileType,self.elevation,hasBlocks) )

class Level:
	tilewidth = 16	#pixel width of tile
	tileheight = 16 #pixel height of tile
	xtiles	= 500	#width of level, essentially
	ytiles = 30
	tilesheet = []	#the tilesheet!
	tilesheetFilename=None
	layout = []#2d array of tiles
	surf = None
	def __init__(self,xt,yt,filename,tw=16,th=16):
		self.xtiles = xt
		self.ytiles = yt
		self.tilewidth = tw
		self.tileheight = th
		self.tilesheet = spritesheet.loadTileSheet(filename,self.tilewidth,self.tileheight,1,1)	
		self.tilesheetFilename=filename
		self.layout = []
		#print "xtiles is: " + str(self.xtiles);
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
					#print "i is " + str(i)
					#print "j is " + str(j)
					tdex = self.layout[i][j].tiledex
					#print type(self.layout[i][j])
					self.surf.blit(self.tilesheet[tdex],(i*self.tilewidth,j*self.tileheight))
		return self.surf

	'''
	write out level particulars
	'''
	def write(self,fhandle):
		fhandle.write("%d,%s\n" % (self.xtiles,self.tilesheetFilename) )
		for i in xrange(self.xtiles):
			for j in xrange(self.ytiles):
				self.layout[i][j].write(fhandle)
				if ( i == self.xtiles - 1):
					fhandle.write("\n")
				else:
					fhandle.write(",")

#this is just a simple test that makes an easy level pattern
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
def parseCell(cell):
	#print "Cell: "+str(cell)
	ssplit = string.split(cell,';')
	t = Tile();
	t.tiledex = int(ssplit[0])
	t.tileType= int(ssplit[1])
	t.elevation= int(ssplit[2])
	t.hasBlocks= int(ssplit[3])
	return t
	
	

#parse a csv file that describes a level
#all levels are 30 tiles high with a variable width
#first line:	width(tiles),tilesheet (filename)
#next 30 lines describe the tiles
#each cell represents a tile in following format: tile index;tileType;elevation;hasBlocks
def parseLevel(filename):
	l = None
	width = 500
	tileFile = None
	f = open(filename, 'r')
	lnum = 0
	for line in f:
		csplit = string.split(line,',')
		if (lnum == 0):	#read in width,tilesheet
			width = csplit[0]
			tileFile = csplit[1]	
			#print "width is " + str(width);
			l = Level(int(width),30,'SMB-Tiles.png')
		elif (lnum <= 31):	#now we are parsing the tiles	
			y = lnum - 31
			for x in range(len(csplit)):
				l.layout[x][y]	= parseCell(csplit[x])	
		lnum = lnum + 1
	return l;
