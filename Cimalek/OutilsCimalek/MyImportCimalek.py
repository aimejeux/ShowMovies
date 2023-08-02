#!/usr/bin/python
# -*- coding: utf-8 -*-
import json,re,requests,os,shutil
########################################################################
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
St = requests.Session()
########################################################################
from Plugins.Extensions.ShowMovies.Cimalek.OutilsCimalek.AllImport import *
folder = '/media/hdd/Cimalek/Images'
def get_Taille():
    folder_size = 0
    for (path, dirs, files) in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)
            folder_size += os.path.getsize(filename)
    Taille = "%0.1f MB" % (folder_size/(1024*1024.0))
    return str(Taille)
########################################################################Clear Txt
def ClearProf(data):
    LATIN_1_CHARS = (
    ('\xe2\x80\x99', "'"),
    ('\xc3\xa9', 'e'),
    ('\xe2\x80\x90', '-'),
    ('\xe2\x80\x91', '-'),
    ('\xe2\x80\x92', '-'),
    ('\xe2\x80\x93', '-'),
    ('\xe2\x80\x94', '-'),
    ('\xe2\x80\x94', '-'),
    ('\xe2\x80\x98', "'"),
    ('\xe2\x80\x9b', "'"),
    ('\xe2\x80\x9c', '"'),
    ('\xe2\x80\x9c', '"'),
    ('\xe2\x80\x9d', '"'),
    ('\xe2\x80\x9e', '"'),
    ('\xe2\x80\x9f', '"'),
    ('\xe2\x80\xa6', '...'),
    ('\xe2\x80\xb2', "'"),
    ('\xe2\x80\xb3', "'"),
    ('\xe2\x80\xb4', "'"),
    ('\xe2\x80\xb5', "'"),
    ('\xe2\x80\xb6', "'"),
    ('\xe2\x80\xb7', "'"),
    ('\xe2\x81\xba', "+"),
    ('\xe2\x81\xbb', "-"),
    ('\xe2\x81\xbc', "="),
    ('\xe2\x81\xbd', "("),
    ('\xe2\x81\xbe', ")"))
    for _hex, _char in LATIN_1_CHARS:
        data = data.replace(_hex, _char)
    return data
########################################################################
def ClearTitle(txt):
    txt = txt.replace('&#8217;s','s-').replace('&#038;','-')
    txt = txt.replace('&#8217;','-')
    txt = txt.replace('- ','-')
    txt = txt.replace('- ','-')
    txt = txt.replace('- ','-')
    txt = txt.replace('صفحة'.decode('utf-8'),'')
    txt = txt.replace('من'.decode('utf-8'),'')
    txt = txt.replace('  ',' ')
    txt = txt.replace('\u2013','')
    return txt
