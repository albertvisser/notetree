"""NoteTree wxPython versie

van een ibm site afgeplukt
"""
import os
# import sys
import gettext
import contextlib
import wx
import wx.adv
from wx import stc
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

    def init_screen(self, title, iconame):
        "setup screen"
        super().__init__(None, title=title, size=(800, 500),
                         style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.nt_icon = wx.Icon(iconame, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.nt_icon)
        self.SetMenuBar(wx.MenuBar())

    def setup_statusbar(self):
        "define a statusbar"
        self.sb = self.CreateStatusBar()

    def setup_trayicon(self):
        "define an icon to put in the systray"
        # tray icon wordt pas opgezet in de hide() methode

    def setup_split_screen(self):
        "define the main splitter widget and place its components"
        self.splitter = wx.SplitterWindow(self)
        self.splitter.SetMinimumPaneSize(1)
        self.splitter.SplitVertically(self.setup_tree(), self.setup_editor())
        self.splitter.SetSashPosition(180, True)
        self.app.SetTopWindow(self)
        self.Show(True)

    def setup_tree(self):
        "define the tree panel"
        self.tree = wx.TreeCtrl(self.splitter)
        self.root = self.tree.AddRoot(self.base.root_title)
        # self.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelChanging, self.tree)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelChanging)
        # self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        return self.tree

    def setup_editor(self):
        "define the editor panel"
        # self.editor = wx.TextCtrl(self.splitter, style=wx.TE_MULTILINE)
        self.editor = stc.StyledTextCtrl(self.splitter)  # , style=wx.TE_MULTILINE)
        self.editor.Enable(False)
        self.setup_text()
        self.editor.Bind(wx.EVT_TEXT, self.OnEvtText)
        return self.editor

    def setup_text(self):
        "define the scintilla widget's properties"
        # Set the default font
        monospace_font = wx.Font()
        monospace_font.SetFamily(wx.FONTFAMILY_TELETYPE)
        # monospace_font.SetFixedPitch(True)
        monospace_font.SetPointSize(10)
        # self.editor.SetFont(font)
        # self.editor.SetMarginsFont(font)
        self.editor.SetWrapMode(stc.STC_WRAP_WORD)

        # # Margin 0 is used for line numbers
        # fontmetrics = gui.QFontMetrics(font)
        # self.editor.SetMarginsFont(font)
        # self.editor.SetMarginWidth(0, fontmetrics.width("00000"))
        # self.editor.SetMarginLineNumbers(0, True)
        # self.editor.SetMarginsBackgroundColor(gui.QColor("#cccccc"))

        # # Enable brace matching, auto-indent, code-folding
        # self.editor.SetBraceMatching(sci.QsciScintilla.SloppyBraceMatch)
        # self.editor.SetAutoIndent(True)
        # self.editor.SetFolding(sci.QsciScintilla.PlainFoldStyle)

        # # Current line visible with special background color
        self.editor.SetCaretLineVisible(True)
        self.editor.SetCaretLineBackground(wx.Colour(255, 244, 244))  # "#ffe4e4"))

        # lexer.SetDefaultFont(font)
        self.editor.SetLexer(stc.STC_LEX_MARKDOWN)

        # SCE_MARKDOWN_STRONG1: "**" - Strong emphasis (bold)
        # SCE_MARKDOWN_STRONG2: "__" - Strong emphasis (bold)
        for style in (2, 3):
            self.editor.StyleSetForeground(style, wx.Colour(34, 68, 102))  # 0x224466
            self.editor.StyleSetBold(style, True)

        # SCE_MARKDOWN_EM1: '*' - Emphasis (italic)
        # SCE_MARKDOWN_EM2: '_' - Emphasis (italic)
        for style in (4, 5):
            self.editor.StyleSetForeground(style, wx.Colour(70, 51, 0))  # 0x663300
            self.editor.StyleSetItalic(style, True)

        # SCE_MARKDOWN_HEADER1: "#" - Level-one header
        # SCE_MARKDOWN_HEADER2: "##" - Level-two header
        # SCE_MARKDOWN_HEADER3: "###" - Level-three header
        # SCE_MARKDOWN_HEADER4: "####" - Level-four header
        # SCE_MARKDOWN_HEADER5: "#####" - Level-five header
        # SCE_MARKDOWN_HEADER6: "######" - Level-six header
        for style in range(6, 12):
            self.editor.StyleSetForeground(style, wx.Colour(81, 131, 196))   # 0x5183C4
            self.editor.StyleSetBold(style, True)
            # self.editor.StyleSetFont(style, monospace_font)

        # SCE_MARKDOWN_PRECHAR: Prechar (up to three indent spaces, e.g. for a second-level list)
        self.editor.StyleSetBackground(12, wx.Colour(253, 253, 170))  # 0xEEEEAA
        self.editor.StyleSetForeground(12, wx.Colour(0, 0, 0))        # 0x000000

        # SCE_MARKDOWN_ULIST_ITEM: "- ", "* ", "+ " - Unordered list item
        # SCE_MARKDOWN_OLIST_ITEM: "1. " to "9. ", "#. " - Ordered list item
        self.editor.StyleSetForeground(13, wx.Colour(85, 85, 85))   # 0x555555
        self.editor.StyleSetForeground(14, wx.Colour(85, 85, 85))   # 0x555555

        # SCE_MARKDOWN_BLOCKQUOTE: "> " - Block quote
        self.editor.StyleSetForeground(15, wx.Colour(0, 0, 136))   # 0x000088

        # SCE_MARKDOWN_STRIKEOUT: "~~" - Strikeout
        self.editor.StyleSetBackground(16, wx.Colour(169, 186, 157))   # 0xA9BA9D
        self.editor.StyleSetForeground(16, wx.Colour(24, 69, 59))   # 0x18453B
        # self.editor.StyleSetFont(16, monospace_font)

        # SCE_MARKDOWN_HRULE: "---", "***", "___" - Horizontal rule
        self.editor.StyleSetForeground(17, wx.Colour(85, 85, 85))   # 0x555555
        self.editor.StyleSetBold(17, True)
        # self.editor.StyleSetFont(17, monospace_font)

        # SCE_MARKDOWN_LINK: "[]", "![]" - Link or image
        self.editor.StyleSetForeground(18, wx.Colour(0, 0, 170))    # 0x0000AA
        self.editor.StyleSetUnderline(style, True)

        # SCE_MARKDOWN_CODE: '`' - Inline code
        # SCE_MARKDOWN_CODE2: "``" - Inline code (quotes code containing a single backtick)
        # SCE_MARKDOWN_CODEBK: "~~~" - Code block
        for style in range(19, 22):
            self.editor.StyleSetBackground(style, wx.Colour(253, 253, 253))   # 0xEEEEEE
            self.editor.StyleSetForeground(style, wx.Colour(0, 0, 136))   # 0x000088
            # self.editor.StyleSetFont(style, monospace_font)

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
                # breakpoint()
                if keydef:
                    test = keydef.split(',')
                    primary, extra = test[0], test[1:]
                else:
                    primary, extra = None, []
                menuitem, label, primary = self.create_menuitem(
                    label, menu_label, submenu, primary, info, handler)
                submenu.Append(menuitem)
                accel_list.extend(self.create_accelerators(label, primary, extra, menuitem, handler))
            if has_items:
                menu_bar.Replace(ix, submenu, menu_label)
                menuitems[ix][0].Destroy()
            else:
                menu_bar.Append(submenu, menu_label)
            ix += 1
        self.SetAcceleratorTable(wx.AcceleratorTable(accel_list))
        for item in self.selactions.values():
            item.Check(False)
        with contextlib.suppress(KeyError):
            self.selactions[_('m_revorder')].Check(self.base.opts['RevOrder'])
            self.selactions[self.seltypes[abs(self.base.opts['Selection'][0])]].Check(True)

    def create_menuitem(self, label, menu_label, submenu, primary, info, handler):
        if label != "":
            orig_label = label
            if primary:
                if primary == 'Ctrl+PgDown':
                    primary = 'Ctrl+PgDn'
                label = f'{label}\t{primary}'
            if menu_label == _('m_view'):
                if orig_label != _('m_revorder'):
                    self.seltypes.append(label)
                menu_item = wx.MenuItem(submenu, wx.ID_ANY, label, info, wx.ITEM_CHECK)
                self.selactions[orig_label] = menu_item
            else:
                menu_item = wx.MenuItem(submenu, wx.ID_ANY, label, info)
            self.Bind(wx.EVT_MENU, handler, menu_item)
            # menu_item.Bind(wx.EVT_MENU, handler)
        else:
            menu_item = wx.MenuItem(submenu, wx.ID_SEPARATOR)
        return menu_item, label, primary

    def create_accelerators(self, label, primary, extra, menu_item, handler):
        "build keyboard shortcut and bind to menu of return in list"
        accel_list = []
        # if label in (_('m_forward'), _('m_back')):
        if label.startswith((_('m_forward'), _('m_back'))):
            accel = wx.AcceleratorEntry(cmd=menu_item.GetId())
            if accel.FromString(primary):
                accel_list.append(accel)
        for key in extra:  # define extra keydefs via accelerator table
            menu_item = wx.MenuItem(text=label)
            self.Bind(wx.EVT_MENU, handler, menu_item)
            # menu_item.Bind(wx.EVT_MENU, handler)
            accel = wx.AcceleratorEntry(cmd=menu_item.GetId())
            if accel.FromString(key):
                if key == 'Delete':
                    self.tree.SetAcceleratorTable(wx.AcceleratorTable([accel]))
                else:
                    accel_list.append(accel)
        return accel_list

    def OnEvtText(self, event):
        """reimplemented event handler
        """
        self.editor.IsModified = True

    def OnSelChanging(self, event):
        """reimplemented event handler
        """
        # oorspronkelijk mocht je niet naar het root item navigeren maar in de qt versie kan dat
        # niet zo makkelijk voorkomen worden
        # misschien moet je de tekst ook maar kunnen invullen net als in treedocs?

    def OnSelChanged(self, event):
        """reimplemented event handler
        """
        item_to_activate = event.GetItem()
        # if item_to_activate == self.root:
        #     return
        self.base.check_active()
        print(f'in onselchanged: item is {item_to_activate}, root is {self.root}')
        self.base.activate_item(item_to_activate)
        event.Skip()

    def close(self, event):
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

    def emphasize_activeitem(self, value):
        "emphisize the active item's title"
        self.tree.SetItemBold(self.activeitem, value)

    def editor_text_was_changed(self):
        "return the editor's state"
        return self.editor.IsModified

    def copy_text_from_editor_to_activeitem(self):
        "transfer the editor's text to a treeitem"
        self.set_item_text(self.activeitem, self.editor.GetValue())

    def copy_text_from_activeitem_to_editor(self):
        "transfer a treeitem's text to the editor"
        self.editor.SetValue(self.get_item_text(self.activeitem))

    def select_item(self, item):
        "set selection"
        self.tree.SelectItem(item)

    def get_selected_item(self):
        "get selection"
        return self.tree.GetSelection()

    def remove_item_from_tree(self, item):
        "remove an item from the tree"
        isnotlastitem = self.tree.GetNextSibling(item).IsOk()
        prev = None if isnotlastitem else self.tree.GetPrevSibling(item)
        self.activeitem = None  # prev
        self.tree.Delete(item)
        if prev:
            self.select_item(prev)

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

    def get_next_item(self):
        "return the next item in the tree if possible"
        item = self.tree.GetNextSibling(self.activeitem)
        return item if item.IsOk() else None

    def get_prev_item(self):
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
        dialog = cls(self, *args)
        with dialog.gui as dlg:
            ok = dlg.ShowModal() == wx.ID_OK
            data = dialog.confirm() if ok else None
        return ok, data

    def get_text_from_user(self, prompt, default):
        "ask for text in a popup"
        with wx.TextEntryDialog(self, prompt, self.base.app_title, default) as dlg:
            ok = dlg.ShowModal() == wx.ID_OK
            text = dlg.GetValue()  # if ok else ''
        return text, ok

    def get_choice_from_user(self, prompt, choices, default):
        "pop up a selection list"
        with wx.SingleChoiceDialog(self, prompt, self.base.app_title, choices,
                                   wx.CHOICEDLG_STYLE) as dlg:
            dlg.SetSelection(default)
            h = dlg.ShowModal()
            ok = h == wx.ID_OK
            sel = dlg.GetStringSelection()
        return sel, ok


class OptionsDialog(wx.Dialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, master, parent, title):
        self.master = master
        self.parent = parent
        super().__init__(parent, title)
        # pnl = self  # wx.Panel(self, -1)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        self.gsizer = wx.FlexGridSizer(cols=2)
        self.vsizer.Add(self.gsizer, 0,
                        wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(True)
        self.vsizer.Fit(self)
        self.vsizer.SetSizeHints(self)
        self.Layout()

    def add_checkbox_line_to_grid(self, row, labeltext, value):
        # FlexGridsizer heeft row / col niet nodig
        self.gsizer.Add(wx.StaticText(self, label=labeltext), 1, wx.ALL, 5)
        chk = wx.CheckBox(self)
        chk.SetValue(value)
        self.gsizer.Add(chk, 1, wx.ALL, 5)

    def add_buttonbox(self, okvalue, cancelvalue):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, id=wx.ID_OK, label=okvalue)
        hsizer.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        # self.SetAffirmativeId(wx.ID_APPLY)
        btn = wx.Button(self, id=wx.ID_CLOSE, label=cancelvalue)
        hsizer.Add(btn, 0, wx.EXPAND | wx.ALL, 2)
        self.SetEscapeId(wx.ID_CLOSE)
        # sizer1 = self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        self.vsizer.Add(hsizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

    def get_checkbox_value(self, check):
        "dialoog afsluiten"
        return check.GetValue()


class CheckDialog(wx.Dialog):
    """Generieke dialoog om iets te melden en te vragen of deze melding in het vervolg
    nog getoond moet worden

    Eventueel ook te implementeren m.b.v. wx.RichMessageDialog
    """
    def __init__(self, master, parent, title):
        self.master = master
        self.parent = parent
        wx.Dialog.__init__(self, parent, title=title, size=(-1, 120))
        self.SetIcon(wx.Icon(parent.nt_icon))
        # pnl = wx.Panel(self)
        self.vsizer = wx.BoxSizer(wx.VERTICAL)
        # pnl.SetSizer(self.vsizer)
        # pnl.SetAutoLayout(True)
        # self.vsizer.Fit(pnl)
        # self.vsizer.SetSizeHints(pnl)
        # pnl.Layout()
        self.SetSizer(self.vsizer)
        self.SetAutoLayout(True)
        self.vsizer.Fit(self)
        self.vsizer.SetSizeHints(self)
        self.Layout()

    def add_label(self, labeltext):
        self.vsizer.Add(wx.StaticText(self, label=labeltext), 1, wx.ALL, 5)

    def add_checkbox(self, caption):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        check = wx.CheckBox(self, label=caption)
        hsizer.Add(check, 0, wx.EXPAND)
        self.vsizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        return check

    def add_ok_buttonbox(self):
        self.vsizer.Add(self.CreateButtonSizer(wx.OK), 0, wx.ALIGN_CENTER_HORIZONTAL)

    def get_checkbox_value(self, check):
        "dialoog afsluiten"
        return check.GetValue()


class KeywordsDialog(wx.Dialog):
    """Dialoog voor het koppelen van trefwoorden
    """
    def __init__(self, master, parent, title):
        self.master = master
        self.parent = parent
        super().__init__(parent)
        self.SetTitle(title)
        self.SetIcon(self.parent.nt_icon)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.vbox.Add(self.hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)
        self.Layout()
        self.SetSize(400, 264)

    def add_list(self, title, items, callback, first=False, last=False):
        if first:
            self.hbox.AddStretchSpacer()
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticText(self, label=title))
        lst = wx.ListBox(self, size=(120, 156), style=wx.LB_EXTENDED)
        lst.Bind(wx.EVT_LISTBOX_DCLICK, callback)
        lst.Append(items)
        # lst.InsertItems(items, 0)
        vbox.Add(lst)
        self.hbox.Add(vbox)
        if last:
            self.hbox.AddStretchSpacer()
        return lst

    def add_buttons(self, buttondefs):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddStretchSpacer()
        buttons = []
        for text, callback in buttondefs:
            if callback is None:
                vbox.Add(wx.StaticText(self, label=text))
            else:
                button = wx.Button(self, label=text)
                button.Bind(wx.EVT_BUTTON, callback)
                vbox.Add(button)
                buttons.append(button)
        vbox.AddStretchSpacer()
        self.hbox.Add(vbox)
        return buttons

    def create_buttonbox(self):
        self.vbox.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL), 0,
                      wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)

    def create_actions(self, actionlist):
        """define what can be done in this screen
        """
        accel_list = []
        for name, shortcut, callback in actionlist:
            act = wx.MenuItem(text=name)
            # act.Bind(wx.EVT_MENU, callback)
            self.Bind(wx.EVT_MENU, callback, act)
            accel = wx.AcceleratorEntry(cmd=act.GetId())
            ok = accel.FromString(shortcut)
            if ok:
                accel_list.append(accel)
        accel_table = wx.AcceleratorTable(accel_list)
        self.SetAcceleratorTable(accel_table)

    def activate(self, win):
        """set focus to list
        """
        item = win.GetSelections()  # currentItem()
        if not item:
            item = [0]  # win.item(0)
        # try:
        win.SetSelection(item[0])  # ed(True)
        # except wx._core.wxAssertionError:
        #     if win == self.fromlist:
        #         self.activate_right()
        #     else:
        #         self.activate_left()
        #     return
        win.SetFocus()

    def moveitem(self, fromlist, tolist):
        """trefwoord verplaatsen van de ene lijst naar de andere
        """
        selected = fromlist.GetSelections()  # selectedItems()
        if selected:
            selection = [fromlist.GetString(i) for i in selected]
            for indx in reversed(selected):
                fromlist.Delete(indx)
                tolist.Insert(selection, tolist.GetCount())

    def ask_for_tag(self, caption, message):
        with wx.TextEntryDialog(self, message, caption) as dlg:
            ok = dlg.ShowModal() == wx.ID_OK
            text = dlg.GetValue() if ok else ''
        return text, ok

    def add_tag_to_list(self, text, listwidget):
        listwidget.Append(text)

    def get_listvalues(self, listwidget):    # def accept(self):
        """geef de geselecteerde trefwoorden aan het hoofdprogramma
        """
        return listwidget.GetItems()


