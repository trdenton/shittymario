#!/usr/bin/python


# a horrible program written to produce level files.
# TODO: add ability to specify width
# TODO: add ability to change tile properties other than graphics
# TODO: add ability to scroll through width
# TODO: add export functionality


import level
import spritesheet
import Tkinter
import ImageTk
from Tkinter import *
from PIL import Image
import pygame
from pygame.locals import *

cbutts=[]	#control buttons - the ones to select current tile
tbutts=[]	#tile buttons - the ones that make up the map
currentTile = 0
dragMode = 0
#pygame.init()

print "loading tiles..."
tiles = spritesheet.loadTileSheet('SMB-Tiles.png',16,16,1,1)
class Butt:
	def __init__(self, master, tdex=0):
		self.tiledex = tdex
		self.setImage(tdex)
		self.maxdex=len(tiles)
		self.b=Button(master,command=self.setTile())
	def setTileDex(self, i):
		self.tiledex=i

	def setImage(self, tdex):
		self.tiledex=tdex
		self.image = convertImage(tiles[tdex])

	def setTile(self):
		def ret():
			self.tiledex = currentTile
			self.setImage(self.tiledex)		
		return ret
class TButt(Butt):
	def __init__(self, master, tdex=0):
		Butt.__init__(self,master,tdex)
		self.b.bind('<Motion>',self.enterB())

	def enterB(self):
		def ret(event):
			global dragMode
			if (dragMode):
				self.tiledex = currentTile
				self.setImage(self.tiledex)		
				#print "OVER!"
		return ret


		

def convertImage(im):
	image_str = pygame.image.tostring(im, 'RGB')         # use 'RGB' to export
	w, h      = (16, 16)
	pic     = Image.fromstring('RGB', (w, h), image_str) # use 'RGB' to import
	tkim = ImageTk.PhotoImage(pic)
	return tkim
		


def selectTile(x):
	def ret():
		global currentTile
		currentTile=x
		print "current tile is " + str(currentTile)
	return ret

def keyPressHandler (event):
	global dragMode
	dragMode=1-dragMode
	print "down"
def mouseUp (event):
	mouseIsDown=0
	print "up"

print "done!"
root = Tk()
root.bind('<KeyPress>', keyPressHandler)
#root.bind('<ButtonRelease-1>',mouseUp)
topFrame = Frame(root)
topFrame.pack(side=TOP)
topFrame.focus_set()
middleFrame = Frame(root,bg="red")
middleFrame.pack(side=TOP)
seperator = Label(middleFrame,text="^^MAP  VV TILES")
seperator.pack(side=LEFT)
#currentTileImage = Button(middleFrame)
bottomFrame=Frame(root)
bottomFrame.pack(side=BOTTOM)
root.title('Shitty Mario Level Editor')

for x in range(30):
	tbutts.append([])
	for y in range(30):
		b = TButt(topFrame,0)
		tbutts[x].append(b)
		tbutts[x][y].b.config(image=b.image)
		tbutts[x][y].b.grid(row=x,column=y)

for x in range(len(tiles)):
	c = Butt(bottomFrame,x)
	c.b.config(image=c.image,command=selectTile(x))
	c.b.grid(row= (x / 30),column= (x%30))
	cbutts.append(c)
	
	

def task():
	global currentTile
	for x in range(len(tbutts)):
		for y in range(len(tbutts[0])):
			b = tbutts[x][y]
			b.b.config(image=b.image)
			b.b.grid(row=x,column=y)	
	root.after(20,task)

root.after(20,task)
root.mainloop()
#just make a big scrollable grid, clicking on a tile toggles the type

