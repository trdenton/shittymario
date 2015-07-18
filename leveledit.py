#!/usr/bin/python


# a horrible program written to produce level files.
# TODO: add ability to specify width
# TODO: add ability to change tile properties other than graphics
# TODO: add export functionality


import level
from level import Tile
import spritesheet
import Tkinter
import ImageTk
from Tkinter import *
import tkFileDialog
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

class App(Tk):
	(DRAW_SINGLE,DRAW_FREE,DRAW_RECT) = range(0,3)
	def __init__(self,parent):

		Tk.__init__(self,parent)
		self.initialize()
	
	def initialize(self):
		global currentTileDex
		self.cbutts=[]	#control buttons - the ones to select current tile
		#some variables to keep track of drawing state
		currentTileDex = 0
		self.drawMode = App.DRAW_SINGLE
		self.currentTile = (0,0)
		self.currentMouse=(0,0)
		self.drawRectOrigTile = (0,0)
		self.drawRectPointTile = (5,5)
		self.drawRectOrigMouse = (0,0)
		self.drawRectPointMouse = (5,5)

		self.maxsize(600,1000)


		self.canvas = Canvas(self,bg="white",height="480",scrollregion=(0,0,4800,480))
		self.canvas.pack()
		self.middleFrame = Frame(self,width="480",height="32")
		self.middleFrame.pack(side=TOP)
		self.middleFrame.pack_propagate(0)

		self.hsb = Scrollbar(self.middleFrame, orient="horizontal", command=self.canvas.xview)
		self.hsb.pack(side=TOP,fill=X)
		self.canvas.configure(xscrollcommand=self.hsb.set,xscrollincrement=16,confine=True)

		self.bind('<KeyPress>', self.keyPressHandler)
		self.canvas.bind("<Configure>",self.resize_frame)
		self.canvas.bind("<Button-1>",self.leftClickHandler)
		self.canvas.bind("<Motion>",self.motionHandler)


		self.seperator = Label(self.middleFrame,text="^^MAP  VV TILES")
		self.seperator.pack(side=BOTTOM)

		self.bottomFrame=Frame(self)
		self.bottomFrame.pack(side=BOTTOM)
		self.title('Shitty Mario Level Editor')

		self.tilesheet = spritesheet.loadTileSheet('SMB-Tiles.png',16,16,1,1)
 
		
		self.setupTileButtons()


		self.level = level.Level(300,30,"SMB-Tiles.png")
		
		self.menubar = Menu(self)
		self.menubar.add_command(label="Export...", command=self.exportCSV)
	
		# display the menu
		self.config(menu=self.menubar)
	
	def motionHandler(self,mevent):
		#print dir(event)
		#print "currentTiledex " + str(self.currentTileDex)
		self.currentMouse = (self.canvas.canvasx(mevent.x),self.canvas.canvasy(mevent.y))
		self.currentTile = (int(self.canvas.canvasx( int(mevent.x/16))),int( self.canvas.canvasy(int(mevent.y/16))))
		#print self.currentTile
		#print "x,y: " +  str(mevent.x) + ", " + str(mevent.y)
		if (self.drawMode == App.DRAW_FREE):
			self.drawCurrentTile(event=mevent)
		elif (self.drawMode == App.DRAW_RECT):
			self.drawRectPointTile = self.currentTile
			self.drawRectPointMouse = self.currentMouse
			#can we do something to draw a temporary box?
			#ie just draw a shitty rectangle... refresh image, then draw
			#self.refreshTiles()
			self.canvas.delete("selection")
			start = self.drawRectOrigMouse
			end = self.drawRectPointMouse
			#start=tuple(16*x for x in self.drawRectOrigTile)
			#end=tuple(16*(x + 1)  for x in self.drawRectPointTile)
			self.canvas.create_rectangle( start,end ,outline="green",width="3",tag="selection")
					

	def drawCurrentTile(self, event=None,tilex=0,tiley=0):
		global currentTileDex
		if event is not None:
			x = self.canvas.canvasx(event.x)
			y = self.canvas.canvasy(event.y)
			#get the tile to which this refers...
			tilex = int(x/16)
			tiley = int(y/16)
		
		#self.level.layout[tilex][tiley].image = convertImage(self.tilesheet[currentTileDex])
		self.level.layout[tilex][tiley].img = convertImage(self.tilesheet[currentTileDex])
		self.canvas.create_image((16*tilex,16*tiley),image=self.level.layout[tilex][tiley].img,anchor="nw")
	
	def refreshTiles(self):
		self.canvas.delete("all")
		for x in range(len(self.level.layout)):
			for y in range(len(self.level.layout[0])):
				if self.level.layout[x][y].img is not None:
					self.canvas.create_image((16*x,16*y),image=self.level.layout[x][y].img,anchor="nw")

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
		#orig = self.drawRectOrigTile
		#end = self.drawRectPointTile
		orig = tuple(int(x/16) for x in self.drawRectOrigMouse)
		end = tuple(int(x/16) for x in self.drawRectPointMouse)
		#end = self.drawRectPointMouse
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
			self.drawRectOrigTile = self.currentTile
			self.drawRectOrigMouse = self.currentMouse
			self.drawRectPointTile = self.currentTile
			self.drawRectPointMouse = self.currentMouse
		elif (event.keysym == "Shift_L" and self.drawMode == App.DRAW_RECT):
			self.drawMode = App.DRAW_SINGLE
			self.refreshTiles()
			self.fillSquare()
		elif (event.keysym == "r"):
			self.refreshTiles()
	
	def resize_frame (self,e):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
	
		
	def exportCSV(self ):
		fileName = tkFileDialog.asksaveasfilename(parent=self,filetypes=[("CSV File", "*.csv")],title="Save as...")
		f = open(fileName,'w')
		for y in range(len(self.tiles[0])):
			 f.write( ",".join(self.tiles[x][y].toString() for x in range(len(self.tiles))) + "\n")
			
	
	def task(self):
		#print drawRectOrigTile

		#self.drawTileButtons()
		#self.drawCanvas()

		self.after(20,self.task)
	
	

if __name__ == "__main__":
	app = App(None)
	app.after(20,app.task)
	app.mainloop()



