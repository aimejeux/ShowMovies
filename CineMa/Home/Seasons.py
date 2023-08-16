# -*- coding: utf-8 -*-
#!/usr/bin/python
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Components.Pixmap import Pixmap
from enigma import ePixmap, eTimer, ePoint, gPixmapPtr
from Components.AVSwitch import AVSwitch
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Components.Sources.StaticText import StaticText
import json, os, re
##################################################################
from enigma import ePoint, eSize, eTimer,ePicLoad
from enigma import getDesktop
################################################ yasser
black,white,gray='\c00000000','\c00??????','\c00808080'
blue,green,red,yellow,cyan,magenta,ivory='\c000000??','\c0000??00','\c00??0000','\c00????00','\c0000????','\c00??00??','\c0???????'
#########################################
#########################################
dwidth = getDesktop(0).size().width()
#########################################
from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.AllImport import *
from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.MyImportCima import *
from Plugins.Extensions.ShowMovies.CineMa.Home.SeasonsImport import SeasonsEpisodes
path = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/FilsJs/Episodes.js'
path1 = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/FilsJs/Seasons.js'
class HomeShowMoviesSeasons(Screen,SeasonsEpisodes):
	def __init__(self, session, Mydict,Title,Poster,UrlOrg):
		SeasonsEpisodes.__init__(self)
		if dwidth == 1280:
		    with open(PLUGIN_PATH_SKIN + '/HomeShowMoviesSeasons.xml', 'r') as f:
		        self.skin = f.read()
		        f.close()
		else:
		    with open(PLUGIN_PATH_SKIN + '/HomeShowMoviesSeasons.xml', 'r') as f:
		        self.skin = f.read()
		        f.close()
		##############################
		self['actions'] = ActionMap(['ShowMoviesPanelActions'], {'cancel': self.exit,
			'left': self.left,
			'right': self.right,
			"down": self.keyDown,
			"up": self.keyUp,
			'ok': self.ok,
		}, -1)
		self.session = session
		Screen.__init__(self, session)
		self.onLayoutFinish.append(self.decodeImage)
		self.onLayoutFinish.append(self.ShowImage)
		# ##############################Ditc Infos
		self.NewDictSaison = {}
		self.Mydict = Mydict
		############################## path for Posters
		self.Poster = Poster
		self.UrlOrg = UrlOrg
		self.a = 0
		self.MyDictSeas = {}
		try:self.MyPath = self.Poster
		except:self.MyPath = '/media/hdd/CineMa/'+'i_0.png'
		##############################Rating
		try:self.Rating = self.Mydict.get('rating','')
		except:self.Rating = 0
		try:self.watchBTn = self.Mydict.get('Watchability','')
		except:self.watchBTn = 'nada'
		self.Title = Title
		self.Import_MyInfosSeasons()
		##############################Start
	##############################keyDown
	def keyDown(self):
		if self['menu'].getSelectionIndex() == len(self.menu)-1:self['menu'].moveToIndex(0)
		else:self['menu'].down()
	##############################keyUp
	def keyUp(self):
		if self['menu'].getSelectionIndex() == 0:self['menu'].moveToIndex(len(self.menu)-1)
		else:self['menu'].up()
	##############################left
	def right(self):
		self['menu'].pageDown()
	##############################right
	def left(self):
		self['menu'].pageUp()
	##############################ok get_Episodes
	def ok(self):
		saiso = self['menu'].getCurrent()[0]
		self.watchBTn = self.Seasons.get(saiso,'')[1]
		Sais = get_Episodes(self.watchBTn)
		if Sais:
		    self.NewDictSaison = Read_Js(path)
		    self.session.open(HomeShowMoviesEpisodes,self.NewDictSaison,self.MyDictSeas,self.Title,self.Poster,self.Rating)
		else:self.session.open(MessageBox, _('Maaaafffihacheeeeeeee'), MessageBox.TYPE_INFO)
	##############################exit
	def exit(self, ret=None):
		self.close(True)
