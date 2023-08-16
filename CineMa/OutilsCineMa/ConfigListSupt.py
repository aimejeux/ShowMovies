from Components.HTMLComponent import HTMLComponent
from Components.GUIComponent import GUIComponent
from Components.config import KEY_LEFT, KEY_RIGHT, KEY_HOME, KEY_END, KEY_0, KEY_DELETE, KEY_BACKSPACE, KEY_OK, KEY_TOGGLEOW, KEY_ASCII, KEY_TIMEOUT, KEY_NUMBERS, config, configfile, ConfigElement, ConfigText, ConfigPassword
from Components.ActionMap import NumberActionMap, ActionMap
from enigma import eListbox, eListboxPythonConfigContent, eRCInput, eTimer, quitMainloop
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
import skin
from Tools.NumericalTextInput import NumericalTextInput
class ConfigListSupt(HTMLComponent, GUIComponent, object):
    def __init__(self, list, session = None):
        GUIComponent.__init__(self)
        self.l = eListboxPythonConfigContent()
        self.timer = eTimer()
        self.list = list
        self.onSelectionChanged = []
        self.current = None
        self.session = session
        return
    def execBegin(self):
        rcinput = eRCInput.getInstance()
        rcinput.setKeyboardMode(rcinput.kmAscii)
        try:
            self.timer.callback.append(self.timeout)
        except:
            self.timer_conn = self.timer.timeout.connect(self.timeout)
    def execEnd(self):
        rcinput = eRCInput.getInstance()
        rcinput.setKeyboardMode(rcinput.kmNone)
        try:
            self.timer.callback.remove(self.timeout)
        except:
            self.timer.callback_conn = None
        return
    def toggle(self):
        selection = self.getCurrent()
        selection[1].toggle()
        self.invalidateCurrent()
    def handleKey(self, key):
        selection = self.getCurrent()
        if selection and selection[1].enabled:
            selection[1].handleKey(key)
            self.invalidateCurrent()
            if key in KEY_NUMBERS:
                self.timer.start(1000, 1)
    def getCurrent(self):
        return self.l.getCurrentSelection()

    def getCurrentIndex(self):
        return self.l.getCurrentSelectionIndex()
    def setCurrentIndex(self, index):
        if self.instance is not None:
            self.instance.moveSelectionTo(index)
        return
    def invalidateCurrent(self):
        self.l.invalidateEntry(self.l.getCurrentSelectionIndex())
    def invalidate(self, entry):
        if entry in self.__list:
            self.l.invalidateEntry(self.__list.index(entry))
    GUI_WIDGET = eListbox
    def selectionChanged(self):
        if isinstance(self.current, tuple) and len(self.current) == 2:
            self.current[1].onDeselect(self.session)
        self.current = self.getCurrent()
        if isinstance(self.current, tuple) and len(self.current) == 2:
            self.current[1].onSelect(self.session)
        else:
            return
        for x in self.onSelectionChanged:
            x()
    def postWidgetCreate(self, instance):
        try:
            instance.selectionChanged.get().append(self.selectionChanged)
        except:
            instance_selectionChanged_conn = instance.selectionChanged.connect(self.selectionChanged)
        instance.setContent(self.l)
    def preWidgetRemove(self, instance):
        if isinstance(self.current, tuple) and len(self.current) == 2:
            self.current[1].onDeselect(self.session)
        try:
            instance.selectionChanged.get().remove(self.selectionChanged)
        except:
            instance.selectionChanged_conn = None
        instance.setContent(None)
        return
    def setList(self, l):
        self.timer.stop()
        self.__list = l
        self.l.setList(self.__list)
        if l is not None:
            for x in l:
                pass
        return
    def getList(self):
        return self.__list
    list = property(getList, setList)
    def timeout(self):
        self.handleKey(KEY_TIMEOUT)
    def isChanged(self):
        is_changed = False
        for x in self.list:
            is_changed |= x[1].isChanged()
        return is_changed
    def pageUp(self):
        if self.instance is not None:
            self.instance.moveSelection(self.instance.pageUp)
        return
    def pageDown(self):
        if self.instance is not None:
            self.instance.moveSelection(self.instance.pageDown)
        return
    def moveUp(self):
        if self.instance is not None:
            self.instance.moveSelection(self.instance.moveUp)
        return
    def moveDown(self):
        if self.instance is not None:
            self.instance.moveSelection(self.instance.moveDown)
        return
    def refresh(self):
        self.pageUp()
