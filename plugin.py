from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Components.Pixmap import Pixmap
from Plugins.Extensions.ShowMovies.TestMove import LinuxsatTestMoveImage,isHD
#########################################
Ver = 1.0
#########################################
def main(session, **kwargs):
    if isHD():
        session.open(MessageBox, _('Skin is not supported\nShowMovies works only with FHD skins'), MessageBox.TYPE_ERROR)
    else:
        session.open(LinuxsatTestMoveImage)
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