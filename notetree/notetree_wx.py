# -*- coding: utf-8 -*-
# van een ibm site afgeplukt
import os
import wx
from datetime import datetime
import gettext
from notetree_shared import NoteTreeMixin, app_title, root_title, languages

## app_title = "NoteTree"
## HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
## locale = os.path.join(HERE, 'locale')
## print locale
## gettext.install(app_title, locale)
## languages = {'nl': gettext.translation(app_title, locale, languages=['nl']),
    ## 'en': gettext.translation(app_title, locale, languages=['en'])}

## root_title = "MyNotes"

class KeywordsDialog(wx.Dialog):
    """Dialoog voor het koppelen van trefwoorden
    """
    pass

class CheckDialog(wx.Dialog):
    """Dialoog om te melden dat de applicatie verborgen gaat worden
    AskBeforeHide bepaalt of deze getoond wordt of niet
    """
    def __init__(self,parent,id,title, size=(-1,120), pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self,parent,id,title,pos,size,style)
        pnl = wx.Panel(self,-1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(wx.StaticText(pnl,-1,_("sleep_message")),1,wx.ALL,5)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.Check = wx.CheckBox(pnl, -1, _("hide_message"))
        sizer1.Add(self.Check,0,wx.EXPAND)
        sizer0.Add(sizer1,0,wx.ALIGN_CENTER_HORIZONTAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.bOk = wx.Button(pnl,id=wx.ID_OK)
        ## self.bOk.Bind(wx.EVT_BUTTON,self.on_ok)
        sizer1.Add(self.bOk,0,wx.EXPAND | wx.ALL, 2)
        sizer0.Add(sizer1,0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL |
            wx.ALIGN_CENTER_VERTICAL,5)
        pnl.SetSizer(sizer0)
        pnl.SetAutoLayout(True)
        sizer0.Fit(pnl)
        sizer0.SetSizeHints(pnl)
        pnl.Layout()

class MainWindow(wx.Frame, NoteTreeMixin):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = (800, 500),
                         style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.nt_icon = wx.Icon(os.path.join(
            os.path.dirname(__file__),"notetree.ico"),wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.nt_icon)
        mainwindow = self
        self.sb = self.CreateStatusBar()

        # tray icon wordt pas opgezet in de hide() methode

        menuBar = wx.MenuBar()
        self.SetMenuBar(menuBar)
        self.create_menu()

        self.splitter = wx.SplitterWindow (self, -1, style=wx.NO_3D) # |wx.SP_3D
        self.splitter.SetMinimumPaneSize (1)

        self.tree = wx.TreeCtrl (self.splitter, -1, style=
            wx.TR_HAS_BUTTONS |
            wx.TR_EDIT_LABELS |
            wx.TR_HAS_VARIABLE_ROW_HEIGHT
            )
        self.root = self.tree.AddRoot(root_title)
        self.activeitem = self.root
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelChanging, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.tree.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.editor = wx.TextCtrl(self.splitter, -1, style=wx.TE_MULTILINE)
        self.editor.Enable(0)
        self.editor.Bind(wx.EVT_TEXT, self.OnEvtText)
        self.editor.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.splitter.SplitVertically(self.tree, self.editor)
        self.splitter.SetSashPosition(180, True)
        self.splitter.Bind(wx.EVT_KEY_DOWN, self.on_key)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.Show(True)

    def create_menu(self):
        print("(re)creating menu")
        menu_bar = self.GetMenuBar()
        menuitems = menu_bar.GetMenus()
        has_items = bool(menuitems)
        ix = 0
        self.keydef_to_method = {}
        for item, data in self.get_menudata(): # defined in mixin class
            menu_label = item
            submenu = wx.Menu()
            for label, handler, info, keydef in data:
                if label != "":
                    menu_item = wx.MenuItem(submenu, -1, label, info)
                    self.Bind(wx.EVT_MENU, handler, menu_item)
                else:
                    menu_item = wx.MenuItem(submenu, wx.ID_SEPARATOR)
                submenu.AppendItem(menu_item)
                if keydef:
                    for key in keydef.split(','):
                        mod = ''
                        if '+' in key:
                            mod, key = key.split('+')
                        if key == 'F1':
                            key = wx.WXK_F1
                        elif key == 'F2':
                            key = wx.WXK_F2
                        elif key == 'F6':
                            key = wx.WXK_F6
                        elif key == 'Escape':
                            key = wx.WXK_ESCAPE
                        elif key == 'Delete':
                            key = wx.WXK_DELETE
                        elif key == 'PgDown':
                            key = wx.WXK_PAGEDOWN
                        elif key == 'PgUp':
                            key = wx.WXK_PAGEUP
                        else:
                            key = ord(key)
                        self.keydef_to_method[(mod, key)] = handler
            if has_items:
                menu_bar.Replace(ix, submenu, menu_label)
                menuitems[ix][0].Destroy()
            else:
                menu_bar.Append(submenu, menu_label)
            ix += 1

    def on_key(self,event):
        skip = True
        keycode = event.GetKeyCode()
        win = event.GetEventObject()
        mod = ''
        test = event.GetModifiers()
        if test == wx.MOD_CONTROL:
            mod = 'Ctrl'
        elif test == wx.MOD_SHIFT:
            mod = 'Shift'
        if (mod, keycode) in self.keydef_to_method:
            if keycode == wx.WXK_DELETE and win != self.tree:
                pass # delete key should work normally when not in tree
            else:
                self.keydef_to_method[mod, keycode]()
        if event and skip:
            print 'skipping'
            event.Skip()

    def OnEvtText(self,event):
        self.editor.IsModified = True

    def OnSelChanging(self, event=None):
        if event.GetItem() == self.root:
            event.Veto()

    def OnSelChanged(self, event=None):
        test = event.GetItem()
        self.check_active()
        self.activate_item(event.GetItem())
        event.Skip()

    def close(self, event=None):
        self.save()
        self.Close()

    def open(self):
        msg = NoteTreeMixin.open(self, "Wx", root_title)
        self.tree.SetFocus()
        if self.nt_data == {}:
            return
        if msg:
            self.showmsg(msg)
            return
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot(os.path.splitext(os.path.split(
            self.project_file)[1])[0])
        item_to_activate = self.root
        self.editor.Clear()
        self.editor.Enable (False)
        item_to_activate = self.build_tree(first_time=True)
        self.tree.SetItemText(self.root, self.opts["RootTitle"])
        self.SetSize(self.opts["ScreenSize"])
        self.splitter.SetSashPosition(self.opts["SashPosition"], True)
        self.tree.Expand (self.root)
        self.tree.SelectItem(item_to_activate)
        self.tree.SetFocus()

    def build_tree(self, first_time=False):
        item_to_return = self.root
        self.activeitem = None
        for key, value in self.nt_data.items():
            if key <> 0:
                tag, text = value
                item = self.tree.AppendItem (self.root, tag)
                self.tree.SetItemPyData(item, text)
                if key == self.opts["ActiveItem"]:
                    item_to_return = item
        return item_to_return

    def reread(self,event=None):
        dlg=wx.MessageDialog(self, _("ask_reload"), app_title, wx.OK | wx.CANCEL)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.open()
        dlg.Destroy()

    def tree_to_dict(self):
        self.check_active() # even zorgen dat de editor inhoud geassocieerd wordt
        self.nt_data = {} # don't forget to remove this when we apply selections
        ky = 0
        tag, cookie = self.tree.GetFirstChild(self.root)
        while tag.IsOk():
            ky += 1
            if tag == self.activeitem:
                self.opts["ActiveItem"] = ky
            self.nt_data[ky] = (self.tree.GetItemText(tag),
                self.tree.GetItemPyData(tag))
            tag, cookie = self.tree.GetNextChild(self.root, cookie)

    def save(self, event=None):
        self.tree_to_dict() # check for changed values in tree not in dict
        self.opts["ScreenSize"] = self.GetSize()
        self.opts["SashPosition"] = self.splitter.GetSashPosition()
        NoteTreeMixin._save(self)

    def rename(self, event=None):
        dlg = wx.TextEntryDialog(self, _("t_root"), app_title,
                self.tree.GetItemText(self.root))
        if dlg.ShowModal() == wx.ID_OK:
            self.tree.SetItemText(self.root,dlg.GetValue())
        dlg.Destroy()

    def hide_me(self, event=None):
        if self.opts["AskBeforeHide"]:
            dlg = CheckDialog(self,-1,app_title)
            dlg.ShowModal()
            if dlg.Check.GetValue():
                self.opts["AskBeforeHide"] = False
            dlg.Destroy()
        self.tbi = wx.TaskBarIcon()
        self.tbi.SetIcon(self.nt_icon,_("revive_message"))
        wx.EVT_TASKBAR_LEFT_UP(self.tbi, self.revive)
        wx.EVT_TASKBAR_RIGHT_UP(self.tbi, self.revive)
        self.Hide()

    def revive(self, event=None):
        self.Show()
        self.tbi.Destroy()

    def new_item(self, event=None):
        # kijk waar de cursor staat (of altijd onderaan toevoegen?)
        start = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        dlg = wx.TextEntryDialog (self, _("t_new"), app_title, start)
        if dlg.ShowModal() == wx.ID_OK:
            text = dlg.GetValue()
            item = self.tree.AppendItem (self.root, text)
            self.tree.SetItemPyData(item, "")
            # maybe set data to a tuple of (dict key, editor text, list of keywords)
            self.tree.SelectItem(item)
            self.tree.Expand (self.root)
            self.editor.Clear()
            self.editor.Enable(True)
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()
        dlg.Destroy()

    def delete_item(self, event=None):
        item = self.tree.GetSelection()
        if item != self.root:
            prev = self.tree.GetPrevSibling(item)
            self.activeitem = None
            self.tree.Delete(item)
            if self.tree.GetItemText(prev):
                self.activate_item(prev)
            else:
                self.editor.Clear()
                self.editor.Enable(False)
        else:
            self.showmsg(_("no_delete_root"))

    def ask_title(self, event=None):
        dlg = wx.TextEntryDialog(self, _("t_name"), app_title,
                self.tree.GetItemText(self.activeitem))
        if dlg.ShowModal() == wx.ID_OK:
            self.tree.SetItemText(self.activeitem, dlg.GetValue())
        dlg.Destroy()

    def next_note(self, event=None):
        item = self.tree.GetNextSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)
        else:
            self.showmsg(_("no_next_item"))

    def prev_note(self, event=None):
        item = self.tree.GetPrevSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)
        else:
            self.showmsg(_("no_prev_item"))

    def check_active(self, message=None):
        if self.activeitem and self.activeitem != self.root:
            self.tree.SetItemBold(self.activeitem, False)
            if self.editor.IsModified:
                if message:
                    self.showmsg(message)
                text = self.editor.GetValue()
                self.tree.SetItemPyData(self.activeitem, self.editor.GetValue())

    def activate_item(self, item):
        self.activeitem = item
        if item != self.root:
            self.tree.SetItemBold(item, True)
            self.editor.SetValue(self.tree.GetItemPyData(item))
            self.editor.Enable(True)
        else:
            self.editor.Clear()
            self.editor.Enable(False)

    def info_page(self,event=None):
        self.showmsg(_("info_text"))

    def help_page(self,event=None):
        self.showmsg(_("help_text"))

    def choose_language(self, event=None):
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        data = [(code, _('t_{}'.format(code))) for code in ('nl', 'en')]
        ## data = [('nl', _('t_nl')), ('en', _('t_en'))]
        dlg = wx.SingleChoiceDialog(self,
            _("t_lang"), "Apropos",
            [x[1] for x in data],
            wx.CHOICEDLG_STYLE
            )
        for idx, lang in enumerate([x[0] for x in data]):
            if lang == self.opts["Language"]:
                dlg.SetSelection(idx)
                break
        h = dlg.ShowModal()
        if h == wx.ID_OK:
            sel = dlg.GetStringSelection()
            for idx, lang in enumerate([x[1] for x in data]):
                if lang == sel:
                    code = data[idx][0]
                    self.opts["Language"] = code
                    languages[code].install()
                    print('installing language "{}"'.format(code))
                    self.create_menu()
                    break
        dlg.Destroy()
    def link_keywords(self, event=None):
        pass

    def no_selection(self, event=None):
        pass

    def keyword_select(self, event=None):
        pass

    def text_select(self, event=None):
        pass
    def showmsg(self, message):
        wx.MessageBox(message, app_title, wx.OK | wx.ICON_INFORMATION, self)

def main(fn):
    ## self.fn = fn
    app = wx.App(False)
    frame = MainWindow(None, -1, " - ".join((app_title, fn))) # self.fn)))
    app.SetTopWindow(frame)
    frame.project_file = fn # self.fn
    frame.open()
    app.MainLoop()

if __name__ == "__main__":
    main('NoteTree_wx.pck')
