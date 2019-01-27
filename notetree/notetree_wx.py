# -*- coding: utf-8 -*-
"""NoteTree wxPython versie - niet in onderhoud

van een ibm site afgeplukt
"""
import os
import sys
import logging
import gettext
from datetime import datetime
import wx
import wx.adv
from .notetree_shared import NoteTreeMixin, app_title, root_title, languages

## app_title = "NoteTree"
## HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
## locale = os.path.join(HERE, 'locale')
## print locale
## gettext.install(app_title, locale)
## languages = {'nl': gettext.translation(app_title, locale, languages=['nl']),
    ## 'en': gettext.translation(app_title, locale, languages=['en'])}

## root_title = "MyNotes"


class KeywordsManager(wx.Dialog):
    """Dialoog voor het wijzigen van trefwoorden
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.SetTitle('{} - {}'.format(app_title, _("t_tagman")))
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
        self.oldtag.AppendItems(self.parent.opts['Keywords'])
        # self.oldtag.clearEditText()
        self.newtag.Clear()

    def update_items(self, oldtext, newtext=''):
        """refresh list of associated keywords
        """
        for ix in range(self.parent.root.childCount()):
            item = self.parent.root.child(ix)
            keywords = []  # item.data(1, core.Qt.UserRole)
            try:
                ix = keywords.index(oldtext)
            except ValueError:
                continue
            if newtext:
                keywords[ix] = newtext
            else:
                keywords.pop(ix)
            # item.setData(1, core.Qt.UserRole, keywords)

    def remove_keyword(self, event):
        """delete a keyword aftre selecting from the dropdown
        """
        oldtext = self.oldtag.GetValue()
        msg = _('t_remtag').format(oldtext)
        ask = wx.MessageBox(msg, app_title, wx.YES_NO | wx.ICON_QUESTION, self)
        if ask != wx.YES:
            return
        self.parent.opts['Keywords'].remove(oldtext)
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
                ix = self.parent.opts['Keywords'].index(oldtext)
                self.parent.opts['Keywords'][ix] = newtext
                if ask == wx.ID_YES:
                    self.update_items(oldtext, newtext)
                else:
                    self.update_items(oldtext)
        else:
            msg = _('t_addtag').format(newtext)
            ask = wx.MessageBox(msg, app_title, wx.YES_NO | wx.ICON_QUESTION, self)
            if ask != wx.YES:
                return
            self.parent.opts['Keywords'].append(newtext)
        self.refresh_fields()


class KeywordsDialog(wx.Dialog):
    """Dialoog voor het koppelen van trefwoorden
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.SetTitle('{} - {}'.format(app_title, _("w_tags")))
        self.SetIcon(self.parent.nt_icon)
        # define widgets
        self.fromlist = wx.ListBox(self, size=(120, 150), style=wx.LB_EXTENDED)
        # self.fromlist = wx.ListCtrl(self, size=(120, 150), style=wx.LC_REPORT)
        self.fromlist.Bind(wx.EVT_LISTBOX_DCLICK, self.move_right)
        # self.fromlist.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.move_right)
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
        # self.tolist = wx.ListCtrl(self, size=(120, 150), style=wx.LC_REPORT)
        self.tolist.Bind(wx.EVT_LISTBOX_DCLICK, self.move_left)
        # self.tolist.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.move_left)
        self.create_actions()
        # get data from parent
        all_trefw = self.parent.opts['Keywords']
        self.data = self.parent.activeitem
        curr_trefw = self.parent.tree.GetItemData(self.data)[1]
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
        # hbox.Add(bbox)
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
        return  # do nothing for now
        self.actionlist = (('a_from', 'Ctrl+L', self.activate_left),
                           (_('b_tag'), 'Ctrl+Right', self.move_right),
                           ('a_to', 'Ctrl+R', self.activate_right),
                           (_('b_untag'), 'Ctrl+Left', self.move_left),
                           (_('b_newtag'), 'Ctrl+N', self.add_trefw))
        for name, shortcut, callback in self.actionlist:
            act = wx.MenuItem(self, '\n'.join(name, shortcut))
            act.Bind(wx.MENU_ITEM, callback)

    def activate_left(self):
        """activate "from" list
        """
        print('in activate_left')
        self._activate(self.fromlist)

    def activate_right(self):
        """activate "to" list
        """
        print('in activate_right')
        self._activate(self.tolist)

    def _activate(self, win):
        """set focus to list
        """
        item = win.GetSelection()  # currentItem()
        if not item:
            item = 0  # win.item(0)
        item.setSelection(item)  # ed(True)
        win.SetFocus()

    def move_right(self, event):
        """trefwoord selecteren
        """
        print('move to right')
        self._moveitem(self.fromlist, self.tolist)

    def move_left(self, event):
        """trefwoord on-selecteren
        """
        print('move to left')
        self._moveitem(self.tolist, self.fromlist)

    def _moveitem(self, from_, to):
        """trefwoord verplaatsen van de ene lijst naar de andere
        """
        selected = from_.GetSelections()  # selectedItems()
        print('moving', selected)
        selection = [from_.GetString(i) for i in selected]
        for indx in reversed(selected):
            from_.Delete(indx)
        to.Insert(selection, to.GetCount())

    def add_trefw(self, event):
        """nieuwe trefwoorden opgeven en direct in de linkerlijst zetten
        """
        with wx.TextEntryDialog(self, caption=app_title, message=_('t_newtag')) as dlg:
            ok = dlg.ShowModal()
            if ok == wx.ID_OK:
                text = dlg.GetValue()
                self.parent.opts["Keywords"].append(text)
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
            dlg.SetTitle(app_title + " " + _("t_keys"))
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

    def accept(self, event):
        """geef de geselecteerde trefwoorden aan het hoofdprogramma
        """
        return  # do nothing for now
        self.parent.new_keywords = [self.tolist.item(i).text() for i in range(
            len(self.tolist))]
        super().accept()


