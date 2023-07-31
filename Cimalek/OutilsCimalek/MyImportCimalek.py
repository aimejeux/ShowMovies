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
    print 'url = ',url
    print 'get = ',get
    print 'typ = ',typ
    print 'param = ',param
    print 'headers = ',headers
    print 'type(headers) = ',type(headers)
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
    Donnees = get_Data(url,get='get',typ='content')
    if Donnees == '':return False,Donnees,''
    tmx = '''<div class="pagination-tol"><span>(.+?)</span>'''
    try:
        pagination = re.findall(tmx,Donnees,re.M|re.I|re.DOTALL)[0].decode('utf-8')
        pagination = ClearTitle(pagination)
        pagination = pagination.split()
    except:pagination='nada'
    pagination
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
        #print 'Discrpt ----> ',Discrpt
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
                _KL += f+'\n'#Discrpt_3.append((f))
                #print f
        MyDict_['Film Properties']=_KL
        #print 'Discrpt_2 ----> ',_KL
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
            #print _H
        MyDict_['Genre']=_H
        #print 'genre ----> ',_H
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
    try:data = get_Data(url,get='get',typ='content')#requests.get(url,verify=False).content#get_Data(url,get='get',typ='content')#requests.get(url,verify=False).content param=None,headers=None
    except:data=''#get_Data(url,get='get',typ='content')
    if data:
        try:Donnees = re.findall(rgx,data)
        except: Donnees=''
        if Donnees:
            i = 1
            for a,b,c,d in Donnees:#('Cloud_V1', '569243', '1')
                link = "https://w.cimalek.to/wp-json/lalaplayer/v2/?p=%s&t=%s&n=%s" % (b,a,c)
                #print '/////////////////////',link param=None,headers=None
                try:_dat = get_Data(link,get='get',typ='json()',headers=HDR)#requests.get(link,headers=HDR,verify=False).json()
                except:_dat=''
                if _dat:
                    _A = _dat['embed_url']
                    #print '*****************', _A
                    try:NwDat = get_Data(_A,get='get',typ='content',headers=_Hd)#requests.get(_A,headers=_Hd,verify=False).content
                    except:NwDat=''
                    #print '+++++++++++++++',NwDat
                    if NwDat:
                        #print "============================",NwDat
                        try:
                            _rgx  = '''sources":\{"file":"(.+?)".+?"type":"(.+?)"'''
                            _file = re.findall(_rgx,NwDat)[0]
                            _file = _file.replace('\\','')
                        except:
                            try:
                                _rgx = '''{"file":"(.+?)".+?"type":"(.+?)"'''
                                #_rgx  = '''\{"file":"(.+?)"'''
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
                    #print "===============================================",str(i)
                    i = i + 1
    if len(MyListFilms)!=0:
        MyListFilms = list(set(MyListFilms))
        # for a,b in MyListFilms:
            # NewMyListFilms.append(show_LinkMovies(a,b))
        return True,MyListFilms
    else:return False,[]