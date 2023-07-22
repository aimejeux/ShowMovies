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
def Read_Js():
    with open(cfg_path) as mon_Js:
        data = json.load(mon_Js)
    #print type(data)
    return data
#######################################################################Get Data From Js File
def get_Data(url,get='',typ='',param=None,headers=None):
    _Data = ''
    if param and headers:
        try:exec "_Data = St."+get+"(url,data=param,heades=headers,verify=False,timeout=10)."+typ
        except:_Data = ''
    elif param and not headers:
        try:exec "_Data = St."+get+"(url,data=param,verify=False,timeout=10)."+typ
        except:_Data = ''
    elif headers and not param :
        try:exec "_Data = St."+get+"(url,heades=headers,verify=False,timeout=10)."+typ
        except:_Data = ''
    else :
        try: exec "_Data=St."+get+"(url,verify=False,timeout=10)."+typ
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
    blocks=Donnees.split('<div class="film-poster"')
    blocks.pop(0)
    i = 1
    for block in blocks:
        try:
            rgx = '''data-id="(.+?)"'''
            Id = re.findall(rgx,block,re.M|re.I|re.DOTALL)[0]
        except:
            Id= 'nada'
        #print Id
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
        #print img
        try:
            rgx = '''<div class="rating">(.+?)</div>'''
            rating = re.findall(rgx,block,re.M|re.I|re.DOTALL)[0]
        except:
            rating= 'nada'
        #print rating
        try:
            rgx = '''<div class="quality">(.+?)</div>'''
            quality = re.findall(rgx,block,re.M|re.I|re.DOTALL)[0]
        except:
            quality= 'nada'
        #print quality
        try:
            rgx = '''<div class="title">(.+?)</div>'''
            title = re.findall(rgx,block,re.M|re.I|re.DOTALL)[0].decode('utf-8')
            title = title.replace('فيلم '.decode('utf-8'),'')
            title = ClearTitle(title)
        except:
            title= 'title'
        #print title
        try:
            rgx = '''<div class="desc">(.+?)</div>'''
            desc = re.findall(rgx,block,re.M|re.I|re.DOTALL)[0].decode('utf-8')
        except:
            desc= 'nada'
        #print desc
        MyDict_[Id]=[title,Href,img,nam_img,rating,quality,desc]
        #print "==========================================",str(i)
        i = i + 1
    TXT = json.dumps(MyDict_)
    return True,export_txt(TXT),pagination
