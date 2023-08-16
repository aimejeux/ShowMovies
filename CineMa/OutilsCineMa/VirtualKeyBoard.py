from enigma import eListboxPythonMultiContent, gFont, RT_HALIGN_CENTER, RT_VALIGN_CENTER, getPrevAsciiCode
from Screens.Screen import Screen
from Components.Language import language
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Tools.Directories import resolveFilename, SCOPE_CURRENT_SKIN, SCOPE_FONTS
from Tools.LoadPixmap import LoadPixmap
import skin
# from Plugins.Extensions.NcamAddons.Componen.ConfigListNcam import ConfigListNcam, ConfigListNcamScreen
from skin import loadSkin
from enigma import getDesktop
dwidth = getDesktop(0).size().width()
PLUGIN_PATH = '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/Skins'
class VirtualKeyBoardList(MenuList):
    def __init__(self, list, enableWrapAround = False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        font = skin.fonts.get('VirtualKeyBoard_1', ('Regular', 40, 20))
        self.l.setFont(0, gFont(font[0], font[1]))
        self.l.setFont(1, gFont('Regular', 30))
        self.l.setFont(2, gFont('Regular', 24))
        self.l.setFont(3, gFont('Regular', 18))
        self.l.setItemHeight(font[2])
def VirtualKeyBoardEntryComponent(keys, selectedKey, shiftMode = False):
    key_backspace = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imageskin/vkey_backspace.png'))
    key_bg = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imageskin/vkey_bg.png'))
    key_clr = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imageskin/vkey_clr.png'))
    key_esc = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imageskin/vkey_esc.png'))
    key_ok = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imageskin/vkey_ok.png'))
    key_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imageskin/vkey_sel.png'))
    key_shift = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imageskin/vkey_shift.png'))
    key_shift_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imageskin/vkey_shift_sel.png'))
    key_space = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imageskin/vkey_space.png'))
    res = [keys]
    x = 0
    count = 0
    if shiftMode:
        shiftkey_png = key_shift_sel
    else:
        shiftkey_png = key_shift
    for key in keys:
        xu = ''
        width = None
        if key == 'EXIT':
            width = key_esc.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 100), png=key_esc))
        elif key == 'BACKSPACE':
            width = key_backspace.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 100), png=key_backspace))
        elif key == 'CLEAR':
            width = key_clr.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 100), png=key_clr))
        elif key == 'SHIFT':
            width = shiftkey_png.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 100), png=shiftkey_png))
        elif key == 'SPACE':
            width = key_space.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 100), png=key_space))
        elif key == 'OK':
            width = key_ok.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 100), png=key_ok))
        else:
            if key == 'http://' or key == '.com':
                xu = 1
            else:
                xu = 0
            width = key_bg.size().width()
            res.extend((MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 100), png=key_bg), MultiContentEntryText(pos=(x, 25), size=(width, 45), font=xu, text=key.encode('utf-8'), flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER)))
        if selectedKey == count:
            width = key_sel.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 100), png=key_sel))
        if width is not None:
            x += width
        else:
            x += 45
        count += 1
    return res
def VirtualKeyBoardEntryComponentsd(keys, selectedKey, shiftMode = False):
    key_backspace = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imagesdkeyboard/vkey_backspace.png'))
    key_bg = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imagesdkeyboard/vkey_bg.png'))
    key_clr = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imagesdkeyboard/vkey_clr.png'))
    key_esc = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imagesdkeyboard/vkey_esc.png'))
    key_ok = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imagesdkeyboard/vkey_ok.png'))
    key_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imagesdkeyboard/vkey_sel.png'))
    key_shift = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imagesdkeyboard/vkey_shift.png'))
    key_shift_sel = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imagesdkeyboard/vkey_shift_sel.png'))
    key_space = LoadPixmap(cached=True, path=resolveFilename(SCOPE_CURRENT_SKIN, '/usr/lib/enigma2/python/Plugins/Extensions/ShowMovies/CineMa/Images/imagesdkeyboard/vkey_space.png'))
    res = [keys]
    x = 0
    count = 0
    if shiftMode:
        shiftkey_png = key_shift_sel
    else:
        shiftkey_png = key_shift
    for key in keys:
        xu = ''
        width = None
        if key == 'EXIT':
            width = key_esc.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_esc))
        elif key == 'BACKSPACE':
            width = key_backspace.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_backspace))
        elif key == 'CLEAR':
            width = key_clr.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_clr))
        elif key == 'SHIFT':
            width = shiftkey_png.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=shiftkey_png))
        elif key == 'SPACE':
            width = key_space.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_space))
        elif key == 'OK':
            width = key_ok.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_ok))
        else:
            if key == 'http://' or key == '.com':
                xu = 3
            else:
                xu = 2
            width = key_bg.size().width()
            res.extend((MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_bg), MultiContentEntryText(pos=(x, 0), size=(width, 45), font=xu, text=key.encode('utf-8'), flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER)))
        if selectedKey == count:
            width = key_sel.size().width()
            res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, 45), png=key_sel))
        if width is not None:
            x += width
        else:
            x += 45
        count += 1
    return res
