# -*- coding: utf-8 -*-
#!/usr/bin/python
from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Components.Pixmap import Pixmap
from enigma import ePixmap, eTimer, ePoint, gPixmapPtr
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS
from Components.Sources.StaticText import StaticText
import json
import os
from sys import version_info
##################################################################ADJ
from Tools.Directories import fileExists, pathExists
##################################################################
from Components.AVSwitch import AVSwitch
from Tools.BoundFunction import boundFunction
from enigma import ePoint, eSize, eTimer,ePicLoad
from enigma import getDesktop, eListboxPythonMultiContent, eListbox, gFont, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_WRAP, loadPNG
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest, MultiContentEntryPixmapAlphaBlend
################################################ yasser
black,white,gray='\c00000000','\c00??????','\c00808080'
blue,green,red,yellow,cyan,magenta,ivory='\c000000??','\c0000??00','\c00??0000','\c00????00','\c0000????','\c00??00??','\c0???????'
################################################ yasser
PY3 = version_info[0] == 3
##################################################################My Imort
from Plugins.Extensions.ShowMovies.Cimalek.OutilsCimalek.MyImportCimalek import get_My_Donnees,Read_Js,ClearProf,get_D1,get_Info_Film
def getDesktopSize():
	s = getDesktop(0).size()
	return (s.width(), s.height())
#########################################
def isHD():
	desktopSize = getDesktopSize()
	if desktopSize[0] < 1920:
		return True
	else:
		return False
#########################################
def isDreamOS():
	if fileExists('/var/lib/dpkg/status'):
		return True
	else:
		return False
#########################################
if os.path.exists('/var/lib/dpkg/status'):
    enigmaos = 'oe2.2'
else:
    enigmaos = 'oe2.0'
#########################################
def is_ascii(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
#########################################
from enigma import iPlayableService, iServiceInformation, eServiceCenter, eServiceReference, iFrontendInformation, eTimer , gRGB , eConsoleAppContainer
from ServiceReference import ServiceReference
from Components.ServiceEventTracker import ServiceEventTracker
def Write_Donnees(txt):
    Path = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/dimimage.txt'
    outfile = open(Path, 'a')
    outfile.write(txt)
    outfile.close()
    #print 'Cool'
def colorize(txt,selcolor='white',marker1="[",marker2="]"):
    txt = txt.replace(',','')
    #txt = txt.replace('.','')
    if enigmaos == "oe2.2" or  is_ascii(txt)==False:
        return txt
    #else:txt = txt.encode('utf-8')
    colors={'black':'\c00000000','white':'\c00??????','grey':'\c00808080',
    'blue':'\c000000??','green':'\c0000??00','red':'\c00??0000','ivory':"\c0???????",
    'yellow':'\c00????00','cyan':'\\c0000????','magenta':'\c00??00??'}
    color=colors.get(selcolor,'\c0000????')
    color1=colors.get('cyan','\c0000????')
    try:
        if not marker1 in txt :
            txt = txt.split()
            tx = ''
            for tx in txt:
                tx+=color+" "+tx
            Write_Donnees('\n0-----------------'+tx+'\n'+str(type(tx))+'\n')
            return tx#color+" "+str(txt[0])+color+" "+str(txt[1])+color+" "+str(txt[2])
        txtparts=txt.split(marker1)
        txt1=txtparts[0]
        txt2=txtparts[1]
        try:
            txt2 = txt2.decode('utf-8')
        except:txt2=txt2
        Write_Donnees('\n1-----------------'+txt1+'\n'+txt2+'\n')
        if marker2 in txt2:
            Write_Donnees('\n2-----------------'+txt2+'++++++++++++'+str(type(txt2))+'\n')
            txtos = ''
            txt2 = txt2.replace(']','')
            txt3=txt2.split()
            for txto in txt3:
                try:
                    txto = txto.decode('utf-8')
                    txtos+=" "+color+txto
                except:txtos+=" "+color+txto
            Write_Donnees('\n3-----------------'+txto+'++++++++++++'+str(type(txto))+'\n')
            return txt1+txtos
			
        # if marker2 in txt:
            # txt3=txt2.split(marker2)#[0]
            # if len(txt3)>=2:
                # if txt3[1]!='':
                    # txt3,txt4 = txt3[0],txt3[1]
                    # ftxt=txt1+" "+color+marker1+txt3+marker2+color1+txt4
                # else:
                    # txt3= txt3[0]
                    # ftxt=txt1+" "+color+marker1+txt3+marker2
        # else:
            # txt3=txt2
            # ftxt=txt1+" "+color+marker1+txt3+marker2
        # return ftxt
    except:
        Write_Donnees(txt+'--------------------------probleme '+str(type(txt))+'\n')
        return txt
#########################################
def getversioninfo():
	currversion = '1.0'
	version_file = resolveFilename(SCOPE_PLUGINS, 'Extensions/ShowMovies/Version')
	if os.path.exists(version_file):
		try:
			fp = open(version_file, 'r').readlines()
			for line in fp:
				if 'version' in line:
					currversion = line.split('=')[1].strip()
		except:
			pass
	return (currversion)
Ver = getversioninfo()
#########################################
class m2list(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 10))
        self.l.setFont(1, gFont('Regular', 16))
        self.l.setFont(2, gFont('Regular', 18))
        self.l.setFont(3, gFont('Regular', 20))
        self.l.setFont(4, gFont('Regular', 22))
        self.l.setFont(5, gFont('Regular', 24))
        self.l.setFont(6, gFont('Regular', 26))
        self.l.setFont(7, gFont('Regular', 28))
        self.l.setFont(8, gFont('Regular', 30))
