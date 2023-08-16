#!/usr/bin/python
# -*- coding: utf-8 -*-
from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.ConfigListSupt import ConfigListShowMoviesScreen
from supcompnt import *
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from enigma import eTimer
from Components.Label import Label
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.config import config, NoSave,ConfigSelection, getConfigListEntry, ConfigSubsection, configfile, ConfigText,ConfigDirectory
from Tools.Directories import fileExists, pathExists
from Components.ActionMap import NumberActionMap, ActionMap
import os
import re
from Screens.LocationBox import LocationBox
###############################################################################
Version = 'Vrs_1.0'
_VERSION_ = '1.0'
ChIptv_7 = 'This choice means the entry interface is This choice means the entry interface is vertical'+'\n'+'هذا الاختيار يعني واجهة الدخول عمودية'
ChIptv_7_1 = 'This choice means the entry interface is This choice means the entry interface is horizontal'+'\n'+'هذا الاختيار يعني واجهة الدخول أفقي'
ChIptv_3 = 'This Choice Is To Keep You Informed Of a New Version'+'\n'+'هذا الاختيار لموافاتك بوجود نسخة جديدة'
ChIptv_3_1 = 'This Option Is To Disable Your Notification Of A New Version '+'\n'+'هذا الاختيار لتعطيل موافاتك بوجود نسخة جديدة'
def SearchIpBox():
    Doss = '/etc/network/interfaces'
    IpBox = ''
    if fileExists(Doss):
        ecmf = open(Doss, 'rb')
        ecm = ecmf.readlines()
        try:
            for line in ecm:
                if 'address' in line:
                    IpBox = line.split(' ')[1].replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '').replace('\\s', '')
        except:
            IpBox = 'Not Find'
    return IpBox
def get_IpConnec():
    import requests
    _Ip,data = '',''
    url='http://checkip.amazonaws.com/'
    try:
        data=requests.get(url,timeout=10).content
    except:data='nada'
    if data!='nada' and data!='':_Ip = data.replace('\n','')
    else:_Ip = 'not Found'
    return _Ip
def selectPlayer():#thk's faraj
    defaultPlayer = 'systemplayer'
    serviceApp = False
    try:
        if os.path.exists('/usr/lib/enigma2/python/Plugins/SystemPlugins/ServiceApp'):
            from Plugins.SystemPlugins.ServiceApp.plugin import config_serviceapp
            if config_serviceapp.servicemp3.replace.value:
                defaultPlayer = config_serviceapp.servicemp3.player.value
            else:
                defaultPlayer = 'systemPlayer'
            serviceApp = True
        else:
            defaultPlayer = 'systemPlayer'
    except:
        defaultPlayer = 'systemPlayer'
    return (defaultPlayer, serviceApp)
def get_Adrs_mac():
    mac = ''
    try:
        import uuid
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        mac = mac.replace('\n', '').replace('\t', '').replace('\r', '').replace('\\s', '').replace('\\d', '').replace(' ', '')
    except:
        mac = 'Not Found'
    return mac
def ImportDonneeServer(ind,nme):
    H = ''
    Path_1 = '/tmp/SuptvServer'
    if fileExists(Path_1):
        ptfile = open(Path_1, 'r')
        data = ptfile.readlines()
        ptfile.close()
        try:
            H = data[ind].replace('\n', '').replace('\t', '').replace('\r', '')
            H = H.split('=')[1]
        except:H=nme
    else:H=nme
    return H
