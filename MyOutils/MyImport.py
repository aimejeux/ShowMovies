#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests,re,base64,shutil
St = requests.Session()
from Tools.Directories import fileExists, pathExists
########################################################################
# import warnings
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# warnings.simplefilter('ignore',InsecureRequestWarning)
########################################################################
import sys, os
os_platform=sys.platform
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
cfg_path = os.path.join(__location__, 'Test.xml')
def export_txt(txt):
    with open(cfg_path, "w", encoding="utf-8") as f:
        f.write(txt)
    f.close()
def Downloads_Images(uri,dist):
    if fileExists(dist):pass
    else:
        response = St.get(uri, stream=True)
        with open(dist, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
_distI = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/MyOutils/IMAGES_D/Page_%s_i_%s%s'
def get_data_Fajre(url,page):
    url = url+'page/'+str(page)+'/'
    try:data = St.get(url,verify=False).text
    except:data=''
    if data:
        #Rgx = '''<div class="poster"><img src="(.+?)" alt.+?<div class="see"></div></a></div><div class="data"><h3><a href="(.+?)">(.+?)</a></h3> <span>(.+?)</span></div> <div class="animation-1 dtinfo"> <div class="title"> <h4>.+?</h4> </div> <div class="metadata"> <span class="imdb">(.+?)</span> <span>(.+?)</span> <span>(.+?)</span> <span>.+?</span> </div> <div class="texto">(.+?)</div> <div class="genres"><div class="mta">(.+?)</a></div></div> </div>'''
        Rgx = '''<div class="poster"><img src="(.+?)" alt.+?<div class="see"></div></a></div><div class="data"><h3><a href="(.+?)">(.+?)</a></h3> <span>.+?</span>'''
        try:
            My_Infos = re.findall(Rgx,data,re.M|re.I|re.DOTALL)
        except:My_Infos=''
        if My_Infos:
            try:
                Tmx = '''<div class="pagination"><span>(.+?)</span>'''
                pagination = re.findall(Tmx,data,re.M|re.I|re.DOTALL)[0]
                a = 'صفحة'.decode('utf-8')
                b = 'من'.decode('utf-8')
                pagination = pagination.replace(a,'').replace(b,'')
                _pagination = int(pagination.split()[1])
            except:_pagination='0'
            i = 0
            #for img,href,title,tim,imdb,annee,durtfilm,infos,donnees in My_Infos:
            for img,href,title in My_Infos:
                print 'href = ',href
                print "-----------------"
                # print 'tim = ',tim
                # print "-----------------"
                print 'img = ',img
                print 'ooooo',img[-4:]
                #dist = _distI+str(page)+'_i_'+str(i)+img[-4:]
                dist = _distI % (str(page),str(i),img[-4:])
                Downloads_Images(img,dist)
                print "-----------------"
                print 'title = ',title
                print "-----------------"
                # print 'imdb = ',imdb
                # print "-----------------"
                # print 'annee = ',annee
                # print "-----------------"
                # if 'span' in durtfilm:durtfilm='...'
                # print 'durtfilm = ',durtfilm
                # print "-----------------"
                # print 'infos = ',infos
                # print "-----------------"
                # Mohawala = re.findall('"tag">(.+?)</a>',donnees,re.M|re.I|re.DOTALL)
                # xt=''
                # for xt in Mohawala:
                    # print 'donnees = ',xt
                print "===========================================================",str(i)
                if i>50:break
                i=i+1
            return 'Image_Download',_pagination
        else:return 'Image_Not_Download','0'