#############################################################
class HomeShowMoviesEpisodes(Screen,):
	def __init__(self, session, Mydict,MyDictSeas,Title,Poster,Rating):
		if dwidth == 1280:
		    with open(PLUGIN_PATH_SKIN + '/HomeShowMoviesEpisodes.xml', 'r') as f:
		        self.skin = f.read()
		        f.close()
		else:
		    with open(PLUGIN_PATH_SKIN + '/HomeShowMoviesEpisodes.xml', 'r') as f:
		        self.skin = f.read()
		        f.close()
		#self.session = session		
		##############################
		self['actions'] = ActionMap(['ShowMoviesPanelActions'], {'cancel': self.exit,
			'left': self.left,
			'right': self.right,
			"down": self.keyDown,
			"up": self.keyUp,
			'ok': self.ok,
		}, -1)
		self.session = session
		Screen.__init__(self, session)
		self.onLayoutFinish.append(self.decodeImage)
		self.onLayoutFinish.append(self.ShowImage)
		self.onLayoutFinish.append(self.MyInfosEpisodes)
		# ##############################Ditc Infos
		self.NewDictSaison = {}
		self.Mydict = Mydict
		self.picload = ePicLoad()
		self.Showss = False
		self.menu = []
		self['menu'] = m2list([])
		for x in range(7):
		    self['InfosFlm_'+str(x)] = Label()
		############################## path for Posters
		self.Poster = Poster
		self['Posters'] = Pixmap()
		self['Img_star'] = Pixmap()
		self.a = 0
		self.timer = eTimer()
		try:self.MyPath = self.Poster
		except:self.MyPath = '/media/hdd/CineMa/'+'i_0.png'
		##############################Rating
		try:self.Rating = Rating
		except:self.Rating = 0
		self.Title = Title
		try:self.Youtub = self.Mydict.get('Youtub','')
		except:self.Youtub='....'
		self.MyDictSeasEp = MyDictSeas
		self.Import_MyInfosEpisodes()
	##############################Start
	def Import_MyInfosEpisodes(self):
		self.Seasons = self.Mydict
		if len(self.Seasons)!=0:
		    self.d2 = sorted(self.Seasons.items(), key=lambda t: t[1][0])
		    for keys in self.d2:
		        if keys[0] == 'Youtub':continue
		        self.menu.append(show_SeasEpsod(str(keys[1][0])))
		else:self.menu.append(show_SeasEpsod('Not Data'))
		self['menu'].l.setList(self.menu)
		self['menu'].l.setItemHeight(50)
		self['InfosFlm_0'].setText(self.Title)
		try:
		    self.timer.callback.append(self.resizeList)
		except:
		    self.timer_conn = self.timer.timeout.connect(self.resizeList)
		self.timer.start(10, True)
	def resizeList(self):
		self.timer.stop()
		a = 50*len(self.menu)
		self['menu'].instance.resize(eSize(500, a))
	##############################keyDown
	def MyInfosEpisodes(self):
		if len(self.menu)!=0 and self['menu'].getCurrent()[0]!= 'Not Data':
		    if len(self.MyDictSeasEp)!=0:#' \c0000????'
		        #self.Showss = True
		        try:
		            changelist = ['original Name','Country','Presentation Date','Duration','Language']
		            self.Rating = self.MyDictSeasEp.get('Rating_s','')
		            self['InfosFlm_1'].setText('Rating : \c0000????'+str(self.Rating))
		            b = self.MyDictSeasEp.get('Genre_s','')
		            p = ''
		            for g in b:
		                p += g.decode('utf-8')+','
		            self['InfosFlm_2'].setText('Genre : \c0000????'+str(p))
		            c = self.MyDictSeasEp.get('Item_s','')
		            k = ''
		            for v in c:
		                k+=v[0].decode('utf-8')+' '+v[1].decode('utf-8')+'\n\t'
		            self['InfosFlm_3'].setText('Item : \c0000????'+str(k))
		            d = self.MyDictSeasEp.get('Title_s','')
		            self['InfosFlm_4'].setText('Title : \c0000????'+str(d))
		            m = self.MyDictSeasEp.get('Discrpt_S','').decode('utf-8')
		            self['InfosFlm_5'].setText('\c0000????'+str(m))
		            self.TestRating()
		        except:
		            self['InfosFlm_1'].setText('..........')
		            self['InfosFlm_2'].setText('..........')
		            self['InfosFlm_3'].setText('..........')
		            self['InfosFlm_4'].setText('..........')
		            self['InfosFlm_5'].setText('..........')
		    else:
		        self['InfosFlm_1'].setText('..........')
		        self['InfosFlm_2'].setText('..........')
		        self['InfosFlm_3'].setText('..........')
		        self['InfosFlm_4'].setText('..........')
		        self['InfosFlm_5'].setText('..........')
		else:
		    self['InfosFlm_1'].setText('..........')
		    self['InfosFlm_2'].setText('..........')
		    self['InfosFlm_3'].setText('..........')
		    self['InfosFlm_4'].setText('..........')
		    self['InfosFlm_5'].setText('..........')
	def TestRating(self):
		if self.Rating != 'nada':
		    try:
		        a = self.Rating
		        x = 50*float(a)
		        b = "%.0f" % x
		        self['Img_star'].instance.resize(eSize(int(b), 50))
		    except:self['Img_star'].instance.resize(eSize(0, 0))
		else:self['Img_star'].instance.resize(eSize(0, 0))
	def decodeImage(self):
		self['Posters'].instance.resize(eSize(500, 750))#######185,278
	def ShowImage(self):
		picfile = self.MyPath
		picobject = self['Posters']
		picobject.instance.setPixmap(gPixmapPtr())
		self.scale = AVSwitch().getFramebufferScale()
		size = picobject.instance.size()
		self.picload = ePicLoad()
		self.picload.setPara((500,700,0,0,0,0,'#80000000'))
		if self.picload.startDecode(picfile, 0, 0, False) == 0:
		    ptr = self.picload.getData()
		    if ptr != None:
		        picobject.instance.setPixmap(ptr)
		        picobject.show()
		        del self.picload
	def keyDown(self):
		if self['menu'].getSelectionIndex() == len(self.menu)-1:self['menu'].moveToIndex(0)
		else:self['menu'].down()
	##############################keyUp
	def keyUp(self):
		if self['menu'].getSelectionIndex() == 0:self['menu'].moveToIndex(len(self.menu)-1)
		else:self['menu'].up()
	##############################left
	def right(self):
		#if self.Move:
		self['menu'].pageDown()
	##############################right
	def left(self):
		#if self.Move:
		self['menu'].pageUp()
	##############################ok get_Episodes
	def Trailler(self):
		self['menu'].show()
		self.menu = []
		if self.Youtub=='nada':
		    self.ImportShowMovies()
		    return
		Si,self.ListShows_1 = get_Youtub_link(self.Youtub)
		if Si:
		    self.ListShows_1 = self.ListShows_1
		self.ImportShowMovies()
	def ImportShowMovies(self):
		index = self['menu'].getSelectionIndex()
		self.watchBTn = self.Seasons["Episodes_"+str(index+1)][1]
		if self.watchBTn=='nada':return
		Si,self.ListShows = get_D1(self.watchBTn)
		if Si:
		    self.Title = self['menu'].getCurrent()[0]
		    if self.Youtub!='nada':self.ListShows_1 +=self.ListShows
		    else:self.ListShows_1 =self.ListShows
		    self.session.open(ShowEpisodes,self.ListShows_1,self.MyDictSeasEp,self.Title,self.Poster,self.Rating)
		else:
		    self.session.open(MessageBox, _('تعذر الوصول الى روابط المشاهدة'), MessageBox.TYPE_INFO)
	def ok(self):
		self.Trailler()
	##############################exit
	def exit(self, ret=None):
		self.close(True)
