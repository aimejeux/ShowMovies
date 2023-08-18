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
path = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/FilsJs/Episodes.js'
path1 = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/FilsJs/Seasons.js'
class HomeShowMoviesSelect(Screen):
	def __init__(self, session, Mydict,Title):
		if dwidth == 1280:
		    with open(PLUGIN_PATH_SKIN + '/HomeShowMoviesSelect.xml', 'r') as f:
		        self.skin = f.read()
		        f.close()
		else:
		    with open(PLUGIN_PATH_SKIN + '/HomeShowMoviesSelect.xml', 'r') as f:
		        self.skin = f.read()
		        f.close()
		self.session = session		
		##############################
		self['actions'] = ActionMap(['ShowMoviesPanelActions'], {'cancel': self.exit,
			'left': self.left,
			'right': self.right,
			"down": self.keyDown,
			"up": self.keyUp,
			'ok': self.ok,
			'blue': self.Trailler,
			'green': self.ShowMoviesSelect ,
		}, -1)
		Screen.__init__(self, session)
		self.picload = ePicLoad()
		self.menu = []
		self['menu'] = m2list([])
		self['menu'].hide()
		self["action"] = Label()
		self["action"].hide()
		self.onLayoutFinish.append(self.decodeImage)
		self.onLayoutFinish.append(self.ShowImage)
		self.onLayoutFinish.append(self.TestRating)
		self.onLayoutFinish.append(self.Show_Image_Home)
		self.FoldImag = '/media/hdd/CineMa/Images/'
		self.homeImage = '/media/hdd/CineMa/Home/home.'
		##############################Posters
		self['Posters'] = Pixmap()
		self['Img_star'] = Pixmap()
		self['PostersHome'] = Pixmap()
		##############################Ditc Infos
		self.NewDictSaison = {}
		self.Mydict = Mydict
		############################## path for Posters
		try:self.MyPath = self.FoldImag+self.Mydict.get('poster','')
		except:self.MyPath = '/media/hdd/CineMa/'+'i_0.png'
		##############################Rating
		try:self.Rating = self.Mydict.get('rating','')
		except:self.Rating = 0
		try:self.watchBTn = self.Mydict.get('Watchability','')
		except:self.watchBTn = 'nada'
		self.Title = Title
		##############################List
		self.Move = False
		self.Showss = False
		self.Youtsss = False
		self.List_Secour = ['الاسم الاصلي'.encode('utf-8'),'البلد المنشئ'.encode('utf-8'),'المدة'.encode('utf-8'),'تاريخ العرض'.encode('utf-8'),'اللغة'.encode('utf-8')]
		##############################Start
		try:self.Youtub = self.Mydict.get('Youtub','')
		except:self.Youtub='....'
		for x in range(7):
		    changelist = ['original Name','Country','Presentation Date','Duration','Language']
		    a = self.Mydict.items()[x][0].replace('About The Movie','')
		    b = self.Mydict.items()[x][1]
		    if a == 'Watchability': b = 'watchBTn Ok'
		    elif a == 'Film Properties':
		        d = b.split('\n')
		        e = ''
		        try:
		            for t in range(5):
		                #e += '\c00??????'+changelist[t]+ ' : \c0000????'+d[t].replace('  ','')+'\n'
		                e += '\c00??????'+changelist[t]+ ' : \c00????00'+d[t].replace('  ','')+'\n'
		            e += '\c00??????'+'Youtub'+ ' : \c00????00'+self.Youtub
		        except:
		            for t in range(len(d)):#????00
		                #e += ' \c0000????'+d[t].replace('  ','')+'\n'
		                e += ' \c00????00'+d[t].replace('  ','')+'\n'
		        c = str(a)+' : '+str(e)
		    else:c = str(a) + ' : \c00????00'+str(b)#c = str(a) + ' : \c0000????'+str(b)
		    self['InfosFlm_'+str(x)] = Label()
		    self['InfosFlm_'+str(x)].setText(c)
		#self.Show_Image() original name,country of origin,Presentation date,duration,the language
		##############################
		#self.decodeImage()
		#self.ShowImage()
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
	def TestRating(self):
		if self.Rating != 'nada':
		    try:
		        a = self.Rating
		        x = 50*float(a)
		        b = "%.0f" % x
		        self['Img_star'].instance.resize(eSize(int(b), 50))
		    except:self['Img_star'].instance.resize(eSize(0, 0))
		else:self['Img_star'].instance.resize(eSize(0, 0))
	def Show_Image_Home(self):#self.homeImage
		Url = self.watchBTn
		if self.watchBTn=='nada':return
		_Data = get_Data(Url,get='get',typ='content')
		if _Data != '':
		    try:
		        rgx = '''<meta property="og:image" content="(.+?)" >'''
		        HomeImg = re.findall(rgx,_Data)[0]
		    except:HomeImg='nada'
		    if HomeImg !='nada':
		        try:
		            self.typ = HomeImg.split('/')[-1]
		            self.typ = self.typ.split('.')[-1]
		            Repns = Downloads_Images_Home(HomeImg,self.homeImage+str(self.typ))
		        except:Repns=False
		    if Repns: self.ShowImageHome()
	def ShowImageHome(self):
		picfile = self.homeImage+str(self.typ)
		picobject = self['PostersHome']
		picobject.instance.setPixmap(gPixmapPtr())
		self.scale = AVSwitch().getFramebufferScale()
		size = picobject.instance.size()
		self.picload = ePicLoad()
		self.picload.setPara((1920,1080,0,0,0,0,'#80000000'))
		if self.picload.startDecode(picfile, 0, 0, False) == 0:
		    ptr = self.picload.getData()
		    if ptr != None:
		        picobject.instance.setPixmap(ptr)
		        picobject.show()
		        del self.picload
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
		if self.watchBTn=='nada':return
		Si,self.ListShows = get_D1(self.watchBTn)
		if Si:
		    if self.Youtub=='nada':self.ListShows_1 =self.ListShows
		    else:self.ListShows_1 +=self.ListShows
		    F = ''
		    for a in self.ListShows_1:
		        if 'Trailer' in a[0]:F = "\c0000??00Trailer \c0000????mp4|720p"
		        else:F='\c00??????Watch - \c0000????'+a[0]
		        self.menu.append(show_Movies_2(F))
		    self.Move = True
		    self.Showss = True
		else:
		    self.menu.append(show_Movies('Not Found'))
		    self.Move = False
		    self.Showss = False
		self['menu'].l.setList(self.menu)
		self['menu'].l.setItemHeight(50)
		self["action"].hide()
		self.resizeList()
	def resizeList(self):
		a = 50*len(self.menu)
		self['menu'].instance.resize(eSize(500, a))#######185,278
	def ShowMoviesSelect(self):
		import urllib2
		from enigma import eServiceReference
		from Screens.InfoBar import InfoBar, MoviePlayer
		from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.MyImportCima import get_player
		index = self['menu'].getSelectionIndex()
		name = self.Title
		rds = get_player()
		#self.session.open(MessageBox, _('-------------'+str(self.ListShows_1[index])), MessageBox.TYPE_INFO)
		#return
		self.stream_url = self.ListShows_1[index][1]
		if 'Trailer' not in self.ListShows_1[index][0]:
		    Referer = self.ListShows_1[index][2]
		    a,NvUrl = get_D2(self.stream_url,Referer,'V')
		    if a:
		        self.stream_url = NvUrl[0][1]
		        #self.session.open(MessageBox, _('-------------'+str(self.stream_url)), MessageBox.TYPE_INFO)
		    else:
		        self.session.open(MessageBox, _('تعذر الوصول الى رابط المشاهدة'), MessageBox.TYPE_INFO)
		        self["action"].hide()
		        return
		if  self.stream_url.startswith('/hls2'): self.stream_url = 'https://s16.upstreamcdn.co'+self.stream_url
		self.reference = eServiceReference(rds, 0, str(self.stream_url))
		self.reference.setName(name)
		self.session.open(MoviePlayer,self.reference)
		self["action"].hide()
	##############################keyDown
	def StarDownload(self, txt, function):
		self["action"].show()
		self["action"].setText(txt)
		self.timer = eTimer()
		try:
		    self.timer_conn = self.timer.timeout.connect(function)
		except:
		    self.timer.callback.append(function)
		self.timer.start(1, True)
	def keyDown(self):
		if self.Move:self['menu'].down()
	##############################keyUp
	def keyUp(self):
		if self.Move:self['menu'].up()
	##############################left
	def right(self):
		if self.Move:self['menu'].pageDown()
	##############################right
	def left(self):
		if self.Move:self['menu'].pageUp()
	##############################ok
	def ok(self):
		if self.Showss == False:
		    self.StarDownload(_("Wait Download Server ..."), self.Trailler)
		    #self.Trailler()#self.ImportShowMovies()
		else:
		    self.StarDownload(_("Wait Download Server Movie..."), self.ShowMoviesSelect)
		    #self.ShowMoviesSelect()
	##############################exit
	def exit(self, ret=None):
		self.close(True)