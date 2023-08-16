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
########################################################################################Import themoviedb
api_key='b7cf9324cbeb6f4fb811144aa9397093'
searchT = "https://api.themoviedb.org/3/search/movie?include_adult=false&query=%s&language=fr&api_key=%s"
searchID= 'https://api.themoviedb.org/3/movie/%s?&append_to_response=videos&language=en&api_key=%s'
def get_TMDB_Search(ST):
    ListYoutub = {}#"https://api.themoviedb.org/3/search/movie?include_adult=false&query=%s&language=fr&api_key=b7cf9324cbeb6f4fb811144aa9397093" %ST
    ListYoutub_1 = {}
    url = searchT %(ST,api_key)
    try:data = get_Data(url,get='get',typ='json()')#St.get(url,verify=False).json()
    except:data='nada'
    if data=='nada':return False,ListYoutub
    if data!='nada':
        i = 1
        results = data['results']
        for keys in results:
            try:
                poster = keys['poster_path']
                if poster:poster = "https://image.tmdb.org/t/p/w500"+poster
            except:poster='nada'
            ListYoutub['poster']=poster
            try:title = keys['title']
            except:title='nada'
            ListYoutub['title']=title
            try:original_title = keys['original_title']
            except:original_title='nada'
            ListYoutub['original_title']=original_title
            try:overview = keys['overview']
            except:overview='nada'
            ListYoutub['overview']=overview
            try:backdrop_path = "https://image.tmdb.org/t/p/w500/"+keys['backdrop_path']
            except:backdrop_path='nada'
            ListYoutub['backdrop_path']=backdrop_path
            try:vote_count = keys['vote_count']
            except:vote_count='nada'
            ListYoutub['vote_count']=vote_count
            try:video = keys['video']
            except:video='nada'
            ListYoutub['video']=video
            try:vote_average = keys['vote_average']
            except:vote_average='nada'
            ListYoutub['vote_average']=vote_average
            try:genre_ids = keys['genre_ids']
            except:genre_ids='nada'
            ListYoutub['genre_ids']=genre_ids
            try:_id = keys['id']
            except:_id='nada'
            ListYoutub['_id']=_id
            try:original_language = keys['original_language']
            except:original_language='nada'
            ListYoutub['original_language']=original_language
            print "============================================",str(i)
            ListYoutub_1['_Donnees_'+str(i)]=ListYoutub
            i = i + 1
        return True,ListYoutub_1
    else:return False,ListYoutub_1
def get_TMDB_ID(_id):
    ListinfosID = {}#"https://api.themoviedb.org/3/search/movie?include_adult=false&query=%s&language=fr&api_key=b7cf9324cbeb6f4fb811144aa9397093" %ST
    url = searchID % (_id,api_key)
    try:data = get_Data(url,get='get',typ='json()')#St.get(url,verify=False).json()
    except:data='nada'
    if data=='nada':return False,ListinfosID
    if data!='nada':
        try:
            title = data['title']
        except:title='nada'
        ListinfosID['title']=title
        try:
            original_title = data['original_title']
        except:original_title='nada'
        ListinfosID['original_title']=original_title
        try:
            poster = "https://image.tmdb.org/t/p/w500"+data['poster_path']
        except:poster='nada'
        ListinfosID['poster']=poster
        try:
            countries = data['production_countries'][0]['name']
        except:countries='nada'
        ListinfosID['countries']=countries
        try:
            genres = data['genres']
            D = ''
            for k in genres:
                D += k['name']+' '
            #print D
        except:D='nada'
        ListinfosID['genres']=D
        try:
            videos = data['videos']['results'][0]
            key = videos['key']
            #print key
        except:key='nada'
        ListinfosID['videos']=key
        try:
            vote_count = data['vote_count']
        except:vote_count='nada'
        ListinfosID['vote_count']=vote_count
        try:
            original_language = data['original_language']
        except:original_language='nada'
        ListinfosID['original_language']=original_language
        try:
            imdb_id = data['imdb_id']
        except:imdb_id='nada'
        ListinfosID['imdb_id']=imdb_id
        try:
            F = ''
            production_companies = data['production_companies']
            for g in production_companies:
                F += g['name']+','
            #print "****",F
        except:F='nada'
        ListinfosID['production_companies']=F
        try:
            release_date = data['release_date']
        except:release_date='nada'
        ListinfosID['release_date']=release_date
        try:
            popularity = data['popularity']
        except:popularity='nada'
        ListinfosID['popularity']=popularity
        try:
            vote_average = data['vote_average']
        except:vote_average='nada'
        ListinfosID['vote_average']=vote_average
        return True,ListinfosID
    else:return False,ListinfosID