class GetTextDialog(wx.Dialog):
    """Dialog to get search string (with options)
    """
    def __init__(self, parent, seltype, seltext, labeltext='', use_case=None):
        self.parent = parent
        super().__init__(parent)
        self.SetTitle(app_title)
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


class GetItemDialog(GetTextDialog):
    """Dialog to select a keyword from a list
    """
    def create_inputwin(self, seltext):
        """define the widgets to use
        """
        selection_list = self.parent.opts['Keywords']
        try:
            selindex = selection_list.index(seltext)
        except ValueError:
            selindex = -1
        self.inputwin = wx.ComboBox(self, choices=selection_list)
        self.inputwin.SetSelection(selindex)
        self.use_case = None


class CheckDialog(wx.Dialog):
    """Dialoog om te melden dat de applicatie verborgen gaat worden
    AskBeforeHide bepaalt of deze getoond wordt of niet

    Eventueel ook te implementeren m.b.v. wx.RichMessageDialog
    """
    def __init__(self, parent, id, title, size=(-1, 120), pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
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


class GridDialog(wx.Dialog):
    """dialog showing texts in a grid layout
    """
    def __init__(self, parent, title):
        # print('set up dialog')
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


class MainWindow(wx.Frame, NoteTreeMixin):
    """Application main screen
    """
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size=(800, 500),
                          style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.nt_icon = wx.Icon(os.path.join(os.path.dirname(__file__), "notetree.ico"),
                               wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.nt_icon)
        self.sb = self.CreateStatusBar()

        # tray icon wordt pas opgezet in de hide() methode

        menuBar = wx.MenuBar()
        self.SetMenuBar(menuBar)
        # self.create_menu()

        self.splitter = wx.SplitterWindow(self, -1)
        self.splitter.SetMinimumPaneSize(1)

        self.tree = wx.TreeCtrl(self.splitter)
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
        """Build the application menu
        """
        menu_bar = self.GetMenuBar()
        menuitems = menu_bar.GetMenus()
        has_items = bool(menuitems)
        self.selactions = {}
        self.seltypes = []
        ix = 0
        self.keydef_to_method = {}
        for item, data in self.get_menudata():
            menu_label = item
            submenu = wx.Menu()
            for label, handler, info, keydef in data:
                if keydef:
                    defs = keydef.split(',')
                    primary = defs[0]
                    keydef = ','.join(defs[1:])
                else:
                    primary = None
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
                        elif key == 'F9':
                            key = wx.WXK_F9
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
        for item in self.selactions.values():
            item.Check(False)
        self.selactions[_('m_revorder')].Check(self.opts['RevOrder'])
        self.selactions[self.seltypes[abs(self.opts['Selection'][0])]].Check(True)

    def on_key(self, event):
        """keypress handler
        """
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
                pass  # delete key should work normally when not in tree
            else:
                self.keydef_to_method[mod, keycode]()
                skip = False
        if event and skip:
            ## print 'skipping'
            event.Skip()

    def OnEvtText(self, event):
        """reimplemented event handler
        """
        self.editor.IsModified = True

    def OnSelChanging(self, event=None):
        """reimplemented event handler
        """
        if event.GetItem() == self.root:
            event.Veto()

    def OnSelChanged(self, event=None):
        """reimplemented event handler
        """
        ## test = event.GetItem()
        self.check_active()
        self.activate_item(event.GetItem())
        event.Skip()

    def close(self, event=None):
        """save before shutting down
        """
        self.update()
        self.Close()

    def open(self):
        """read a file from disk and turn it into a tree structure
        """
        msg = NoteTreeMixin.open(self, "Wx", root_title)
        self.tree.SetFocus()
        if self.nt_data == {}:
            return
        if msg:
            self.showmsg(msg)
            return
        # recreate menu after loading (because of language)
        self.create_menu()
        self.tree.DeleteAllItems()
        self.root = self.tree.AddRoot(os.path.splitext(os.path.basename(self.project_file))[0])
        item_to_activate = self.root
        self.editor.Clear()
        self.editor.Enable(False)
        item_to_activate = self.build_tree(first_time=True)
        self.tree.SetItemText(self.root, self.opts["RootTitle"])
        self.SetSize(self.opts["ScreenSize"])
        self.splitter.SetSashPosition(self.opts["SashPosition"], True)
        self.tree.Expand(self.root)
        self.tree.SelectItem(item_to_activate)
        self.tree.SetFocus()

    def build_tree(self, first_time=False):
        """translate the dictionary read to a tree structure
        """
        if not first_time:
            # self.tree_to_dict()
            self.check_active()  # even zorgen dat de editor inhoud geassocieerd wordt
            self.tree.DeleteChildren(self.root)
        item_to_return = self.root
        self.activeitem = None
        seltype, seldata = self.opts["Selection"][:2]
        use_case = None
        if len(self.opts["Selection"]) > 2:
            use_case = self.opts["Selection"][2]
        for key, value in self.nt_data.items():
            if key == 0:
                continue
            try:
                tag, text, keywords = value
            except ValueError:
                tag, text = value
                keywords = []
            if seltype == 1 and seldata not in keywords:
                continue
            if seltype == 2:
                ok = False
                if use_case and seldata in text:
                    ok = True
                elif not use_case and seldata.upper() in text.upper():
                    ok = True
                if not ok:
                    continue
            if seltype == -1 and seldata in keywords:
                continue
            if self.opts['RevOrder']:
                item = self.tree.PrependItem(self.root, tag)
            else:
                item = self.tree.AppendItem(self.root, tag)
            self.tree.SetItemData(item, (text, keywords))
            if key == self.opts["ActiveItem"]:
                item_to_return = item
        return item_to_return

    def reread(self, event=None):
        """revert to the saved version of the notes file
        """
        dlg = wx.MessageDialog(self, _("ask_reload"), app_title, wx.OK | wx.CANCEL)
        result = dlg.ShowModal()
        if result == wx.ID_OK:
            self.open()
        dlg.Destroy()

    def tree_to_dict(self):
        """translate the entire tree structure to a dictionary suitable for saving
        """
        self.check_active()  # even zorgen dat de editor inhoud geassocieerd wordt
        self.nt_data = {}    # don't forget to remove this when we apply selections
        ky = 0
        tag, cookie = self.tree.GetFirstChild(self.root)
        while tag.IsOk():
            ky += 1
            if tag == self.activeitem:
                self.opts["ActiveItem"] = ky
            self.nt_data[ky] = (self.tree.GetItemText(tag), *self.tree.GetItemData(tag))
            tag, cookie = self.tree.GetNextChild(self.root, cookie)

    def update(self, event=None):
        """resave the notes to a file
        """
        self.tree_to_dict()   # check for changed values in tree not in dict
        self.opts["ScreenSize"] = self.GetSize()
        self.opts["SashPosition"] = self.splitter.GetSashPosition()
        NoteTreeMixin.save(self)

    def rename(self, event=None):
        """ask for a new title for the root item
        """
        dlg = wx.TextEntryDialog(self, _("t_root"), app_title, self.tree.GetItemText(self.root))
        if dlg.ShowModal() == wx.ID_OK:
            self.tree.SetItemText(self.root, dlg.GetValue())
        dlg.Destroy()

    def hide_me(self, event=None):
        """Minimize application to an icon in the system tray
        """
        cancel = False
        if self.opts["AskBeforeHide"]:
            with CheckDialog(self, -1, app_title) as dlg:
                if dlg.ShowModal() == wx.ID_CANCEL:
                    cancel = True
                elif dlg.Check.GetValue():
                    self.opts["AskBeforeHide"] = False
                # dlg.Destroy()
        if cancel:
            return
        ## self.tbi = wx.adv.TaskBarIcon()
        self.tbi = TaskbarIcon(self)
        ## self.tbi.SetIcon(self.nt_icon, _("revive_message"))
        ## self.tbi.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.revive)
        ## self.tbi.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.revive)
        self.Hide()

    def revive(self, event=None):
        """make application visible again
        """
        self.Show()
        self.tbi.Destroy()

    def new_item(self, event=None):
        """add a new item to the tree after asking for a title
        """
        # kijk waar de cursor staat (of altijd onderaan toevoegen?)
        start = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        dlg = wx.TextEntryDialog(self, _("t_new"), app_title, start)
        if dlg.ShowModal() == wx.ID_OK:
            text = dlg.GetValue()
            item = self.tree.AppendItem(self.root, text)
            self.tree.SetItemData(item, "")
            # maybe set data to a tuple of (dict key, editor text, list of keywords)
            self.tree.SelectItem(item)
            self.tree.Expand(self.root)
            self.editor.Clear()
            self.editor.Enable(True)
            self.editor.SetInsertionPoint(0)
            self.editor.SetFocus()
        dlg.Destroy()

    def delete_item(self, event=None):
        """remove item from tree
        """
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
        """Get/change a title for this note
        """
        dlg = wx.TextEntryDialog(self, _("t_name"), app_title,
                                 self.tree.GetItemText(self.activeitem))
        if dlg.ShowModal() == wx.ID_OK:
            self.tree.SetItemText(self.activeitem, dlg.GetValue())
        dlg.Destroy()

    def next_note(self, event=None):
        """Go to next
        """
        item = self.tree.GetNextSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)
        else:
            self.showmsg(_("no_next_item"))

    def prev_note(self, event=None):
        """Go to previous
        """
        item = self.tree.GetPrevSibling(self.activeitem)
        if item.IsOk():
            self.tree.SelectItem(item)
        else:
            self.showmsg(_("no_prev_item"))

    def check_active(self, message=None):
        """if there's a suitable "active" item, make sure its text is saved to the tree
        structure

        """
        if self.activeitem and self.activeitem != self.root:
            self.tree.SetItemBold(self.activeitem, False)
            if self.editor.IsModified:
                if message:
                    self.showmsg(message)
                oldtext, keywords = self.tree.GetItemData(self.activeitem)
                self.tree.SetItemData(self.activeitem, (self.editor.GetValue(), keywords))

    def activate_item(self, item):
        """make the new item "active" and get the text for itfrom the tree structure
        """
        self.activeitem = item
        if item != self.root:
            self.tree.SetItemBold(item, True)
            self.editor.SetValue(self.tree.GetItemData(item)[0])
            self.editor.Enable(True)
            self.tree.EnsureVisible(item)
        else:
            self.editor.Clear()
            self.editor.Enable(False)

    def info_page(self, event=None):
        """show program info
        """
        self.showmsg(_("info_text"))

    def help_page(self, event=None):
        """show keyboard shortcuts
        """
        with GridDialog(self, title=app_title + " " + _("t_keys")) as dlg:
            dlg.ShowModal()

    def choose_language(self, event=None):
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        data = [(code, _('t_{}'.format(code))) for code in ('nl', 'en')]
        with wx.SingleChoiceDialog(self, _("t_lang"), "Apropos", [x[1] for x in data],
                                   wx.CHOICEDLG_STYLE) as dlg:
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
                        print('now using language "{}"'.format(code))
                        self.create_menu()
                        break

    def link_keywords(self, event=None):
        """Open a dialog where keywords can be assigned to the text
        """
        text, old_keywords = self.tree.GetItemData(self.activeitem)
        print(old_keywords)
        with KeywordsDialog(self) as dlg:
            ok = dlg.ShowModal()
            if ok == wx.ID_OK:
                new_keywords = dlg.tolist.GetItems()
                print(new_keywords)
                self.tree.SetItemData(self.activeitem, (text, new_keywords))
                print(self.tree.GetItemData(self.activeitem))

    def manage_keywords(self, event=None):
        """Open a dialog where keywords can be renamed, removed or added
        """
        with KeywordsManager(self) as dlg:
            dlg.ShowModal()

    def reverse(self, event=None):
        """set to "newest first"
        """
        print('in reverse')
        print('  option is ', self.opts['RevOrder'])
        self.opts['RevOrder'] = not self.opts['RevOrder']
        print('  option is now', self.opts['RevOrder'])
        item_to_activate = self.build_tree()
        print('tree is rebuilt')
        # self.tree.setCurrentItem(item_to_activate)
        self.activate_item(item_to_activate)

    def no_selection(self, event=None):
        """make sure nothing is selected
        """
        # return  # do nothing for now
        self._set_selection((0, ""), _("h_selall"))

    def keyword_select(self, event=None):
        """Open a dialog where a keyword can be chosen to select texts that it's assigned to
        """
        # return  # do nothing for now
        seltype, seltext = self.opts['Selection'][:2]
        if abs(seltype) != 1:
            seltext = ''
        with GetItemDialog(self, seltype, seltext, _("i_seltag")) as dlg:
            ok = dlg.ShowModal()
            if ok == wx.ID_OK:
                exclude = dlg.in_exclude.GetValue()
                text = dlg.inputwin.GetValue()
                if exclude:
                    seltype, in_ex = -1, "all except"
                else:
                    seltype, in_ex = 1, 'only'
                self._set_selection((seltype, text), _("s_seltag").format(in_ex, text))
            else:
                self._set_option(1, "m_seltag")

    def text_select(self, event=None):
        """Open a dialog box where text can be entered that the texts to be selected contain
        """
        # return  # do nothing for now
        try:
            seltype, seltext, use_case = self.opts['Selection']
        except ValueError:
            seltype, seltext = self.opts['Selection']
            use_case = None
        if abs(seltype) != 2:
            seltext = ''
        with GetTextDialog(self, seltype, seltext, _("i_seltxt"), use_case) as dlg:
            ok = dlg.ShowModal()
            if ok == wx.ID_OK:
                exclude = dlg.in_exclude.GetValue()
                text = dlg.inputwin.GetValue()
                use_case = dlg.use_case.GetValue()
                ## self.opts['Selection'] = (2, text)
                if exclude:
                    seltype, in_ex = -2, "all except"
                else:
                    seltype, in_ex = 2, 'only'
                self._set_selection((seltype, text, use_case), _("s_seltxt").format(in_ex, text))
            else:
                self._set_option(2, "m_seltxt")

    def _set_selection(self, sel, seltext):
        """selectie aanpassen"""
        self.opts["Selection"] = sel
        self.sb.SetStatusText(seltext)
        item_to_activate = self.build_tree()
        self.tree.SelectItem(item_to_activate)
        for text, action in self.selactions.items():
            if text == seltext:
                action.Check(True)
            elif text != _("m_revorder"):
                action.Check(False)

    def _set_option(self, seltype, name):
        """bij cancelen selectiedialoog de juiste menukeuze weer aan/uitzetten
        """
        if abs(self.opts['Selection'][0]) == seltype:
            self.selactions[_(name)].Check(True)
        else:
            self.selactions[_(name)].Check(False)

    def showmsg(self, message):
        wx.MessageBox(message, app_title, wx.OK | wx.ICON_INFORMATION, self)


def main(fn):
    """application start
    """
    app = wx.App(False)
    frame = MainWindow(None, -1, " - ".join((fn, app_title)))
    app.SetTopWindow(frame)
    frame.project_file = fn
    frame.open()

    app.MainLoop()
