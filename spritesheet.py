#!/usr/bin/python
#	functions to automagically load spritesheets, tilesheets
#	Troy Denton, Dec 2012
#
#	loadSpriteSheet(filename) -> list of pygame images
#	where filename is a spritesheet image, where sprites are laid out on a solid backbround
#	uses the top-left corner of the image to determine what the background image is
#	uses opencv to automatically segment each sprite into its minimum bounding box (not a rotated box)
#
#	loadTileSheet(filename,width,height,xspace,yspace) -> list of pygame images
import cv,pygame,math
from pygame.locals import *


def loadTileSheet(filename,width,height,xspace=0,yspace=0): 
	global screen
	img = pygame.image.load(filename).convert()
	xtiles = 0
	ytiles = 0
	tiles = []
	#xtiles*width + (xtiles-1)*xspacing = width 

	while (xtiles*width + (xtiles-1)*xspace != img.get_width()):
		xtiles = xtiles + 1
	while (ytiles*width + (ytiles-1)*yspace != img.get_height()):
		ytiles = ytiles + 1
	
	for j in range(ytiles):
		for i in range(xtiles):
			r = pygame.Rect((i*width + (i)*xspace,j*height + (j)*yspace),(width,height))
			subsurf = pygame.Surface(r.size).convert()
			subsurf.blit(img,(0,0),r)
			#screen.blit(subsurf,r)
			tiles.append(subsurf)	
	
	return tiles
#pygame.init()
#screen = pygame.display.set_mode((640, 480),DOUBLEBUF)
#img = pygame.image.load('SMB-Tiles.png')
#tiles = loadTileSheet('SMB-Tiles.png',16,16,1,1)


def fillConnected(cvm,i,j,m):
	w = cvm.cols 
	h = cvm.rows

	if ((i-1) >= 0 and (i-1) < h and (j-1) >= 0 and (j-1) < w and cv.GetReal2D(cvm,i-1,j-1) > 0):
		cv.SetReal2D(cvm,i-1,j-1,m)	
	if ((i-1) >= 0 and (i-1) < h and (j) >= 0 and (j) < w and cv.GetReal2D(cvm,i-1,j) > 0):
		cv.SetReal2D(cvm,i-1,j,m)	
	if ((i-1) >= 0 and (i-1) < h and (j+1) >= 0 and (j+1) < w and cv.GetReal2D(cvm,i-1,j+1) > 0):
		cv.SetReal2D(cvm,i-1,j+1,m)
	if ((i) >= 0 and (i) < h and (j-1) >= 0 and (j-1) < w and cv.GetReal2D(cvm,i,j-1) > 0):
		cv.SetReal2D(cvm,i,j-1,m)		
	if ((i) >= 0 and (i) < h and (j) >= 0 and (j) < w and cv.GetReal2D(cvm,i,j) > 0):
		cv.SetReal2D(cvm,i,j,m)		
	if ((i) >= 0 and (i) < h and (j+1) >= 0 and (j+1) < w and cv.GetReal2D(cvm,i,j+1) > 0):
		cv.SetReal2D(cvm,i,j+1,m)	
	if ((i+1) >= 0 and (i+1) < h and (j-1) >= 0 and (j-1) < w and cv.GetReal2D(cvm,i+1,j-1) > 0):
		cv.SetReal2D(cvm,i+1,j-1,m)	
	if ((i+1) >= 0 and (i+1) < h and (j) >= 0 and (j) < w and cv.GetReal2D(cvm,i+1,j) > 0):
		cv.SetReal2D(cvm,i+1,j,m)	
	if ((i+1) >= 0 and (i+1) < h and (j+1) >= 0 and (j+1) < w and cv.GetReal2D(cvm,i+1,j+1) > 0):
		cv.SetReal2D(cvm,i+1,j+1,m)	
	return m