class VirtualKeyBoard_1(Screen):
    def __init__(self, session, title = '', text = ''):
        Screen.__init__(self, session)
        skin = loadSkin(PLUGIN_PATH + '/VirtualKeyBoardFHD.xml')
        self.keys_list = []
        self.shiftkeys_list = []
        self.lang = language.getLanguage()
        self.nextLang = None
        self.shiftMode = False
        self.text = text
        self.Title = 'Show_Movies Virtual KeyBoard'
        self.selectedKey = 0
        self['country'] = StaticText('')
        self['header'] = Label(title)
        self['text'] = Label(self.text)
        self['list'] = VirtualKeyBoardList([])
        self['actions'] = ActionMap(['OkCancelActions',
         'WizardActions',
         'ColorActions',
         'KeyboardInputActions',
         'InputBoxActions',
         'InputAsciiActions'], {'ok': self.okClicked,
         'cancel': self.exit,
         'left': self.left,
         'right': self.right,
         'up': self.up,
         'down': self.down,
         'red': self.exit,
         'green': self.ok,
         'yellow': self.switchLang,
         'blue': self.shiftkeys,
         'deleteBackward': self.backClicked,
         'back': self.exit}, -2)
        self.setLang()
        self.onExecBegin.append(self.setKeyboardModeAscii)
        if dwidth == 1280:
            self.onLayoutFinish.append(self.buildVirtualKeyBoardsd)
        else:
            self.onLayoutFinish.append(self.buildVirtualKeyBoard)
        return
    def shiftkeys(self):
        if self.shiftMode == False:
            self.shiftMode = True
        else:
            self.shiftMode = False
        self.selectedKey = 0
        if dwidth == 1280:
            self.buildVirtualKeyBoardsd()
        else:
            self.buildVirtualKeyBoard()
    def switchLang(self):
        self.lang = self.nextLang
        self.setLang()
        if dwidth == 1280:
            self.buildVirtualKeyBoardsd()
        else:
            self.buildVirtualKeyBoard()
    def setLang(self):
        if self.lang == 'de_DE':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfc',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\xf6',
              u'\xe4',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\xdf',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'-',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xdc',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\xd6',
              u'\xc4',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'OK']]
            self.nextLang = 'fr_FR'
        elif self.lang == 'fr_FR':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'a',
              u'z',
              u'e',
              u'r',
              u't',
              u'y',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfa',
              u'+'],
             [u'q',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'm',
              u'\xf9',
              u'*'],
             [u'<',
              u'w',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u',',
              u';',
              ':',
              u'!',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'?',
              u'.',
              u'[',
              u']',
              u'{',
              u'}',
              u'"',
              u'#',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'http://',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'A',
              u'Z',
              u'E',
              u'R',
              u'T',
              u'Y',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xda',
              u'\xa3'],
             [u'Q',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'M',
              u'%',
              u'-'],
             [u'>',
              u'W',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'?',
              u'.',
              u'/',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\xb0',
              u'<',
              u'\xe0',
              u'\xe9',
              u'\xe8',
              u'\xe0',
              u'.com',
              u'OK']]
            self.nextLang = 'es_ES'
        elif self.lang == 'es_ES':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfa',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\xf3',
              u'\xe1',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\u0141',
              u'\u0155',
              u'\xe9',
              u'\u010d',
              u'\xed',
              u'\u011b',
              u'\u0144',
              u'\u0148',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xda',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\xd3',
              u'\xc1',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u0154',
              u'\xc9',
              u'\u010c',
              u'\xcd',
              u'\u011a',
              u'\u0143',
              u'\u0147',
              u'OK']]
            self.nextLang = 'fi_FI'
        elif self.lang == 'fi_FI':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xe9',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\xf6',
              u'\xe4',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\xdf',
              u'\u013a',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xc9',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\xd6',
              u'\xc4',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u0139',
              u'OK']]
            self.nextLang = 'sv_SE'
        elif self.lang == 'sv_SE':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xe9',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\xf6',
              u'\xe4',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\xdf',
              u'\u013a',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xc9',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\xd6',
              u'\xc4',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u0139',
              u'OK']]
            self.nextLang = 'sk_SK'
        elif self.lang == 'sk_SK':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfa',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\u013e',
              u'@',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'\u0161',
              u'\u010d',
              u'\u017e',
              u'\xfd',
              u'\xe1',
              u'\xed',
              u'\xe9',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\u0165',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\u0148',
              u'\u010f',
              u"'"],
             [u'\xc1',
              u'\xc9',
              u'\u010e',
              u'\xcd',
              u'\xdd',
              u'\xd3',
              u'\xda',
              u'\u017d',
              u'\u0160',
              u'\u010c',
              u'\u0164',
              u'\u0147'],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\xe4',
              u'\xf6',
              u'\xfc',
              u'\xf4',
              u'\u0155',
              u'\u013a',
              u'OK']]
            self.nextLang = 'cs_CZ'
        elif self.lang == 'cs_CZ':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfa',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\u016f',
              u'@',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'\u011b',
              u'\u0161',
              u'\u010d',
              u'\u0159',
              u'\u017e',
              u'\xfd',
              u'\xe1',
              u'\xed',
              u'\xe9',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\u0165',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\u0148',
              u'\u010f',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u010c',
              u'\u0158',
              u'\u0160',
              u'\u017d',
              u'\xda',
              u'\xc1',
              u'\xc9',
              u'OK']]
            self.nextLang = 'en_EN'
        else:
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'y',
              u'u',
              u'i',
              u'o',
              u'p',
              u'+',
              u'@'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'#',
              u'\\',
              u'|'],
             [u'<',
              u'z',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'CLEAR'],
             [u'SHIFT', u'SPACE', u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Y',
              u'U',
              u'I',
              u'O',
              u'P',
              u'*',
              u'['],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u"'",
              u'?',
              u']'],
             [u'>',
              u'Z',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT', u'SPACE', u'OK']]
            self.lang = 'en_EN'
            self.nextLang = 'de_DE'
        self['country'].setText(self.lang)
        self.max_key = 47 + len(self.keys_list[4])
    def buildVirtualKeyBoard(self, selectedKey = 0):
        list = []
        if self.shiftMode:
            self.k_list = self.shiftkeys_list
            for keys in self.k_list:
                keyslen = len(keys)
                if selectedKey < keyslen and selectedKey > -1:
                    list.append(VirtualKeyBoardEntryComponent(keys, selectedKey, True))
                else:
                    list.append(VirtualKeyBoardEntryComponent(keys, -1, True))
                selectedKey -= keyslen
        else:
            self.k_list = self.keys_list
            for keys in self.k_list:
                keyslen = len(keys)
                if selectedKey < keyslen and selectedKey > -1:
                    list.append(VirtualKeyBoardEntryComponent(keys, selectedKey))
                else:
                    list.append(VirtualKeyBoardEntryComponent(keys, -1))
                selectedKey -= keyslen
        self['list'].setList(list)
    def buildVirtualKeyBoardsd(self, selectedKey = 0):
        list = []
        if self.shiftMode:
            self.k_list = self.shiftkeys_list
            for keys in self.k_list:
                keyslen = len(keys)
                if selectedKey < keyslen and selectedKey > -1:
                    list.append(VirtualKeyBoardEntryComponentsd(keys, selectedKey, True))
                else:
                    list.append(VirtualKeyBoardEntryComponentsd(keys, -1, True))
                selectedKey -= keyslen
        else:
            self.k_list = self.keys_list
            for keys in self.k_list:
                keyslen = len(keys)
                if selectedKey < keyslen and selectedKey > -1:
                    list.append(VirtualKeyBoardEntryComponentsd(keys, selectedKey))
                else:
                    list.append(VirtualKeyBoardEntryComponentsd(keys, -1))
                selectedKey -= keyslen
        self['list'].setList(list)
    def backClicked(self):
        self.text = self['text'].getText()[:-1]
        self['text'].setText(self.text)
    def okClicked(self):
        if self.shiftMode:
            list = self.shiftkeys_list
        else:
            list = self.keys_list
        selectedKey = self.selectedKey
        text = None
        for x in list:
            xlen = len(x)
            if selectedKey < xlen:
                if selectedKey < len(x):
                    text = x[selectedKey]
                break
            else:
                selectedKey -= xlen
        if text is None:
            return
        else:
            text = text.encode('UTF-8')
            if text == 'EXIT':
                self.close(None)
            elif text == 'BACKSPACE':
                self.text = self['text'].getText()[:-1]
                self['text'].setText(self.text)
            elif text == 'CLEAR':
                self.text = ''
                self['text'].setText(self.text)
            elif text == 'SHIFT':
                if self.shiftMode:
                    self.shiftMode = False
                else:
                    self.shiftMode = True
                if dwidth == 1280:
                    self.buildVirtualKeyBoardsd(self.selectedKey)
                else:
                    self.buildVirtualKeyBoard(self.selectedKey)
            elif text == 'SPACE':
                self.text += ' '
                self['text'].setText(self.text)
            elif text == 'OK':
                self.close(self['text'].getText())
            else:
                self.text = self['text'].getText()
                self.text += text
                self['text'].setText(self.text)
            return
    def ok(self):
        self.close(self['text'].getText())
    def exit(self):
        self.close(None)
        return
    def left(self):
        self.selectedKey -= 1
        if self.selectedKey == -1:
            self.selectedKey = 11
        elif self.selectedKey == 11:
            self.selectedKey = 23
        elif self.selectedKey == 23:
            self.selectedKey = 35
        elif self.selectedKey == 35:
            self.selectedKey = 47
        elif self.selectedKey == 47:
            self.selectedKey = self.max_key
        self.showActiveKey()
    def right(self):
        self.selectedKey += 1
        if self.selectedKey == 12:
            self.selectedKey = 0
        elif self.selectedKey == 24:
            self.selectedKey = 12
        elif self.selectedKey == 36:
            self.selectedKey = 24
        elif self.selectedKey == 48:
            self.selectedKey = 36
        elif self.selectedKey > self.max_key:
            self.selectedKey = 48
        self.showActiveKey()
    def up(self):
        self.selectedKey -= 12
        if self.selectedKey < 0 and self.selectedKey > self.max_key - 60:
            self.selectedKey += 48
        elif self.selectedKey < 0:
            self.selectedKey += 60
        self.showActiveKey()
    def down(self):
        self.selectedKey += 12
        if self.selectedKey > self.max_key and self.selectedKey > 59:
            self.selectedKey -= 60
        elif self.selectedKey > self.max_key:
            self.selectedKey -= 48
        self.showActiveKey()
    def showActiveKey(self):
        if dwidth == 1280:
            self.buildVirtualKeyBoardsd(self.selectedKey)
        else:
            self.buildVirtualKeyBoard(self.selectedKey)
    def inShiftKeyList(self, key):
        for KeyList in self.shiftkeys_list:
            for char in KeyList:
                if char == key:
                    return True
        return False
    def keyGotAscii(self):
        from Components.config import getCharValue
        char = getCharValue(getPrevAsciiCode())
        if len(str(char)) == 1:
            char = char.encode('utf-8')
        if self.inShiftKeyList(char):
            self.shiftMode = True
            list = self.shiftkeys_list
        else:
            self.shiftMode = False
            list = self.keys_list
        if char == ' ':
            char = 'SPACE'
        selkey = 0
        for keylist in list:
            for key in keylist:
                if key == char:
                    self.selectedKey = selkey
                    self.okClicked()
                    self.showActiveKey()
                    return
                selkey += 1