#############################################################
class ShowEpisodes(Screen,):
	def __init__(self, session, Mydict,MyDictSeas,Title,Poster,Rating):
		if dwidth == 1280:
		    with open(PLUGIN_PATH_SKIN + '/ShowEpisodes.xml', 'r') as f:
		        self.skin = f.read()
		        f.close()
		else:
		    with open(PLUGIN_PATH_SKIN + '/ShowEpisodes.xml', 'r') as f:
		        self.skin = f.read()
		        f.close()
		##############################
		self['actions'] = ActionMap(['ShowMoviesPanelActions'], {'cancel': self.exit,
			'left': self.left,
			'right': self.right,
			"down": self.keyDown,
			"up": self.keyUp,
			'ok': self.ok,
			'green': self.Download_with_FreeDownloadYano
		}, -1)
		self.session = session
		Screen.__init__(self, session)
		self.onLayoutFinish.append(self.decodeImage)
		self.onLayoutFinish.append(self.ShowImage)
		self.onLayoutFinish.append(self.MyInfosEpisodes)
		# ##############################Ditc Infos
		self.NewDictSaison = {}
		self.Mydict = Mydict
		self.picload = ePicLoad()
		#self.Showss = False
		self.menu = []
		self['menu'] = m2list([])
		for x in range(7):
		    self['InfosFlm_'+str(x)] = Label()
		############################## path for Posters
		self.Poster = Poster
		#self.UrlOrg = UrlOrg
		self['Posters'] = Pixmap()
		self['Img_star'] = Pixmap()
		self.a = 0
		self.timer = eTimer()
		try:self.MyPath = self.Poster
		except:self.MyPath = '/media/hdd/CineMa/'+'i_0.png'
		##############################Rating
		try:self.Rating = Rating
		except:self.Rating = 0
		self.Title = Title
		self.MyDictSeasEp = MyDictSeas
		self.Write_Js_Yano()
		self.Import_MyInfosEpisodes()
	##############################Start
	def Write_Js_Yano(self):
		path = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/FilsJs/DownloadMovies.js'
		Dicremove = {'url':'nada','filename':'nada'}
		with open(path,'w') as chcfg:
		    json.dump(Dicremove, chcfg,ensure_ascii=False)
		print "OK"
	def Import_MyInfosEpisodes(self):
		self.Seasons = self.Mydict
		if len(self.Seasons)!=0:
		    for a in self.Seasons:
		        if 'Trailer' in a[0]:F = "\c00??????Trailer \c0000????mp4|720p"
		        else:F='\c00??????Watch - \c0000????'+a[0]
		        self.menu.append(show_SeasEpsod(F))
		else:self.menu.append(show_SeasEpsod('Not Data'))
		self['menu'].l.setList(self.menu)
		self['menu'].l.setItemHeight(50)
		self['InfosFlm_0'].setText(self.Title)
		try:
		    self.timer.callback.append(self.resizeList)
		except:
		    self.timer_conn = self.timer.timeout.connect(self.resizeList)
		self.timer.start(10, True)
	def resizeList(self):
		self.timer.stop()
		a = 50*len(self.menu)
		self['menu'].instance.resize(eSize(500, a))
	##############################keyDown
	def MyInfosEpisodes(self):
		if len(self.menu)!=0 and self['menu'].getCurrent()[0]!= 'Not Data':
		    if len(self.MyDictSeasEp)!=0:#' \c0000????'
		        try:
		            changelist = ['original Name','Country','Presentation Date','Duration','Language']
		            self.Rating = self.MyDictSeasEp.get('Rating_s','')
		            self['InfosFlm_1'].setText('Rating : \c0000????'+str(self.Rating))
		            b = self.MyDictSeasEp.get('Genre_s','')
		            p = ''
		            for g in b:
		                p += g.decode('utf-8')+','
		            self['InfosFlm_2'].setText('Genre : \c0000????'+str(p))
		            c = self.MyDictSeasEp.get('Item_s','')
		            k = ''
		            for v in c:
		                k+=v[0].decode('utf-8')+' '+v[1].decode('utf-8')+'\n\t'
		            self['InfosFlm_3'].setText('Item : \c0000????'+str(k))
		            d = self.MyDictSeasEp.get('Title_s','')
		            self['InfosFlm_4'].setText('Title : \c0000????'+str(d))
		            m = self.MyDictSeasEp.get('Discrpt_S','').decode('utf-8')
		            self['InfosFlm_5'].setText('\c0000????'+str(m))
		            self.TestRating()
		        except:
		            self['InfosFlm_1'].setText('..........')
		            self['InfosFlm_2'].setText('..........')
		            self['InfosFlm_3'].setText('..........')
		            self['InfosFlm_4'].setText('..........')
		            self['InfosFlm_5'].setText('..........')
		    else:
		        self['InfosFlm_1'].setText('..........')
		        self['InfosFlm_2'].setText('..........')
		        self['InfosFlm_3'].setText('..........')
		        self['InfosFlm_4'].setText('..........')
		        self['InfosFlm_5'].setText('..........')
		else:
		    self['InfosFlm_1'].setText('..........')
		    self['InfosFlm_2'].setText('..........')
		    self['InfosFlm_3'].setText('..........')
		    self['InfosFlm_4'].setText('..........')
		    self['InfosFlm_5'].setText('..........')
	def TestRating(self):
		if self.Rating != 'nada':
		    try:
		        a = self.Rating
		        x = 50*float(a)
		        b = "%.0f" % x
		        self['Img_star'].instance.resize(eSize(int(b), 50))
		    except:self['Img_star'].instance.resize(eSize(0, 0))
		else:self['Img_star'].instance.resize(eSize(0, 0))
	def decodeImage(self):
		self['Posters'].instance.resize(eSize(500, 750))#######185,278
	def ShowImage(self):
		picfile = self.MyPath
		picobject = self['Posters']
		picobject.instance.setPixmap(gPixmapPtr())
		self.scale = AVSwitch().getFramebufferScale()
		size = picobject.instance.size()
		self.picload = ePicLoad()
		self.picload.setPara((500,700,0,0,0,0,'#80000000'))
		if self.picload.startDecode(picfile, 0, 0, False) == 0:
		    ptr = self.picload.getData()
		    if ptr != None:
		        picobject.instance.setPixmap(ptr)
		        picobject.show()
		        del self.picload
	def keyDown(self):
		if self['menu'].getSelectionIndex() == len(self.menu)-1:self['menu'].moveToIndex(0)
		else:self['menu'].down()
	##############################keyUp
	def keyUp(self):
		if self['menu'].getSelectionIndex() == 0:self['menu'].moveToIndex(len(self.menu)-1)
		else:self['menu'].up()
	##############################left
	def right(self):
		self['menu'].pageDown()
	##############################right
	def left(self):
		self['menu'].pageUp()
	##############################
	def ShowMoviesSelect3333333(self):
		import urllib2
		from enigma import eServiceReference
		from Screens.InfoBar import InfoBar, MoviePlayer
		from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.MyImportCima import get_player
		index = self['menu'].getSelectionIndex()
		name = self.Title
		rds = get_player()
		try:
		    stream_url = self.Seasons[index][1]
		except:
		    stream_url = 'nada'
		if stream_url!='nada':
		    if  stream_url.startswith('/hls2'): stream_url = 'https://s16.upstreamcdn.co'+stream_url
		    self.reference = eServiceReference(rds, 0, str(stream_url))
		    self.reference.setName(name)
		    self.session.open(MoviePlayer,self.reference)
	def ShowMoviesSelect(self):
		import urllib2
		from enigma import eServiceReference
		from Screens.InfoBar import InfoBar, MoviePlayer
		from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.MyImportCima import get_player
		index = self['menu'].getSelectionIndex()
		name = self.Title
		rds = get_player()
		#self.session.open(MessageBox, _('-------------'+str(self.Seasons[index])), MessageBox.TYPE_INFO)
		#return
		self.stream_url = self.Seasons[index][1]
		if 'Trailer' not in self.Seasons[index][0]:
		    Referer = self.Seasons[index][2]
		    a,NvUrl = get_D2(self.stream_url,Referer,'V')
		    if a:
		        self.stream_url = NvUrl[0][1]
		        #self.session.open(MessageBox, _('-------------'+str(self.stream_url)), MessageBox.TYPE_INFO)
		    else:
		        self.session.open(MessageBox, _('تعذر الوصول الى رابط المشاهدة'), MessageBox.TYPE_INFO)
		        return
		if  self.stream_url.startswith('/hls2'): self.stream_url = 'https://s16.upstreamcdn.co'+self.stream_url
		self.reference = eServiceReference(rds, 0, str(self.stream_url))
		self.reference.setName(name)
		self.session.open(MoviePlayer,self.reference)
	def ok(self):
		if len(self.menu)!=0 and self['menu'].getCurrent()[0]!= 'Not Data': self.ShowMoviesSelect()
		else:pass
	##############################exit
	def exit(self, ret=None):
		self.close(True)
	def Download_with_FreeDownloadYano(self):
		try:
		    from Components.Converter.FreeDownloadYano import FreeDownloadYano
		    self.ImportYano = True
		except:self.ImportYano = False
		self.MyDictJs = {}
		index = self['menu'].getSelectionIndex()
		self.MyDictJs['url']= self.Seasons[index][1]
		self.MyDictJs['filename']= '/media/hdd/CineMa/movie/[ShowMovies'+str(self.Title)+']'
		TXT = json.dumps(self.MyDictJs,indent = 4)
		export_txt(TXT,path='/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/FilsJs/DownloadMovies.js')
		if self.ImportYano==True:FreeDownloadYano('download')
		else:self.session.open(MessageBox, 'File FreeDownloadYano Not Found', MessageBox.TYPE_INFO, timeout=10)