def get_Infos_FreeAbonnement(host,port,name,passw):#Add by aime_jeux
    status,exp_date,max_connections,Free_Host,_Donnees,Infos = '','','','','',''
    import requests,json
    from time import ctime
    host = host.replace(' ','')
    port = port.replace(' ','')
    name = name.replace(' ','')
    passw = passw.replace(' ','')
    A1 = colorize('Host : '+str(host),selcolor='cyan')
    A2 = colorize('Port : '+str(port),selcolor='cyan')
    A3 = colorize('username : '+str(name),selcolor='cyan')
    A4 = colorize('password : '+str(passw),selcolor='cyan')
    Infos = A1+'\n'+A2+'\n'+A3+'\n'+A4
    Href = 'http://'+host+':'+str(port)+'/player_api.php?username='+str(name)+'&password='+str(passw)
    try:
        data             = requests.get(Href).json()
    except:
        data = 'nada'
    if data!='nada':
        try:
            status       = 'status : '+str(data['user_info']['status'])
            status       = colorize(status,selcolor='cyan')
        except:
            status       = 'status : None'
            status       = colorize(status,selcolor='cyan')
        try:
            exp_date     = 'exp_date : '+str(ctime(int(data['user_info']['exp_date'])))
            exp_date     = colorize(exp_date,selcolor='cyan')
        except:
            exp_date     = 'exp_date : None'
            exp_date     = colorize(exp_date,selcolor='cyan')
        try:
            max_connections = 'max_connections : '+str(data['user_info']['max_connections'])
            max_connections = colorize(max_connections,selcolor='cyan')
        except:
            max_connections = 'max_connections : None'
            max_connections = colorize(max_connections,selcolor='cyan')
        try:
            Free_Host       = 'Free_Host : '+str(data['server_info']['url'])
            Free_Host       = colorize(Free_Host,selcolor='cyan')
        except:
            Free_Host       = 'Free_Host : None'
            Free_Host       = colorize(Free_Host,selcolor='cyan')
        _Donnees            = Free_Host+'\n'+status+'\n'+exp_date+'\n'+max_connections
        _Donnees            = Infos+'\n'+_Donnees
    else:_Donnees = Infos+'\n makach'
    return _Donnees
###############################################################################
black   = '\c00000000'
white   = '\c00??????'
gray    = '\c00808080'
blue    = '\c000000??'
green   = '\c0000??00'
red     = '\c00??0000'
yellow  = '\c00????00'
cyan    = '\c0000????'
magenta = '\c00??00??'
orange  = '\c00??500'
blueViolet='\c008?2??2'
lime    = '\c0000??00'
config.plugins.ShowMoviesConfig = ConfigSubsection()
config.plugins.ShowMoviesConfig.notification = ConfigSelection(default='disabled', choices=[('disabled', _('Disabled')), 
    ('enabled', _('Enabled'))])
config.plugins.ShowMoviesConfig.Activskin = ConfigSelection(default='vertical', choices=[('vertical', _('Vertical')), ('horizontal', _('Horizontal'))])
config.plugins.ShowMoviesConfig.Colors    = ConfigSelection(default='yellow', choices=[
    ('yellow', _(yellow+'Yellow')), 
    ('white', _(white+'White')), 
    ('gray', _(gray+'Gray')), 
    ('blue', _(blue+'Blue')), 
    ('green', _(green+'Green')), 
    ('red', _(red+'Red')), 
    ('cyan', _(cyan+'Cyan')), 
    ('magenta', _(magenta+'Magenta')),
    ('orange', _(orange+'Orange')),
    ('blueViolet', _(blueViolet+'BlueViolet')),
    ('lime', _(lime+'Lime'))
    ])
config.plugins.ShowMoviesConfig.ActivUpdattime = ConfigSelection(default='yes', choices=[('yes', _('Yes')), ('no', _('No'))])
config.plugins.ShowMoviesConfig.Posters = ConfigDirectory(default='/tmp/')
config.plugins.ShowMoviesConfig.Tmdb = ConfigSelection(default='disabled', choices=[('disabled', _('Disabled')),('enabled', _('Enabled'))])
config.plugins.ShowMoviesConfig.TmdbToken = ConfigText(default='Your Token', visible_width=50, fixed_size=False)
config.plugins.ShowMoviesConfig.TmdbLang = ConfigSelection(default='fr', choices=[('fr', _('FR')), ('en', _('EN')),('us', _('US')),('it', _('IT')),('es', _('ES')),('de', _('DE'))])
config.plugins.ShowMoviesConfig.Imdb = ConfigSelection(default='disabled', choices=[('disabled', _('Disabled')),('enabled', _('Enabled'))])
config.plugins.ShowMoviesConfig.ImdbToken = ConfigText(default='k_7nggq46b', visible_width=50, fixed_size=False)
config.plugins.ShowMoviesConfig.ImdbLang = ConfigSelection(default='fr', choices=[('fr', _('FR')), ('uk', _('UK')),('us', _('US')),('it', _('IT')),('es', _('ES')),('de', _('DE'))])
PATH_SKINS = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/Skins'
def get_Posters():
    return config.plugins.ShowMoviesConfig.Posters.value
