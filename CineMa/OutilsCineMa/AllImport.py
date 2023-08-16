# -*- coding: utf-8 -*-
#!/usr/bin/python
import os
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS
from Components.MenuList import MenuList
from enigma import getDesktop, eListboxPythonMultiContent, eListbox, gFont, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_WRAP, loadPNG
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmap, MultiContentEntryPixmapAlphaTest, MultiContentEntryPixmapAlphaBlend
PLUGIN_PATH_SKIN = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/Skins'
##############################################
def getDesktopSize():
	s = getDesktop(0).size()
	return (s.width(), s.height())
def isHD():
	desktopSize = getDesktopSize()
	if desktopSize[0] < 1920:
		return True
	else:
		return False
##############################################
def get_enigmaos():
    if os.path.exists('/var/lib/dpkg/status'):
        enigmaos = 'oe2.2'
    else:
        enigmaos = 'oe2.0'
    return enigmaos
def isDreamOS():
	if fileExists('/var/lib/dpkg/status'):
		return True
	else:
		return False
##############################################
def Write_Donnees(txt):
    Path = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/dimimage.txt'
    outfile = open(Path, 'a')
    outfile.write(txt)
    outfile.close()
##############################################
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
##############################################
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
def show_SeasEpsod(Title):
    res = [Title]
    res.append(MultiContentEntryText(pos=(2, 2), size=(500, 50), font=5, text=Title, flags=RT_HALIGN_CENTER))
    return res
def show_Movies(Title):
    res = [Title]
    res.append(MultiContentEntryText(pos=(2, 2), size=(500, 35), font=5, text=Title, flags=RT_HALIGN_CENTER))
    #res.append(MultiContentEntryText(pos=(670, 2), size=(668, 35), font=4, text=List_Y, flags=RT_HALIGN_LEFT))
    return res
def show_Movies_2(Title):
    res = [Title]
    res.append(MultiContentEntryText(pos=(2, 2), size=(500, 50), font=5, text=Title, flags=RT_HALIGN_CENTER))
    #res.append(MultiContentEntryText(pos=(670, 2), size=(668, 35), font=4, text=List_Y, flags=RT_HALIGN_LEFT))
    return res