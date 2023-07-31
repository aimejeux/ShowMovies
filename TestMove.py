# -*- coding: utf-8 -*-
#!/usr/bin/python
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Components.Pixmap import Pixmap
from enigma import ePixmap, eTimer, ePoint, gPixmapPtr
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Components.Sources.StaticText import StaticText
import json
import os
from sys import version_info
##################################################################ADJ
##################################################################
from Components.AVSwitch import AVSwitch
from enigma import ePoint, eSize, eTimer,ePicLoad
from enigma import getDesktop
################################################ yasser
black,white,gray='\c00000000','\c00??????','\c00808080'
blue,green,red,yellow,cyan,magenta,ivory='\c000000??','\c0000??00','\c00??0000','\c00????00','\c0000????','\c00??00??','\c0???????'
################################################ yasser
PY3 = version_info[0] == 3
##################################################################My Imort
from Plugins.Extensions.ShowMovies.Cimalek.OutilsCimalek.MyImportCimalek import get_My_Donnees,Read_Js,ClearProf,get_D1,get_Info_Film,get_Taille
from Plugins.Extensions.ShowMovies.Cimalek.OutilsCimalek.AllImport import *
from Plugins.Extensions.ShowMovies.Cimalek.Home.Watchability import HomeShowMoviesSelect
#########################################
from enigma import eServiceReference
#########################################
#########################################
dwidth = getDesktop(0).size().width()
#########################################
############start of list
###############end of list
class MenuShowMovies(Screen):
	def __init__(self, session, *args):
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
		y1, y2 = (1080, 535)
		self.y1 = y1
		self.y2 = y2
		self.y = y1
		self.dy = (y1 - y2) // 21
		##############################
		y11, y22 = (-1080, 30)
		self.y11 = y11
		self.y22 = y22
		self.yx = y11
		self.dyx = (y22 - y11) // 30
		##############################Pixmap
		self['Img_star'] = Pixmap()
		##############################Label
		self['rating'] =StaticText()
		self['Title_Film'] = Label()
		self['Infos'] = Label()
		self['Infos'].setText('wait ......... data download')
		#self['Infos'].hide()
		self['Infos_indx'] = Label()
		self['Infos_indx'].setText('')
		self.FoldImag = '/media/hdd/Cimalek/Images/'
		self.watchBTn = False
		##############################
		for x in range(10):
			self['poster_'+str(x)] = Pixmap()
			self['poster_'+str(x)].show()
		for x in range(9):
		    self['Box_'+str(x)] = Label()
		for x in range(1,10):
		    self['Title_'+str(x)] = Label()
		self.NewListJS = {}
		##############################Timer
		self.moniTimer = eTimer()
		self.timeaffich = eTimer()
		#self.moniTimer.callback.append(self.updatePoster)
		#self.moniTimer.timeout.get().append(self.affich_Menu)
		self.Timer = eTimer()
		self.Timer.callback.append(self.updatePoster)
		self.AnimTimer = eTimer()
		self.AnimTimer.callback.append(self.newupdateLabel)
		#self.onLayoutFinish.append(self.layoutFinish)
		##############################
		self.Page = 1
		self.picload = ePicLoad()
		self.menu = []
		self['menu'] = m2list([])
		# self.menuWatch = []
		# self['menu_Watch'] = []
		#self['menu_Watch'].hide()
		##############################Start
		#self.onShown.append(self.affich_Infos_cond)
		self.affich_DEbut()
		self.Pox = 400
		self.Poy = 350
		self.Condit = 1
	def affich_DEbut(self):
		self.onLayoutFinish.append(self.layoutFinish)
		self.getposi_image()
		self.ImportImages()
		self.onLayoutFinish.append(self.decodeImage)
		
		#self.onLayoutFinish.append(self.newlayoutFinish)
		self.onLayoutFinish.append(self.showDescAnim)
		self.onLayoutFinish.append(self.setText_Films)
		self.onLayoutFinish.append(self.TestRating)
		#self.onLayoutFinish.append(self.ConvertDeco)
	def ConvertDeco(self):
		self.x = self.Pox
		self.y = self.Poy
		self.w = 500
		self.h = 0
		self.moniTimer.start(200)
	def TestRating(self):
		if self.Msg_[0]:
		    try:
		        index = self['menu'].getSelectionIndex()
		        _H = self.NewListJS.items()[index][1]
		        a = _H[4]
		        x = 50*float(a)
		        b = "%.0f" % x
		        self['Img_star'].instance.resize(eSize(int(b), 50))
		    except:self['Img_star'].instance.resize(eSize(0, 0))
		else:self['Img_star'].instance.resize(eSize(0, 0))
		# self.Timer.stop()
		# self.AnimTimer.stop()
		# self.ConvertDeco()
	def affich_Menu(self):
		#self.moniTimer.stop()
		self['menu'].instance.resize(eSize(int(self.w), int(self.h)))
		if self.h < self.Poy:
		    self.h += self.Poy //60
		    self.moniTimer.start(50)
		else:
		    self.moniTimer.stop()
	def ImportImages(self):
		self.timeaffich.stop()
		self.menu = []
		uri = '''https://w.cimalek.to/category/aflam-online/'''
		uri1= '''https://w.cimalek.to/category/aflam-online/page/%s/''' % (str(self.Page))
		uri2= '''https://w.cimalek.to/recent/'''
		uri3= '''https://w.cimalek.to/category/aflam-online/page/255/'''
		uri4='''https://w.cimalek.to/recent/page/1325/'''
		self.Msg_ = get_My_Donnees(uri1)
		if self.Msg_[0]:
		    self.NewListJS = Read_Js()
		    for _dons in self.NewListJS:
		        Prblm = self.NewListJS[_dons][0]#ClearProf(_dons)
		        self.menu.append(show_Movies(str(Prblm)))
		    self.pagination = self.Msg_[2]
		    p_1 =self.pagination[0]
		    p_2 =self.pagination[1]
		    _B = 'الصفحة'.encode('utf-8')+'  '+str(p_1)+' / '+str(p_2)
		    self['Infos_indx'].setText(_B)
		    if self.Page < int(p_2):self.Page = int(p_1) + 1
		    else:self.Page=1
		    TxC = 'p_1 = '+str(p_1)+'\n'+'p_2 = '+str(p_2)+'\nPage = '+str(self.Page)+'\n'+str(uri1)+'\n====================\n'
		    Write_Donnees(TxC)
		else:
		    self.menu.append(show_Movies('Not Data'))
		self['menu'].l.setList(self.menu)
		self['menu'].l.setItemHeight(35)
		self['menu'].moveToIndex(0)
		##############################List_Film
	def newlayoutFinish(self):#
		if self.Msg_[0]:
		    index = self['menu'].getSelectionIndex()
		    _H = self.NewListJS.items()[index][1]
		    a = 'Title        :  \c0000????'+str(_H[0]).replace('nada','........')
		    b = 'Rating     :  \c0000????'+str(_H[4]).replace('nada','........')
		    c = 'Quality    :  \c0000????'+str(_H[5]).replace('nada','........')
		    d = 'Descpt    :  \c0000????'+str(_H[6]).replace('nada','........')#.replace('\n','\n\t')
		    Msg = [a,b,c,d]
		    self['rating'].setText(_H[4])
		    for tx in range(4):
		        v = Msg[tx]
		        v = v.replace('[','').replace(']','').replace('N/A','...')
		        self['Box_'+str(tx)].setText(str(v))
		    self['Box_0'].instance.move(ePoint(self.yx, 35))
		    self['Box_1'].instance.move(ePoint(self.yx, 90))
		    self['Box_2'].instance.move(ePoint(self.yx, 145))
		    self['Box_3'].instance.move(ePoint(self.yx, 200))
		    #self['Infos'].setText(str(_H[0]))
		    #self['Infos'].instance.move(ePoint(self.yx, 835))
		    Z = self.Msg_[2]
		    self.AnimTimer.start(100//10, True)
		    self['Infos_indx'].setText(str(Z[0])+' / '+str(Z[1]))
		##############################
	def layoutFinish(self):
		if self.Msg_[0]:
		    for x in range(10):
		        self['poster_'+str(x)].instance.move(ePoint(0, 1080))
		    self.Timer.start(100//10, True)
		##############################
	def updatePoster(self):
		p = self['poster_0'].instance.position()
		#self.y -= 2703
		self.y -= self.dy+10
		self['poster_0'].instance.move(ePoint(5, self.y-800))
		self['poster_1'].instance.move(ePoint(5, self.y))
		self['poster_2'].instance.move(ePoint(218, self.y))
		self['poster_3'].instance.move(ePoint(431, self.y))
		self['poster_4'].instance.move(ePoint(644, self.y))
		self['poster_5'].instance.move(ePoint(857, self.y))
		self['poster_6'].instance.move(ePoint(1070, self.y))
		self['poster_7'].instance.move(ePoint(1283, self.y))
		self['poster_8'].instance.move(ePoint(1496, self.y))
		self['poster_9'].instance.move(ePoint(1709, self.y))
		if self.y > 792:#if self.y > self.y2:##
			self.Timer.start(100//10, True)
		else:
			self.Timer.stop()
			#self.session.open(MessageBox, _(), MessageBox.TYPE_INFO)
	##############################
	def newupdateLabel(self):
		self.yx += +100#self.dyx
		#self['Infos'].instance.move(ePoint(self.yx, 835))
		#self['Title_Film'].instance.move(ePoint(self.yx, 35))
		self['Box_0'].instance.move(ePoint(self.yx+500, 5))
		self['Box_1'].instance.move(ePoint(self.yx+500, 55))
		self['Box_2'].instance.move(ePoint(self.yx+500, 110))
		self['Box_3'].instance.move(ePoint(self.yx+500, 165))
		if self.yx < self.y22:
			self.AnimTimer.start(100//10, True)
		else:
			self.AnimTimer.stop()
	def newupdateLabel555555(self):
		#self.yx += self.dyx
		self.yx += 100
		#self['Infos'].instance.move(ePoint(self.yx, 835))
		#self['Title_Film'].instance.move(ePoint(self.yx, 35))
		self['Box_0'].instance.move(ePoint(self.yx, 750))
		self['Box_1'].instance.move(ePoint(self.yx, 835))
		self['Box_2'].instance.move(ePoint(self.yx, 885))
		self['Box_3'].instance.move(ePoint(self.yx, 935))
		if self.yx < self.y22:
			self.AnimTimer.start(100//10, True)
		else:
			self.AnimTimer.stop()
	##############################
	def Regroupement(self):
		self.Moveframe()
		self.decodeImage()
		self.setText_Films()
		self.TestRating()
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
	def setText_Films(self):
		if self.Msg_[0]:
		    #self['Infos'].setText('wait ......... data download')
		    self.setText_Films_1()
	def setText_Films_1(self):
		index = self['menu'].getSelectionIndex()
		Y = len(self.NewListJS)-1
		if index == Y:
		    Nw_List =[0,1,2,3,4,5,6,7,8]
		    for x in range(1,10):
		        V = Nw_List[x-1]
		        _G = self.NewListJS.items()[V][1]
		        self['Title_'+str(x)].setText(str(_G[0]))
		elif index+10 > Y:
		    Nw_List = range(index,Y+1)+[0,1,2,3,4,5,6,7,8]
		    for x in range(1,10):
		        V = Nw_List[x]
		        _G = self.NewListJS.items()[V][1]
		        self['Title_'+str(x)].setText(str(_G[0]))
		else:
		    try:
		        for x in range(1,10):
		            _G = self.NewListJS.items()[x+index][1]
		            self['Title_'+str(x)].setText(str(_G[0]))
		    except:
		        _G = self['menu'].getCurrent()[0]
		        # self['Title_'+str(8)].setText(str(_G))
		        self.session.open(MessageBox, _(str(_G)+'\nindex ='+str(index)), MessageBox.TYPE_INFO)
		p_1 =self.pagination[0]
		p_2 =self.pagination[1]
		_B = 'الصفحة'.encode('utf-8')+'  '+str(p_1)+' / '+str(p_2)
	##############################
	def Moveframe(self):
		self.yx = self.y11
		self.dyx = (self.y22 - self.y11) // 40
		if self.newupdateLabel in self.AnimTimer.callback:
		    self.AnimTimer.callback.remove(self.newupdateLabel)
		    self.AnimTimer.callback.append(self.showDescAnim)
		self.AnimTimer.start(100//10, True)
	##############################\c0000????
	def showDescAnim(self):
		if self.Msg_[0]:
		    self.yx += self.dyx+100
		    index = self['menu'].getSelectionIndex()
		    _H = self.NewListJS.items()[index][1]
		    a = 'Title        :  \c0000????'+str(_H[0]).replace('nada','........')
		    b = 'Rating     :  \c0000????'+str(_H[4]).replace('nada','........')
		    c = 'Quality    :  \c0000????'+str(_H[5]).replace('nada','........')
		    d = 'Descpt    :  \c0000????'+str(_H[6]).replace('nada','........')#.replace('\n','\n\t')
		    self['rating'].setText(_H[4])
		    Msg = [a,b,c,d]
		    for tx in range(4):
		        v = Msg[tx]
		        v = v.replace('[','').replace(']','').replace('N/A','...')
		        self['Box_'+str(tx)].setText(str(v))
		    self['Box_0'].instance.move(ePoint(self.yx+500, 5))
		    self['Box_1'].instance.move(ePoint(self.yx+500, 55))
		    self['Box_2'].instance.move(ePoint(self.yx+500, 110))
		    self['Box_3'].instance.move(ePoint(self.yx+500, 165))
		    #self['Infos'].setText(str(_H[0]))
		    #self['Infos'].instance.move(ePoint(self.yx, 835))
		    self.AnimTimer.start(100//10, True)
		    #p = self['Box_0'].instance.position()
		    if self.yx < self.y22:
		        self.AnimTimer.start(100//10, True)
		    else:
		        self.AnimTimer.stop()
		Taill_Fold = get_Taille()
		self['Infos'].setText('Image File Size : \c0000????'+str(Taill_Fold))
	##############################
	def getposi_image(self):
		self.Positions = [(5,37),(5,792),(218,792),(431,792),(644,792),(857,792),(1070,792),(1283,792),(1496,792),(1709,792)]
		self.sizeimag = [(185,278)]
	##############################
	def decodeImage(self):
		#self.AnimTimer.stop()
		if self.Msg_[0]:
		    #self['Infos'].setText('wait ......... data download')
		    self.decodeImage_6(0)
	##############################
	def decodeImage_50(self,b):
		self['poster_'+str(b)].instance.resize(eSize(500, 750))#######185,278
	##############################
	def decodeImage_6(self,cty):
		Ds , Fs = 0,0
		self.index = self['menu'].getSelectionIndex()
		if self.index == len(self.NewListJS)-1:
		    self.decodeImage_uniq()
		    return
		elif self.index+10 == len(self.NewListJS):Ds,Fs =self.index,len(self.NewListJS)
		elif self.index+10 > len(self.NewListJS):
		    self.decodeImage_uniq_2(self.index)
		    return
		else:Ds,Fs =self.index,self.index+10
		for f in range(self.index,Fs):
		    _H = self.NewListJS.items()[f][1]
		    picfile = self.FoldImag+str(_H[3])
		    picobject = self['poster_'+str(f-self.index)]	
		    picobject.instance.setPixmap(gPixmapPtr())
		    self.scale = AVSwitch().getFramebufferScale()
		    self.picload = ePicLoad()
		    size = picobject.instance.size()
		    if f-self.index == 0:self.picload.setPara((500,700,0,0,0,0,'#80000000'))
		    else:self.picload.setPara((185,278,0,0,0,0,'#80000000'))
		    if self.picload.startDecode(picfile, 0, 0, False) == 0:
		        ptr = self.picload.getData()
		        if ptr != None:
		            picobject.instance.setPixmap(ptr)
		            picobject.show()
		            del self.picload
		return
	def decodeImage_uniq(self):
		Nw_List =[len(self.NewListJS)-1,0,1,2,3,4,5,6,7,8]
		for f in Nw_List:
		    _H = self.NewListJS.items()[f][1]
		    picfile = self.FoldImag+str(_H[3])
		    if f == Nw_List[0]:T=0
		    else:T=f+1
		    picobject = self['poster_'+str(T)]	
		    picobject.instance.setPixmap(gPixmapPtr())
		    self.scale = AVSwitch().getFramebufferScale()
		    size = picobject.instance.size()
		    self.picload = ePicLoad()
		    if T == 0:self.picload.setPara((500,700,0,0,0,0,'#80000000'))
		    else:self.picload.setPara((185,278,0,0,0,0,'#80000000'))
		    if self.picload.startDecode(picfile, 0, 0, False) == 0:
		        ptr = self.picload.getData()
		        if ptr != None:
		            picobject.instance.setPixmap(ptr)
		            picobject.show()
		            del self.picload
	##############################				
	def decodeImage_uniq_2(self,indx):
		Nw_List = []
		Y = len(self.NewListJS)-1
		Nw_List = range(indx,Y+1)+[0,1,2,3,4,5,6,7,8,9]
		for f in range(1,11):
		    f1 = Nw_List[f-1]
		    _H = self.NewListJS.items()[f1][1]
		    picfile = self.FoldImag+str(_H[3])
		    picobject = self['poster_'+str(f-1)]
		    picobject.instance.setPixmap(gPixmapPtr())
		    self.scale = AVSwitch().getFramebufferScale()
		    size = picobject.instance.size()
		    self.picload = ePicLoad()
		    if f1 == indx:self.picload.setPara((500,700,0,0,0,0,'#80000000'))
		    else:self.picload.setPara((185,278,0,0,0,0,'#80000000'))
		    if self.picload.startDecode(picfile, 0, 0, False) == 0:
		        ptr = self.picload.getData()
		        if ptr != None:
		            picobject.instance.setPixmap(ptr)
		            picobject.show()
		            del self.picload
	##############################
	def Import_My_Watch_Url(self):
		self.Import_My_Infos()
		return
		self.menuWatch =[]
		self['menu_Watch'] = []
		from enigma import eServiceReference
		from Screens.InfoBar import InfoBar, MoviePlayer
		MyFilms = ['nada']
		if self.watchBTn:
		    #self.watc
		    sft,_Df = get_D1(self.watc)
		    if sft:
		        #MyFilms = _Df
		        if len(_Df)!=0:
		            self.menuWatch = _Df
		            self['menu_Watch'].l.setList(self.menuWatch)
		            self['menu_Watch'].l.setItemHeight(35)
		            for a in self.menuWatch:
		                self.session.open(MessageBox, _(str(a[0])+'\n'+str(a[1])), MessageBox.TYPE_INFO)
		            #stream_url = _Df[0][1]
		            # name = self['menu'].getCurrent()[0]
		            # self.reference = eServiceReference(5002, 0, stream_url.encode('utf-8'))
		            # self.reference.setName(name)
		            # self.session.open(MoviePlayer,self.reference)
		        else:self.session.open(MessageBox, _('Not Data Film'), MessageBox.TYPE_INFO)
		    self.watchBTn = False
	def ShoHid(self):
		self['Infos'].show()
	def Import_second_Page(self):
		#self['Infos'].show()
		self.moniTimer.stop()
		self.Timer.stop()
		self.getposi_image()
		#self.ShoHid()
		self.ImportImages()
		self.decodeImage()
		self.setText_Films()
		self.TestRating()
		self.Moveframe()
		#self.layoutFinish()
		#self.Timer.callback.append(self.updatePoster)
		#self.AnimTimer.callback.append(self.newupdateLabel)
		#self.affich_DEbut()
		# self.session.open(MessageBox, _('watchBTn = '+str(self.watc)+'\n'+str(_H)+'\n'+str(_Info)), MessageBox.TYPE_INFO)
	##############################
	def Import_My_Infos(self):
		if self.Msg_[0]:
		    index = self['menu'].getSelectionIndex()
		    _H = self.NewListJS.items()[index][1][1]
		    self._Info = get_Info_Film(_H)
		    self.watc = ''
		    i= 4
		    List_Secour = ['الاسم الاصلي'.encode('utf-8'),'البلد المنشئ'.encode('utf-8'),'المدة'.encode('utf-8'),'تاريخ العرض'.encode('utf-8'),'اللغة'.encode('utf-8')]
		    if len(self._Info)!=0:
		        _Title = self['menu'].getCurrent()[0]
		        self.session.open(HomeShowMoviesSelect,self._Info,_Title)
		        # try:
		            # _Z = ''
		            # for keys in self._Info:
		                # a = self._Info[keys]
		                # if type(a)==list:
		                    # for q in a:
		                        # _Z += q+' '
		                    # a = _Z
		                # if keys=='Watchability':a = 'قابلية المشاهدة'.encode('utf-8')
		                # if keys=='About The Movie':a = cyan+str(a)
		                # else:a = str(keys)+'    :  '+cyan+str(a)
		                # self['Box_'+str(i)].setText(a)
		                # i = i +1
		                # if i>9:break
		            # self.watc = self._Info['Watchability']
		            # self.watchBTn = True
		        # except:
		            # for tx in range(4,9):
		                # v = '  .......'+List_Secour[tx-4]
		                # self['Box_'+str(tx)].setText(v)
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
	def Clear_Folder_Img(self):
		Milef = '/media/hdd/Cimalek/Images/'
		for root, dirs, files in os.walk(Milef):
		    for f in files:
		        os.unlink(os.path.join(root, f))
		Taill_Fold = get_Taille()
		self['Infos'].setText('Image File Size : \c0000????'+str(Taill_Fold))