########################################################################Downloads Images
_distI = '/media/hdd/Cimalek/Images/%s'
########################################################################
def Downloads_Images_Home(uri,dist):
    Repns = False
    try:
        response = St.get(uri, stream=True)
        print 'response = ',response.status_code
        if response.status_code == 200:
            with open(dist, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            Repns = True
        else:Repns = False
    except:
        Repns = False
    return Repns
########################################################################
def Downloads_Images(uri,dist):
    Repns = False
    if  os.path.exists(dist):
        print 'Img Exist'
        Repns = True
        pass
    else:
        try:
            response = St.get(uri, stream=True)
            print 'response = ',response.status_code
            if response.status_code == 200:
                with open(dist, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
                Repns = True
            else:Repns = False
        except:
            Repns = False
    return Repns
####################################################################### Write Js File
cfg_path = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/Cimalek/FilsJs/DonnesJs.js'
########################################################################
def export_txt(txt):
    with open(cfg_path, "w") as f:
        f.write(txt)
    f.close()
    return 'Mission accomplished'
####################################################################### Lire Js File
def Read_Js():
    with open(cfg_path) as mon_Js:
        data = json.load(mon_Js)
    return data
#######################################################################Get Data From Js or Content File
def get_Data(url,get='',typ='',param=False,headers=False):
    _Data = ''
    if param and headers:
        try:exec "_Data = St."+get+"(url,data=param,headers=headers,verify=False)."+typ
        except:_Data = ''
    elif param and not headers:
        try:exec "_Data = St."+get+"(url,data=param,verify=False,timeout=10)."+typ
        except:_Data = ''
    elif headers and not param :
        try:
            exec ("_Data = St."+get+"(url,headers=headers,verify=False,timeout=10)."+typ)
        except:_Data = ''
    else :
        try: exec ("_Data=St."+get+"(url,verify=False,timeout=10)."+typ)
        except:_Data = ''
    return _Data
#######################################################################Import Site Data
def get_My_Donnees(url):
    MyDict_ = {}
    i = 1
    Donnees = get_Data(url,get='get',typ='content')
    if Donnees == '':return False,Donnees,''
    tmx = '''<div class="pagination-tol"><span>(.+?)</span>'''
    try:
        pagination = re.findall(tmx,Donnees,re.M|re.I|re.DOTALL)[0].decode('utf-8')
        pagination = ClearTitle(pagination)
        pagination = pagination.split()
    except:
            tmx = '''<a class='arrow_pag' href=".+?/page/(.+?)/.+?><i id='nextpagination'''
            try:
                pagination = re.findall(tmx,Donnees,re.M|re.I|re.DOTALL)[0]
                pagination = [str(pagination),'not limited']
            except:
                if 'current' in Donnees:pagination=['nada','not limited']
                else:pagination=['nada','nada']
    blocks=Donnees.split('<div class="film-poster"')
    blocks.pop(0)
    for block in blocks:
        try:
            rgx = '''data-id="(.+?)"'''
            Id = re.findall(rgx,block,re.M|re.I|re.DOTALL)[0]
        except:
            Id= 'nada'
        try:
            rgx = '''<a href="(.+?)">.+?<img'''
            Href = re.findall(rgx,block,re.M|re.I|re.DOTALL)[0]
        except:
            Href= 'nada'
        try:
            rgx = '''<img class="film-poster-img lazy" data-src="(.+?)"'''
            img = re.findall(rgx,block,re.M|re.I|re.DOTALL)[0]
            nam_img = img.split('/')[-1]
            dist = _distI % (nam_img)
            Downloads_Images(img,dist)
        except:
            img= 'nada'
        try:
            rgx = '''<div class="rating">(.+?)</div>'''
            rating = re.findall(rgx,block,re.M|re.I|re.DOTALL)[0]
        except:
            rating= 'nada'
        try:
            rgx = '''<div class="quality">(.+?)</div>'''
            quality = re.findall(rgx,block,re.M|re.I|re.DOTALL)[0]
        except:
            quality= 'nada'
        try:
            rgx = '''<div class="title">(.+?)</div>'''
            title = re.findall(rgx,block,re.M|re.I|re.DOTALL)[0].decode('utf-8')
            title = title.replace('فيلم '.decode('utf-8'),'')
            title = ClearTitle(title)
        except:
            title= 'title'
        try:
            rgx = '''<div class="desc">(.+?)</div>'''
            desc = re.findall(rgx,block,re.M|re.I|re.DOTALL)#[0].decode('utf-8')
        except:
            desc= 'nada'
        if desc!= 'nada':
            dsc = ''
            for a in desc:
                dsc += a.decode('utf-8')+' '
            desc = dsc
        MyDict_[Id]=[title,Href,img,nam_img,rating,quality,desc]
        i = i+1
        #if i>:break
    TXT = json.dumps(MyDict_,indent = 4)
    if len(MyDict_)==0:return False,'',''
    else:return True,export_txt(TXT),pagination
#######################################################################Import Info_Film
def get_Info_Film(url):
    MyDict_ = {}
    Discrpt_3 = []
    print url
    Donnees = get_Data(url,get='get',typ='content')
    if Donnees == '':return False,Donnees
    tmx = '''<div class="anisc-detail">(.+?)<div class="module_single_sda">'''
    try:
        blocks = re.findall(tmx,Donnees,re.M|re.I|re.DOTALL)[0].decode('utf-8')
    except:blocks='nada'
    if blocks!='nada':
        try:
            rgx = '''<span class="item rating">(.+?)</span>'''
            rating = re.findall(rgx,Donnees,re.M|re.I|re.DOTALL)[0].replace(' ','')
        except:rating='nada'
        MyDict_['rating']=rating
        try:
            rgx = '''<img src="(.+?)".+?class="film-poster-img">'''
            poster = re.findall(rgx,Donnees,re.M|re.I|re.DOTALL)[0].split('/')[-1]
        except:poster='nada'
        MyDict_['poster']=poster
        try:
            rgx = '''<a href="(.+?)" class="watchBTn">'''
            watchBTn = re.findall(rgx,blocks,re.M|re.I|re.DOTALL)[0]
        except:watchBTn='nada'
        MyDict_['Watchability']=watchBTn
        try:
            rgx = '''<div class="text">(.+?)</div>'''
            Discrpt = re.findall(rgx,blocks,re.M|re.I|re.DOTALL)[0]#.decode('utf-8')
        except:Discrpt='nada'
        MyDict_['About The Movie']=Discrpt
        try:
            rgx = '''<span class="item-head">'''
            Discrpt_1 = blocks.split(rgx)
            Discrpt_1.pop(0)
        except:Discrpt_1='nada'
        try:
            gbx = '''<div class="item">.+?<span>(.+?)</span>.+?</div>'''
            Discrpt_2 = re.findall(gbx,blocks,re.M|re.I|re.DOTALL)
        except:Discrpt_2='nada'
        if Discrpt_2!='nada':
            _KL = ''
            for f in Discrpt_2:
                if 'href' in f:continue
                _KL += f+'\n'
        MyDict_['Film Properties']=_KL
        try:
            gbx = '''<span class="text"><span>(.+?)</span> من <span>(.+?)</span></span>'''
            Rat = re.findall(gbx,Donnees,re.M|re.I|re.DOTALL)
            Rating = Rat[0][0]+'/'+Rat[0][1]
        except:Rating='nada'
        MyDict_['Rating2']=Rating
        try:
            gnx = '''<div class="item-list">(.+?)<div class="film-description w-hide">'''
            genres = re.findall(gnx,Donnees,re.S|re.M|re.I|re.DOTALL)[0]
            genres = genres.replace('\n','').replace('\t','').replace('\r','').replace('\s','')
            genre = re.findall('>(.+?)<',genres,re.S|re.M|re.I|re.DOTALL)
        except:genre='nada'
        _H = ''
        if genre!='nada':
            for w in genre:
                if w=='' or w=='  ':continue
                w = w.replace('\n','').replace('\t','').replace('\r','').replace('\n\n','')
                _H += w.decode('utf-8')+' '
        MyDict_['Genre']=_H
    return MyDict_
#######################################################################Import watch Link
def get_D1(url):
    MyListFilms = []
    NewMyListFilms = []
    HDR = {'Host': 'w.cimalek.to',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'X-Requested-With': 'XMLHttpRequest',
           'Connection': 'keep-alive',
           'Referer': url}
    _Hd = {'Host': 'zorona.cam',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
           'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Alt-Used': 'zorona.cam',
           'Connection': 'keep-alive',
           'Referer': 'https://w.cimalek.to/'}
    rgx = '''<div id='player-option-.+?' class='btn lalaplay_player_option' data-type='(.+?)' data-post='(.+?)' data-nume='(.+?)'><ul><li>(.+?)</li>'''
    try:data = get_Data(url,get='get',typ='content')
    except:data=''
    if data:
        try:Donnees = re.findall(rgx,data)
        except: Donnees=''
        if Donnees:
            for a,b,c,d in Donnees:
                link = "https://w.cimalek.to/wp-json/lalaplayer/v2/?p=%s&t=%s&n=%s" % (b,a,c)
                try:_dat = get_Data(link,get='get',typ='json()',headers=HDR)
                except:_dat=''
                if _dat:
                    _A = _dat['embed_url']
                    try:NwDat = get_Data(_A,get='get',typ='content',headers=_Hd)
                    except:NwDat=''
                    if NwDat:
                        try:
                            _rgx  = '''sources":\{"file":"(.+?)".+?"type":"(.+?)"'''
                            _file = re.findall(_rgx,NwDat)[0]
                            _file = _file.replace('\\','')
                        except:
                            try:
                                _rgx = '''{"file":"(.+?)".+?"type":"(.+?)"'''
                                _file = re.findall(_rgx,NwDat)
                            except:_file = 'nada'
                        try:
                            _rgx1 ='''"file":"(.+?)".+?"type":"(.+?)"'''
                            sub_id = re.findall(_rgx1,NwDat)
                        except:sub_id='nada'
                        if _file!='nada':
                            typo = ''
                            for lnko,label in _file:
                                lnko = lnko.replace('\\','')
                                label=label.replace('\\/','|')
                                MyListFilms.append((d,lnko))
                        if sub_id!='nada':
                            typo = ''
                            for lnk,lang in sub_id:
                                lnk = lnk.replace('\\','')
                                lang=lang.replace('\\/','|')
                                MyListFilms.append((d,lnk))
                    else:print 'nada_NwDat'
    if len(MyListFilms)!=0:
        MyListFilms = list(set(MyListFilms))
        return True,MyListFilms
    else:return False,[]
##################################################################
from Components.Label import Label
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Components.Pixmap import Pixmap
from enigma import ePixmap, eTimer, ePoint, gPixmapPtr
from Components.Sources.StaticText import StaticText
import json
import os
from sys import version_info
from Components.AVSwitch import AVSwitch
from enigma import ePoint, eSize, eTimer,ePicLoad
from enigma import getDesktop
################################################ yasser
black,white,gray='\c00000000','\c00??????','\c00808080'
blue,green,red,yellow,cyan,magenta,ivory='\c000000??','\c0000??00','\c00??0000','\c00????00','\c0000????','\c00??00??','\c0???????'
################################################ yasser
##################################################################My Imort
from Plugins.Extensions.ShowMovies.Cimalek.OutilsCimalek.AllImport import *
from Plugins.Extensions.ShowMovies.Cimalek.Home.Watchability import HomeShowMoviesSelect
#########################################
dwidth = getDesktop(0).size().width()
#########################################
class ShowMovies_New():
    def __init__(self):
        self.Loading = 'Loading  ...... List Live TV %s.. ' % 'Please wait'
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
        self.Timer = eTimer()
        self.Timer.callback.append(self.updatePoster)
        self.AnimTimer = eTimer()
        self.AnimTimer.callback.append(self.newupdateLabel)
        ##############################
        self.Page = 1
        self.picload = ePicLoad()
        self.menu = []
        self['menu'] = m2list([])
        ##############################Start
        #self.affich_DEbut()
        self.Pox = 400
        self.Poy = 350
        self.Condit = 1
    #############################
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
            self.Timer.start(50//10, True)
        else:
            self.Timer.stop()
    #############################
    def newupdateLabel(self):
        self.yx += +100#self.dyx
        self['Box_0'].instance.move(ePoint(self.yx+400, 5))
        self['Box_1'].instance.move(ePoint(self.yx+400, 55))
        self['Box_2'].instance.move(ePoint(self.yx+400, 110))
        self['Box_3'].instance.move(ePoint(self.yx+400, 165))
        if self.yx < self.y22:
            self.AnimTimer.start(50//10, True)
        else:
            self.AnimTimer.stop()
    #############################
    def layoutFinish(self):
        if self.Msg_[0]:
            for x in range(10):
                self['poster_'+str(x)].instance.move(ePoint(0, 1080))
            self.Timer.start(50//10, True)
    #############################
    def getposi_image(self):
        self.Positions = [(5,37),(5,792),(218,792),(431,792),(644,792),(857,792),(1070,792),(1283,792),(1496,792),(1709,792)]
        self.sizeimag = [(185,278)]
    #############################
    def Moveframe(self):
        self.yx = self.y11
        self.dyx = (self.y22 - self.y11) // 40
        if self.newupdateLabel in self.AnimTimer.callback:
            self.AnimTimer.callback.remove(self.newupdateLabel)
            self.AnimTimer.callback.append(self.showDescAnim)
        self.AnimTimer.start(50//10, True)
    #############################
    def ImportImages(self,url=None,pageT=None):
        self.timeaffich.stop()
        self.menu = []
        uri   = '''https://w.cimalek.to/category/aflam-online/'''
        uri1  = '''https://w.cimalek.to/category/aflam-online/page/%s/''' % (str(self.Page))
        uri2  = '''https://w.cimalek.to/recent/'''
        uri3  = '''https://w.cimalek.to/category/aflam-online/page/255/'''
        uri4  ='''https://w.cimalek.to/recent/page/1325/'''
        linko = '''https://w.cimalek.to/release/2023/page/%s/?type=movies''' % (str(self.Page))
        linko1= '''https://w.cimalek.to/category/netflix-movies/page/%s/'''  % (str(self.Page))
        self.Msg_ = get_My_Donnees(linko1)
        if self.Msg_[0]:
            self.NewListJS = Read_Js()
            for _dons in self.NewListJS:
                Prblm = self.NewListJS[_dons][0]#ClearProf(_dons)
                self.menu.append(show_Movies(str(Prblm)))
            self.pagination = self.Msg_[2]
            if self.pagination == ['nada','nada']:self.Page=1
            else:
                p_1 =self.pagination[0]
                p_2 =self.pagination[1]
                if p_2== 'not limited':
                    if p_1!='nada':
                        self.Page = int(p_1)
                        _B = 'الصفحة'.encode('utf-8')+'  '+str(int(p_1)-1)+' / '+str(p_2)
                    else:
                        self.Page = self.Page
                        _B = 'الصفحة'.encode('utf-8')+'  '+str(self.Page)+' / '+str(p_2)
                        self.Page = 1
                else:
                    if self.Page < int(p_2):self.Page = int(p_1) + 1
                    else:self.Page=1
                    _B = 'الصفحة'.encode('utf-8')+'  '+str(p_1)+' / '+str(p_2)
                self['Infos_indx'].setText(_B)
        else:
            self.menu.append(show_Movies('Not Data'))
        self['menu'].l.setList(self.menu)
        self['menu'].l.setItemHeight(35)
        self['menu'].moveToIndex(0)
    #############################
    def decodeImage(self):
        #self.AnimTimer.stop()
        if self.Msg_[0]:
            if len(self.NewListJS)<10:self.decodeImage_inferieur()
            else:self.decodeImage_6(0)
    def decodeImage_inferieur(self):
        for b in range(len(self.NewListJS),10):
            self['poster_'+str(b)].hide()
        Ds = len(self.NewListJS)
        self.index = self['menu'].getSelectionIndex()
        if self.index == len(self.NewListJS)-1:
            self.decodeImage_inferieur_1()
            return
        
        else:
            listrang = range(self.index,Ds)+range(self.index+1)
        for f in range(Ds):#range(self.index,Fs):
            _k = listrang[f]
            _H = self.NewListJS.items()[_k][1]
            picfile = self.FoldImag+str(_H[3])
            picobject = self['poster_'+str(f)]	
            picobject.instance.setPixmap(gPixmapPtr())
            self.scale = AVSwitch().getFramebufferScale()
            self.picload = ePicLoad()
            size = picobject.instance.size()
            #Write_Donnees(str(listrang)+'_____'+str(_k)+'_____'+str(picfile)+'_____'+str(f)+'_____'+str(self.index)+'\n')
            if _k==self.index:self.picload.setPara((500,700,0,0,0,0,'#80000000'))
            else:self.picload.setPara((185,278,0,0,0,0,'#80000000'))
            if self.picload.startDecode(picfile, 0, 0, False) == 0:
                ptr = self.picload.getData()
                if ptr != None:
                    picobject.instance.setPixmap(ptr)
                    picobject.show()
                    del self.picload
        #Write_Donnees('*********************************************************************\n')
        return
    def decodeImage_inferieur_1(self):
        Nw_List=[len(self.NewListJS)-1]+range(len(self.NewListJS)-1)
        self.index = self['menu'].getSelectionIndex()
        for f in Nw_List:
            _M = ''
            _H = self.NewListJS.items()[f][1]
            picfile = self.FoldImag+str(_H[3])
            if f == Nw_List[0]:T=0
            else:T=f+1
            picobject = self['poster_'+str(T)]	
            picobject.instance.setPixmap(gPixmapPtr())
            self.scale = AVSwitch().getFramebufferScale()
            size = picobject.instance.size()
            self.picload = ePicLoad()
            #Write_Donnees('decodeImage_inferieur_1_____ '+str(Nw_List)+'_____ '+str(_H[3])+'_____ '+str(f)+'_____ '+str(T)+'_____ '+'\n')
            if f == self.index:self.picload.setPara((500,700,0,0,0,0,'#80000000'))
            else:self.picload.setPara((185,278,0,0,0,0,'#80000000'))
            if self.picload.startDecode(picfile, 0, 0, False) == 0:
                ptr = self.picload.getData()
                if ptr != None:
                    picobject.instance.setPixmap(ptr)
                    picobject.show()
                    del self.picload
        #Write_Donnees('//////////////////////////////////////////////////////////////////////\n')
    #############################
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
    #############################
    def decodeImage_uniq(self):
        if len(self.NewListJS)<10:Nw_List=range(len(self.NewListJS)-1)
        else:Nw_List =[len(self.NewListJS)-1,0,1,2,3,4,5,6,7,8]
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
    #############################
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
    #############################
    def showDescAnim(self):
        if self.Msg_[0]:
            self.yx += +100#self.dyx+100
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
            self['Box_0'].instance.move(ePoint(self.yx+400, 5))
            self['Box_1'].instance.move(ePoint(self.yx+400, 55))
            self['Box_2'].instance.move(ePoint(self.yx+400, 110))
            self['Box_3'].instance.move(ePoint(self.yx+400, 165))
            self.AnimTimer.start(50//10, True)
            if self.yx < self.y22:
                self.AnimTimer.start(50//10, True)
            else:
                self.AnimTimer.stop()
        Taill_Fold = get_Taille()
        self['Infos'].setText('Image File Size : \c0000????'+str(Taill_Fold))
    #############################
    def setText_Films(self):
        if self.Msg_[0]:
            #self['Infos'].setText('wait ......... data download')
            self.setText_Films_1()
    #############################
    def setText_Films_1(self):
        index = self['menu'].getSelectionIndex()
        if len(self.NewListJS)<10:
            self.setText_Films_2()
            return
        Y = len(self.NewListJS)-1
        if index == Y:
            Nw_List =[0,1,2,3,4,5,6,7,8]
            if Y+1<10 :Nw_1 =range(1,Y+1)
            else:Nw_1 =range(1,10)
            for x in Nw_1:#for x in range(1,10):
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
                self.session.open(MessageBox, _(str(_G)+'\nindex ='+str(index)), MessageBox.TYPE_INFO)
        p_1 =self.pagination[0]
        p_2 =self.pagination[1]
        _B = 'الصفحة'.encode('utf-8')+'  '+str(p_1)+' / '+str(p_2)
    #############################
    def setText_Films_2(self):
        index = self['menu'].getSelectionIndex()
        Y = len(self.NewListJS)-1
        if index == Y:
            Nw_List =range(Y)
            #Write_Donnees(str(index)+'_____'+str(Y)+'_____'+str(Nw_List)+'\n')
            try:
                for x in range(1,Y+1):
                    _D = Nw_List[x-1]
                    _G = self.NewListJS.items()[_D][1]
                    self['Title_'+str(x)].setText(str(_G[0]))
            except:
                pass
        elif 0 < index < Y:
            Nw_List =range(index,Y+1)+range(index)
            try:
                for x in range(1,Y+1):
                    _D = Nw_List[x]
                    _G = self.NewListJS.items()[_D][1]
                    #Write_Donnees('coucou****************'+str(_G[0])+'\n')
                    self['Title_'+str(x)].setText(str(_G[0]))
                #Write_Donnees('=========================================================\n')
            except:
                pass
        else:
            try:
                for x in range(1,Y+1):
                    _G = self.NewListJS.items()[x][1]
                    self['Title_'+str(x)].setText(str(_G[0]))
            except:
                pass
                #self.session.open(MessageBox, _(str(_G)+'\nindex ='+str(index)), MessageBox.TYPE_INFO)
        p_1 =self.pagination[0]
        p_2 =self.pagination[1]
        _B = 'الصفحة'.encode('utf-8')+'  '+str(p_1)+' / '+str(p_2)
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
    ##############################
    def Import_My_Infos(self):
        if self.Msg_[0]:
            index = self['menu'].getSelectionIndex()
            _H = self.NewListJS.items()[index][1][1]
            self._Info = get_Info_Film(_H)
            self.watc = ''
            # i= 4
            List_Secour = ['الاسم الاصلي'.encode('utf-8'),'البلد المنشئ'.encode('utf-8'),'المدة'.encode('utf-8'),'تاريخ العرض'.encode('utf-8'),'اللغة'.encode('utf-8')]
            if len(self._Info)!=0:
                _Title = self['menu'].getCurrent()[0]
                self.session.open(HomeShowMoviesSelect,self._Info,_Title)
