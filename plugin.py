from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Components.Pixmap import Pixmap
from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.AllImport import *
from Plugins.Extensions.ShowMovies.TestMove import MenuShowMovies
from Plugins.Extensions.ShowMovies.CineMa.Home.Home import HomeShowMovies
#########################################
Ver = getversioninfo()#1.0
#########################################
import os,errno,shutil
Fold_1 = '/media/hdd/CineMa/Home'
Fold_2 = '/media/hdd/CineMa/Images'
Fold_3 = '/media/hdd/CineMa/i_0.png'
Fold_4 = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/Images/i_0.png'
ListImage = [Fold_1,Fold_2]
for fold in ListImage:
    try:os.makedirs(fold)
    except OSError as e:
        if e.errno == errno.EEXIST:
            print('Directory not created.')
        else:raise
try:
    if os.path.exists(Fold_3):
        print 'Img Exist'
    else:shutil.copy(Fold_4,Fold_3)
except:pass
#########################################
def main(session, **kwargs):
    if isHD():
        session.open(MessageBox, _('Skin is not supported\nShowMovies works only with FHD skins'), MessageBox.TYPE_ERROR)
    else:
        session.open(HomeShowMovies)
        #session.open(MenuShowMovies)
#########################################
def showmenu(menuid, **kwargs):
    if menuid == "mainmenu":
        return [("ShowMovies", main, "ShowMovies", 1)]
    else:
        return []        
#########################################
def Plugins(**kwargs):
    Descriptors=[]
    Descriptors.append(PluginDescriptor(where=[PluginDescriptor.WHERE_MENU], fnc=showmenu))
    Descriptors.append(PluginDescriptor(name='ShowMovies', description='ShowMovies By AbouYacine {}'.format(Ver), where=PluginDescriptor.WHERE_PLUGINMENU, icon='genuine.png', fnc=main))
    return Descriptors
#########################################