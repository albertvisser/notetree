"""NoteTree wxPython versie

van een ibm site afgeplukt
"""
import os
# import sys
import gettext
import wx
import wx.adv
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gettext.install("NoteTree", os.path.join(HERE, 'locale'))


class MainWindow(wx.Frame):
    """Application main screen
    """
    def __init__(self, root):
        self.base = root
        self.app = wx.App(False)
        self.activeitem = None

    def start(self):
        "start the GUI"
        self.app.MainLoop()

    def build_screen(self, parent=None, title='', iconame=''):
        "setup screen"
        super().__init__(parent, title=title, size=(800, 500),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        if iconame:
            self.nt_icon = wx.Icon(iconame, wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.nt_icon)
        self.sb = self.CreateStatusBar()

        # tray icon wordt pas opgezet in de hide() methode

        self.SetMenuBar(wx.MenuBar())
        # self.create_menu()

        self.splitter = wx.SplitterWindow(self, -1)
        self.splitter.SetMinimumPaneSize(1)

        self.tree = wx.TreeCtrl(self.splitter)
        self.root = self.tree.AddRoot(self.base.root_title)
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelChanging, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
#        self.tree.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.editor = wx.TextCtrl(self.splitter, -1, style=wx.TE_MULTILINE)
        self.editor.Enable(0)
        self.editor.Bind(wx.EVT_TEXT, self.OnEvtText)
#        self.editor.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.splitter.SplitVertically(self.tree, self.editor)
        self.splitter.SetSashPosition(180, True)
#        self.splitter.Bind(wx.EVT_KEY_DOWN, self.on_key)
#        self.Bind(wx.EVT_KEY_DOWN, self.on_key)

        self.Show(True)
        self.app.SetTopWindow(self)

    def create_menu(self):
        """Build the application menu
        """
        menu_bar = self.GetMenuBar()
        menuitems = menu_bar.GetMenus()
        has_items = bool(menuitems)
        self.selactions = {}
        self.seltypes = []
        ix = 0
        # self.keydef_to_method = {}
        accel_list = []
        for item, data in self.base.get_menudata():
            menu_label = item
            submenu = wx.Menu()
            for label, handler, info, keydef in data:
                if keydef:
                    test = keydef.split(',')
                    primary = test[0]
                    keydef = test[1:]
                else:
                    primary = None
                    keydef = []
                if label != "":
                    label_ = label
                    if primary:
                        if primary == 'Ctrl+PgDown':
                            primary = 'Ctrl+PgDn'
                        label = '\t'.join((label, primary))
                    if menu_label == _('m_view'):
                        if label_ != _('m_revorder'):
                            self.seltypes.append(label_)
                        menu_item = wx.MenuItem(submenu, -1, label, info, wx.ITEM_CHECK)
                        self.selactions[label_] = menu_item
                    else:
                        menu_item = wx.MenuItem(submenu, -1, label, info)
                    self.Bind(wx.EVT_MENU, handler, menu_item)
                else:
                    menu_item = wx.MenuItem(submenu, wx.ID_SEPARATOR)
                submenu.Append(menu_item)
                if label_ in (_('m_forward'), _('m_back')):
                    accel = wx.AcceleratorEntry(cmd=menu_item.GetId())
                    if accel.FromString(primary):
                        accel_list.append(accel)
                for key in keydef:  # define extra keydefs via accelerator table
                    menu_item = wx.MenuItem(id=wx.NewId(), text=label)
                    self.Bind(wx.EVT_MENU, handler, menu_item)
                    accel = wx.AcceleratorEntry(cmd=menu_item.GetId())
                    if accel.FromString(key):
                        if key == 'Delete':
                            self.tree.SetAcceleratorTable(wx.AcceleratorTable([accel]))
                        else:
                            accel_list.append(accel)
            if has_items:
                menu_bar.Replace(ix, submenu, menu_label)
                menuitems[ix][0].Destroy()
            else:
                menu_bar.Append(submenu, menu_label)
            ix += 1
        self.SetAcceleratorTable(wx.AcceleratorTable(accel_list))
        for item in self.selactions.values():
            item.Check(False)
        self.selactions[_('m_revorder')].Check(self.base.opts['RevOrder'])
        self.selactions[self.seltypes[abs(self.base.opts['Selection'][0])]].Check(True)

    def OnEvtText(self, event):
        """reimplemented event handler
        """
        self.editor.IsModified = True

    def OnSelChanging(self, event=None):
        """reimplemented event handler
        """
        # oorspronkelijk mocht je niet naar het root item navigeren maar in de qt versie kan dat
        # niet zo makkelijk voorkomen worden
        # nisschien moet je de tekst ook maar kunnen invullen net als in treedocs?

    def OnSelChanged(self, event=None):
        """reimplemented event handler
        """
        self.base.check_active()
        self.base.activate_item(event.GetItem())
        event.Skip()

    def close(self, event=None):
        """save before shutting down
        """
        if self.activeitem:
            self.base.update()
        self.Close()

    def clear_editor(self):
        'set up editor'
        self.editor.Clear()
        self.editor.Enable(False)

    def open_editor(self):
        'set up editor'
        self.editor.Enable(True)

    def set_screen(self, screensize):
        'set application size'
        self.SetSize(screensize)

    def set_splitter(self, split):
        'split screen at the specified position'
        self.splitter.SetSashPosition(split[0], True)

    def create_root(self, title):
        "show the item's child elements"
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot(title)  # self.base.opts["RootTitle"])
        self.activeitem = self.root
        return self.root

    def set_item_expanded(self, item):
        "show the item's child elements"
        self.tree.Expand(item)

    def emphasize_activeitem(value):
        "emphisize the active item's title"
        self.tree.SetItemBold(self.activeitem, False)

    def editor_text_was_changed(self):
        "return the editor's state"
        return self.editor.document().isModified

    def copy_text_from_editor_to_activeitem(self):
        "transfer the editor's text to a treeitem"
        self.set_item_text(self.activeitem, self.editor.GetValue())

    def copy_text_from_item_to_editor()
        "transfer a treeitem's text to the editor"
        self.editor.setText(item.text(1))

    def select_item(self, item):
        "set selection"
        self.tree.SelectItem(item)

    def get_selected_item(self):
        "get selection"
        return self.tree.GetSelection()

    def remove_item_from_tree(self, item):
        "remove an item from the tree and return it"
        prev = self.tree.GetPrevSibling(item)
        self.activeitem = None
        self.tree.Delete(item)
        # deze retourneerde ook nog het item dat geactiveerd moet worden
        # omdat wx na verwijderen het volgende item actief maakt ipv het voorgaande?
        # misschien moet hier daarom nog activeren van het voorafgaande item bij:
        # if prev.IsOk():
        # # if self.tree.GetItemText(prev):
        #     self.base.activate_item(prev)
        # else:
        #     self.editor.Clear()
        #     self.editor.Enable(False)
        return item  # , prev

    def get_key_from_item(self, item):
        "return the data dictionary's key for this item"
        return self.tree.GetItemData(item)[0]

    def get_activeitem_title(self):
        "return the selected item's title"
        return self.tree.GetItemText(self.activeitem)

    def set_activeitem_title(self, text):
        "set the selected item's title to a new value"
        self.tree.SetItemText(self.activeitem, text)

    def set_focus_to_tree(self):
        "schakel over naar tree"
        self.tree.SetFocus()

    def set_focus_to_editor(self):
        "schakel over naar editor"
        self.editor.SetFocus()

    def add_item_to_tree(self, key, tag, text, keywords):  # , revorder):
        "add an item to the tree and return it"
        if self.base.opts['RevOrder']:
            item = self.tree.PrependItem(self.root, tag)
        else:
            item = self.tree.AppendItem(self.root, tag)
        self.tree.SetItemData(item, (key, text, keywords))
        return item

    def get_treeitems(self):
        "return a list with the items in the tree"
        treeitemlist, activeitem = [], 0
        tag, cookie = self.tree.GetFirstChild(self.root)
        while tag.IsOk():
            tag_text = self.tree.GetItemText(tag)
            key, text, keywords = self.tree.GetItemData(tag)
            if tag == self.activeitem:
                activeitem = key
            treeitemlist.append((key, tag_text, text, keywords))
            tag, cookie = self.tree.GetNextChild(self.root, cookie)
            return treeitemlist, activeitem

    def get_screensize(self):
        "return the applications screens's size"
        screensize = self.GetSize()
        return screensize.GetWidth(), screensize.GetHeight()

    def get_splitterpos(self):
        "return the position the screen is split at"
        return (self.splitter.GetSashPosition(),)

    def sleep(self):
        "hide application"
        self.tray_icon = TaskbarIcon(self)
        self.Hide()

    def revive(self, event=None):
        """make application visible again
        """
        self.Show()
        self.tray_icon.Destroy()

    def goto_next_item(self):
        "return the next item in the tree if possible"
        item = self.tree.GetNextSibling(self.activeitem)
        return item if item.IsOk() else None

    def goto_prev_item(self):
        "return the previous item in the tree if possible"
        item = self.tree.GetPrevSibling(self.activeitem)
        return item if item.IsOk() else None

    def get_rootitem_title(self):
        "return the root item's title"
        return self.tree.GetItemText(self.root)

    def set_rootitem_title(self, text):
        "set the root item's title to a new value"
        self.tree.SetItemText(self.root, text)

    def get_item_text(self, item):
        "return the full text for an item"
        return self.tree.GetItemData(item)[1]

    def set_editor_text(self, text):
        "transfer text to the editor"
         self.editor.SetValue(text)

    def get_editor_text(self):
        "return the text in the editor"
        return self.editor.GetValue()

    def set_item_text(self, item, text):
        "set the full text for an item in the tree"
        itemdata = self.tree.GetItemData(item)
        key, data = itemdata[0], itemdata[2]
        self.tree.SetItemData(item, (key, text, data))

    def get_item_keywords(self, item):
        "return the keywords for an item in a list"
        return self.tree.GetItemData(item)[2]

    def set_item_keywords(self, item, data):
        "set the keywords for an item in the tree"
        key, text = self.tree.GetItemData(item)[:2]
        self.tree.SetItemData(item, (key, text, data))

    def show_statusbar_message(self, text):
        "display a message in the application's status bar"
        self.sb.SetStatusText(text)

    def enable_selaction(self, actiontext):
        "mark the specified selection method as active"
        self.selactions[actiontext].Check(True)

    def disable_selaction(self, actiontext):
        "mark the specified selection method as inactive"
        self.selactions[actiontext].Check(False)

    def showmsg(self, message):
        """show a message in a standard box with a standard title"""
        wx.MessageBox(message, self.base.app_title, wx.OK | wx.ICON_INFORMATION, self)

    def ask_question(self, question):
        """ask a question in a standard box with a standard title"""
        answer = wx.MessageBox(question, self.base.app_title, wx.YES_NO | wx.ICON_QUESTION, self)
        return answer == wx.YES
        # alternatively
        # dlg = wx.MessageDialog(self, _("ask_reload"), self.base.app_title, wx.OK | wx.CANCEL)
        # result = dlg.ShowModal()
        # answer = result == wx.ID_OK
        # dlg.Destroy()
        # return answer

    def show_dialog(self, cls, *args):
        "pop up a dialog and return if confirmed"
        with cls(self, *args) as dlg:
            ok = dlg.ShowModal() == wx.ID_OK
            data = dlg.confirm() if ok else None
        return ok, data

    def get_text_from_user(self, prompt, default):
        "ask for text in a popup"
        with wx.TextEntryDialog(self, prompt, self.base.app_title, default) as dlg:
            ok = dlg.ShowModal() == wx.ID_OK
            text = dlg.GetValue()  # if ok else ''
        return text, ok

    def get_choice_from_user(self, prompt, choices, default):
        "pop up a selection list"
        with wx.SingleChoiceDialog(self, prompt, "Apropos", choices,
                                   wx.CHOICEDLG_STYLE) as dlg:
            dlg.SetSelection(default)
            h = dlg.ShowModal()
            ok = h == wx.ID_OK
            sel = dlg.GetStringSelection()
        return sel, ok


class OptionsDialog(wx.Dialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, parent):
        self.parent = parent
        sett2text = self.parent.base.sett2text
        #             {'AskBeforeHide': _('t_hide'),
        #              'NotifyOnLoad': _('t_load'),
        #              'NotifyOnSave': _('t_save')}
        super().__init__(parent, title=_('t_sett'))
        pnl = self  # wx.Panel(self, -1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.FlexGridSizer(cols=2)
        self.controls = []
        for key, value in self.parent.base.opts.items():
            if key not in sett2text:
                continue
            sizer1.Add(wx.StaticText(pnl, -1, sett2text[key]), 1, wx.ALL, 5)
            chk = wx.CheckBox(self, -1, '')
            chk.SetValue(value)
            sizer1.Add(chk, 1, wx.ALL, 5)
            self.controls.append((key, chk))
        sizer0.Add(sizer1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(pnl, id=wx.ID_APPLY, label=_('b_apply'))
        sizer1.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        self.SetAffirmativeId(wx.ID_APPLY)
        btn = wx.Button(pnl, id=wx.ID_CLOSE, label=_('b_close'))
        sizer1.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        self.SetEscapeId(wx.ID_CLOSE)
        # sizer1 = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        sizer0.Add(sizer1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        pnl.SetSizer(sizer0)
        pnl.SetAutoLayout(True)
        sizer0.Fit(pnl)
        sizer0.SetSizeHints(pnl)
        pnl.Layout()

    def confirm(self):
        """update application settings
        """
        for keyvalue, control in self.controls:
            self.parent.base.opts[keyvalue] = control.isChecked()


class CheckDialog(wx.Dialog):
    """Dialoog om te melden dat de applicatie verborgen gaat worden
    AskBeforeHide bepaalt of deze getoond wordt of niet

    Eventueel ook te implementeren m.b.v. wx.RichMessageDialog
    """
    def __init__(self, parent, id_, title, size=(-1, 120), pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent, id_, title, pos, size, style)
        # pnl = wx.Panel(self, -1)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer0.Add(wx.StaticText(self, -1, _("sleep_message")), 1, wx.ALL, 5)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.Check = wx.CheckBox(self, -1, _("hide_message"))
        sizer1.Add(self.Check, 0, wx.EXPAND)
        sizer0.Add(sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        # sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        # self.bOk = wx.Button(pnl, id=wx.ID_OK)
        ## self.bOk.Bind(wx.EVT_BUTTON, self.on_ok)
        # sizer1.Add(self.bOk, 0, wx.EXPAND | wx.ALL, 2)
        # sizer0.Add(sizer1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer0.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL))
        # pnl.SetSizer(sizer0)
        # pnl.SetAutoLayout(True)
        # sizer0.Fit(pnl)
        # sizer0.SetSizeHints(pnl)
        # pnl.Layout()
        self.SetSizer(sizer0)
        self.SetAutoLayout(True)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)
        self.Layout()


class KeywordsDialog(wx.Dialog):
    """Dialoog voor het koppelen van trefwoorden
    """
    def __init__(self, parent, keywords=None):
        self.parent = parent
        if keywords is None:
            keywords = []
        super().__init__(parent)
        self.SetTitle('{} - {}'.format(self.parent.base.app_title, _("w_tags")))
        self.SetIcon(self.parent.nt_icon)
        # define widgets
        self.fromlist = wx.ListBox(self, size=(120, 150), style=wx.LB_EXTENDED)
        self.fromlist.Bind(wx.EVT_LISTBOX_DCLICK, self.move_right)
        text = wx.StaticText(self, label=_("t_tags"))
        fromto_button = wx.Button(self, label=_("b_tag"))
        fromto_button.Bind(wx.EVT_BUTTON, self.move_right)
        tofrom_button = wx.Button(self, label=_("b_untag"))
        tofrom_button.Bind(wx.EVT_BUTTON, self.move_left)
        addtrefw_button = wx.Button(self, label=_("b_newtag"))
        addtrefw_button.Bind(wx.EVT_BUTTON, self.add_trefw)
        help_button = wx.Button(self, label=_("m_keys"))
        help_button.Bind(wx.EVT_BUTTON, self.keys_help)
        self.tolist = wx.ListBox(self, size=(120, 150), style=wx.LB_EXTENDED)
        self.tolist.Bind(wx.EVT_LISTBOX_DCLICK, self.move_left)
        self.create_actions()
        # get data from parent
        all_trefw = self.parent.base.opts['Keywords']
        # self.data = self.parent.activeitem
        curr_trefw = keywords  # self.parent.tree.GetItemData(self.data)[2]
        if curr_trefw:
            [self.tolist.Append(x) for x in curr_trefw]
        if all_trefw:
            [self.fromlist.Append(x) for x in all_trefw if x not in curr_trefw]
        # do layout and show
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(wx.StaticText(self, label=(_("t_left"))))
        vbox2.Add(self.fromlist)
        hbox.Add(vbox2)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.AddStretchSpacer()
        vbox2.Add(text)
        vbox2.Add(fromto_button)
        vbox2.Add(tofrom_button)
        vbox2.AddSpacer(10)
        vbox2.Add(addtrefw_button)
        vbox2.Add(help_button)
        vbox2.AddStretchSpacer()
        hbox.Add(vbox2)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(wx.StaticText(self, label=(_("t_right"))))
        vbox2.Add(self.tolist)
        hbox.Add(vbox2)
        vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL), 0,
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        vbox.Add(hbox)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        self.SetSize(400, 256)

    def create_actions(self):
        """define what can be done in this screen
        """
        accel_list = []
        self.actionlist = ((_('a_from'), 'Ctrl+L', self.activate_left),
                           (_('b_tag'), 'Ctrl+Right', self.move_right),
                           (_('a_to'), 'Ctrl+R', self.activate_right),
                           (_('b_untag'), 'Ctrl+Left', self.move_left),
                           (_('b_newtag'), 'Ctrl+N', self.add_trefw))
        for name, shortcut, callback in self.actionlist:
            act = wx.MenuItem(id=wx.NewId(), text=name)
            self.Bind(wx.EVT_MENU, callback, act)
            accel = wx.AcceleratorEntry(cmd=act.GetId())
            ok = accel.FromString(shortcut)
            if ok:
                accel_list.append(accel)
        accel_table = wx.AcceleratorTable(accel_list)
        self.SetAcceleratorTable(accel_table)

    def activate_left(self, event):
        """activate "from" list
        """
        self._activate(self.fromlist)

    def activate_right(self, event):
        """activate "to" list
        """
        self._activate(self.tolist)

    def _activate(self, win):
        """set focus to list
        """
        item = win.GetSelections()  # currentItem()
        if not item:
            item = [0]  # win.item(0)
        try:
            win.SetSelection(item[0])  # ed(True)
        except wx._core.wxAssertionError:
            if win == self.fromlist:
                self.activate_right()
            else:
                self.activate_left()
            return
        win.SetFocus()

    def move_right(self, event):
        """trefwoord selecteren
        """
        self._moveitem(self.fromlist, self.tolist)

    def move_left(self, event):
        """trefwoord on-selecteren
        """
        self._moveitem(self.tolist, self.fromlist)

    def _moveitem(self, from_, to):
        """trefwoord verplaatsen van de ene lijst naar de andere
        """
        selected = from_.GetSelections()  # selectedItems()
        if selected:
            selection = [from_.GetString(i) for i in selected]
            for indx in reversed(selected):
                from_.Delete(indx)
                to.Insert(selection, to.GetCount())

    def add_trefw(self, event):
        """nieuwe trefwoorden opgeven en direct in de linkerlijst zetten
        """
        with wx.TextEntryDialog(self, caption=self.parent.base.app_title,
                                message=_('t_newtag')) as dlg:
            ok = dlg.ShowModal()
            if ok == wx.ID_OK:
                text = dlg.GetValue()
                self.parent.base.opts["Keywords"].append(text)
                self.tolist.Append(text)

    def keys_help(self, event):
        """Show possible actions and accelerator keys
        """
        with wx.Dialog(self) as dlg:
            data = [x.split(' - ', 1) for x in _('tag_help').split('\n')]
            gbox = wx.FlexGridSizer(cols=2, vgap=2, hgap=25)
            line = 0
            for left, right in data:
                gbox.Add(wx.StaticText(dlg, label=left), 0)
                gbox.Add(wx.StaticText(dlg, label=right), 0)
                line += 1
            dlg.SetTitle(self.parent.base.app_title + " " + _("t_keys"))
            vbox = wx.BoxSizer(wx.VERTICAL)
            vbox.Add(gbox, 0, wx.ALL, 10)
            done_button = wx.Button(dlg, label=_("b_done"))
            dlg.SetAffirmativeId(done_button.GetId())
            vbox.Add(done_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
            # dlg.SetSize(400, 800)
            dlg.SetSizer(vbox)
            dlg.SetAutoLayout(True)
            vbox.Fit(dlg)
            vbox.SetSizeHints(dlg)
            dlg.Layout()
            dlg.ShowModal()

    def confirm(self):    # def accept(self):
        """geef de geselecteerde trefwoorden aan het hoofdprogramma
        """
        return self.tolist.GetItems()


class KeywordsManager(wx.Dialog):
    """Dialoog voor het wijzigen van trefwoorden
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.SetTitle('{} - {}'.format(self.parent.base.app_title, _("t_tagman")))
        self.SetIcon(self.parent.nt_icon)
        self.oldtag = wx.ComboBox(self)
        self.newtag = wx.TextCtrl(self)
        # self.newtag.setMinimumHeight(self.oldtag.height())
        self.refresh_fields()
        remove_button = wx.Button(self, label=_("b_remtag"))
        remove_button.Bind(wx.EVT_BUTTON, self.remove_keyword)
        add_button = wx.Button(self, label=_('b_addtag'))
        add_button.Bind(wx.EVT_BUTTON, self.add_keyword)
        done_button = wx.Button(self, label=_("b_done"))
        self.SetAffirmativeId(done_button.GetId())  # done_button.Bind(wx.EVT_BUTTON, self.accept)
        vbox = wx.BoxSizer(wx.VERTICAL)
        gbox = wx.FlexGridSizer(cols=3)
        gbox.Add(wx.StaticText(self, label=_('l_oldval')), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gbox.Add(self.oldtag, 0, wx.ALL, 5)
        gbox.Add(remove_button, 0, wx.ALL, 5)
        gbox.Add(wx.StaticText(self, label=_('l_newval')), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        gbox.Add(self.newtag, 0, wx.ALL, 5)
        gbox.Add(add_button, 0, wx.ALL, 5)
        vbox.Add(gbox, wx.ALL, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        ## hbox.addWidget(wxStaticText('Changes are applied immediately'))
        hbox.Add(wx.StaticText(self, label=_('t_applied')), 0, wx.ALL, 5)
        vbox.Add(hbox, 0, wx.ALL, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(done_button, 0)
        vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        self.SetSize(400, -1)

    def refresh_fields(self):
        """initialize items on screen
        """
        self.oldtag.Clear()
        self.oldtag.AppendItems(self.parent.base.opts['Keywords'])
        self.oldtag.SetValue('')  # self.oldtag.clearEditText()
        self.newtag.Clear()

    def update_items(self, oldtext, newtext=''):
        """refresh list of associated keywords
        """
        tag, cookie = self.parent.tree.GetFirstChild(self.parent.root)
        while tag.IsOk():
            key, text, keywords = self.parent.tree.GetItemData(tag)
            try:
                ix = keywords.index(oldtext)
                has_keyword = True
            except ValueError:
                has_keyword = False
            if has_keyword:
                if newtext:
                    keywords[ix] = newtext
                else:
                    keywords.pop(ix)
                self.parent.tree.SetItemData(tag, (key, text, keywords))
            tag, cookie = self.parent.tree.GetNextChild(self.parent.root, cookie)

    def remove_keyword(self, event):
        """delete a keyword aftre selecting from the dropdown
        """
        oldtext = self.oldtag.GetValue()
        msg = _('t_remtag').format(oldtext)
        ask = wx.MessageBox(msg, self.parent.base.app_title, wx.YES_NO | wx.ICON_QUESTION, self)
        if ask != wx.YES:
            return
        self.parent.base.opts['Keywords'].remove(oldtext)
        self.update_items(oldtext)
        self.refresh_fields()

    def add_keyword(self, event):
        """Add a new keyword or change an existing one after selecting from the dropdown
        """
        oldtext = self.oldtag.GetValue()
        newtext = self.newtag.GetValue()
        if oldtext:
            with wx.MessageDialog(self, _('t_repltag').format(oldtext, newtext),
                                  style=wx.YES_NO | wx.CANCEL) as prompter:
                prompter.SetExtendedMessage(_('t_repltag2'))
                # prompter.setDefaultButton(wxMessageBox.Yes)
                ## prompter.setEscapeButton(wdg.MessageBox.Cancel)
                ask = prompter.ShowModal()
                if ask == wx.ID_CANCEL:
                    return
                ix = self.parent.base.opts['Keywords'].index(oldtext)
                self.parent.base.opts['Keywords'][ix] = newtext
                if ask == wx.ID_YES:
                    self.update_items(oldtext, newtext)
                else:
                    self.update_items(oldtext)
        else:
            msg = _('t_addtag').format(newtext)
            ask = wx.MessageBox(msg, self.parent.base.app_title, wx.YES_NO | wx.ICON_QUESTION, self)
            if ask != wx.YES:
                return
            self.parent.base.opts['Keywords'].append(newtext)
        self.refresh_fields()

    def confirm(self):
        "finish the dialog"
        pass


class GetTextDialog(wx.Dialog):
    """Dialog to get search string (with options)
    """
    def __init__(self, parent, seltype, seltext, labeltext='', use_case=None):
        self.parent = parent
        super().__init__(parent)
        self.SetTitle(self.parent.base.app_title)
        self.SetIcon(self.parent.nt_icon)

        self.create_inputwin(seltext)

        self.in_exclude = wx.CheckBox(self, label='exclude')
        self.in_exclude.SetValue(False)
        if seltype < 0:
            self.in_exclude.SetValue(True)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label=labeltext), 0, wx.ALL, 5)
        vbox.Add(hbox, 0, wx.ALL, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.inputwin, 1, wx.ALL, 5)
        vbox.Add(hbox, 1, wx.ALL, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.in_exclude, 0, wx.ALL, 5)
        if self.use_case:
            hbox.Add(self.use_case, 0, wx.ALL, 5)
            if use_case:
                self.use_case.SetValue(True)
        vbox.Add(hbox, 0, wx.ALL, 5)
        vbox.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL), 0,
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()

    def create_inputwin(self, seltext):
        """define the widgets to use
        """
        self.inputwin = wx.TextCtrl(self, value=seltext)
        self.use_case = wx.CheckBox(self, label='case sensitive')
        self.use_case.SetValue(False)

    def confirm(self):
        """confirm data changes and communicate to parent window
        """
        self.parent.dialog_data = [self.in_exclude.GetValue(), self.inputwin.GetValue()]
        if self.use_case:
            self.parent.dialog_data.append(self.use_case.GetValue())


class GetItemDialog(GetTextDialog):
    """Dialog to select a keyword from a list
    """
    def create_inputwin(self, seltext):
        """define the widgets to use
        """
        selection_list = self.parent.base.opts['Keywords']
        try:
            selindex = selection_list.index(seltext)
        except ValueError:
            selindex = -1
        self.inputwin = wx.ComboBox(self, choices=selection_list)
        self.inputwin.SetSelection(selindex)
        self.use_case = None


class GridDialog(wx.Dialog):
    """dialog showing texts in a grid layout
    """
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(-1, 320), style=wx.DEFAULT_DIALOG_STYLE)
        # pnl = wx.Panel(self)
        lines = [x.split(' - ', 1) for x in _("help_text").split('\n')]
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        gbox = wx.FlexGridSizer(cols=2)  # , rows = len(lines))
        line = 0
        for left, right in lines:
            gbox.Add(wx.StaticText(self, label=left))
            gbox.Add(wx.StaticText(self, label=right))
            line += 1
        sizer0.Add(gbox, 0, wx.GROW | wx.ALL, 5)
        # sizer1 = wx.BoxSizer(wx.VERTICAL)
        # self.bOk = wx.Button(pnl, id=wx.ID_OK)
        # sizer1.Add(self.bOk, 0, wx.EXPAND | wx.ALL, 2)
        # sizer0.Add(sizer1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        sizer0.Add(self.CreateButtonSizer(wx.OK))
        # pnl.SetSizer(sizer0)
        # pnl.SetAutoLayout(True)
        # sizer0.Fit(pnl)
        # sizer0.SetSizeHints(pnl)
        self.SetSizer(sizer0)
        self.SetAutoLayout(True)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)
        # pnl.Layout()
        self.Layout()

    def confirm(self):
        "finish the dialog (no data to exchange)"
        pass


class TaskbarIcon(wx.adv.TaskBarIcon):
    "icon in the taskbar"
    id_revive = wx.NewId()

    def __init__(self, parent):
        super().__init__(wx.adv.TBI_DOCK)
        # wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(parent.nt_icon, _("revive_message"))
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, parent.revive)
        self.Bind(wx.EVT_MENU, parent.revive, id=self.id_revive)

    def CreatePopupMenu(self):
        """reimplemented"""
        menu = wx.Menu()
        menu.Append(self.id_revive, 'Revive NoteTree')
        return menu
