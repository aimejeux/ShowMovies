# -*- coding: utf-8 -*-
#!/usr/bin/python
from Screens.Screen import Screen
from sys import version_info
from Components.ActionMap import ActionMap
##################################################################
from enigma import getDesktop
################################################ yasser
black,white,gray='\c00000000','\c00??????','\c00808080'
blue,green,red,yellow,cyan,magenta,ivory='\c000000??','\c0000??00','\c00??0000','\c00????00','\c0000????','\c00??00??','\c0???????'
################################################ yasser
PY3 = version_info[0] == 3
##################################################################My Imort
from Plugins.Extensions.ShowMovies.Cimalek.OutilsCimalek.MyImportCimalek import ShowMovies_New,get_D1,get_Info_Film,get_Taille
from Plugins.Extensions.ShowMovies.Cimalek.OutilsCimalek.AllImport import *
from Plugins.Extensions.ShowMovies.Cimalek.Home.Watchability import HomeShowMoviesSelect
#########################################
from enigma import eServiceReference
#########################################
#########################################
dwidth = getDesktop(0).size().width()
#########################################
class MenuShowMovies(Screen,ShowMovies_New):
	def __init__(self, session, *args):
		ShowMovies_New.__init__(self)
		if dwidth == 1280:
		    with open(PLUGIN_PATH_SKIN + '/MainTestAnimFHD.xml', 'r') as f:
		        self.skin = f.read()
		        f.close()
		else:
		    with open(PLUGIN_PATH_SKIN + '/MainTestAnimFHD.xml', 'r') as f:
		        self.skin = f.read()
		        f.close()
		self.session = session
		Screen.__init__(self, session)
		self['actions'] = ActionMap(['DirectionActions','SetupActions','ColorActions'], {'cancel': self.exit,#self['actions'] = ActionMap(['ShowMoviesPanelActions'], {'cancel': self.exit,
			'left': self.left,
			'right': self.right,
			"down": self.keyDown,
			"up": self.keyUp,
			'ok': self.ok,
			#'green': self.affich_DEbut,
			'green': self.Import_My_Watch_Url,
			'blue': self.Import_second_Page,
			'yellow': self.Clear_Folder_Img,
		}, -1)
		self.affich_DEbut()
	##############################
	def affich_DEbut(self):
		self.onLayoutFinish.append(self.layoutFinish)
		self.getposi_image()
		self.ImportImages()
		self.onLayoutFinish.append(self.decodeImage)
		self.onLayoutFinish.append(self.showDescAnim)
		self.onLayoutFinish.append(self.setText_Films)
		self.onLayoutFinish.append(self.TestRating)
	##############################
	def Regroupement(self):
		self.Moveframe()
		self.decodeImage()
		self.setText_Films()
		self.TestRating()
	##############################
	def keyDown(self):
		self['menu'].down()
		idx = self['menu'].getSelectionIndex()
		self.Regroupement()
	##############################
	def keyUp(self):
		self['menu'].up()
		idx = self['menu'].getSelectionIndex()
		self.Regroupement()
	##############################
	def left(self):
		self['menu'].pageUp()
		idx = self['menu'].getSelectionIndex()
		self.Regroupement()
	##############################
	def right(self):
		self['menu'].pageDown()
		idx = self['menu'].getSelectionIndex()
		self.Regroupement()
	##############################
	# def Moveframe(self):
		# self.yx = self.y11
		# self.dyx = (self.y22 - self.y11) // 40
		# if self.newupdateLabel in self.AnimTimer.callback:
		    # self.AnimTimer.callback.remove(self.newupdateLabel)
		    # self.AnimTimer.callback.append(self.showDescAnim)
		# self.AnimTimer.start(100//10, True)
	##############################
	def Import_My_Watch_Url(self):
		self.Import_My_Infos()
	##############################
	def ShoHid(self):
		self['Infos'].show()
	##############################
	def Import_second_Page(self):
		self.moniTimer.stop()
		self.Timer.stop()
		self.getposi_image()
		self.ImportImages()
		self.decodeImage()
		self.setText_Films()
		self.TestRating()
		self.Moveframe()
	#############################
	# def Import_My_Infos(self):
		# if self.Msg_[0]:
		    # index = self['menu'].getSelectionIndex()
		    # _H = self.NewListJS.items()[index][1][1]
		    # self._Info = get_Info_Film(_H)
		    # self.watc = ''
		    # i= 4
		    # List_Secour = ['الاسم الاصلي'.encode('utf-8'),'البلد المنشئ'.encode('utf-8'),'المدة'.encode('utf-8'),'تاريخ العرض'.encode('utf-8'),'اللغة'.encode('utf-8')]
		    # if len(self._Info)!=0:
		        # _Title = self['menu'].getCurrent()[0]
		        # self.session.open(HomeShowMoviesSelect,self._Info,_Title)
	##############################
	def ok(self):
		if self.Msg_[0]:
		    self.Timer.stop()
		    self.AnimTimer.stop()
		    self.Import_My_Infos()
	##############################
	def exit(self, ret=None):
		self.Timer.stop()
		self.AnimTimer.stop()
		self.close(True)
	##############################
	def Clear_Folder_Img(self):
		Milef = '/media/hdd/Cimalek/Images/'
		for root, dirs, files in os.walk(Milef):
		    for f in files:
		        os.unlink(os.path.join(root, f))
		Taill_Fold = get_Taille()
		self['Infos'].setText('Image File Size : \c0000????'+str(Taill_Fold))
