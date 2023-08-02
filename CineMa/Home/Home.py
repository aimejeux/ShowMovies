# -*- coding: utf-8 -*-
#!/usr/bin/python
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Components.Pixmap import Pixmap
from enigma import ePixmap, eTimer, ePoint
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Components.Sources.StaticText import StaticText
import json, os 
##################################################################
from enigma import ePoint, eSize, eTimer,ePicLoad
from enigma import getDesktop
################################################ yasser
black,white,gray='\c00000000','\c00??????','\c00808080'
blue,green,red,yellow,cyan,magenta,ivory='\c000000??','\c0000??00','\c00??0000','\c00????00','\c0000????','\c00??00??','\c0???????'
#########################################
PLUGIN_PATH_SKIN = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/Skins'
#########################################
dwidth = getDesktop(0).size().width()
#########################################
from Plugins.Extensions.ShowMovies.TestMove import MenuShowMovies
class HomeShowMovies(Screen):
	def __init__(self, session, *args):
		if dwidth == 1280:
		    with open(PLUGIN_PATH_SKIN + '/HomeShowMovies.xml', 'r') as f:
		        self.skin = f.read()
		        f.close()
		else:
		    with open(PLUGIN_PATH_SKIN + '/HomeShowMovies.xml', 'r') as f:
		        self.skin = f.read()
		        f.close()
		self.session = session
		##############################Pixmap
		for x in range(5):
		    self['Selct_'+str(x)] = Pixmap()
		    if x == 0:self['Selct_'+str(x)].hide()
		    else:self['Selct_'+str(x)].show()
		##############################
		self['actions'] = ActionMap(['ShowMoviesPanelActions'], {'cancel': self.exit,
			'left': self.left,
			'right': self.right,
			"down": self.keyDown,
			"up": self.keyUp,
			'ok': self.ok,
		}, -1)
		Screen.__init__(self, session)
		self.picload = ePicLoad()
		self.menu = []
		##############################Start
		self.My_List = ['self.session.open(MenuShowMovies)','','','','']
		self.Index = 0
		self.Show_Image()
		##############################
		self.Pox = 400
		self.Poy = 350
	def Show_Image(self):
		if self.Index > 4: self.Index = 0
		if self.Index < 0: self.Index = 4
		for t in range(5):
		    if t == self.Index:self['Selct_'+str(t)].hide()
		    else:self['Selct_'+str(t)].show()
	##############################keyDown
	def keyDown(self):
		self.Index = self.Index + 1
		self.Show_Image()
	##############################keyUp
	def keyUp(self):
		self.Index = self.Index - 1
		self.Show_Image()
	##############################left
	def right(self):
		self.Index = self.Index + 1
		self.Show_Image()
	##############################right
	def left(self):
		self.Index = self.Index - 1
		self.Show_Image()
	##############################ok
	def ok(self):
		if self.Index > 4: self.Index = 0
		if self.Index == 0: exec(self.My_List[0])
	##############################exit
	def exit(self, ret=None):
		self.close(True)