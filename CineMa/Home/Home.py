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
from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.Setup import ShowMovies_Config
from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.AllImport import *
from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.MyImportCima import *
from skin import loadSkin
from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.Setup import *
def get_Skin():
    if get_Activskin() == 'vertical':foldSkin = PLUGIN_PATH_SKIN + '/HomeShowMoviesV.xml'
    else:foldSkin = PLUGIN_PATH_SKIN + '/HomeShowMovies.xml'
    return foldSkin
class HomeShowMovies(Screen):
	def __init__(self, session, *args):
		with open(get_Skin(), 'r') as f:
		    self.skin = f.read()
		    f.close()
		self.session = session
		Screen.__init__(self, session)
		##############################
		self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'cancel': self.exit,
			'left': self.left,
			'right': self.right,
			"down": self.keyDown,
			"up": self.keyUp,
			'ok': self.ok,
		}, -1)
		self.onLayoutFinish.append(self.show_all_chang)
		self.picload = ePicLoad()
		self.menu = []
		self['menu'] = m2list([])
		##############################Start
		self['Version'] = Label()
		self['Version'].setText('Version '+str(getversioninfo()))
		try:
		    self.Host = GetHost('https://cimalek.art/')
		except:self.Host='cimalek.art'
		self.Url_0='https://'+self.Host+'/recent/movies/page/%s/'
		self.Url_1='https://'+self.Host+'/release/2023/page/%s/?type=movies'
		self.Url_2='https://'+self.Host+'/genre/science-fiction/page/%s/?type=movies'
		self.Url_3='https://'+self.Host+'/category/anime-movies/page/%s/'
		self.Url_4='https://'+self.Host+'/category/english-series/page/%s/'
		self.Url_5='https://'+self.Host+'/seasons/page/%s/'
		self.Url_6='https://'+self.Host+'/episodes/page/%s/'
		for x in range(8):
		    self['Selct_'+str(x)] = Pixmap()
		    if x == 0:self['Selct_'+str(x)].hide()
		    else:self['Selct_'+str(x)].show()
		self.My_List = [('Settings',"self.session.open(ShowMovies_Config)"),
		                ('Movies',"self.session.open(MenuShowMovies,Url='"+self.Url_0+"')"),
		                ('Years',"self.session.open(MenuShowMovies,Url='"+self.Url_1+"')"),
		                ('Genres',"self.session.open(MenuShowMovies,Url='"+self.Url_2+"')"),
		                ('Animations',"self.session.open(MenuShowMovies,Url='"+self.Url_3+"')"),
		                ('Series',"self.session.open(MenuShowMovies,Url='"+self.Url_4+"')"),
		                ('Seasons',"self.session.open(MenuShowMovies,Url='"+self.Url_5+"')"),
		                ('Episodes',"self.session.open(MenuShowMovies,Url='"+self.Url_6+"')")]
		for choix in self.My_List:
		    self.menu.append(show_Movies(choix))
		self['menu'].l.setList(self.menu)
		self['menu'].l.setItemHeight(35)
		self.Show_Image()
		##############################
	def show_all_chang(self):
		self.PosMenu = get_Activskin()
	def Show_Image(self):
		idx = self['menu'].getSelectionIndex()
		for x in range(8):
		    if x == idx:self['Selct_'+str(x)].hide()
		    else:self['Selct_'+str(x)].show()
	##############################keyDown
	def keyDown(self):
		if self.PosMenu == 'vertical':self['menu'].down()
		else:
		    idx = self['menu'].getSelectionIndex()
		    if idx in [0,1,2,3]:self['menu'].moveToIndex(idx+4)
		    else:self['menu'].moveToIndex(idx-4)
		self.Show_Image()
	##############################keyUp
	def keyUp(self):
		if self.PosMenu == 'vertical':self['menu'].up()
		else:
		    idx = self['menu'].getSelectionIndex()
		    #self.session.open(MessageBox, _('keyUp ='+str(idx)), MessageBox.TYPE_INFO)
		    if idx in [4,5,6,7]:self['menu'].moveToIndex(idx-4)
		    else:self['menu'].moveToIndex(idx+4)
		self.Show_Image()
	##############################left
	def right(self):
		if self.PosMenu == 'vertical':self['menu'].pageDown()
		else:
		    idx = self['menu'].getSelectionIndex()
		    if idx == len(self.menu)-1:self['menu'].moveToIndex(0)
		    else:self['menu'].moveToIndex(idx+1)
		self.Show_Image()
	##############################right
	def left(self):
		if self.PosMenu == 'vertical':self['menu'].pageUp()
		else:
		    idx = self['menu'].getSelectionIndex()
		    if idx == 0:self['menu'].moveToIndex(len(self.menu)-1)
		    else:self['menu'].moveToIndex(idx-1)
		self.Show_Image()
	##############################ok
	def ok(self):
		exec(self['menu'].getCurrent()[0][1])
	##############################exit
	def exit(self, ret=None):
		self.close(True)