def get_TMDB():
    A = config.plugins.ShowMoviesConfig.TmdbToken.value
    B = config.plugins.ShowMoviesConfig.TmdbLang.value
    if config.plugins.ShowMoviesConfig.Tmdb.value == 'enabled':
        return A,B
    else:
        return '','fr'
def get_IMDB():
    A = config.plugins.ShowMoviesConfig.ImdbToken.value
    B = config.plugins.ShowMoviesConfig.ImdbLang.value
    if config.plugins.ShowMoviesConfig.Imdb.value == 'enabled':
        return A,B
    else:
        return '','fr'
def get_Tmdbvalue():
    return config.plugins.ShowMoviesConfig.Tmdb.value
def get_Activskin():
    if config.plugins.ShowMoviesConfig.notification.value == 'enabled':
        return config.plugins.ShowMoviesConfig.Activskin.value
    else:return 'vertical'
from skin import loadSkin
class ShowMovies_Config(Screen, ConfigListShowMoviesScreen):
    def __init__(self, session):
        loadSkin(PATH_SKINS + '/SetupFHD.xml')
        # with open(PATH_SKINS + '/SetupFHD.xml', 'r') as f:
            # self.skin = f.read()
            # f.close()
        self.session = session
        Screen.__init__(self, session)
        self.onChangedEntry = []
        self.list = []
        ConfigListShowMoviesScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions', 'DirectionActions','MenuActions'], {'green': self.keySave,
            'red': self.keyClose,
            'cancel': self.keyClose,
            'ok': self.ok,
            'left': self.keyLeft,
            'right': self.keyRight,
            'up': self.up,
            'down': self.down
         }, -2)
        self.__changed = self.changedEntry
        for x in range(1,20):
            self['Box_'+str(x)] = Label()
        self.ListFreeServer = ['Your Host','Your Port','Your Username','Your Password']
        self.runSetupVod()
    def runSetupSupNew(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Notify on_off'), config.plugins.ShowMoviesConfig.notification))
        self['config'].list = self.list
        self['config'].setList(self.list)
        self['config'].l.setItemHeight(50)
        self['Box_3'].setText('')
        self['Box_1'].setText('Notify Disable')
    def runSetupVod(self):
        self.list.append(getConfigListEntry(_('Notify'), config.plugins.ShowMoviesConfig.notification))
        self.list = []
        self.list.append(getConfigListEntry(_('Notify'), config.plugins.ShowMoviesConfig.notification))
        if config.plugins.ShowMoviesConfig.notification.value == 'enabled':
            self.list.append(getConfigListEntry(_('Skin Change'), config.plugins.ShowMoviesConfig.Activskin))
            self.list.append(getConfigListEntry(_('Skin Colors'), config.plugins.ShowMoviesConfig.Colors))
            self.list.append(getConfigListEntry(_('AutoUpdat'), config.plugins.ShowMoviesConfig.ActivUpdattime))
            self.list.append(getConfigListEntry(_('Adress Poster File'), config.plugins.ShowMoviesConfig.Posters))
            # self.list.append(getConfigListEntry(_('TMDB'),config.plugins.ShowMoviesConfig.Tmdb))
            # if config.plugins.ShowMoviesConfig.Tmdb.value == 'enabled':
                # self.list.append(getConfigListEntry(_('Tmdb Token'),config.plugins.ShowMoviesConfig.TmdbToken))
                # self.list.append(getConfigListEntry(_('Tmdb Lang'),config.plugins.ShowMoviesConfig.TmdbLang))
            # self.list.append(getConfigListEntry(_('IMDB'),config.plugins.ShowMoviesConfig.Imdb))
            # if config.plugins.ShowMoviesConfig.Imdb.value == 'enabled':
                # self.list.append(getConfigListEntry(_('Imdb Token'),config.plugins.ShowMoviesConfig.ImdbToken))
                # self.list.append(getConfigListEntry(_('Imdb Lang'),config.plugins.ShowMoviesConfig.ImdbLang))
            self['config'].list = self.list
            self['config'].setList(self.list)
            self['config'].l.setItemHeight(50)
            if config.plugins.ShowMoviesConfig.ActivUpdattime.value == 'yes':
                Updattime = 'Active'
                self['Box_3'].setText('      AutoUpdate..Time... ' + str(Updattime))
            else:
                self['Box_3'].setText('      AutoUpdat Time ... Disabled')
            self.Index_Infos_1()
    def Index_Infos_1(self):
        HH = self['config'].l.getCurrentSelectionIndex()
        ADS = self['config'].list[HH][0]
        ADS_1 = self['config'].list[HH][1].value
        if config.plugins.ShowMoviesConfig.notification.value == 'enabled':
            if ADS == 'Notify':
                self['Box_1'].setText('Notify Enable')
            elif config.plugins.ShowMoviesConfig.Activskin.value == 'vertical' and ADS == 'Skin Change':
                self['Box_1'].setText(ChIptv_7)
            elif config.plugins.ShowMoviesConfig.Activskin.value == 'horizontal' and ADS == 'Skin Change':
                self['Box_1'].setText(ChIptv_7_1)
            elif config.plugins.ShowMoviesConfig.ActivUpdattime.value == 'yes'  and ADS == 'AutoUpdat':
                self['Box_1'].setText(ChIptv_3)
            elif config.plugins.ShowMoviesConfig.ActivUpdattime.value == 'no'  and ADS == 'AutoUpdat':
                self['Box_1'].setText(ChIptv_3_1)
            elif ADS == 'Skin Colors':########
                self['Box_1'].setText('change Colors Skin\n'+'اختيار لون التعريفات في السكين')
            elif ADS == 'Adress Poster File':
                self['Box_1'].setText('Press OK to change location\n'+'اضغط على زر اوكي لتحديد مسار الملف')
            elif ADS == 'TMDB':
                self['Box_1'].setText('This Is The Option To Set The Movie Database\n'+'هذا الاختيار لوضع قاعدة بيانات الفيلم')
            elif ADS == 'Tmdb Token':
                self['Box_1'].setText('This Is The Choice For Setting The Search Token\n'+'هذا الختيار لوضع التوكن الخاص بالبحث')
                self.KeyText()
            elif ADS == 'Tmdb Lang':
                self['Box_1'].setText('This Option Selects The Search Language\n'+'هذا الاختيار لتحديد لغة البحث')
			####################"
            elif ADS == 'IMDB':
                self['Box_1'].setText('This Is The Option To Set Internet Movie Database\n'+'هذا الاختيار لوضع قاعدة بيانات الأفلام على الإنترنت')
            elif ADS == 'Imdb Token':
                self['Box_1'].setText('This Is The Choice For Setting The Search Token\n'+'هذا الختيار لوضع التوكن الخاص بالبحث')
                self.KeyText()
            elif ADS == 'Imdb Lang':
                self['Box_1'].setText('This Option Selects The Search Language\n'+'هذا الاختيار لتحديد لغة البحث')
            else:
                self['Box_1'].setText(ADS + '  '+str(ADS_1))
                self['Box_3'].setText('      ................')
            # if config.plugins.ShowMoviesConfig.Activskin.isChanged():self._Messg = 'ShowMovies  ' + Version+'\nYou Must Restart The Device Because You Changed The Nature Of The Skin \n'+'يجب اعادة تشغيل الجهاز لانك غيرت طبيعة السكين'
            # else:self._Messg = 'ShowMovies  ' + Version+'\nDo You Want To Restart Igu \n'+'هل تريد اعادة تشغيل الانغما'
    def up(self):
        Indx = self['config'].l.getCurrentSelectionIndex()
        if Indx == 0:
            #self['config'].pageDown()
            self['config'].setCurrentIndex(len(self.list)-1)
        else:
            self['config'].moveUp()
        self.Index_Infos_1()
    def down(self):
        Indx = self['config'].l.getCurrentSelectionIndex()
        if Indx == len(self.list)-1:
            #self['config'].pageUp()
            self['config'].setCurrentIndex(0)
        else:
            self['config'].moveDown()
        self.Index_Infos_1()
    def keyLeft(self):
        ConfigListShowMoviesScreen.keyLeft(self)
        if config.plugins.ShowMoviesConfig.notification.value == 'enabled':
            self.runSetupVod()
        else:
            self.runSetupSupNew()
    def keyRight(self):
        ConfigListShowMoviesScreen.keyRight(self)
        if config.plugins.ShowMoviesConfig.notification.value == 'enabled':
            self.runSetupVod()
        else:
            self.runSetupSupNew()
    def keySave(self):
        for x in self['config'].list:
            if x[0] == 'Ip Connect':continue
            x[1].save()
        configfile.save()
        if config.plugins.ShowMoviesConfig.notification.value == 'enabled':
            mesageboxint = ''
            if config.plugins.ShowMoviesConfig.ActivUpdattime.value == 'yes':
                Updattime = 'Active'
                self['Box_3'].setText('You Have Chosen..Time\n' + str(Updattime) + '\n To Update Your Servers')
            else:
                self['Box_3'].setText('AutoUpdat Time ... Disabled')
        else:
            # self._Messg = 'ShowMovies  ' + Version+'\nDo You Want To Restart Igu \n'+'هل تريد اعادة تشغيل الانغما'
            self['Box_3'].setText('')
        # if config.plugins.ShowMoviesConfig.Activskin.isChanged():_Messg = 'ShowMovies  ' + Version+'\nYou Must Restart The Device Because You Changed The Nature Of The Skin \n'+'يجب اعادة تشغيل الجهاز لانك غيرت طبيعة السكين'
        self._Messg = 'ShowMovies  ' + Version+'\nDo You Want To Restart Igu \n'+'هل تريد اعادة تشغيل الانغما'
        self.session.openWithCallback(self.restartenigma, MessageBox, _(self._Messg), MessageBox.TYPE_YESNO)
    def restartenigma(self, result):
        if result:
            self.session.open(TryQuitMainloop, 3)
    def keyClose(self):
        for x in self['config'].list:
            x[1].cancel()
        self.close()
    def ok(self):
        sel = self['config'].getCurrent()[1]
        if sel and sel == config.plugins.ShowMoviesConfig.Posters:
            self.setting = 'adrsposter'
            self.openDirectoryBrowser(config.plugins.ShowMoviesConfig.Posters.value)
        ConfigListShowMoviesScreen.keyOK(self)
    def openDirectoryBrowser(self, path):
        try:
            self.session.openWithCallback(
                self.openDirectoryBrowserCB,
                LocationBox,
                windowTitle=_('Choose Directory:'),
                text=_('Choose directory'),
                currDir=str(path),
                bookmarks=config.movielist.videodirs,
                autoAdd=False,
                editDir=True,
                inhibitDirs=['/bin', '/boot', '/dev', '/home', '/lib', '/proc', '/run', '/sbin', '/sys', '/var'],
                minFree=15)
        except Exception as e:
            print("open Directory Browser get failed: %s" % e)
    def openDirectoryBrowserCB(self, path):
        if path is not None:
            if self.setting == 'adrsposter':
                config.plugins.ShowMoviesConfig.Posters.setValue(path)
        return