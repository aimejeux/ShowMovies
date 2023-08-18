# -*- coding: utf-8 -*-
#!/usr/bin/python
from Screens.Screen import Screen
from sys import version_info
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
##################################################################
from enigma import getDesktop, eTimer,eServiceReference
from Components.Label import Label
import os,time
################################################ yasser
black,white,gray='\c00000000','\c00??????','\c00808080'
blue,green,red,yellow,cyan,magenta,ivory='\c000000??','\c0000??00','\c00??0000','\c00????00','\c0000????','\c00??00??','\c0???????'
################################################ yasser
PY3 = version_info[0] == 3
##################################################################My Imort
from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.MyImportCima import ShowMovies_New,get_D1,get_Info_Film,get_Taille
from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.AllImport import *
from Plugins.Extensions.ShowMovies.CineMa.Home.Watchability import HomeShowMoviesSelect
from Plugins.Extensions.ShowMovies.CineMa.Home.Seasons import HomeShowMoviesSeasons
#########################################
#########################################
#########################################
dwidth = getDesktop(0).size().width()
#########################################
URLOTST = "https://imdb-video.media-imdb.com/vi1209648153/hls-preview-7fb41ae7-af9b-4224-a0f7-7bcc2988b433.m3u8?Expires=1691785913\u0026Signature=SsLUMYNVGies01G6k29474VAeHAudkfbC8c4DdbRoBfoI5StM~wLAlIFEnaSztnH~Nq5y0U5bHhypWs9nq6SYTtk9Bm2DBR3E9Caw3RGzNSeMjYa7IJ2mnaZb1fIv3oygGq~n-vbWRhE34SIKLR2kt7ogepE6DNEKOhpCsyIp2n2DnCG08NIyqrJUsVfwUbc~zZLlxRf-jdK0g49b7RboxIousWXxm3XfvMdGZRVScrxsozkTslBHyci12ex1esveJ0cXNcgyx-JtlIOAns0xgRUIqsZM~78wSZvakFu~c~dLrXUGkrlLNJcW4nBQa~xs93nCEUly3R5CDz3HaUIwA__\u0026Key-Pair-Id=APKAIFLZBVQZ24NQH3KA".replace('\u0026','&')
class MenuShowMovies(Screen,ShowMovies_New):
	def __init__(self, session,Url=None):
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
			#'yellow': self.TestImdb,
			'green': self.Import_My_Watch_Url,
			'blue': self.Import_second_Page,
			#'yellow': self.animate_text,
		}, -1)
		if Url is not None:self.Url = Url
		else:self.Url = None
		self["action"] = Label()
		self["action"].hide()
		self.onLayoutFinish.append(self.AffichTitles)
		self.affich_DEbut()
	##############################
	def TestImdb(self):
		from enigma import eServiceReference
		from Screens.InfoBar import InfoBar, MoviePlayer
		name = 'badi3elzeman'
		stream_url = URLOTST
		self.reference = eServiceReference(5002, 0, str(stream_url))
		self.reference.setName(name)
		self.session.open(MoviePlayer,self.reference)
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
		idx = self['menu'].getSelectionIndex()
		if idx == 0:self['menu'].moveToIndex(len(self.menu)-1)
		else:self['menu'].pageUp()
		self.Regroupement()
	##############################
	def right(self):
		idx = self['menu'].getSelectionIndex()
		if idx == len(self.menu)-1:self['menu'].moveToIndex(0)
		else:self['menu'].pageDown()
		self.Regroupement()
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
	##############################
	def StarDownload(self, actiontext, function):
		self["action"].show()
		self["action"].setText(actiontext)
		self.timer = eTimer()
		try:
		    self.timer_conn = self.timer.timeout.connect(function)
		except:
		    self.timer.callback.append(function)
		self.timer.start(1, True)
	def ok(self):
		if self.Msg_[0]:
		    self.Timer.stop()
		    self.AnimTimer.stop()
		    self.StarDownload(_("Wait Download data..."), self.Import_My_Infos)
	##############################
	def exit(self, ret=None):
		self.Timer.stop()
		self.AnimTimer.stop()
		self.close(True)
	##############################
	def Clear_Folder_Img(self):
		Milef = '/media/hdd/CineMa/Images/'
		for root, dirs, files in os.walk(Milef):
		    for f in files:
		        os.unlink(os.path.join(root, f))
		Taill_Fold = get_Taille()
		self['Infos'].setText('Image File Size : \c0000????'+str(Taill_Fold))