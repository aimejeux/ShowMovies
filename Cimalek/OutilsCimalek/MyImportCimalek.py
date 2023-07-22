#!/usr/bin/python
# -*- coding: utf-8 -*-
import json,re,requests,os,shutil
########################################################################
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
St = requests.Session()
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
    txt = txt.replace('&#8217;s','s-')
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
            desc = re.findall(rgx,block,re.M|re.I|re.DOTALL)[0].decode('utf-8')
        except:
            desc= 'nada'
        MyDict_[Id]=[title,Href,img,nam_img,rating,quality,desc]
    TXT = json.dumps(MyDict_)
    return True,export_txt(TXT),pagination
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
            rgx = '''<a href="(.+?)" class="watchBTn">'''
            watchBTn = re.findall(rgx,blocks,re.M|re.I|re.DOTALL)[0]
        except:watchBTn='nada'
        MyDict_['watchBTn']=watchBTn
        try:
            rgx = '''<div class="text">(.+?)</div>'''
            Discrpt = re.findall(rgx,blocks,re.M|re.I|re.DOTALL)[0]
        except:Discrpt='nada'
        MyDict_['Discrpt']=Discrpt
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
            for f in Discrpt_2:
                if 'href' in f:continue
                Discrpt_3.append((f))
                print f
            MyDict_['Discrpt_2']=Discrpt_3
        try:
            gbx = '''<span class="text"><span>(.+?)</span> من <span>(.+?)</span></span>'''
            Rat = re.findall(gbx,Donnees,re.M|re.I|re.DOTALL)
            Rating = Rat[0][0]+'/'+Rat[0][1]
        except:Rating='nada'
        MyDict_['Rating']=Rating
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
            print _H
            MyDict_['genre']=_H
    return MyDict_
#######################################################################Import watch Link
def get_D1(url):
    MyListFilms = []
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
    rgx = '''<div id='player-option-.+?' class='btn lalaplay_player_option' data-type='(.+?)' data-post='(.+?)' data-nume='(.+?)'>'''
    try:data = get_Data(url,get='get',typ='content')
    except:data=''
    if data:
        try:Donnees = re.findall(rgx,data)
        except: Donnees=''
        if Donnees:
            i = 1
            for a,b,c in Donnees:#('Cloud_V1', '569243', '1')
                link = "https://w.cimalek.to/wp-json/lalaplayer/v2/?p=%s&t=%s&n=%s" % (b,a,c)
                try:_dat = get_Data(link,get='get',typ='json()',headers=HDR)
                except:_dat=''
                if _dat:
                    _A = _dat['embed_url']
                    try:NwDat = get_Data(_A,get='get',typ='content',headers=_Hd)
                    except:NwDat=''
                    if NwDat:
                        try:
                            _rgx  = '''sources":\{"file":"(.+?)","label":"(.+?)"'''
                            _file = re.findall(_rgx,NwDat)[0]
                            _file = _file.replace('\\','')
                        except:
                            try:
                                _rgx = '''{"file":"(.+?)","label":"(.+?)","type"'''
                                _file = re.findall(_rgx,NwDat)
                            except:_file = 'nada'
                        try:
                            _rgx1 ='''"sub_id":.+?,"language":"(.+?)",.+?,"file":"(.+?)"'''
                            sub_id = re.findall(_rgx1,NwDat)
                        except:sub_id='nada'
                        if _file!='nada':
                            for lnko,label in _file:
                                lnko = lnko.replace('\\','')
                                MyListFilms.append((label,lnko))
                        if sub_id!='nada':
                            for lang,lnk in sub_id:
                                lnk = lnk.replace('\\','')
                                MyListFilms.append((lang,lnk))
                    else:print 'nada_NwDat'
    if len(MyListFilms)!=0:return True,MyListFilms
    else:return False,[]
