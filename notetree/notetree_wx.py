# van een ibm site afgeplukt
import os
import wx
import pickle
import gettext

app_title = "NoteTree"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
locale = os.path.join(HERE, 'locale')
print locale
gettext.install(app_title, locale)
languages = {'nl': gettext.translation(app_title, locale, languages=['nl']),
    'en': gettext.translation(app_title, locale, languages=['en'])}

root_title = "MyNotes"

class CheckDialog(wx.Dialog):
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

class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size = (800, 500),
                         style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)
        self.nt_icon = wx.Icon(os.path.join(
            os.path.dirname(__file__),"notetree.ico"),wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.nt_icon)
        mainwindow = self
        self.sb = self.CreateStatusBar()

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
        menudata = (
            (_("m_main"), (
                    (_("m_reload"), self.reread, _("h_reload")),
                    (_("m_save"), self.save, _("h_save")),
                    ("", None, None),
                    (_("m_root"), self.rename, _("h_root")),
                    ("", None, None),
                    (_("m_hide"), self.hide, _("h_hide")),
                    (_("m_lang"), self.choose_language, _("h_lang")),
                    ("", None, None),
                    (_("m_exit"),self.afsl, _("h_exit")),
                ), ),
            (_("m_note"), (
                    (_("m_new"), self.new_item, _("h_new")),
                    (_("m_delete"), self.delete_item, _("h_delete")),
                    (_("m_name"), self.ask_title, _("h_name")),
                    ("", None, None),
                    (_("m_forward"), self.next_note,_("h_forward")),
                    (_("m_back"), self.prev_note,_("h_back")),
                ), ),
            (_("m_help"), (
                    (_("m_about"), self.info_page, _("h_about")),
                    (_("m_keys"), self.help_page, _("h_keys")),
                ), ),
            )
        menu_bar = self.GetMenuBar()
        menuitems = menu_bar.GetMenus()
        has_items = bool(menuitems)
        ix = 0
        for item, data in menudata:
            menu_label = item
            submenu = wx.Menu()
            for label, handler, info in data:
                if label != "":
                    menu_item = wx.MenuItem(submenu, -1, label, info)
                    self.Bind(wx.EVT_MENU, handler, menu_item)
                else:
                    menu_item = wx.MenuItem(submenu, wx.ID_SEPARATOR)
                submenu.AppendItem(menu_item)
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
        if event.GetModifiers() == wx.MOD_CONTROL: # evt.ControlDown()
            if keycode == ord("L"): # 76: Ctrl-L reload tabs
                self.reread()
            elif keycode == ord("N"): # 78: Ctrl-N nieuwe tab
                self.new_item()
            elif keycode == ord("D"):
                self.delete_item()
            elif keycode == ord("H"): # 72: Ctrl-H Hide/minimize
                self.hide()
            elif keycode == ord("S"): # 83: Ctrl-S saven zonder afsluiten
                self.save()
            elif keycode == ord("Q"): # 81: Ctrl-Q afsluiten na saven
                self.afsl()
            elif keycode == wx.WXK_PAGEDOWN: #  and win == self.editor:
                self.next_note()
            elif keycode == wx.WXK_PAGEUP: #  and win == self.editor:
                self.prev_note()
            elif keycode == wx.WXK_F1:
                self.choose_language()
        elif keycode == wx.WXK_F1:
            self.help_page()
        elif keycode == wx.WXK_F2: # and win == self.tree:
            if event.GetModifiers() == wx.MOD_SHIFT:
                self.rename()
            else:
                self.ask_title()
        elif keycode == wx.WXK_DELETE and win == self.tree:
            self.delete_item()
        elif keycode == wx.WXK_ESCAPE:
            self.afsl()
        if event and skip:
            event.Skip()

    def OnEvtText(self,event): # seems to work
        self.editor.IsModified = True

    def OnSelChanging(self, event=None): # works (tm)
        if event.GetItem() == self.root:
            event.Veto()

    def OnSelChanged(self, event=None): # works (tm)
        self.check_active()
        self.activate_item(event.GetItem())
        event.Skip()

    def open(self):
        print("calling open")
        self.opts = {
            "AskBeforeHide": True,
            "ActiveItem": 0,
            "SashPosition": 180,
            "ScreenSize": (800, 500),
            'Language': 'en',
            "RootTitle": root_title
            }
        self.nt_data = {}
        try:
            file = open(self.project_file)
        except IOError:
            return
        try:
            self.nt_data = pickle.load(file)
        except EOFError:
            return
        file.close()
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot(os.path.splitext(os.path.split(
            self.project_file)[1])[0])
        item_to_activate = self.root
        self.editor.Clear()
        self.editor.Enable (False)
        for key, value in self.nt_data.items():
            if key == 0 and "AskBeforeHide" in value:
                for key,val in value.items():
                    self.opts[key] = val
            else:
                tag, text = value
                item = self.tree.AppendItem (self.root, tag)
                self.tree.SetItemPyData(item, text)
                if key == self.opts["ActiveItem"]:
                    item_to_activate = item
        languages[self.opts["Language"]].install()
        print('installing language "{}"'.format(self.opts["Language"]))
        self.tree.SetItemText(self.root,self.opts["RootTitle"])
        self.SetSize(self.opts["ScreenSize"])
        self.splitter.SetSashPosition(self.opts["SashPosition"], True)
        self.tree.Expand (self.root)
        self.tree.SelectItem(item_to_activate)
        self.tree.SetFocus()

    def reread(self,event=None):
        dlg=wx.MessageDialog(self, _("ask_reload"), app_title, wx.OK | wx.CANCEL)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.open()
        dlg.Destroy()

    def save(self, event=None):
        self.check_active() # even zorgen dat de editor inhoud geassocieerd wordt
        self.opts["ScreenSize"] = self.GetSize()
        self.opts["SashPosition"] = self.splitter.GetSashPosition()
        ky = 0
        self.nt_data = {ky: self.opts}
        tag, cookie = self.tree.GetFirstChild(self.root)
        while tag.IsOk():
            ky += 1
            if tag == self.activeitem:
                self.opts["ActiveItem"] = ky
            self.nt_data[ky] = (self.tree.GetItemText(tag),
                self.tree.GetItemPyData(tag))
            tag, cookie = self.tree.GetNextChild(self.root, cookie)
        file = open(self.project_file,"w")
        pickle.dump(self.nt_data, file)
        file.close()

    def rename(self, event=None):
        dlg = wx.TextEntryDialog(self, _("t_root"), app_title,
                self.tree.GetItemText(self.root))
        if dlg.ShowModal() == wx.ID_OK:
            self.tree.SetItemText(self.root,dlg.GetValue())
        dlg.Destroy()

    def hide(self, event=None):
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

    def afsl(self, event=None):
        self.save()
        self.Close()

    def new_item(self, event=None): # works
        # kijk waar de cursor staat (of altijd onderaan toevoegen?)
        dlg = wx.TextEntryDialog (self, _("t_new"), app_title)
        if dlg.ShowModal() == wx.ID_OK:
            text = dlg.GetValue()
            item = self.tree.AppendItem (self.root, text)
            self.tree.SetItemPyData(item, "")
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
            wx.MessageBox(_("no_delete_root"), app_title, self)

    def ask_title(self, event=None):
        dlg = wx.TextEntryDialog(self, _("t_name"), app_title,
                self.tree.GetItemText(self.activeitem))
        if dlg.ShowModal() == wx.ID_OK:
            self.tree.SetItemText(self.activeitem,dlg.GetValue())
        dlg.Destroy()

    def next_note(self, event=None):
        item = self.tree.GetNextSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)
        else:
            wx.MessageBox(_("no_next_item"), app_title, self)

    def prev_note(self, event=None):
        item = self.tree.GetPrevSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)
        else:
            wx.MessageBox(_("no_prev_item"), app_title, self)

    def check_active(self,message=None): # works, I guess
        if self.activeitem and self.activeitem != self.root:
            self.tree.SetItemBold(self.activeitem, False)
            if self.editor.IsModified:
                if message:
                    print(message)
                self.tree.SetItemPyData(self.activeitem,self.editor.GetValue())

    def activate_item(self, item): # works too, it would seem
        self.activeitem = item
        if item != self.root:
            self.tree.SetItemBold(item, True)
            self.editor.SetValue(self.tree.GetItemPyData(item))
            self.editor.Enable(True)
        else:
            self.editor.Clear()
            self.editor.Enable(False)

    def info_page(self,event=None):
        wx.MessageBox(_("info_text"), app_title, wx.OK | wx.ICON_INFORMATION, self)

    def help_page(self,event=None):
        wx.MessageBox(_("help_text"), app_title, wx.OK | wx.ICON_INFORMATION, self)

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

def main(fn):
    self.fn = fn
    app = wx.App(False)
    frame = MainWindow(None, -1, " - ".join((app_title, self.fn)))
    self.SetTopWindow(frame)
    frame.project_file = self.fn
    frame.open()
    app.MainLoop()

if __name__ == "__main__":
    main('NoteTree.ini')
