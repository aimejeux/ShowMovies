#!/usr/bin/python
# -*- coding: utf-8 -*-
################################### modified by aime_jeux ##################################
#############                           Aout 2021                              #############
############################################################################################
import os
from os import system as os_system
import sys
#####################################################################
if os.path.exists('/var/lib/dpkg/status'):
    enigmaos = 'oe2.2'
else:
    enigmaos = 'oe2.0'
##############################################################
def is_ascii(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        try:s.decode('utf-8')
        except UnicodeDecodeError:
            return False
    else:
        return True
def colorize(txt,selcolor='white',marker1=":",marker2="]"):
    if enigmaos == "oe2.2" or  is_ascii(txt)==False:
        return txt
    colors={'black':'\c00000000','white':'\c00??????','grey':'\c00808080',
    'blue':'\c000000??','green':'\c0000??00','red':'\c00??0000','ivory':"\c0???????",
    'yellow':'\c00????00','cyan':'\\c0000????','magenta':'\c00??00??'}
    color=colors.get(selcolor,'\c0000????')
    color1=colors.get('cyan','\c0000????')
    try:
        if not marker1 in txt :
            return color+" "+txt
        txtparts=txt.split(marker1)
        txt1=txtparts[0]
        txt2=txtparts[1]
        if marker2 in txt:
            txt3=txt2.split(marker2)#[0]
            if len(txt3)>=2:
                if txt3[1]!='':
                    txt3,txt4 = txt3[0],txt3[1]
                    ftxt=txt1+" "+color+marker1+txt3+color1+txt4
                else:
                    txt3= txt3[0]
                    ftxt=txt1+" "+color+marker1+txt3#+marker2
        else:
            txt3=txt2
            ftxt=txt1+" "+color+marker1+txt3#+marker2
        return ftxt
    except:
        return txt