########################################################################################
class SeasonsEpisodes():
	def __init__(self):
		self.picload = ePicLoad()
		self.menu = []
		self['menu'] = m2list([])
		self['menu'].hide()
		#self.onLayoutFinish.append(self.decodeImage)
		#self.onLayoutFinish.append(self.ShowImage)
		#self.onLayoutFinish.append(self.TestRating)
		#self.onLayoutFinish.append(self.Show_Image_Home)
		self.FoldImag = '/media/hdd/CineMa/Images/'
		self.homeImage = '/media/hdd/CineMa/Home/home.'
		##############################Posters
		self['Posters'] = Pixmap()
		self['Img_star'] = Pixmap()
		self['PostersHome'] = Pixmap()
		self['InfosFlm_0'] = Label()
		self.timer = eTimer()
		##############################Ditc Infos
		self.MyDictSeas = {}
		# self.Mydict = Mydict
		# ############################## path for Posters
		# self.Poster = Poster
		# self.UrlOrg = UrlOrg
		# self.a = 0
		# try:self.MyPath = self.Poster
		# except:self.MyPath = '/media/hdd/CineMa/'+'i_0.png'
		# ##############################Rating
		# try:self.Rating = self.Mydict.get('rating','')
		# except:self.Rating = 0
		# try:self.watchBTn = self.Mydict.get('Watchability','')
		# except:self.watchBTn = 'nada'
		# self.Title = Title
		for x in range(7):
		    self['InfosFlm_'+str(x)] = Label()
		##############################List
		self.Move = False
		self.Showss = False
		self.List_Secour = ['الاسم الاصلي'.encode('utf-8'),'البلد المنشئ'.encode('utf-8'),'المدة'.encode('utf-8'),'تاريخ العرض'.encode('utf-8'),'اللغة'.encode('utf-8')]
		#self.Import_MyInfosSeasons()
	def Import_MyInfosSeasons(self):
		self.Seasons = Read_Js(path1)
		if len(self.Seasons)!=0:
		    self['menu'].show()
		    self.d2 = sorted(self.Seasons.items(), key=lambda t: t[1][0])
		    for keys in self.d2:
		        self.menu.append(show_Movies(str(keys[0])))
		else:self.menu.append(show_Movies('Not Data'))
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
		self.MyInfosSeasons()
	def MyInfosSeasons(self):
		if len(self.menu)!=0 and self['menu'].getCurrent()[0]!= 'Not Data':
		    rs,self.MyDictSeas = get_donnees_season(self.UrlOrg)
		    if rs and len(self.MyDictSeas)!=0:#' \c0000????'
		        #self.Showss = True
		        try:
		            changelist = ['original Name','Country','Presentation Date','Duration','Language']
		            self.Rating = self.MyDictSeas.get('Rating_s','')
		            self['InfosFlm_1'].setText('Rating : \c0000????'+str(self.Rating))
		            b = self.MyDictSeas.get('Genre_s','')
		            p = ''
		            for g in b:
		                p += g.decode('utf-8')+','
		            self['InfosFlm_2'].setText('Genre : \c0000????'+str(p))
		            c = self.MyDictSeas.get('Item_s','')
		            k = ''
		            for v in c:
		                k+=v[0].decode('utf-8')+' '+v[1].decode('utf-8')+'\n\t'
		            self['InfosFlm_3'].setText('Item : \c0000????'+str(k))
		            d = self.MyDictSeas.get('Title_s','')
		            self['InfosFlm_4'].setText('Title : \c0000????'+str(d))
		            m = self.MyDictSeas.get('Discrpt_S','').decode('utf-8')
		            self['InfosFlm_5'].setText('\c0000????'+str(m))
		            self.TestRating()
		        except:
		            self['InfosFlm_1'].setText('')
		            self['InfosFlm_2'].setText('')
		            self['InfosFlm_3'].setText('')
		            self['InfosFlm_4'].setText('')
		            self['InfosFlm_5'].setText('')
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
		Url = self.UrlOrg
		if self.UrlOrg=='nada':return
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
	def ImportShowMovies(self):
		saiso = self['menu'].getCurrent()[0]
		self.session.open(MessageBox, _(str(saiso)), MessageBox.TYPE_INFO)
		self.session.open(MessageBox, _(str(self.Seasons)), MessageBox.TYPE_INFO)
		self.watchBTn = self.Seasons.get(saiso,'')[1]
		self.session.open(MessageBox, _(str(self.watchBTn)), MessageBox.TYPE_INFO)
		if self.watchBTn=='nada':return
		Si,self.ListShows = get_Episodes(self.watchBTn)
		if Si:
		    self.session.open(MessageBox, _(str(self.ListShows)), MessageBox.TYPE_INFO)
		    #self.menu = self.ListShows
		    # for a in self.ListShows:
		        # self.menu.append(show_Movies_2('\c00??????Watch - \c0000????'+a[0]))
		    # # self['menu'].l.setList(self.menu)
		    # # self['menu'].l.setItemHeight(35)
		    # self.Move = True
		    # self.Showss = True
		# else:
		    # self.menu.append(show_Movies('Not Found'))
		    # self.Move = False
		    # self.Showss = False
		# self['menu'].l.setList(self.menu)
		# self['menu'].l.setItemHeight(35)
		# self.resizeList()
	def ShowMoviesSelect(self):
		from enigma import eServiceReference
		from Screens.InfoBar import InfoBar, MoviePlayer
		index = self['menu'].getSelectionIndex()
		name = self.Title
		stream_url = self.ListShows[index][1]
		type_movies = self.ListShows[index][0]
		if  stream_url.startswith('/hls2'): stream_url = 'https://s16.upstreamcdn.co'+stream_url
		#self.session.open(MessageBox, _(str(type_movies)+'\n'+str(name)+'\n'+str(stream_url)), MessageBox.TYPE_INFO)
		self.reference = eServiceReference(5002, 0, stream_url.encode('utf-8'))
		self.reference.setName(name)
		self.session.open(MoviePlayer,self.reference)