class KeywordsManager(wx.Dialog):
    """Dialoog voor het wijzigen van trefwoorden
    """
    def __init__(self, master, parent, title, donetext):
        self.master = master
        self.parent = parent
        super().__init__(parent, title=title)
        self.SetIcon(self.parent.nt_icon)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.gbox = wx.GridBagSizer()
        vbox.Add(self.gbox, 1, wx.ALL, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        button = wx.Button(self, label=donetext)
        self.SetAffirmativeId(button.GetId())
        hbox.Add(button)
        vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 10)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        vbox.Fit(self)
        vbox.SetSizeHints(self)
        self.Layout()
        self.SetSize(408, 200)

    def add_label(self, text, row, col):
        if col == -1:
            self.gbox.Add(wx.StaticText(self, label=text), (row, 0), (1, 3), wx.ALL, 5)
            # self.gbox.Add(wx.StaticText(self, label=text), (row, 0), (1, 3), wx.HORIZONTAL, 5)
        else:
            self.gbox.Add(wx.StaticText(self, label=text), (row, col),
                          flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border=5)

    def add_combobox(self, row, col):
        combo = wx.ComboBox(self)
        self.gbox.Add(combo, (row, col), flag=wx.ALL, border=5)
        # self.gbox.Add(combo, (row, col), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        return combo

    def add_lineinput(self, row, col):
        editor = wx.TextCtrl(self, size=(180, -1))
        # self.gbox.Add(editor, (row, col), flag=wx.ALL, border=5)
        self.gbox.Add(editor, (row, col), flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        return editor

    def add_button(self, text, callback, row, col):
        button = wx.Button(self, label=text)
        button.Bind(wx.EVT_BUTTON, callback)
        self.gbox.Add(button, (row, col), flag=wx.ALL, border=5)

    def reset_combobox(self, widget, items):
        """initialize items on screen
        """
        widget.Clear()
        widget.AppendItems(items)
        widget.SetValue('')

    def reset_lineinput(self, widget):
        """initialize items on screen
        """
        widget.Clear()

    def get_combobox_value(self, widget):
        return widget.GetValue()

    def ask_question(self, title, text):
        ask = wx.MessageBox(text, title, wx.YES_NO | wx.ICON_QUESTION, self)
        return ask == wx.YES

    def get_lineinput_text(self, widget):
        return widget.GetValue()

    def ask_question_w_cancel(self, text, extratext):
        with wx.MessageDialog(self, text, style=wx.YES_NO | wx.CANCEL) as prompter:
            prompter.SetExtendedMessage(extratext)
            ask = prompter.ShowModal()
        return ask == wx.ID_YES, ask == wx.ID_CANCEL


class GetTextDialog(wx.Dialog):
    """Dialog to get search string (with options)
    """
    def __init__(self, master, parent, title):
        self.master = master
        self.parent = parent
        super().__init__(parent)
        self.SetTitle(title)
        self.SetIcon(parent.nt_icon)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)
        self.Layout()

    def add_label(self, labeltext):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label=labeltext), 0, wx.ALL, 5)
        self.vbox.Add(hbox, 0, wx.ALL, 5)

    def add_lineinput(self, seltext):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        inputwin = wx.TextCtrl(self, value=seltext)
        hbox.Add(inputwin, 1, wx.ALL, 5)
        self.vbox.Add(hbox, 1, wx.ALL, 5)
        return inputwin

    def add_checkbox_line(self, checkdefs):
        result = []
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        for text, value in checkdefs:
            check = wx.CheckBox(self, label=text)
            check.SetValue(value)
            hbox.Add(check, 0, wx.ALL, 5)
            result.append(check)
        self.vbox.Add(hbox, 0, wx.ALL, 5)
        return result

    def add_okcancel_buttonbox(self):
        self.vbox.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL), 0,
                      wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)

    def get_checkbox_value(self, widget):
        return widget.GetValue()

    def get_lineinput_value(self, widget):
        return widget.GetValue()


