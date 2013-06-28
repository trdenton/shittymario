#!/usr/bin/python


# a horrible program written to produce level files.
# TODO: add ability to specify width
# TODO: add ability to change tile properties other than graphics
# TODO: add export functionality


import level
import spritesheet
import Tkinter
import ImageTk
from Tkinter import *
from PIL import Image
import pygame
from pygame.locals import *

def convertImage(im):
	image_str = pygame.image.tostring(im, 'RGB')         # use 'RGB' to export
	w, h      = (16, 16)
	pic     = Image.fromstring('RGB', (w, h), image_str) # use 'RGB' to import
	tkim = ImageTk.PhotoImage(pic)
	return tkim

class tileButton(Button):
	def __init__(self, master, i=None, tdex=0):
		Button.__init__(self,master)
		self.setImage(i)
		self.tiledex=tdex
		self.bind('<Button-1>',self.clickHandler)

	def setImage(self, i):
		self.image = convertImage(i)
	def clickHandler(self,event):
		self.master.currentTileDex = self.tiledex
		print dir(self.master)
		#print "currentTileDex is " + str(self.master.currentTileDex)


class Tile:
	def __init__(self, x=0,y=0,tdex=0):
		self.x=x
		self.y=y
		self.tiledex = tdex
		self.image = None
class App(Tk):
	(DRAW_SINGLE,DRAW_FREE,DRAW_RECT) = range(0,3)
	def __init__(self,parent):

		Tk.__init__(self,parent)
		self.initialize()
	
	def initialize(self):
		self.cbutts=[]	#control buttons - the ones to select current tile
		self.tiles=[]	#tile buttons - the ones that make up the map
		#some variables to keep track of drawing state
		self.currentTileDex = 0
		self.drawMode = App.DRAW_SINGLE
		self.dragMode = 0	#freeform drawing
		self.dragBoxMode=0	#drawing a rectangle
		self.currentTile = (0,0)
		self.dragBoxMode_orig = (0,0)
		self.dragBoxMode_point = (5,5)

		self.maxsize(900,800)

		#setup tk stuff
		self.bind('<KeyPress>', self.keyPressHandler)
		self.topFrame = Frame(self)
		self.topFrame.pack(side=TOP,expand=False)
		self.topFrame.focus_set()

		self.canvas = Canvas(self.topFrame,height="720",width="7200")
		self.hsb = Scrollbar(self.topFrame, orient="horizontal", command=self.canvas.xview)

		self.canvas.pack(side=TOP,expand=True)
		self.hsb.pack(side=TOP,fill="y")
		self.canvas.configure(xscrollcommand=self.hsb.set)
		self.canvas.bind("<Configure>",self.resize_frame)
		self.canvas.bind("<Button-1>",self.leftClickHandler)
		self.canvas.bind("<Motion>",self.motionHandler)

		self.middleFrame = Frame(self,bg="red")
		self.middleFrame.pack(side=TOP)

		self.seperator = Label(self.middleFrame,text="^^MAP  VV TILES")
		self.seperator.pack(side=LEFT)

		self.bottomFrame=Frame(self)
		self.bottomFrame.pack(side=BOTTOM)
		self.title('Shitty Mario Level Editor')

		self.tilesheet = spritesheet.loadTileSheet('SMB-Tiles.png',16,16,1,1)
 
		
		self.setupTileButtons()

		#setup tile structures
		for x in range(30):
			self.tiles.append([])
			for y in range(30):
				self.tiles[x].append(Tile(x,y))
	
	def motionHandler(self,event):
		#print "currentTiledex " + str(self.currentTileDex)
		if (self.drawMode == App.DRAW_FREE):
			self.drawCurrentTile(event)
		elif (self.drawMode == App.DRAW_RECT):
			print "ha"

	def drawCurrentTile(self, event):
		x = self.canvas.canvasx(event.x)
		y = self.canvas.canvasy(event.y)
		#get the tile to which this refers...
		tilex = int(x/16)
		tiley = int(y/16)
		self.tiles[tilex][tiley].tiledex = self.currentTileDex
		self.tiles[tilex][tiley].image = convertImage(self.tilesheet[self.currentTileDex])
		self.canvas.create_image((16*tilex,16*tiley),image=self.tiles[tilex][tiley].image,anchor="nw")

	def leftClickHandler(self,event):
		self.drawCurrentTile(event)

		#setup the clickable tiles
	def setupTileButtons(self):
		for x in range(len(self.tilesheet)):
			c = tileButton(self.bottomFrame,self.tilesheet[x],x)
			c.config(image=c.image)#command=    need to make new tile picking handler
			c.grid(row= (x / 30),column= (x%30))
			self.cbutts.append(c)

#	need to rewrite this badboy		
#	def fillSquare( orig, end ):
#		self.currentTileDex
#		self.tbutts
#		for x in range(min(orig[0],end[0]),max(orig[0],end[0])+1):
#			for y in range(min(orig[1],end[1]),max(orig[1],end[1])+1):
#				
#				b = tbutts[x][y].setTile()
#				b()
#				#b.b.config(image=b.image)
#				#b.b.grid(row=b.x,column=b.y)	
#			
	
			
	
	
	def keyPressHandler (self,event):
		if (event.keysym == "space"):
			self.dragMode=1-self.dragMode
		if (event.keysym == "Shift_L"):
			self.dragBoxMode = 1 - self.dragBoxMode
			if (self.dragBoxMode == 1):
				self.dragBoxMode_orig = self.currentTile
	
	def resize_frame (self,e):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
	
		
	
	def task(self):
		#print dragBoxMode_orig
			
		if (self.dragBoxMode):
			fillSquare(self.dragBoxMode_orig,self.dragBoxMode_point)	
		else:
			self.dragBoxMode_orig = self.currentTile
			self.dragBoxMode_point = self.currentTile

		#self.drawTileButtons()
		#self.drawCanvas()

		self.after(20,self.task)
	
	

if __name__ == "__main__":
	app = App(None)
	app.after(20,app.task)
	app.mainloop()



