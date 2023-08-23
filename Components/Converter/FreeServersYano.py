#!/usr/bin/python
# -*- coding: utf-8 -*-
from Components.Converter.Converter import Converter
from Components.Element import cached
from Tools.Directories import fileExists
from Components.Converter.Poll import Poll
import requests,json
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore',InsecureRequestWarning)
import sys
PY3 = (sys.version_info[0] == 3)
try:
	if PY3:
		from _thread import start_new_thread
	else:
		from thread import start_new_thread
except:
	pass
from urllib import quote_plus
import os
def get_Size(fil):
    if fileExists(fil):
        stats = os.stat(fil)
        return stats.st_size
    else:return '.......'
def get_Taille(folder,total):
    if fileExists(folder):
        try:
            file_size = os.path.getsize(folder)
            Taille = "%0.1f MB" % (int(file_size)/(1024*1024.0))
        except:Taille='nada'
    else:Taille = 'nada'
    if fileExists(total):
        try:
            file = open(total,"r")
            ToTal = file.read()
            ToTal = "%0.1f MB" % (int(ToTal)/(1024*1024.0))
            file.close()
        except:ToTal='nada'
    else:ToTal='nada'
    return str(Taille),str(ToTal)
def web_info(message):
    try:
        message = quote_plus(str(message))
        cmd = "wget -qO - 'http://127.0.0.1/web/message?type=1&timeout=20&text=%s' 2>/dev/null &" % message
        #debug(cmd, 'CMD -> Console -> WEBIF')
        os.popen(cmd)
    except:
        print 'web_info ERROR'
class FreeDownloadYano(Poll,Converter,object):
    DOWNLOAD = 0
    def __init__(self, type):
        Converter.__init__(self, type)
        Poll.__init__(self)
        self.poll_interval = 1000
        self.poll_enabled = True
        self.messg_1 = 'Problem With Downloading With FreeDownloadYano The Movie %s\n%s'
        self.messg_2 = 'Problem With Downloading With FreeDownloadYano The Movie %s\n%s\n Stopped At%s'
        self.messg_3 = 'Your Movie %s download is complete %s'
        self.Pourcentage = '0%'
        self.url = ''
        self.filename = ''
        self.downloaded = 0
        self.total = ''
        self.A = ''
        self.action = False
        self.type = {'download': self.DOWNLOAD,}[type]
        self.get_service()
    def Write_Js_Yano(self,Txt=None,Fold=None):
        path = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/FilsJs/DownloadMovies.js'
        Dicremove = {'url':'nada','filename':'nada'}
        if Fold is not None and Txt is not None:
            with open(Fold,'w') as g:
                g.write(str(Txt))
                g.close()
        else:
            with open(path,'w') as chcfg:
                json.dump(Dicremove, chcfg,ensure_ascii=False)
        print "OK"
    def get_FoldMovies(self):
        path = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/FilsJs/DownloadMovies.js'
        if fileExists(path):
            with open(path) as jsf:
                urljsdata=json.load(jsf)
            self.url      = urljsdata['url']
            self.filename = urljsdata['filename']+'.mp4'
        return self.filename
    def get_service(self):
        path = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/FilsJs/DownloadMovies.js'
        if fileExists(path):
            with open(path) as jsf:
                urljsdata=json.load(jsf)
            self.url      = urljsdata['url']
            self.filename = urljsdata['filename']+'.mp4'
            start_new_thread(self.DownloadFiles, ())
            if ".m3u8" in self.url:
                self.downloaded = "Problem With Downloading With .m3u8 File"
                return self.downloaded
        else:self.downloaded='Coucou____FreeDownloadYano File Not Found'
    def DownloadFiles(self):
            if self.url=='nada' and 'nada' in self.filename.encode('utf-8'): 
                self.downloaded = 'Not File............'
                return
            if '.m3u' in self.url:
                self.downloaded = "Problem With Downloading With .m3u8 File"
                return
            self.Titl = self.filename.encode('utf-8').split('/')[-1]
            resp = requests.get(self.url,verify=False,stream=True)
            with open(self.filename.encode('utf-8'),'wb') as f:
                self.total = int(resp.headers.get('content-length'))
                self.Write_Js_Yano(Txt=self.total,Fold='/tmp/Total')
                for chunk in resp.iter_content(chunk_size=max(int(self.total/10000), 1024*1024)):
                    if chunk:
                        self.downloaded += len(chunk)
                        f.write(chunk)
                        f.flush()
                    if (self.downloaded/self.total) >= 1:
                        self.Write_Js_Yano()
                        self.Write_Js_Yano(Txt='...',Fold='/tmp/Total')
                        web_info(self.messg_3 % (self.Titl,self.filename.encode('utf-8')))
    @cached
    def getText(self):
        if self.type == self.DOWNLOAD:#return str(self.filename)
            self.filename = self.get_FoldMovies()
            if 'nada' in self.filename.encode('utf-8'):return 'No File To Download'
            Taille,total = get_Taille(self.filename.encode('utf-8'),'/tmp/Total')
            try:
                K = Taille.replace(' MB','')#int(str(Taille).replace(' MB','').replace('\n','').replace(' ',''))
                V = total.replace(' MB','')#.replace('\n','').replace(' ','')
                self.A = "%.0f" % float(100*((float(K))/(float(V))))
            except:self.A=''
            return str(self.A)+' %     '+str(Taille)+'/'+str(total)
    text = property(getText)
    def changed(self, what):
        Converter.changed(self, (self.CHANGED_POLL,))
