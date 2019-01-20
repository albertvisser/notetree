# -*- coding: utf-8 -*-
"""NoteTree wxPython versie - niet in onderhoud

van een ibm site afgeplukt
"""
import os
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
    pass


class KeywordsDialog(wx.Dialog):
    """Dialoog voor het koppelen van trefwoorden
    """
    pass


class GetTextDialog(wx.Dialog):
    pass


class GetItemDialog(wx.Dialog):
    pass


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
        self.create_menu()

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
        ix = 0
        self.keydef_to_method = {}
        for item, data in self.get_menudata():
            menu_label = item
            submenu = wx.Menu()
            for label, handler, info, keydef in data:
                if label != "":
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
        self.save()
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
        item_to_return = self.root
        self.activeitem = None
        for key, value in self.nt_data.items():
            # print(key, value)
            if key != 0:
                tag, text = value
                item = self.tree.AppendItem(self.root, tag)
                self.tree.SetItemData(item, text)
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
            self.nt_data[ky] = (self.tree.GetItemText(tag), self.tree.GetItemData(tag))
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
                self.tree.SetItemData(self.activeitem, self.editor.GetValue())

    def activate_item(self, item):
        """make the new item "active" and get the text for itfrom the tree structure
        """
        self.activeitem = item
        if item != self.root:
            self.tree.SetItemBold(item, True)
            self.editor.SetValue(self.tree.GetItemData(item))
            self.editor.Enable(True)
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
        pass

    def manage_keywords(self, event=None):
        """Open a dialog where keywords can be renamed, removed or added
        """
        pass

    def reverse(self, event=None):
        """set to "newest first"
        """
        pass

    def no_selection(self, event=None):
        """make sure nothing is selected
        """
        pass

    def keyword_select(self, event=None):
        """Open a dialog where a keyword can be chosen to select texts that it's assigned to
        """
        pass

    def text_select(self, event=None):
        """Open a dialog box where text can be entered that the texts to be selected contain
        """
        pass

    def showmsg(self, message):
        wx.MessageBox(message, app_title, wx.OK | wx.ICON_INFORMATION, self)


def main(fn):
    """application start
    """
    app = wx.App(False)
    frame = MainWindow(None, -1, " - ".join((app_title, fn)))
    app.SetTopWindow(frame)
    frame.project_file = fn
    frame.open()
    app.MainLoop()