def connectedMin(cvm,i,j):
	w = cvm.cols 
	h = cvm.rows
	m = cv.GetReal2D(cvm,i,j)

	if ((i-1) >= 0 and (i-1) < h and (j-1) >= 0 and (j-1) < w and cv.GetReal2D(cvm,i-1,j-1) < m 
	and cv.GetReal2D(cvm,i-1,j-1) > 0):
		m = cv.GetReal2D(cvm,i-1,j-1)	
	if ((i-1) >= 0 and (i-1) < h and (j) >= 0 and (j) < w and cv.GetReal2D(cvm,i-1,j) < m
	and cv.GetReal2D(cvm,i-1,j) > 0):
		m = cv.GetReal2D(cvm,i-1,j)	
	if ((i-1) >= 0 and (i-1) < h and (j+1) >= 0 and (j+1) < w and cv.GetReal2D(cvm,i-1,j+1) < m
	and cv.GetReal2D(cvm,i-1,j+1) > 0):
		m = cv.GetReal2D(cvm,i-1,j+1)
	if ((i) >= 0 and (i) < h and (j-1) >= 0 and (j-1) < w and cv.GetReal2D(cvm,i,j-1) < m
	and cv.GetReal2D(cvm,i,j-1) > 0):
		m = cv.GetReal2D(cvm,i,j-1)		
	if ((i) >= 0 and (i) < h and (j+1) >= 0 and (j+1) < w and cv.GetReal2D(cvm,i,j+1) < m
	and cv.GetReal2D(cvm,i,j+1) > 0):
		m = cv.GetReal2D(cvm,i,j+1)	
	if ((i+1) >= 0 and (i+1) < h and (j-1) >= 0 and (j-1) < w and cv.GetReal2D(cvm,i+1,j-1) < m
	and cv.GetReal2D(cvm,i+1,j-1) > 0):
		m = cv.GetReal2D(cvm,i+1,j-1)	
	if ((i+1) >= 0 and (i+1) < h and (j) >= 0 and (j) < w and cv.GetReal2D(cvm,i+1,j) < m
	and cv.GetReal2D(cvm,i+1,j) > 0):
		m = cv.GetReal2D(cvm,i+1,j)	
	if ((i+1) >= 0 and (i+1) < h and (j+1) >= 0 and (j+1) < w and cv.GetReal2D(cvm,i+1,j+1) < m
	and cv.GetReal2D(cvm,i+1,j+1) > 0):
		m = cv.GetReal2D(cvm,i+1,j+1)	
	return m

#segment image based on 8-connectivity

def loop_connected(im):
	im = cv.GetMat(im)
	c = 1;
	for i in xrange(im.rows):
		for j in xrange(im.cols):
			p = cv.GetReal2D(im,i,j)
			if (p > 0):
				m = connectedMin(im,i,j)
				fillConnected(im,i,j,m)

			if (p == 255):	#untouched pixels are at 255
				fillConnected(im,i,j,c)
				c = c + 1

#returns a list of images
def segment(img):
	#make a clone to wang around with
	im = cv.CloneImage(img)
	#create RGB image for pygame use
	cv.CvtColor(img,img,cv.CV_BGR2RGB)
	bw = cv.CreateImage(cv.GetSize(im), cv.IPL_DEPTH_8U, 1);
	cv.FloodFill(im,(0,0),(0,0,0))
	cv.CvtColor(im,bw,cv.CV_BGR2GRAY)
	cv.Threshold(bw,bw,0,255,cv.CV_THRESH_BINARY)

	segs = []
	loop_connected(bw)	
	loop_connected(bw)	
	mat = cv.GetMat(bw)
	
	hist = cv.CreateHist([255], cv.CV_HIST_ARRAY,[(0,255)],1)
	cv.CalcHist([bw],hist)
	for v in range(1,255):
		if (cv.QueryHistValue_1D(hist,v) > 0):
			maxx = maxy = 0
			minx = miny = 500000
			for i in xrange(mat.cols):
				for j in xrange(mat.rows):
					if (cv.GetReal2D(mat,j,i)==v):
						if (i < minx): minx = i
						if (i > maxx): maxx = i
						if (j < miny): miny = j
						if (j > maxy): maxy = j
			subw = maxx-minx
			subh = maxy-miny
			if (subw > 0 and subh > 0):	
				derp = cv.GetSubRect(img,(minx,miny,subw,subh))#use orig image
				a=pygame.image.frombuffer(derp.tostring(),cv.GetSize(derp),"RGB")
				a.set_colorkey(a.get_at((0,0)))
				segs.append(a)
				
	return segs
	

def loadSpriteSheet(filename):
	img = cv.LoadImage(filename)
	segs = segment(img)
	return segs



