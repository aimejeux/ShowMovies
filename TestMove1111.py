# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.Label import Label
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Components.Pixmap import Pixmap
# from Plugins.Extensions.DreamSat.core.commons import readFromFile, isDreamOS, cfg, parseColor
from Plugins.Extensions.DreamSat.ui.plugins import PluginsInstaller
from Plugins.Extensions.DreamSat.ui.Servers import ActiveCode
from Plugins.Extensions.DreamSat.ui.ConfigFile import ConfigPlugin
# from Plugins.Extensions.DreamSat.ui.VirtualKeyboard import DreamSatKeyBoard
from Plugins.Extensions.DreamSat.ui.Subscription import DreamSatSubscription
# from Plugins.Extensions.DreamSat.ui.MessageBox import DreamSatMessageBox
# from Plugins.Extensions.DreamSat.ui.Console import Console2
# from Components.GUIComponent import GUIComponent
from enigma import ePixmap, eTimer, ePoint, gPixmapPtr
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS
# from twisted.web.client import getPage
# from twisted.internet.protocol import Factory
import json
import os
from sys import version_info
#from . animation import AnimationTopToBottom
##################################################################ADJ
from Tools.Directories import fileExists, pathExists
##################################################################
PY3 = version_info[0] == 3

# Factory.noisy = False


def getversioninfo():
	currversion = '1.0'
	version_file = resolveFilename(SCOPE_PLUGINS, 'Extensions/DreamSat/Version')
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
##########################################################ADJ
from enigma import getDesktop, eListboxPythonMultiContent, eListbox, gFont, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_WRAP, loadPNG
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest, MultiContentEntryPixmapAlphaBlend
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
def show_VPN(Serv):
    print Serv
    res = [Serv]
    res.append(MultiContentEntryText(pos=(2, 2), size=(668, 35), font=4, text=Serv, color=16777215, color_sel=13870629, flags=RT_HALIGN_LEFT))
    return res
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/Images/i_'
from Components.AVSwitch import AVSwitch
from Tools.BoundFunction import boundFunction
from enigma import ePoint, eSize, eTimer,ePicLoad
def Write_Donnees(txt):
    Path = '/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/dimimage.txt'
    outfile = open(Path, 'a')
    outfile.write(txt)
    outfile.close()
    #print 'Cool'
