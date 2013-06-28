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

currentTileDex = 0


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
		global currentTileDex
		currentTileDex = self.tiledex
		print "currentTileDex is " + str(currentTileDex)


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
		global currentTileDex
		self.cbutts=[]	#control buttons - the ones to select current tile
		self.tiles=[]	#tile buttons - the ones that make up the map
		#some variables to keep track of drawing state
		currentTileDex = 0
		self.drawMode = App.DRAW_SINGLE
		self.currentTile = (0,0)
		self.drawRect_orig = (0,0)
		self.drawRect_point = (5,5)

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
		self.canvas.configure(xscrollcommand=self.hsb.set,scrollregion=(0,0,480,480),confine=True)
		self.canvas.bind("<Configure>",self.resize_frame)
		self.canvas.bind("<Button-1>",self.leftClickHandler)
		self.canvas.bind("<Motion>",self.motionHandler)

		self.middleFrame = Frame(self)
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
	
	def motionHandler(self,mevent):
		#print dir(event)
		#print "currentTiledex " + str(self.currentTileDex)
		self.currentTile = (int(self.canvas.canvasx( int(mevent.x/16))),int( self.canvas.canvasy(int(mevent.y/16))))
		print self.currentTile
		print "x,y: " +  str(mevent.x) + ", " + str(mevent.y)
		if (self.drawMode == App.DRAW_FREE):
			self.drawCurrentTile(event=mevent)
		elif (self.drawMode == App.DRAW_RECT):
			self.drawRect_point = self.currentTile
			#can we do something to draw a temporary box?
			#ie just draw a shitty rectangle... refresh image, then draw
			self.refreshTiles()
			start=tuple(16*x for x in self.drawRect_orig)
			end=tuple(16*(x + 1)  for x in self.drawRect_point)
			self.canvas.create_rectangle( start,end ,outline="green",width="3")
					

	def drawCurrentTile(self, event=None,tilex=0,tiley=0):
		global currentTileDex
		if event is not None:
			x = self.canvas.canvasx(event.x)
			y = self.canvas.canvasy(event.y)
			#get the tile to which this refers...
			tilex = int(x/16)
			tiley = int(y/16)
		self.tiles[tilex][tiley].tiledex = currentTileDex
		self.tiles[tilex][tiley].image = convertImage(self.tilesheet[currentTileDex])
		self.canvas.create_image((16*tilex,16*tiley),image=self.tiles[tilex][tiley].image,anchor="nw")
		print "printler"
	
	def refreshTiles(self):
		self.canvas.delete("all")
		for x in range(len(self.tiles)):
			for y in range(len(self.tiles[0])):
				self.canvas.create_image((16*x,16*y),image=self.tiles[x][y].image,anchor="nw")

	def leftClickHandler(self,event):
		self.drawCurrentTile(event)

		#setup the clickable tiles
	def setupTileButtons(self):
		for x in range(len(self.tilesheet)):
			c = tileButton(self.bottomFrame,self.tilesheet[x],x)
			c.config(image=c.image)#command=    need to make new tile picking handler
			c.grid(row= (x / 30),column= (x%30))
			self.cbutts.append(c)

	def fillSquare( self):
		orig = self.drawRect_orig
		end = self.drawRect_point
		for x in range(min(orig[0],end[0]),max(orig[0],end[0])+1):
			for y in range(min(orig[1],end[1]),max(orig[1],end[1])+1):
				self.drawCurrentTile(tilex=x,tiley=y) #use none because we dont have an event object, use x and y
			
	
			
	
	
	def keyPressHandler (self,event):
		if (event.keysym == "space" and self.drawMode == App.DRAW_SINGLE):
			self.drawMode = App.DRAW_FREE
		elif (event.keysym == "space" and self.drawMode == App.DRAW_FREE):
			self.drawMode = App.DRAW_SINGLE
		elif (event.keysym == "Shift_L" and self.drawMode == App.DRAW_SINGLE):
			self.drawMode = App.DRAW_RECT
			self.drawRect_orig = self.currentTile
			self.drawRect_point = self.currentTile
		elif (event.keysym == "Shift_L" and self.drawMode == App.DRAW_RECT):
			self.drawMode = App.DRAW_SINGLE
			self.refreshTiles()
			self.fillSquare()
	
	def resize_frame (self,e):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
	
		
	
	def task(self):
		#print drawRect_orig

		#self.drawTileButtons()
		#self.drawCanvas()

		self.after(20,self.task)
	
	

if __name__ == "__main__":
	app = App(None)
	app.after(20,app.task)
	app.mainloop()