#########################################
def show_VPN(Prblm):
    res = [Prblm]
    res.append(MultiContentEntryText(pos=(2, 2), size=(668, 35), font=4, text=Prblm, color=16777215, color_sel=13870629, flags=RT_HALIGN_LEFT))
    #res.append(MultiContentEntryText(pos=(670, 2), size=(668, 35), font=4, text=List_Y, flags=RT_HALIGN_LEFT))
    return res
#########################################
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/Images/i_'
PLUGIN_PATH_SKIN = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/Skins'
#########################################
dwidth = getDesktop(0).size().width()
#########################################
############start of list
###############end of list
class LinuxsatTestMoveImage(Screen):
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
		self['poster_0'] = Pixmap()
		self['poster_1'] = Pixmap()
		self['poster_2'] = Pixmap()
		self['poster_3'] = Pixmap()
		##############################Label
		self['rating'] =StaticText()
		self['Title_Film'] = Label()
		self['Infos'] = Label()
		self['Infos'].setText('Test Move Text')
		self['Infos_indx'] = Label()
		self['Infos_indx'].setText('')
		self.FoldImag = '/media/hdd/Cimalek/Images/'
		self.watchBTn = False
		##############################NewList
		self.List_Film =['ينطلق دانتي – ابن زعيم الجريمة (هيرنان رييس) – الذي قُتل قبل عشر سنوات للانتقام من البطل دوم توريتو وعائلته وشركائه بعد التسبب في مقتل والده وسرقة أمواله.','تخرج قاتلة محترفة تلقت تدريبًا عسكريًّا من مخبئها لحماية ابنتها التي لم تقابلها قط من فتك مجرمَين عديمَي الرحمة يسعيان للانتقام.','يجد وكيل العمليات الخاصة الفولاذية أن أخلاقه تخضع للاختبار عندما يتسلل إلى نقابة إجرامية ويربط بشكل غير متوقع مع ابن رئيسه الصغير.','يُسافر سباك يُدعى ماريو عبر متاهة تحت الأرض رفقة شقيقه لويجي، وسرعان ما يخوض الثنائي العديد من المغامرات معًا على أمل إنقاذ أميرة.']
		self.NewList = ['i_0.jpg','i_1.jpg','i_2.jpg','i_3.jpg']
		self.NewListTitle = ['Fast X','The Mother','AKA','The Super Mario Bros. Movie']
		for x in range(10):
			self['poster_'+str(x)] = Pixmap()
			self['poster_'+str(x)].show()
			#self.Dist = PLUGIN_PATH+str(x)+'.png'
		for x in range(9):
		    self['Box_'+str(x)] = Label()
		for x in range(1,10):
		    self['Title_'+str(x)] = Label()
		self.NewListJS = {}
		##############################Timer
		self.Timer_ = eTimer()
		self.Timer = eTimer()
		self.AnimTimer = eTimer()
		self.timer = eTimer()
		self.Timer.callback.append(self.updatePoster)
		self.AnimTimer.callback.append(self.newupdateLabel)
		##############################
		self['actions'] = ActionMap(['ShowMoviesPanelActions'], {'cancel': self.exit,
			'left': self.left,
			'right': self.right,
			"down": self.keyDown,
			"up": self.keyUp,
			'ok': self.ok,
			'green': self.Import_My_Watch_Url,
		}, -1)
		Screen.__init__(self, session)
		self.picload = ePicLoad()
		self.menu = []
		self['menu'] = m2list([])
		#self.picload = ePicLoad()
		##############################Start
		self.getposi_image()
		self.ImportImages()
		self.onLayoutFinish.append(self.decodeImage)
		self.onLayoutFinish.append(self.layoutFinish)
		self.onLayoutFinish.append(self.newlayoutFinish)
		self.onLayoutFinish.append(self.setText_Films)
	def ImportImages(self):
		self.menu = []
		uri = '''https://w.cimalek.to/category/aflam-online/'''
		uri1= '''https://w.cimalek.to/category/aflam-online/page/2/'''
		#Msg_ = get_data_Fajre(uri,3)
		self.Msg_ = get_My_Donnees(uri)
		#self.session.open(MessageBox, _(str(self.Msg_[1])+'\n'+str(self.Msg_[0])), MessageBox.TYPE_ERROR)
		if self.Msg_[0]:
		    self.NewListJS = Read_Js()
		    for _dons in self.NewListJS:
		        Prblm = self.NewListJS[_dons][0]#ClearProf(_dons)
		        #List_Y = self.NewListJS[_dons]
		        self.menu.append(show_VPN(str(Prblm)))
		    self.pagination = self.Msg_[2]
		else:
		    self.menu.append(show_VPN('Not Data'))
		self['menu'].l.setList(self.menu)
		self['menu'].l.setItemHeight(35)
		#self.session.open(MessageBox, _(str(_dons)), MessageBox.TYPE_ERROR)
		##############################List_Film
	def newlayoutFinish(self):#
		if self.Msg_[0]:
		    index = self['menu'].getSelectionIndex()
		    _H = self.NewListJS.items()[index][1]
		    a = 'Title        :  \c0000????'+str(_H[0])
		    b = 'Rating     :  \c0000????'+str(_H[4])
		    c = 'Quality    :  \c0000????'+str(_H[5])
		    d = 'Descpt    :  \c0000????'+str(_H[6])
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
		    self['Infos'].setText(str(_H[0]))
		    self['Infos'].instance.move(ePoint(self.yx, 835))
		    self.AnimTimer.start(1000//50, True)
		    self['Infos_indx'].setText(str(_H[0]))
		##############################
	def layoutFinish(self):
		if self.Msg_[0]:
		    for x in range(10):
		        self['poster_'+str(x)].instance.move(ePoint(0, 1080))
		    self.Timer.start(1000//60, True)
		##############################
	def updatePoster(self):
		self.y -= self.dy
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
		#Write_Donnees(str(self.y)+"--------")
		if self.y > 792:#if self.y > self.y2:
			self.Timer.start(1000//60, True)
		else:
			self.Timer.stop()
			#p = self['poster_0'].instance.position()
			#self.session.open(MessageBox, _(str(p.x())+'     '+str(p.y())), MessageBox.TYPE_ERROR)
	##############################
	def newupdateLabel(self):
		self.yx += self.dyx
		self['Infos'].instance.move(ePoint(self.yx, 835))
		#self['Title_Film'].instance.move(ePoint(self.yx, 35))
		self['Box_0'].instance.move(ePoint(self.yx+500, 5))
		self['Box_1'].instance.move(ePoint(self.yx+500, 55))
		self['Box_2'].instance.move(ePoint(self.yx+500, 110))
		self['Box_3'].instance.move(ePoint(self.yx+500, 165))
		if self.yx < self.y22:
			self.AnimTimer.start(1000//50, True)
		else:
			self.AnimTimer.stop()
	def newupdateLabel555555(self):
		self.yx += self.dyx
		self['Infos'].instance.move(ePoint(self.yx, 835))
		#self['Title_Film'].instance.move(ePoint(self.yx, 35))
		self['Box_0'].instance.move(ePoint(self.yx, 750))
		self['Box_1'].instance.move(ePoint(self.yx, 835))
		self['Box_2'].instance.move(ePoint(self.yx, 885))
		self['Box_3'].instance.move(ePoint(self.yx, 935))
		if self.yx < self.y22:
			self.AnimTimer.start(1000//50, True)
		else:
			self.AnimTimer.stop()
	##############################
	def keyDown(self):
		self['menu'].down()
		idx = self['menu'].getSelectionIndex()
		#self['Infos_indx'].setText('Indx Selection = '+str(idx)+'  '+str(len(self.NewListJS)))
		self.Moveframe()
		self.decodeImage()
		self.setText_Films()
	##############################
	def keyUp(self):
		self['menu'].up()
		idx = self['menu'].getSelectionIndex()
		#self['Infos_indx'].setText('Indx Selection = '+str(idx)+'  '+str(len(self.NewListJS)))
		self.Moveframe()
		self.decodeImage()
		self.setText_Films()
	##############################
	def left(self):
		self['menu'].pageUp()
		idx = self['menu'].getSelectionIndex()
		#self['Infos_indx'].setText('Indx Selection = '+str(idx)+'  '+str(len(self.NewListJS)))
		self.Moveframe()
		self.decodeImage()
		self.setText_Films()
	##############################
	def right(self):
		self['menu'].pageDown()
		idx = self['menu'].getSelectionIndex()
		#self['Infos_indx'].setText('Indx Selection = '+str(idx)+'  '+str(len(self.NewListJS)))
		self.Moveframe()
		self.decodeImage()
		self.setText_Films()
	##############################
	def setText_Films(self):
		if self.Msg_[0]:self.setText_Films_1()
	def setText_Films_1(self):
		index = self['menu'].getSelectionIndex()
		Y = len(self.NewListJS)-1
		if index == Y:
		    Nw_List =[0,1,2,3,4,5,6,7,8]
		    for x in range(1,10):
		        V = Nw_List[x-1]
		        _G = self.NewListJS.items()[V][1]
		        self['Title_'+str(x)].setText(str(_G[0]))
		elif index+7 > Y:
		    Nw_List = range(index,Y+1)+[0,1,2,3,4,5,6,7,8]
		    #self.session.open(MessageBox, _(str(Nw_List)+'\nindex ='+str(index)+'\nY ='+str(Y)), MessageBox.TYPE_ERROR)
		    for x in range(1,10):
		        V = Nw_List[x]
		        _G = self.NewListJS.items()[V][1]
		        self['Title_'+str(x)].setText(str(_G[0]))
		else:
		    for x in range(1,10):
		        _G = self.NewListJS.items()[x+index][1]
		        self['Title_'+str(x)].setText(str(_G[0]))
		p_1 =self.pagination[0]
		p_2 =self.pagination[1]
		_B = 'الصفحة'.encode('utf-8')+'  '+str(p_1)+' / '+str(p_2)
		#self['Infos_indx'].setText(_B)
	##############################
	def Moveframe(self):
		#self.session.open(MessageBox, _(str(self.Msg_[0])), MessageBox.TYPE_ERROR)
		#if self.Msg_[0]:
		    self.yx = self.y11
		    self.dyx = (self.y22 - self.y11) // 40
		    if self.newupdateLabel in self.AnimTimer.callback:
		        self.AnimTimer.callback.remove(self.newupdateLabel)
		        self.AnimTimer.callback.append(self.showDescAnim)
		    self.AnimTimer.start(1000//50, True)
	##############################\c0000????
	def showDescAnim(self):
		if self.Msg_[0]:
		    self.yx += self.dyx
		    index = self['menu'].getSelectionIndex()
		    _H = self.NewListJS.items()[index][1]
		    a = 'Title        :  \c0000????'+str(_H[0])
		    b = 'Rating     :  \c0000????'+str(_H[4])
		    c = 'Quality    :  \c0000????'+str(_H[5])
		    d = 'Descpt    :  \c0000????'+str(_H[6])
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
		    self['Infos'].setText(str(_H[0]))
		    self['Infos'].instance.move(ePoint(self.yx, 835))
		    self.AnimTimer.start(1000//50, True)
		    self['Infos_indx'].setText(str(_H[0]))
		    p = self['Box_0'].instance.position()
		    #Write_Donnees(str(_H[0])+'---'+str(_H[4])+'---p.x()='+str(p.x())+'***p.y()='+str(p.y())+'\n')
		    if self.yx < self.y22:
		        self.AnimTimer.start(1000//50, True)
		    else:
		        self.AnimTimer.stop()
		# self.session.open(MessageBox, _('999999999999999999999'), MessageBox.TYPE_ERROR)
		# index = self['menu'].getSelectionIndex()
		# _H = self.NewListJS.items()[index][1]
		# # a = colorize('Title    :  ['+str(_H[0])+']',selcolor='cyan')
		# # b = colorize('Rating    :  ['+str(_H[4])+']',selcolor='cyan')
		# # c = colorize('Quality    :  ['+str(_H[5])+']',selcolor='cyan')
		# # d = colorize('Descpt    :  '+str(_H[6]),selcolor='cyan')
		# a = 'Title    :  \c0000????'+str(_H[0])+']'
		# b = 'Rating    :  \c0000????'+str(_H[4])+']'
		# c = 'Quality    :  \c0000????'+str(_H[5])+']'
		# d = 'Descpt    :  \c0000????'+str(_H[6])
		# self.session.open(MessageBox, _(str(_H[0])+'\n'+str(_H[4])+'\n'+str(_H[5])+'\n'+str(_H[6])), MessageBox.TYPE_ERROR)
		# Msg = [a,b,c,d]
		# for tx in range(4):
		    # v = Msg[tx]
		    # v = v.replace('[','').replace(']','').replace('N/A','...')
		    # self['Box_'+str(tx)].setText(v)
		# self.yx += self.dyx
		# self['Infos'].setText(str(_H[0]))
		# self['Infos'].instance.move(ePoint(self.yx, 835))
		# self['Box_0'].instance.move(ePoint(self.yx+500, 5))
		# self['Box_1'].instance.move(ePoint(self.yx+500, 55))
		# self['Box_2'].instance.move(ePoint(self.yx+500, 110))
		# self['Box_3'].instance.move(ePoint(self.yx+500, 165))
		# if self.yx < self.y22:#if self.yx < 519:#if self.yx < self.y22:
			# self.AnimTimer.start(1000//50, True)
		# else:
			# self.AnimTimer.stop()
	##############################
	def getposi_image(self):
		self.Positions = [(5,37),(5,792),(218,792),(431,792),(644,792),(857,792),(1070,792),(1283,792),(1496,792),(1709,792)]
		self.sizeimag = [(185,278)]
	##############################
	def decodeImage(self):
		#self.AnimTimer.stop()
		if self.Msg_[0]:self.decodeImage_6(0)
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
		from enigma import eServiceReference
		from Screens.InfoBar import InfoBar, MoviePlayer
		MyFilms = ['nada']
		if self.watchBTn:
		    sft,_Df = get_D1(self.watc)
		    if sft:
		        MyFilms = _Df
		        if len(_Df)!=0:
		            stream_url = _Df[0][1]
		            name = self['menu'].getCurrent()[0]
		            self.reference = eServiceReference(5002, 0, stream_url.encode('utf-8'))
		            self.reference.setName(name)
		            self.session.open(MoviePlayer,self.reference)
		        else:self.session.open(MessageBox, _('Not Data Film'), MessageBox.TYPE_ERROR)
	def Import_My_Infos22222(self):
		index = self['menu'].getSelectionIndex()
		_H = self.NewListJS.items()[index][1][1]
		_Info = get_Info_Film(_H)
		self.watc = ''
		try:
		    self.watc = _Info.get('watchBTn','')
		    self.watchBTn = True
		except:self.watc = 'nada'
		self.session.open(MessageBox, _('watchBTn = '+str(self.watc)+'\n'+str(_H)+'\n'+str(_Info)), MessageBox.TYPE_ERROR)
	##############################
	def Import_My_Infos(self):
		index = self['menu'].getSelectionIndex()
		_H = self.NewListJS.items()[index][1][1]
		self._Info = get_Info_Film(_H)
		# for keys in self._Info:
		    # self.session.open(MessageBox, _('keys= '+str(keys)+'\n'+str(self._Info[keys])), MessageBox.TYPE_ERROR)
		# return
		
		self.watc = ''
		i= 4
		List_Secour = ['الاسم الاصلي'.encode('utf-8'),'البلد المنشئ'.encode('utf-8'),'المدة'.encode('utf-8'),'تاريخ العرض'.encode('utf-8'),'اللغة'.encode('utf-8')]
		if len(self._Info)!=0:
		    try:
		        _Z = ''
		        for keys in self._Info:
		            a = self._Info[keys]
		            if type(a)==list:
		                #self.session.open(MessageBox, _('YES '+'\n'+str(a)), MessageBox.TYPE_ERROR)
		                for q in a:
		                    _Z += q+' '
		                a = _Z
		            if keys=='Watchability':a = 'قابلية المشاهدة'.encode('utf-8')
		            if keys=='About The Movie':a = cyan+str(a)
		            else:a = str(keys)+'    :  '+cyan+str(a)
		            self['Box_'+str(i)].setText(a)
		            i = i +1
		            if i>9:break
		    except:
		        for tx in range(4,9):
		            v = '  .......'+List_Secour[tx-4]
		            self['Box_'+str(tx)].setText(v)
	def ok(self):
		self.AnimTimer.stop()
		self.Import_My_Infos()
	##############################
	def exit(self, ret=None):
		self.AnimTimer.stop()
		self.close(True)