#######################################################################
class LinuxsatTestMoveImage(Screen):
	skin = """<screen name="LinuxsatLauncher" position="2,3" size="1920,1080" flags="wfNoBorder" title="Launcher" backgroundColor="#22000000">
              <widget name="menu" zPosition="4" foregroundColorSelected="white" position="1401,11" size="500,350" enableWrapAround="1" scrollbarMode="showNever" transparent="0" />
              <widget name="poster_0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/Images/i_0.jpg" position="50,535" size="185,278" zPosition="4" transparent="1" />
              <widget name="poster_1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/Images/i_1.jpg" position="512,535" size="185,278" zPosition="4" transparent="1" />
              <widget name="poster_2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/Images/i_2.jpg" position="970,535" size="185,278" zPosition="4" transparent="1" />
              <widget name="poster_3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/DreamSat/Images/i_3.jpg" position="1428,535" size="185,278" zPosition="4" transparent="1" />
			  <widget backgroundColor="CursorForeground" font="Clock;34" halign="left" foregroundColor="Progress" position="1582,1010" render="Label" size="300,50" source="global.CurrentTime" transparent="1" valign="top" zPosition="2">
              <convert type="ClockToText">Format:%H:%M %p </convert>
              </widget>
			  <widget name="Infos" position="32,1119" size="800,100" zPosition="4" font="Regular;55" foregroundColor="white" backgroundColor="#80000000" transparent="1" halign="center" valign="center" />
            </screen>"""
	def __init__(self, session, *args):
		self.session = session
		y1, y2 = (1080, 800)
		self.y1 = y1
		self.y2 = y2
		self.y = y1
		self.dy = (y1 - y2) // 21
		#######################################
		y11, y22 = (-1080, 30)
		self.y11 = y11
		self.y22 = y22
		self.yx = y11
		self.dyx = (y22 - y11) // 30
		#######################################
		self['Infos'] = Label()
		self['Infos'].setText('Test Move Text')
		self.NewList = ['i_0.jpg','i_1.jpg','i_2.jpg','i_3.jpg']
		for x in range(len(self.NewList)):
		    self['poster_'+str(x)] = Pixmap()
		    self['poster_'+str(x)].show()
		    self.Dist = PLUGIN_PATH+str(x)+'.png'
		#######################################
		self.Timer = eTimer()
		self.AnimTimer = eTimer()
		self.timer = eTimer()
		#self.Timer.callback.append(self.updateLabel)
		self.AnimTimer.callback.append(self.newupdateLabel)
		#######################################
		self['actions'] = ActionMap(['DreamSatPanelActions'], {
			'cancel': self.exit,
			'left': self.left,
			'right': self.right,
			"down": self.keyDown,
			"up": self.keyUp,
			'ok': self.ok,
		}, -1)
		Screen.__init__(self, session)
		self.picload = ePicLoad()
		self.menu = []
		self['menu'] = m2list([])
		for _don in self.NewList:
		    self.menu.append(show_VPN(_don))
		self['menu'].l.setList(self.menu)
		self['menu'].l.setItemHeight(35)
		self.getposi_image()
		self.onLayoutFinish.append(self.decodeImage)
		self.onLayoutFinish.append(self.layoutFinish)
		self.onLayoutFinish.append(self.newlayoutFinish)
	def newlayoutFinish(self):
		index = self['menu'].getSelectionIndex()
		self['Infos'].setText('Test Move Text__'+str(index+1))
		self['Infos'].instance.move(ePoint(self.yx, 210))
		self.AnimTimer.start(1000//50, True)
	def layoutFinish(self):
		self['Infos'].instance.move(ePoint(0, 1080))
		self.Timer.start(1000//60, True)
	# def updateLabel(self):
		# self.y -= self.dy
		# if self.y > self.y2:
			# self.Timer.start(1000//60, True)
		# else:
			# self.Timer.stop()
	def newupdateLabel(self):
		self.yx += self.dyx
		self['Infos'].instance.move(ePoint(self.yx, 210))
		if self.yx < self.y22:
			self.AnimTimer.start(1000//50, True)
		else:
			self.AnimTimer.stop()
	def keyDown(self):
		self["menu"].instance.moveSelection(self["menu"].instance.moveDown)
		self.Moveframe()
		self.decodeImage()
	def keyUp(self):
		self["menu"].instance.moveSelection(self["menu"].instance.moveUp)
		self.Moveframe()
		self.decodeImage()
	def left(self):
		self['menu'].up()
		self.Moveframe()
		self.decodeImage()
	def right(self):
		self['menu'].down()
		self.Moveframe()
		self.decodeImage()
	def Moveframe(self):
		index = self['menu'].getSelectionIndex()
		self.yx = self.y11
		self.dyx = (self.y22 - self.y11) // 40
		if index == 0:
			self.yx = self.y11
			self.dyx = (self.y22 - self.y11) // 40
			if self.newupdateLabel in self.AnimTimer.callback:
			    self.AnimTimer.callback.remove(self.newupdateLabel)
			    self.AnimTimer.callback.append(self.showDescAnim)
			self.AnimTimer.start(1000//50, True)
		if index == 1:
			self.yx = self.y11
			self.dyx = (self.y22 - self.y11) // 40
			if self.newupdateLabel in self.AnimTimer.callback:
				self.AnimTimer.callback.remove(self.newupdateLabel)
				self.AnimTimer.callback.append(self.showDescAnim)
			self.AnimTimer.start(1000//50, True)
		if index == 2:
			self.yx = self.y11
			self.dyx = (self.y22 - self.y11) // 40
			if self.newupdateLabel in self.AnimTimer.callback:
				self.AnimTimer.callback.remove(self.newupdateLabel)
				self.AnimTimer.callback.append(self.showDescAnim)
			self.AnimTimer.start(1000//50, True)
		if index == 3:
			self.yx = self.y11
			self.dyx = (self.y22 - self.y11) // 40
			if self.newupdateLabel in self.AnimTimer.callback:
				self.AnimTimer.callback.remove(self.newupdateLabel)
				self.AnimTimer.callback.append(self.showDescAnim)
			self.AnimTimer.start(1000//50, True)
	def showDescAnim(self):
		index = self['menu'].getSelectionIndex()
		self['Infos'].setText('Test Move Text__'+str(index+1))
		self.yx += self.dyx
		self['Infos'].instance.move(ePoint(self.yx, 210))
		if self.yx < self.y22:
			self.AnimTimer.start(1000//50, True)
		else:
			self.AnimTimer.stop()
	def getposi_image(self):
		self.Positions = [(50,535),(512,535),(970,535),(1428,535)]
		self.sizeimag = [(185,278)]
	def decodeImage(self):
		index = self['menu'].getSelectionIndex()
		for b in range(4):
		    if b==index:self['poster_'+str(b)].instance.move(ePoint(self.Positions[b][0], self.Positions[b][1]-120))
		    else:self['poster_'+str(b)].instance.move(ePoint(self.Positions[b][0], self.Positions[b][1]))
		    self.decodeImage_6(b)
		self.decodeImage_50()
	def decodeImage_50(self):
		self.index = self['menu'].getSelectionIndex()
		self['poster_'+str(self.index)].instance.resize(eSize(260, 378))
		self.decodeImage_600()
		# try:
		    # self.timer.callback.append(self.decodeImage_600)
		# except:
		    # self.timer_conn = self.timer.timeout.connect(self.decodeImage_600)
		# self.timer.start(1, True)
	def decodeImage_600(self):
		self.index = self['menu'].getSelectionIndex()
		picfile = PLUGIN_PATH +str(self.index)+'.jpg'
		picobject = self['poster_'+str(self.index)]	
		picobject.instance.setPixmap(gPixmapPtr())
		self.scale = AVSwitch().getFramebufferScale()
		self.picload = ePicLoad()
		size = picobject.instance.size()
		self.picload.setPara((size.width(),
            size.height(),0,0,0,0,'#80000000'))
		if self.picload.startDecode(picfile, 0, 0, False) == 0:
		    ptr = self.picload.getData()
		    if ptr != None:
		        picobject.instance.setPixmap(ptr)
		        picobject.show()
		        del self.picload
		return
	def decodeImage_6(self,cty):
		picfile = PLUGIN_PATH +str(cty)+'.jpg'
		picobject = self['poster_'+str(cty)]	
		picobject.instance.setPixmap(gPixmapPtr())
		self.scale = AVSwitch().getFramebufferScale()
		self.picload = ePicLoad()
		size = picobject.instance.size()
		self.picload.setPara((185,278,0,0,0,0,'#80000000'))
		if self.picload.startDecode(picfile, 0, 0, False) == 0:
		    ptr = self.picload.getData()
		    if ptr != None:
		        picobject.instance.setPixmap(ptr)
		        picobject.show()
		        del self.picload
		return
	def Nmbrs_Image(self):
		n = ''
		file_0 = ''
		if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/DreamSatVpn/choose/USER NEW TUNISIA-SAT.txt'):
		    file_0 = '/usr/lib/enigma2/python/Plugins/Extensions/DreamSatVpn/choose/USER NEW TUNISIA-SAT.txt'
		    n = sum((1 for _ in open(file_0)))
		else:
		    n = 0
		return n
	def ok(self):
		self.AnimTimer.stop()
		self.exit()
	def exit(self, ret=None):
		self.close(True)