class GetItemDialog(wx.Dialog):
    """Dialog to select a keyword from a list
    """
    def __init__(self, master, parent, title):
        self.master = master
        self.parent = parent
        super().__init__(parent)
        self.SetTitle(title)
        self.SetIcon(parent.nt_icon)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)
        self.SetAutoLayout(True)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)
        self.Layout()

    def add_label(self, labeltext):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self, label=labeltext), 0, wx.ALL, 5)
        self.vbox.Add(hbox, 0, wx.ALL, 5)

    def add_combobox(self, selection_list, selvalue):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        inputwin = wx.ComboBox(self, choices=selection_list)
        inputwin.SetSelection(selvalue)
        hbox.Add(inputwin, 1, wx.ALL, 5)
        self.vbox.Add(hbox, 1, wx.ALL, 5)
        return inputwin

    def add_checkbox(self, text, value):
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        check = wx.CheckBox(self, label=text)
        check.SetValue(value)
        hbox.Add(check, 0, wx.ALL, 5)
        self.vbox.Add(hbox, 0, wx.ALL, 5)
        return check

    def add_okcancel_buttonbox(self):
        self.vbox.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL), 0,
                      wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)

    def get_checkbox_value(self, widget):
        return widget.GetValue()

    def get_combobox_value(self, widget):
        return widget.GetValue()


class GridDialog(wx.Dialog):
    """dialog showing texts in a grid layout
    """
    def __init__(self, parent, title, donetext):
        super().__init__(parent, title=title, size=(-1, 320))
        # pnl = wx.Panel(self)
        sizer0 = wx.BoxSizer(wx.VERTICAL)
        self.gbox = wx.FlexGridSizer(cols=2, vgap=2, hgap=25)
        sizer0.Add(self.gbox, 0, wx.GROW | wx.ALL, 5)
        done_button = wx.Button(self, label=donetext)
        self.SetAffirmativeId(done_button.GetId())
        sizer0.Add(done_button, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
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

    def add_label(self, row, col, text):
        # row / col niet nodig bij FlexGridSizer
        self.gbox.Add(wx.StaticText(self, label=text))

    def send(self):
        with self as dlg:
            dlg.ShowModal()


class TaskbarIcon(wx.adv.TaskBarIcon):
    "icon in the taskbar"
    id_revive = wx.NewIdRef()

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