class ConfigListShowMoviesScreen:
    def __init__(self, list, session = None, on_change = None):
        NumericalTextInput(nextFunc=None, handleTimeout=False, search=False)
        self['config_actions'] = NumberActionMap(['SetupActions', 'InputAsciiActions', 'KeyboardInputActions'], {'gotAsciiCode': self.keyGotAscii,
         'ok': self.keyOK,
         'left': self.keyLeft,
         'right': self.keyRight,
         'home': self.keyHome,
         'end': self.keyEnd,
         'deleteForward': self.keyDelete,
         'deleteBackward': self.keyBackspace,
         'toggleOverwrite': self.keyToggleOW,
         '1': self.keyNumberGlobal,
         '2': self.keyNumberGlobal,
         '3': self.keyNumberGlobal,
         '4': self.keyNumberGlobal,
         '5': self.keyNumberGlobal,
         '6': self.keyNumberGlobal,
         '7': self.keyNumberGlobal,
         '8': self.keyNumberGlobal,
         '9': self.keyNumberGlobal,
         '0': self.keyNumberGlobal}, -1)
        self.onChangedEntry = []
        self['VirtualKB'] = ActionMap(['VirtualKeyboardActions'], {'showVirtualKeyboard': self.KeyText}, -2)
        self['VirtualKB'].setEnabled(False)
        self['config'] = ConfigListSupt(list, session=session)
        if on_change is not None:
            self.__changed = on_change
        else:
            self.__changed = lambda : None
        if self.handleInputHelpers not in self['config'].onSelectionChanged:
            self['config'].onSelectionChanged.append(self.handleInputHelpers)
            #self['config'].onSelectionChanged.append(self.KeyText)
        return
    def handleInputHelpers(self):
        if self['config'].getCurrent() is not None:
            if isinstance(self['config'].getCurrent()[1], ConfigText) or isinstance(self['config'].getCurrent()[1], ConfigPassword):
                if self.has_key('VKeyIcon'):
                    self['VirtualKB'].setEnabled(True)
                    self['VKeyIcon'].boolean = True
                if self.has_key('HelpWindow'):
                    if self['config'].getCurrent()[1].help_window.instance is not None:
                        helpwindowpos = self['HelpWindow'].getPosition()
                        from enigma import ePoint
                        self['config'].getCurrent()[1].help_window.instance.move(ePoint(helpwindowpos[0], helpwindowpos[1]))
                        #self.KeyText()
            elif self.has_key('VKeyIcon'):
                self['VirtualKB'].setEnabled(False)
                self['VKeyIcon'].boolean = False
                #self.KeyText()
        elif self.has_key('VKeyIcon'):
            self['VirtualKB'].setEnabled(False)
            self['VKeyIcon'].boolean = False
            #self.KeyText()
        return
    def KeyText(self):
        import os#######
        if os.path.exists('/var/lib/dpkg/status'):
            from Screens.VirtualKeyBoard import VirtualKeyBoard
            self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard, title=self['config'].getCurrent()[0], text=self['config'].getCurrent()[1].getValue())
        else:
            from Plugins.Extensions.ShowMovies.CineMa.OutilsCineMa.VirtualKeyBoard import VirtualKeyBoard_1
            self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard_1, title=self['config'].getCurrent()[0], text=self['config'].getCurrent()[1].getValue())
    def VirtualKeyBoardCallback(self, callback = None):
        if callback is not None and len(callback):
            self['config'].getCurrent()[1].setValue(callback)
            self['config'].invalidate(self['config'].getCurrent())
        return
    def keyOK(self):
        self['config'].handleKey(KEY_OK)
    def keyLeft(self):
        self['config'].handleKey(KEY_LEFT)
        self.__changed()
    def keyRight(self):
        self['config'].handleKey(KEY_RIGHT)
        self.__changed()
    def keyHome(self):
        self['config'].handleKey(KEY_HOME)
        self.__changed()
    def keyEnd(self):
        self['config'].handleKey(KEY_END)
        self.__changed()
    def keyDelete(self):
        self['config'].handleKey(KEY_DELETE)
        self.__changed()
    def keyBackspace(self):
        self['config'].handleKey(KEY_BACKSPACE)
        self.__changed()
    def keyToggleOW(self):
        self['config'].handleKey(KEY_TOGGLEOW)
        self.__changed()
    def keyGotAscii(self):
        self['config'].handleKey(KEY_ASCII)
        self.__changed()
    def keyNumberGlobal(self, number):
        self['config'].handleKey(KEY_0 + number)
        self.__changed()
    def saveAll(self):
        for x in self['config'].list:
            x[1].save()
    def keySave(self):
        self.saveAll()
        self.close()
    def cancelConfirm(self, result):
        if not result:
            return
        for x in self['config'].list:
            x[1].cancel()
        self.close()
    def keyCancel(self):
        if self['config'].isChanged():
            self.session.openWithCallback(self.cancelConfirm, MessageBox, _('Really close without saving settings?'))
        else:
            self.close()
    def changedEntry(self):
        for x in self.onChangedEntry:
            x()