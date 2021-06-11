""" unittests voor wx_gui.py
"""
import os
import pytest
import gettext
import types
import notetree.wx_gui as gui
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gettext.install("NoteTree", os.path.join(HERE, 'locale'))


def setup_mainwindow(monkeypatch):
    monkeypatch.setattr(gui.wx, 'Frame', MockFrame)
    monkeypatch.setattr(gui.wx, 'App', MockApp)
    return gui.MainWindow(MockNoteTree())


#--- redefine gui elements to facilitatie testing ---
class MockApp:
    def __init__(self, *args):
        print('called app.__init__()')
    def MainLoop(self, *args):
        print('called app.MainLoop()')
    def SetTopWindow(self, *args):
        print('called app.SetTopWindow()')


class MockNoteTree:
    def __init__(self):
        print('called MockNoteTree.__init__()')
        self.root_title = 'title'
        self.opts = {}
    def get_menudata(self):
        pass
    def callback(self):
        pass
    def check_active(self, *args):
        print('called base.check_active()')
    def activate_item(self, *args):
        print('called base.activate_item() with arg `{}`'.format(args[0]))
    def update(self):
        print('called base.update()')


class MockFrame:
    def __init__(self, *args, **kwargs):
        print('called frame.__init__()')
    def Show(self, *args):
        print('called frame.Show()')
    def Hide(self, *args):
        print('called frame.Hide()')
    def GetSize(self):
        return wx.Size(1, 2)


class MockSize:
    def __init__(self, *args):
        self.w = args[0]
        self.h = args[1]
    def GetWidth(self):
        return self.w
    def GetHeight(self):
        return self.h


class MockIcon:
    def __init__(self, *args):
        print('called Icon.__init__()')


class MockMenuBar:
    def __init__(self, *args):
        print('called MenuBar.__init__()')
    def GetMenus(self, *args):
        print('called menubar.GetMenus()')
        return [(MockMenu(), 'label1'),( MockMenu(), 'label2')]
    def Append(self, *args):
        print('called menubar.Append()')
    def Replace(self, *args):
        print('called menubar.Replace()')


class MockMenu:
    def __init__(self, *args):
        print('called Menu.__init__()')
    def Append(self, *args):
        print('called menu.Append()')
    def Destroy(self, *args):
        print('called menu.Destroy()')


class MockMenuItem:
    def __init__(self, *args, **kwargs):
        print('called MenuItem.__init__()')
    def GetId(self, *args):
        print('called menuitem.GetId()')
    def Bind(self, *args):
        print('called menuitem.Bind()')
    def Check(self, *args):
        print('called menuitem.Check(`{}`)'.format(args[0]))


class MockSplitter:
    def __init__(self, *args):
        print('called MockSplitter.__init__()')
    def SetMinimumPaneSize(self, *args):
        print('called splitter.SetMinimumPaneSize()')
    def SplitVertically(self, *args):
        print('called splitter.SplitVertically()')
    def SetSashPosition(self, *args):
        print('called splitter.SetSashPosition()')
    def GetSashPosition(self, *args):
        return 55


class MockTree:
    def __init__(self, *args):
        print('called MockTree.__init__()')
    def AddRoot(self, *args):
        print('called tree.AddRoot()')
    def DeleteAllItems(self, *args):
        print('called tree.DeleteAllItems()')
    def Bind(self, *args):
        print('called tree.Bind() for method {}'.format(str(args[1]).split()[2]))
    def SetAcceleratorTable(self, *args):
        print('called tree.SetAcceleratorTable()')
    def Expand(self, *args):
        print('called tree.Expand()')
    def SetItemBold(self, *args):
        print('called tree.SetItemBold() using {}'.format(args[1]))
    def SetFocus(self):
        print('called tree.SetFocus()')
    def SelectItem(self, *args):
        print('called tree.SelectItem()')
    def GetSelection(self, *args):
        return 'selected_item'  # print('called tree.GetSelection()')
    def GetItemText(self, *args):
        return 'itemtext'  # print('called tree.GetItemText()')
    def SetItemText(self, *args):
        print('called tree.SetItemText()')
    def GetItemData(self, *args):
        return 'itemkey', 'itemtext', ['keyword']  # print('called tree.GetItemData()')
    def SetItemData(self, *args):
        print('called tree.SetItemData() with args `{}`'.format(args[1]))
    def GetNextSibling(self, *args):
        print('called tree.GetNextSibling()')
        return MockTreeItem('next treeitem')
    def GetPrevSibling(self, *args):
        print('called tree.GetPrevSibling()')
        return MockTreeItem('previous treeitem')
    def AppendItem(self, *args):
        print('called tree.AppendItem()')
    def PrependItem(self, *args):
        print('called tree.PrependItem()')
    def Delete(self, *args):
        print('called tree.Delete()')
    def GetFirstChild(self, *args):
        print('called tree.GetFirstChild()')
        return MockTreeItem('first item'), 0
    def GetNextChild(self, *args):
        cookie = args[1]
        print('called tree.GetNextChild()')
        if cookie == 0:
            return MockTreeItem('next item'), 1
        else:
            return MockTreeItem('not ok'), -1


class MockTreeItem:
    def __init__(self, *args):
        print('called MockTreeItem.__init__()')
        self.tag = args[0]
    def IsOk(self, *args):
        return not (self.tag == 'not ok')


class MockFont:
    def __init__(self):
        print('called MockFont.__init__()')
    def SetFamily(self, *args):
        print('called font.SetFamily()')
    def SetPointSize(self, *args):
        print('called font.SetPointSize()')


class MockEditor:
    def __init__(self, *args):
        print('called MockEditor.__init__()')
        self.IsModified = 'ismodified'
    def Clear(self, *args):
        print('called editor.Clear()')
    def Enable(self, *args):
        print('called editor.Enable(`{}`)'.format(args[0]))
    def Bind(self, *args):
        print('called editor.Bind() for method {}'.format(str(args[1]).split()[2]))
    def SetWrapMode(self, *args):
        print('called editor.SetWrapMode()')
    def SetCaretLineVisible(self, *args):
        print('called editor.SetCaretLineVisible()')
    def SetCaretLineBackground(self, *args):
        print('called editor.SetCaretLineBackground()')
    def SetLexer(self, *args):
        print('called editor.SetLexer()')
    def StyleSetForeground(self, *args):
        print('called editor.StyleSetForeground() for style {}'.format(args[0]))
    def StyleSetBackground(self, *args):
        print('called editor.StyleSetBackground() for style {}'.format(args[0]))
    def StyleSetBold(self, *args):
        print('called editor.StyleSetBold() for style {}'.format(args[0]))
    def StyleSetItalic(self, *args):
        print('called editor.StyleSetItalic() for style {}'.format(args[0]))
    def StyleSetUnderline(self, *args):
        print('called editor.StyleSetUnderline() for style {}'.format(args[0]))
    def SetValue(self, value):
        print('setting editor text to `{}`'.format(value))
    def GetValue(self):
        return 'fake editor value'
    def SetFocus(self):
        print('called editor.SetFocus()')


class MockTrayIcon:
    def __init__(self, *args):
        print('called TrayIcon.__init__()')
    def SetIcon(self, *args):
        print('called trayicon.SetIcon()')
    def Bind(self, *args, **kwargs):
        print('called trayicon.Bind()')
    def Destroy(self, *args):
        print('called trayicon.Destroy()')


class MockAcceleratorEntry:
    def __init__(self, *args, **kwargs):
        print('called AcceleratorEntry.__init__()')
    def FromString(self, *args):
        print('called MockAcceleratorEntry.FromString()')
        return True


class MockAcceleratorTable:
    def __init__(self, *args):
        print('called AcceleratorTable.__init__()')


class MockEvent:
    def __init__(self):
        print('called event.__init__()')
    def GetItem(self):
        return 'treeitem'
    def Skip(self):
        print('called event.Skip()')


class MockStatusBar:
    def SetStatusText(self, *args):
        print('called statusbar.SetStatusText(`{}`)'.format(args[0]))


class MockDialog(gui.wx.Dialog):
    def __init__(self, parent, *args, **kwargs):
        print('called MockDialog.__init__() with args `{}`'.format(args))
    def ShowModal(self):
        return gui.wx.ID_OK
    def confirm(self):
        return 'confirmation data'
    def Destroy(self):
        print('called dialog.Destroy()')


class MockTextDialog(gui.wx.Dialog):
    def __init__(self, parent, *args, **kwargs):
        print('called MockTextDialog.__init__() with args `{}`'.format(args))
    def ShowModal(self):
        return gui.wx.ID_OK
    def GetValue(self):
        return 'entered value'
    def Destroy(self):
        print('called dialog.Destroy()')


class MockChoiceDialog(gui.wx.Dialog):
    def __init__(self, parent, *args):
        print('called MockChoiceDialog.__init__ with args `{}`'.format(args[:-1]))
    def ShowModal(self):
        return gui.wx.ID_OK
    def SetSelection(self, value):
        print('called dialog.SetSelection(`{}`)'.format(value))
    def GetStringSelection(self):
        return 'selected value'
    def Destroy(self):
        print('called dialog.Destroy()')


class MockBoxSizer:
    def __init__(self, *args, **kwargs):
        self.orient = ('vert' if args[0] == gui.wx.VERTICAL else
                       'hori' if args[0] == gui.wx.HORIZONTAL else '')
        print('called BoxSizer.__init__(`{}`)'.format(self.orient))
    def Add(self, *args):
        print('called {} sizer.Add()'.format(self.orient))
    def AddSpacer(self, *args):
        print('called {} sizer.AddSpacer()'.format(self.orient))
    def AddStretchSpacer(self, *args):
        print('called {} sizer.AddStretchSpacer()'.format(self.orient))
    def Fit(self, *args):
        print('called {} sizer.Fit()'.format(self.orient))
    def SetSizeHints(self, *args):
        print('called {} sizer.SetSizeHints()'.format(self.orient))


class MockGridSizer:
    def __init__(self, *args, **kwargs):
        print('called GridSizer.__init__()')
    def Add(self, *args):
        print('called gridsizer.Add()')


class MockStaticText:
    def __init__(self, *args, **kwargs):
        print('called StaticText.__init__()')


class MockCheckBox:
    def __init__(self, *args, **kwargs):
        print('called CheckBox.__init__()')
    def SetValue(self, *args):
        print('called checkbox.SetValue(`{}`)'.format(args[0]))
    def GetValue(self, *args):
        return 'value from checkbox'


class MockTextCtrl:
    def __init__(self, *args, **kwargs):
        value = kwargs.get('value', '')
        if value:
            value = '`{}`'.format(value)
        print('called TextCtrl.__init__({})'.format(value))
    def Clear(self, *args):
        print('called text.clear()')
    def SetValue(self, *args):
        print('called text.SetValue(`{}`)'.format(args[0]))
    def GetValue(self, *args):
        return 'value from textctrl'


class MockButton:
    def __init__(self, *args, **kwargs):
        print('called Button.__init__()')
    def Bind(self, *args, **kwargs):
        print('called Button.Bind()')
    def GetId(self, *args, **kwargs):
        print('called Button.GetId()')


class MockComboBox:
    def __init__(self, *args, **kwargs):
        sellist = kwargs.get('choices', '')
        if sellist:
            sellist = ' with arg `{}`'.format(sellist)
        print('called ComboBox.__init__(){}'.format(sellist))
    def Clear(self, *args):
        print('called combobox.clear()')
    def AppendItems(self, *args):
        print('called combobox.appenditems() with arg `{}`'.format(args[0]))
    def SetSelection(self, *args):
        print('called combobox.SetSelection(`{}`)'.format(args[0]))
    def SetValue(self, *args):
        print('called combobox.SetValue(`{}`)'.format(args[0]))
    def GetValue(self, *args):
        return 'value from combobox'


class MockListBox:
    def __init__(self, *args, **kwargs):
        # sellist = kwargs.get('choices', '')
        # if sellist:
        #     sellist = ' with arg `{}`'.format(sellist)
        # print('called ListBox.__init__(){}'.format(sellist))
        print('called ListBox.__init__()')
    def Bind(self, *args):
        print('called listbox.bind()')
    def SetFocus(self, *args):
        print('called listbox.SetFocus()')
    def Append(self, *args):
        print('called listbox.append() with arg `{}`'.format(args[0]))
    def SetSelection(self, *args):
        print('called listbox.SetSelection(`{}`)'.format(args[0]))
    def GetSelections(self, *args):
        return [1]
    def GetString(self, *args):
        return 'value {} from listbox'.format(args[0])
    def GetItems(self, *args):
        return ['items from listbox']
    def Delete(self, *args):
        print('delete item {} from listbox'.format(args[0]))
    def Insert(self, *args):
        print('insert `{}` into listbox'.format(args[0]))
    def GetCount(self):
        print('called listbox.GetCount()')


class MockMessageDialog(gui.wx.Dialog):
    def __init__(self, *args, **kwargs):
        print('called MessageDialog.__init__()')
    def SetExtendedMessage(self, *args):
        print('called dialog.SetExtendedMessage()')
    def ShowModal(self):
        print('called dialog.ShowModal()')
    def Destroy(self):
        print('called dialog.Destroy()')


#--- and now for the actual testing stuff ---
class TestMainWindow:
    def test_init(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        assert hasattr(testobj, 'base')
        assert hasattr(testobj, 'app')
        assert testobj.activeitem == None
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n')

    def test_start(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.start()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called app.MainLoop()\n')

    def test_init_screen(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called frame.__init__()')
        def mock_seticon(self, *args):
            print('called frame.SetIcon')
        def mock_setmenubar(self, *args):
            print('called frame.SetMenuBar()')
        monkeypatch.setattr(gui.wx.Frame, '__init__', mock_init)
        monkeypatch.setattr(gui.wx, 'Icon', MockIcon)
        monkeypatch.setattr(gui.wx.Frame, 'SetIcon', mock_seticon)
        monkeypatch.setattr(gui.wx, 'MenuBar', MockMenuBar)
        monkeypatch.setattr(gui.wx.Frame, 'SetMenuBar', mock_setmenubar)
        testobj = setup_mainwindow(monkeypatch)
        testobj.init_screen()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called frame.__init__()\n'
                                           'called MenuBar.__init__()\n'
                                           'called frame.SetMenuBar()\n')
        testobj = setup_mainwindow(monkeypatch)
        testobj.init_screen(parent=None, title='', iconame='x')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called frame.__init__()\n'
                                           'called Icon.__init__()\n'
                                           'called frame.SetIcon\n'
                                           'called MenuBar.__init__()\n'
                                           'called frame.SetMenuBar()\n')

    def test_setup_statusbar(self, monkeypatch, capsys):
        def mock_createstatusbar(self, *args):
            print('called frame.CreateStatusBar()')
            return 'x'
        monkeypatch.setattr(gui.wx.Frame, 'CreateStatusBar', mock_createstatusbar)
        testobj = setup_mainwindow(monkeypatch)
        testobj.setup_statusbar()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called frame.CreateStatusBar()\n')
        assert hasattr(testobj, 'sb')

    def test_setup_trayicon(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.setup_trayicon()  # eigenlijk overbodg want deze doet niks

    def test_setup_split_screen(self, monkeypatch, capsys):
        def mock_setup_tree(*args):
            print('called MainWindow.setup_tree()')
        def mock_setup_editor(*args):
            print('called MainWindow.setup_editor()')
        def mock_show(*args):
            print('called MainWindow.Show()')
        monkeypatch.setattr(gui.wx, 'SplitterWindow', MockSplitter)
        testobj = setup_mainwindow(monkeypatch)
        monkeypatch.setattr(testobj, 'setup_tree', mock_setup_tree)
        monkeypatch.setattr(testobj, 'setup_editor', mock_setup_editor)
        monkeypatch.setattr(testobj, 'Show', mock_show)
        testobj.setup_split_screen()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockSplitter.__init__()\n'
                                           'called splitter.SetMinimumPaneSize()\n'
                                           'called MainWindow.setup_tree()\n'
                                           'called MainWindow.setup_editor()\n'
                                           'called splitter.SplitVertically()\n'
                                           'called splitter.SetSashPosition()\n'
                                           'called app.SetTopWindow()\n'
                                           'called MainWindow.Show()\n')

    def test_setup_tree(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.splitter = 'splitter'
        monkeypatch.setattr(gui.wx, 'TreeCtrl', MockTree)
        tree = testobj.setup_tree()
        assert tree == testobj.tree
        assert hasattr(testobj, 'root')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.AddRoot()\n'
                                           "called tree.Bind() for method"
                                           " MainWindow.OnSelChanging\n"
                                           "called tree.Bind() for method"
                                           " MainWindow.OnSelChanged\n")

    def test_setup_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.splitter = 'splitter'
        monkeypatch.setattr(gui.stc, 'StyledTextCtrl', MockEditor)
        monkeypatch.setattr(gui.wx, 'Font', MockFont)
        editor = testobj.setup_editor()
        assert editor == testobj.editor
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockEditor.__init__()\n'
                                           'called editor.Enable(`False`)\n'
                                           'called MockFont.__init__()\n'
                                           'called font.SetFamily()\n'
                                           'called font.SetPointSize()\n'
                                           'called editor.SetWrapMode()\n'
                                           'called editor.SetCaretLineVisible()\n'
                                           'called editor.SetCaretLineBackground()\n'
                                           'called editor.SetLexer()\n'
                                           'called editor.StyleSetForeground() for style 2\n'
                                           'called editor.StyleSetBold() for style 2\n'
                                           'called editor.StyleSetForeground() for style 3\n'
                                           'called editor.StyleSetBold() for style 3\n'
                                           'called editor.StyleSetForeground() for style 4\n'
                                           'called editor.StyleSetItalic() for style 4\n'
                                           'called editor.StyleSetForeground() for style 5\n'
                                           'called editor.StyleSetItalic() for style 5\n'
                                           'called editor.StyleSetForeground() for style 6\n'
                                           'called editor.StyleSetBold() for style 6\n'
                                           'called editor.StyleSetForeground() for style 7\n'
                                           'called editor.StyleSetBold() for style 7\n'
                                           'called editor.StyleSetForeground() for style 8\n'
                                           'called editor.StyleSetBold() for style 8\n'
                                           'called editor.StyleSetForeground() for style 9\n'
                                           'called editor.StyleSetBold() for style 9\n'
                                           'called editor.StyleSetForeground() for style 10\n'
                                           'called editor.StyleSetBold() for style 10\n'
                                           'called editor.StyleSetForeground() for style 11\n'
                                           'called editor.StyleSetBold() for style 11\n'
                                           'called editor.StyleSetBackground() for style 12\n'
                                           'called editor.StyleSetForeground() for style 12\n'
                                           'called editor.StyleSetForeground() for style 13\n'
                                           'called editor.StyleSetForeground() for style 14\n'
                                           'called editor.StyleSetForeground() for style 15\n'
                                           'called editor.StyleSetBackground() for style 16\n'
                                           'called editor.StyleSetForeground() for style 16\n'
                                           'called editor.StyleSetForeground() for style 17\n'
                                           'called editor.StyleSetBold() for style 17\n'
                                           'called editor.StyleSetForeground() for style 18\n'
                                           'called editor.StyleSetUnderline() for style 11\n'
                                           'called editor.StyleSetBackground() for style 19\n'
                                           'called editor.StyleSetForeground() for style 19\n'
                                           'called editor.StyleSetBackground() for style 20\n'
                                           'called editor.StyleSetForeground() for style 20\n'
                                           'called editor.StyleSetBackground() for style 21\n'
                                           'called editor.StyleSetForeground() for style 21\n'
                                           "called editor.Bind() for method"
                                           " MainWindow.OnEvtText\n")

    def setup_text(self, monkeypatch, capsys):
        "wordt uitgevoerd als onderdeel van setup_editor, dus geen aparte test nodig"

    def test_create_menu(self, monkeypatch, capsys):
        "test for initial creation of menubar"
        def mock_getmenubar(*args):
            return MockMenuBar()
        def mock_get_menudata(*args):
            self = args[0]
            return ( ('other', (
                     (_('m_forward'), self.callback, 'forward', 'Ctrl+PgDown'),
                     (_('m_back'), self.callback, 'back', 'Ctrl+PgUp,F2'),
                     ('other', self.callback, 'other', 'Ctrl+D,Delete'), ), ),
                     (_("m_view"), (
                     (_("m_revorder"), self.callback, _("h_revorder"), 'F9'),
                     ("", None, None, None),
                     (_("m_selall"), self.callback, _("h_selall"), None),
                     (_("m_seltag"), self.callback, _("h_seltag"), None),
                     (_("m_seltxt"), self.callback, _("h_seltxt"), None), ), ), )
        def mock_set_accel(*args):
            print('called mainwindow.SetAcceleratorTable()')
        monkeypatch.setattr(MockNoteTree, 'get_menudata', mock_get_menudata)
        monkeypatch.setattr(gui.wx, 'Menu', MockMenu)
        monkeypatch.setattr(gui.wx, 'MenuItem', MockMenuItem)
        monkeypatch.setattr(gui.wx, 'AcceleratorEntry', MockAcceleratorEntry)
        monkeypatch.setattr(gui.wx, 'AcceleratorTable', MockAcceleratorTable)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.opts['RevOrder'] = True
        testobj.base.opts['Selection'] = (1, True)
        testobj.tree = MockTree()
        monkeypatch.setattr(MockMenuBar, 'GetMenus', lambda x: [])
        monkeypatch.setattr(testobj, 'GetMenuBar', mock_getmenubar)
        monkeypatch.setattr(testobj, 'SetAcceleratorTable', mock_set_accel)
        testobj.create_menu()
        assert list(testobj.selactions.keys()) == ["m_revorder", "m_selall", "m_seltag", "m_seltxt"]
        assert testobj.seltypes == ["m_selall", "m_seltag", "m_seltxt"]
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called MenuBar.__init__()\n'
                                           'called Menu.__init__()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called AcceleratorTable.__init__()\n'
                                           'called tree.SetAcceleratorTable()\n'
                                           'called menubar.Append()\n'
                                           'called Menu.__init__()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menu.Append()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called menubar.Append()\n'
                                           'called AcceleratorTable.__init__()\n'
                                           'called mainwindow.SetAcceleratorTable()\n'
                                           'called menuitem.Check(`False`)\n'
                                           'called menuitem.Check(`False`)\n'
                                           'called menuitem.Check(`False`)\n'
                                           'called menuitem.Check(`False`)\n'
                                           'called menuitem.Check(`True`)\n'
                                           'called menuitem.Check(`True`)\n')

    def test_create_menu_2(self, monkeypatch, capsys):
        "test for recreation of menubar"
        def mock_getmenubar(*args):
            return MockMenuBar()
        def mock_get_menudata(*args):
            self = args[0]
            return ( ('other', (
                     (_('m_forward'), self.callback, 'forward', 'Ctrl+PgDown'),
                     (_('m_back'), self.callback, 'back', 'Ctrl+PgUp,F2'),
                     ('other', self.callback, 'other', 'Ctrl+D,Delete'), ), ),
                     (_("m_view"), (
                     (_("m_revorder"), self.callback, _("h_revorder"), 'F9'),
                     ("", None, None, None),
                     (_("m_selall"), self.callback, _("h_selall"), None),
                     (_("m_seltag"), self.callback, _("h_seltag"), None),
                     (_("m_seltxt"), self.callback, _("h_seltxt"), None), ), ), )
        def mock_set_accel(*args):
            print('called mainwindow.SetAcceleratorTable()')
        monkeypatch.setattr(MockNoteTree, 'get_menudata', mock_get_menudata)
        monkeypatch.setattr(gui.wx, 'Menu', MockMenu)
        monkeypatch.setattr(gui.wx, 'MenuItem', MockMenuItem)
        monkeypatch.setattr(gui.wx, 'AcceleratorEntry', MockAcceleratorEntry)
        monkeypatch.setattr(gui.wx, 'AcceleratorTable', MockAcceleratorTable)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.opts['RevOrder'] = True
        testobj.base.opts['Selection'] = (1, True)
        testobj.tree = MockTree()
        monkeypatch.setattr(testobj, 'GetMenuBar', mock_getmenubar)
        monkeypatch.setattr(testobj, 'SetAcceleratorTable', mock_set_accel)
        testobj.create_menu()
        assert list(testobj.selactions.keys()) == ["m_revorder", "m_selall", "m_seltag", "m_seltxt"]
        assert testobj.seltypes == ["m_selall", "m_seltag", "m_seltxt"]
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called MenuBar.__init__()\n'
                                           'called menubar.GetMenus()\n'
                                           'called Menu.__init__()\n'
                                           'called Menu.__init__()\n'
                                           'called Menu.__init__()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called AcceleratorTable.__init__()\n'
                                           'called tree.SetAcceleratorTable()\n'
                                           'called menubar.Replace()\n'
                                           'called menu.Destroy()\n'
                                           'called Menu.__init__()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menu.Append()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menu.Append()\n'
                                           'called menubar.Replace()\n'
                                           'called menu.Destroy()\n'
                                           'called AcceleratorTable.__init__()\n'
                                           'called mainwindow.SetAcceleratorTable()\n'
                                           'called menuitem.Check(`False`)\n'
                                           'called menuitem.Check(`False`)\n'
                                           'called menuitem.Check(`False`)\n'
                                           'called menuitem.Check(`False`)\n'
                                           'called menuitem.Check(`True`)\n'
                                           'called menuitem.Check(`True`)\n')

    def test_OnEvtText(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor = MockEditor()
        testobj.OnEvtText('x')
        assert testobj.editor.IsModified == True

    def OnSelChanging(self, monkeypatch, capsys):
        "deze methode is wel gedfinieerd maar leeggelaten"

    def test_OnSelChanged(self, monkeypatch, capsys):
        def mock_check_active(*args):
            print('called notetree.check_active()')
        def mock_activate_item(*args):
            print('called notetree.activate_item(`{}`)'.format(args[0]))
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = 'root'
        testobj.OnSelChanged(MockEvent())
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called event.__init__()\n'
                                           'called base.check_active()\n'
                                           'in onselchanged: item is treeitem, root is root\n'
                                           'called base.activate_item() with arg `treeitem`\n'
                                           'called event.Skip()\n')

    def test_close(self, monkeypatch, capsys):
        def mock_close(*args):
            print('called mainwindow.Close()')
        def mock_update(*args):
            print('called notetree.update()')
        testobj = setup_mainwindow(monkeypatch)
        monkeypatch.setattr(testobj, 'Close', mock_close)
        monkeypatch.setattr(testobj.base, 'update', mock_update)
        testobj.activeitem = None
        testobj.close('event')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called mainwindow.Close()\n')
        testobj = setup_mainwindow(monkeypatch)
        monkeypatch.setattr(testobj, 'Close', mock_close)
        monkeypatch.setattr(testobj.base, 'update', mock_update)
        testobj.activeitem = 'item'
        testobj.close('event')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called notetree.update()\n'
                                           'called mainwindow.Close()\n')

    def test_clear_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor = MockEditor()
        testobj.clear_editor()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockEditor.__init__()\n'
                                           'called editor.Clear()\n'
                                           'called editor.Enable(`False`)\n')

    def test_open_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor = MockEditor()
        testobj.open_editor()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockEditor.__init__()\n'
                                           'called editor.Enable(`True`)\n')

    def test_set_screen(self, monkeypatch, capsys):
        def mock_setsize(*args):
            print('called frame.SetSize({})'.format(args[0]))
        testobj = setup_mainwindow(monkeypatch)
        monkeypatch.setattr(testobj, 'SetSize', mock_setsize)
        testobj.set_screen('screensize')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called frame.SetSize(screensize)\n')

    def test_set_splitter(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.splitter = MockSplitter()
        testobj.set_splitter('split')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockSplitter.__init__()\n'
                                           'called splitter.SetSashPosition()\n')

    def test_create_root(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        assert testobj.create_root('title') == testobj.root
        assert testobj.activeitem == testobj.root
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.DeleteAllItems()\n'
                                           'called tree.AddRoot()\n')

    def test_set_item_expanded(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        testobj.set_item_expanded('item')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.Expand()\n')

    def test_emphasize_activeitem(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        testobj.emphasize_activeitem('value')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.SetItemBold() using value\n')

    def test_editor_text_was_changed(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor = MockEditor()
        assert testobj.editor_text_was_changed() == 'ismodified'
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockEditor.__init__()\n')

    def test_copy_text_from_editor_to_activeitem(self, monkeypatch, capsys):
        def mock_set_itemtext(*args):
            print('set text of `{}` to `{}`'.format(args[0], args[1]))
        testobj = setup_mainwindow(monkeypatch)
        testobj.activeitem = 'active item'
        testobj.editor = MockEditor()
        monkeypatch.setattr(testobj, 'set_item_text', mock_set_itemtext)
        testobj.copy_text_from_editor_to_activeitem()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockEditor.__init__()\n'
                                           'set text of `active item` to `fake editor value`\n')

    def test_copy_text_from_activeitem_to_editor(self, monkeypatch, capsys):
        def mock_get_itemtext(*args):
            return 'item text'
        testobj = setup_mainwindow(monkeypatch)
        testobj.activeitem = 'active item'
        testobj.editor = MockEditor()
        monkeypatch.setattr(testobj, 'get_item_text', mock_get_itemtext)
        testobj.copy_text_from_activeitem_to_editor()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockEditor.__init__()\n'
                                           'setting editor text to `item text`\n')

    def test_select_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        testobj.select_item('item')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.SelectItem()\n')

    def test_get_selected_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        assert testobj.get_selected_item() == 'selected_item'
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           )

    def test_remove_item_from_tree(self, monkeypatch, capsys):
        "test for removing any item except last one"
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        testobj.remove_item_from_tree('item')
        assert testobj.activeitem is None
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.GetNextSibling()\n'
                                           'called MockTreeItem.__init__()\n'
                                           'called tree.Delete()\n')

    def test_remove_item_from_tree_2(self, monkeypatch, capsys):
        "test for removing last item"
        def mock_get_next(self, *args):
            print('called tree.GetNextSibling()')
            return MockTreeItem('not ok')
        testobj = setup_mainwindow(monkeypatch)
        monkeypatch.setattr(MockTree, 'GetNextSibling', mock_get_next)
        testobj.tree = MockTree()
        testobj.remove_item_from_tree('item')
        assert testobj.activeitem is None
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.GetNextSibling()\n'
                                           'called MockTreeItem.__init__()\n'
                                           'called tree.GetPrevSibling()\n'
                                           'called MockTreeItem.__init__()\n'
                                           'called tree.Delete()\n'
                                           'called tree.SelectItem()\n')

    def test_get_key_from_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        assert testobj.get_key_from_item('item') == 'itemkey'
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n')

    def test_get_activeitem_title(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        assert testobj.get_activeitem_title() == 'itemtext'
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           )

    def test_set_activeitem_title(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        testobj.set_activeitem_title('title')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.SetItemText()\n')

    def test_set_focus_to_tree(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        testobj.set_focus_to_tree()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.SetFocus()\n')

    def test_set_focus_to_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor = MockEditor()
        testobj.set_focus_to_editor()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockEditor.__init__()\n'
                                           'called editor.SetFocus()\n')

    def test_add_item_to_tree(self, monkeypatch, capsys):
        "test old-to-new order"
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.opts['RevOrder'] = False
        testobj.tree = MockTree()
        testobj.root = 'root'
        testobj.add_item_to_tree('key', 'tag', 'text', ['keywords'])
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.AppendItem()\n'
                                           'called tree.SetItemData() with args'
                                           " `('key', 'text', ['keywords'])`\n")

    def test_add_item_to_tree_2(self, monkeypatch, capsys):
        "test reversed (new-to-old) order"
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.opts['RevOrder'] = True
        testobj.tree = MockTree()
        testobj.root = 'root'
        testobj.add_item_to_tree('key', 'tag', 'text', ['keywords'])
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.PrependItem()\n'
                                           'called tree.SetItemData() with args'
                                           " `('key', 'text', ['keywords'])`\n")

    def test_get_treeitems(self, monkeypatch, capsys):
        item = MockTreeItem('activeitem')
        def mock_GetNextChild(self, *args):
            cookie = args[1]
            print('called tree.GetNextChild()')
            if cookie == 0:
                return item, 1
            else:
                return MockTreeItem('not ok'), -1
        monkeypatch.setattr(MockTree, 'GetNextChild', mock_GetNextChild)
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        testobj.root = 'root'
        testobj.activeitem = item
        # import pdb; pdb.set_trace()
        itemlist, activeitem = testobj.get_treeitems()
        assert itemlist == [('itemkey', 'itemtext', 'itemtext', ['keyword']),
                            ('itemkey', 'itemtext', 'itemtext', ['keyword'])]
        assert activeitem == 'itemkey'
        assert capsys.readouterr().out == ('called MockTreeItem.__init__()\n'
                                           'called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.GetFirstChild()\n'
                                           'called MockTreeItem.__init__()\n'
                                           'called tree.GetNextChild()\n'
                                           'called tree.GetNextChild()\n'
                                           'called MockTreeItem.__init__()\n')

    def test_get_screensize(self, monkeypatch, capsys):
        def mock_getsize(self):
            return MockSize(1, 2)
        monkeypatch.setattr(gui.wx.Frame, 'GetSize', mock_getsize)
        testobj = setup_mainwindow(monkeypatch)
        assert testobj.get_screensize() == (1, 2)

    def test_get_splitterpos(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.splitter = MockSplitter()
        assert testobj.get_splitterpos() == (55,)

    def test_sleep(self, monkeypatch, capsys):
        def mock_hide(self, *args):
            print('called frame.Hide()')
        monkeypatch.setattr(gui.MainWindow, 'Hide', mock_hide)
        monkeypatch.setattr(gui, 'TaskbarIcon', MockTrayIcon)
        testobj = setup_mainwindow(monkeypatch)
        testobj.sleep()
        assert hasattr(testobj, 'tray_icon')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called TrayIcon.__init__()\n'
                                           'called frame.Hide()\n')

    def test_revive(self, monkeypatch, capsys):
        def mock_show(self, *args):
            print('called frame.Show()')
        monkeypatch.setattr(gui.MainWindow, 'Show', mock_show)
        testobj = setup_mainwindow(monkeypatch)
        testobj.tray_icon = MockTrayIcon()
        testobj.revive()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called TrayIcon.__init__()\n'
                                           'called frame.Show()\n'
                                           'called trayicon.Destroy()\n')

    def test_get_next_item(self, monkeypatch, capsys):
        "test next item gevonden"
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        item = testobj.get_next_item()
        assert item.tag == 'next treeitem'

    def test_get_next_item_2(self, monkeypatch, capsys):
        "test next item niet gevonden"
        def mock_getnextsibling(self, *args):
            return MockTreeItem('not ok')
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        monkeypatch.setattr(testobj.tree, 'GetNextSibling', mock_getnextsibling)
        assert testobj.get_next_item() == None

    def test_get_prev_item(self, monkeypatch, capsys):
        "test previous item gevonden"
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        item = testobj.get_prev_item()
        assert item.tag == 'previous treeitem'

    def test_get_prev_item_2(self, monkeypatch, capsys):
        "test previous item niet gevonden"
        def mock_getprevsibling(self, *args):
            return MockTreeItem('not ok')
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        monkeypatch.setattr(testobj.tree, 'GetPrevSibling', mock_getprevsibling)
        assert testobj.get_prev_item() is None

    def test_get_rootitem_title(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        testobj.root = 'root'
        assert testobj.get_rootitem_title() == 'itemtext'

    def test_set_rootitem_title(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        testobj.root = 'root'
        testobj.set_rootitem_title('text')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.SetItemText()\n')

    def test_get_item_text(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        assert testobj.get_item_text('item') == 'itemtext'

    def test_set_editor_text(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor = MockEditor()
        testobj.set_editor_text('text')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockEditor.__init__()\n'
                                           'setting editor text to `text`\n')

    def test_get_editor_text(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor = MockEditor()
        assert testobj.get_editor_text() == 'fake editor value'

    def test_set_item_text(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        testobj.set_item_text('item', 'text')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.SetItemData() with args'
                                           " `('itemkey', 'text', ['keyword'])`\n")

    def test_get_item_keywords(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        testobj.get_item_keywords('item') == ['subitem']

    def test_set_item_keywords(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTree()
        testobj.set_item_keywords('item', ['data'])
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.SetItemData() with args'
                                           " `('itemkey', 'itemtext', ['data'])`\n")

    def test_show_statusbar_message(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.sb = MockStatusBar()
        testobj.show_statusbar_message('text')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called statusbar.SetStatusText(`text`)\n')

    def test_enable_selaction(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.selactions = {'actiontext': MockMenuItem()}
        testobj.enable_selaction('actiontext')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Check(`True`)\n')

    def test_disable_selaction(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.selactions = {'actiontext': MockMenuItem()}
        testobj.disable_selaction('actiontext')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Check(`False`)\n')

    def test_showmsg(self, monkeypatch, capsys):
        def mock_messagebox(*args):
            print('called wx.MessageBox() with args `{}`, `{}`, `{}`'.format(
                args[0], args[1], args[2]))
        monkeypatch.setattr(gui.wx, 'MessageBox', mock_messagebox)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.app_title = 'title'
        flags = gui.wx.OK | gui.wx.ICON_INFORMATION
        testobj.showmsg('message')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called wx.MessageBox() with args'
                                           " `message`, `title`, `{}`\n".format(flags))

    def test_ask_question(self, monkeypatch, capsys):
        def mock_messagebox(*args):
            print('called wx.MessageBox() with args `{}`, `{}`, `{}`'.format(
                args[0], args[1], args[2]))
            return gui.wx.YES
        monkeypatch.setattr(gui.wx, 'MessageBox', mock_messagebox)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.app_title = 'title'
        flags = gui.wx.YES_NO | gui.wx.ICON_QUESTION
        assert testobj.ask_question('question')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called wx.MessageBox() with args'
                                           " `question`, `title`, `{}`\n".format(flags))

    def test_show_dialog(self, monkeypatch, capsys):
        def mock_showmodal(self, *args):
            return gui.wx.ID_OK
        monkeypatch.setattr(gui.wx.Dialog, 'ShowModal', mock_showmodal)
        testobj = setup_mainwindow(monkeypatch)
        assert testobj.show_dialog (MockDialog, 'title') == (True, 'confirmation data')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           "called MockDialog.__init__() with args `('title',)`\n"
                                           'called dialog.Destroy()\n')

    def test_show_dialog_2(self, monkeypatch, capsys):
        def mock_showmodal(self, *args):
            return gui.wx.ID_CANCEL
        monkeypatch.setattr(MockDialog, 'ShowModal', mock_showmodal)
        testobj = setup_mainwindow(monkeypatch)
        assert testobj.show_dialog (MockDialog, ('title',)) == (False, None)

    def test_get_text_from_user(self, monkeypatch, capsys):
        monkeypatch.setattr(gui.wx, 'TextEntryDialog', MockTextDialog)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.app_title = 'title'
        assert testobj.get_text_from_user('prompt', 'default') == ('entered value', True)
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockTextDialog.__init__() with args'
                                           " `('prompt', 'title', 'default')`\n"
                                           'called dialog.Destroy()\n')

    def test_get_text_from_user_2(self, monkeypatch, capsys):
        def mock_showmodal(self, *args):
            return gui.wx.ID_CANCEL
        monkeypatch.setattr(gui.wx, 'TextEntryDialog', MockTextDialog)
        monkeypatch.setattr(MockTextDialog, 'ShowModal', mock_showmodal)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.app_title = 'title'
        assert testobj.get_text_from_user('prompt', 'default') == ('entered value', False)

    def test_get_choice_from_user(self, monkeypatch, capsys):
        monkeypatch.setattr(gui.wx, 'SingleChoiceDialog', MockChoiceDialog)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.app_title = 'title'
        assert testobj.get_choice_from_user('prompt', ['choices'], 'default') == (
                'selected value', True)
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called MockChoiceDialog.__init__ with args'
                                           " `('prompt', 'title', ['choices'])`\n"
                                           'called dialog.SetSelection(`default`)\n'
                                           'called dialog.Destroy()\n')

    def test_get_choice_from_user_2(self, monkeypatch, capsys):
        def mock_showmodal(self, *args):
            return gui.wx.ID_CANCEL
        monkeypatch.setattr(gui.wx, 'SingleChoiceDialog', MockChoiceDialog)
        monkeypatch.setattr(MockChoiceDialog, 'ShowModal', mock_showmodal)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.app_title = 'title'
        assert testobj.get_choice_from_user('prompt', ['choices'], 'default') == (
                'selected value', False)


class TestOptionsDialog:
    def test_init(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called wxDialog.__init__()')
        def mock_setescapeid(self, *args):
            print('called dialog.SetEscapeId()')
        def mock_setsizer(self, *args):
            print('called dialog.SetSizer()')
        def mock_setautolayout(self, *args):
            print('called dialog.SetAutoLayout()')
        def mock_layout(self, *args):
            print('called dialog.Layout()')
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'SetEscapeId', mock_setescapeid)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_layout)
        monkeypatch.setattr(gui.wx, 'BoxSizer', MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'FlexGridSizer', MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', MockStaticText)
        monkeypatch.setattr(gui.wx, 'CheckBox', MockCheckBox)
        monkeypatch.setattr(gui.wx, 'Button', MockButton)
        testobj = gui.OptionsDialog('parent', {'text': 'value'})
        assert testobj.parent == 'parent'
        assert len(testobj.controls) == 1
        assert testobj.controls[0][0] == 'text'
        assert capsys.readouterr().out == ('called wxDialog.__init__()\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called GridSizer.__init__()\n'
                                           'text value\n'
                                           'called StaticText.__init__()\n'
                                           'called gridsizer.Add()\n'
                                           'called CheckBox.__init__()\n'
                                           'called checkbox.SetValue(`value`)\n'
                                           'called gridsizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called Button.__init__()\n'
                                           'called hori sizer.Add()\n'
                                           'called Button.__init__()\n'
                                           'called hori sizer.Add()\n'
                                           'called dialog.SetEscapeId()\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.SetSizer()\n'
                                           'called dialog.SetAutoLayout()\n'
                                           'called vert sizer.Fit()\n'
                                           'called vert sizer.SetSizeHints()\n'
                                           'called dialog.Layout()\n')

    def test_confirm(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called dialog.__init__()')
            self.parent = args[0]
        monkeypatch.setattr(gui.OptionsDialog, '__init__', mock_init)
        testobj = gui.OptionsDialog(types.SimpleNamespace(dialog_data={}), {})
        testobj.controls = [('text', MockCheckBox())]
        assert testobj.confirm() == {'text': 'value from checkbox'}


class TestCheckDialog:
    def test_init(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called wxDialog.__init__()')
            self.parent = args[0]
        def mock_createbuttons(self, *args):
            print('called dialog.CreateButtonSizer()')
        def mock_setsizer(self, *args):
            print('called dialog.SetSizer()')
        def mock_setautolayout(self, *args):
            print('called dialog.SetAutoLayout()')
        def mock_layout(self, *args):
            print('called dialog.Layout()')
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'CreateButtonSizer', mock_createbuttons)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_layout)
        monkeypatch.setattr(gui.wx, 'BoxSizer', MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', MockStaticText)
        monkeypatch.setattr(gui.wx, 'CheckBox', MockCheckBox)
        monkeypatch.setattr(gui.wx, 'Button', MockButton)
        testobj = gui.CheckDialog(mockparent, {}, 'message')
        assert testobj.parent == mockparent
        assert hasattr(testobj, 'check')
        assert capsys.readouterr().out == ('called wxDialog.__init__()\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called StaticText.__init__()\n'
                                           'called vert sizer.Add()\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called CheckBox.__init__()\n'
                                           'called hori sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.CreateButtonSizer()\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.SetSizer()\n'
                                           'called dialog.SetAutoLayout()\n'
                                           'called vert sizer.Fit()\n'
                                           'called vert sizer.SetSizeHints()\n'
                                           'called dialog.Layout()\n')

    def test_confirm(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called dialog.__init__()')
            self.parent = args[0]
        monkeypatch.setattr(gui.CheckDialog, '__init__', mock_init)
        testobj = gui.CheckDialog(types.SimpleNamespace(dialog_data='x'), {}, '')
        testobj.check = MockCheckBox()
        assert testobj.confirm() == 'value from checkbox'


class TestKeywordsDialog:
    def test_init(self, monkeypatch, capsys):
        "test calling with no keywords associated yet"
        def mock_init(self, *args):
            print('called wxDialog.__init__()')
        def mock_SetTitle(self, *args):
            print('called dialog.SetTitle() with args `{}`'.format(args))
        def mock_SetIcon(self, *args):
            print('called dialog.SetIcon() with args `{}`'.format(args))
        def mock_createbuttons(self, *args):
            print('called dialog.createbuttons()')
        def mock_setaffirmativeid(self, *args):
            print('called dialog.SetAffirmativeId()')
        def mock_setsizer(self, *args):
            print('called dialog.SetSizer()')
        def mock_setautolayout(self, *args):
            print('called dialog.SetAutoLayout()')
        def mock_setsize(self, *args):
            print('called dialog.SetSize()')
        def mock_Layout(self, *args):
            print('called dialog.Layout()')
        def mock_create_actions(self, *args):
            print('called dialog.create_actions()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'SetTitle', mock_SetTitle)
        monkeypatch.setattr(gui.wx.Dialog, 'SetIcon', mock_SetIcon)
        # monkeypatch.setattr(gui.wx.Dialog, 'SetAffirmativeId', mock_setaffirmativeid)
        # monkeypatch.setattr(gui.wx.Dialog, 'SetSize', mock_SetSize)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_Layout)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSize', mock_setsize)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'CreateButtonSizer', mock_createbuttons)
        monkeypatch.setattr(gui.wx, 'BoxSizer', MockBoxSizer)
        # monkeypatch.setattr(gui.wx, 'FlexGridSizer', MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', MockStaticText)
        monkeypatch.setattr(gui.wx, 'Button', MockButton)
        monkeypatch.setattr(gui.wx, 'ListBox', MockListBox)
        # monkeypatch.setattr(gui.wx, 'TextCtrl', MockTextCtrl)
        monkeypatch.setattr(gui.KeywordsDialog, 'create_actions', mock_create_actions)
        testobj = gui.KeywordsDialog(mockparent, '')
        assert hasattr(testobj, 'helptext')
        #testobj = gui.KeywordsDialog(mockparent, keywords)
        assert capsys.readouterr().out == ('called wxDialog.__init__()\n'
                                           "called dialog.SetTitle() with args "
                                           "`('title - w_tags',)`\n"
                                           "called dialog.SetIcon() with args `('icon',)`\n"
                                           'called ListBox.__init__()\n'
                                           'called listbox.bind()\n'
                                           'called StaticText.__init__()\n'
                                           'called Button.__init__()\n'
                                           'called Button.Bind()\n'
                                           'called Button.__init__()\n'
                                           'called Button.Bind()\n'
                                           'called Button.__init__()\n'
                                           'called Button.Bind()\n'
                                           'called Button.__init__()\n'
                                           'called Button.Bind()\n'
                                           'called ListBox.__init__()\n'
                                           'called listbox.bind()\n'
                                           'called dialog.create_actions()\n'
                                           'called listbox.append() with arg `x`\n'
                                           'called listbox.append() with arg `y`\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called StaticText.__init__()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called hori sizer.Add()\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called vert sizer.AddStretchSpacer()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.AddSpacer()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.AddStretchSpacer()\n'
                                           'called hori sizer.Add()\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called StaticText.__init__()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called hori sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called dialog.createbuttons()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.SetSizer()\n'
                                           'called dialog.SetAutoLayout()\n'
                                           'called vert sizer.Fit()\n'
                                           'called vert sizer.SetSizeHints()\n'
                                           'called dialog.Layout()\n'
                                           'called dialog.SetSize()\n')

    def test_init_2(self, monkeypatch, capsys):
        "test calling with keywordi(s) already associated"
        def mock_init(self, *args):
            print('called wxDialog.__init__()')
        def mock_SetTitle(self, *args):
            print('called dialog.SetTitle() with args `{}`'.format(args))
        def mock_SetIcon(self, *args):
            print('called dialog.SetIcon() with args `{}`'.format(args))
        def mock_createbuttons(self, *args):
            print('called dialog.createbuttons()')
        def mock_setaffirmativeid(self, *args):
            print('called dialog.SetAffirmativeId()')
        def mock_setsizer(self, *args):
            print('called dialog.SetSizer()')
        def mock_setautolayout(self, *args):
            print('called dialog.SetAutoLayout()')
        def mock_setsize(self, *args):
            print('called dialog.SetSize()')
        def mock_Layout(self, *args):
            print('called dialog.Layout()')
        def mock_create_actions(self, *args):
            print('called dialog.create_actions()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'SetTitle', mock_SetTitle)
        monkeypatch.setattr(gui.wx.Dialog, 'SetIcon', mock_SetIcon)
        # monkeypatch.setattr(gui.wx.Dialog, 'SetAffirmativeId', mock_setaffirmativeid)
        # monkeypatch.setattr(gui.wx.Dialog, 'SetSize', mock_SetSize)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_Layout)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSize', mock_setsize)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'CreateButtonSizer', mock_createbuttons)
        monkeypatch.setattr(gui.wx, 'BoxSizer', MockBoxSizer)
        # monkeypatch.setattr(gui.wx, 'FlexGridSizer', MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', MockStaticText)
        monkeypatch.setattr(gui.wx, 'Button', MockButton)
        monkeypatch.setattr(gui.wx, 'ListBox', MockListBox)
        # monkeypatch.setattr(gui.wx, 'TextCtrl', MockTextCtrl)
        monkeypatch.setattr(gui.KeywordsDialog, 'create_actions', mock_create_actions)
        testobj = gui.KeywordsDialog(mockparent, '', ['y'])
        assert hasattr(testobj, 'helptext')
        assert capsys.readouterr().out == ('called wxDialog.__init__()\n'
                                           "called dialog.SetTitle() with args "
                                           "`('title - w_tags',)`\n"
                                           "called dialog.SetIcon() with args `('icon',)`\n"
                                           'called ListBox.__init__()\n'
                                           'called listbox.bind()\n'
                                           'called StaticText.__init__()\n'
                                           'called Button.__init__()\n'
                                           'called Button.Bind()\n'
                                           'called Button.__init__()\n'
                                           'called Button.Bind()\n'
                                           'called Button.__init__()\n'
                                           'called Button.Bind()\n'
                                           'called Button.__init__()\n'
                                           'called Button.Bind()\n'
                                           'called ListBox.__init__()\n'
                                           'called listbox.bind()\n'
                                           'called dialog.create_actions()\n'
                                           'called listbox.append() with arg `y`\n'
                                           'called listbox.append() with arg `x`\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called StaticText.__init__()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called hori sizer.Add()\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called vert sizer.AddStretchSpacer()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.AddSpacer()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.AddStretchSpacer()\n'
                                           'called hori sizer.Add()\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called StaticText.__init__()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called hori sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called dialog.createbuttons()\n'
                                           'called vert sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.SetSizer()\n'
                                           'called dialog.SetAutoLayout()\n'
                                           'called vert sizer.Fit()\n'
                                           'called vert sizer.SetSizeHints()\n'
                                           'called dialog.Layout()\n'
                                           'called dialog.SetSize()\n')

    def test_create_actions(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
        def mock_set_accels(self, *args, **kwargs):
            print('called dialog.SetAcceleratorTable()')
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, 'SetAcceleratorTable', mock_set_accels)
        monkeypatch.setattr(gui.wx, 'MenuItem', MockMenuItem)
        monkeypatch.setattr(gui.wx, 'AcceleratorEntry', MockAcceleratorEntry)
        monkeypatch.setattr(gui.wx, 'AcceleratorTable', MockAcceleratorTable)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.create_actions()
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called MenuItem.__init__()\n'
                                           'called menuitem.Bind()\n'
                                           'called menuitem.GetId()\n'
                                           'called AcceleratorEntry.__init__()\n'
                                           'called MockAcceleratorEntry.FromString()\n'
                                           'called AcceleratorTable.__init__()\n'
                                           'called dialog.SetAcceleratorTable()\n')

    def test_activate_left(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
        def mock_activate(self, *args):
            print('called dialog._activate(`{}`)'.format(args[0]))
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, '_activate', mock_activate)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.fromlist = 'fromlist'
        testobj.activate_left('event')
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called dialog._activate(`fromlist`)\n')

    def test_activate_right(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
        def mock_activate(self, *args):
            print('called dialog._activate(`{}`)'.format(args[0]))
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, '_activate', mock_activate)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.tolist = 'tolist'
        testobj.activate_right('event')
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called dialog._activate(`tolist`)\n')

    def test_activate(self, monkeypatch, capsys):
        "test when list-to-activate can be activated"
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog('parent', '')
        testobj._activate(MockListBox())
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called ListBox.__init__()\n'
                                           'called listbox.SetSelection(`1`)\n'
                                           'called listbox.SetFocus()\n')

    def test_activate_2(self, monkeypatch, capsys):
        "test when nothing was previously selected"
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(MockListBox, 'GetSelections', lambda x: None)
        testobj = gui.KeywordsDialog('parent', '')
        testobj._activate(MockListBox())
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called ListBox.__init__()\n'
                                           'called listbox.SetSelection(`0`)\n'
                                           'called listbox.SetFocus()\n')

    def test_activate_3(self, monkeypatch, capsys):
        "test activating fromlist fails"
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
        def mock_activate_left(self, *args, **kwargs):
            print('called dialog.activate_left()')
        def mock_activate_right(self, *args, **kwargs):
            print('called dialog.activate_right()')
        def mock_setselection(self, *args):
            raise gui.wx._core.wxAssertionError
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, 'activate_left', mock_activate_left)
        monkeypatch.setattr(gui.KeywordsDialog, 'activate_right', mock_activate_right)
        monkeypatch.setattr(MockListBox, 'SetSelection', mock_setselection)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.fromlist = MockListBox()
        testobj.tolist = MockListBox()
        testobj._activate(testobj.fromlist)
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called ListBox.__init__()\n'
                                           'called ListBox.__init__()\n'
                                           'called dialog.activate_right()\n')

    def test_activate_4(self, monkeypatch, capsys):
        "test activating fromlist fails"
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
        def mock_activate_left(self, *args, **kwargs):
            print('called dialog.activate_left()')
        def mock_activate_right(self, *args, **kwargs):
            print('called dialog.activate_right()')
        def mock_setselection(self, *args):
            raise gui.wx._core.wxAssertionError
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, 'activate_left', mock_activate_left)
        monkeypatch.setattr(gui.KeywordsDialog, 'activate_right', mock_activate_right)
        monkeypatch.setattr(MockListBox, 'SetSelection', mock_setselection)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.fromlist = MockListBox()
        testobj.tolist = MockListBox()
        testobj._activate(testobj.tolist)
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called ListBox.__init__()\n'
                                           'called ListBox.__init__()\n'
                                           'called dialog.activate_left()\n')

    def test_move_right(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
        def mock_moveitem(self, *args):
            print('called dialog._moveitem(`{}`, `{}`)'.format(args[0], args[1]))
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, '_moveitem', mock_moveitem)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.fromlist = 'fromlist'
        testobj.tolist = 'tolist'
        testobj.move_right('event')
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called dialog._moveitem(`fromlist`, `tolist`)\n')

    def test_move_left(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
        def mock_moveitem(self, *args):
            print('called dialog._moveitem(`{}`, `{}`)'.format(args[0], args[1]))
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, '_moveitem', mock_moveitem)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.fromlist = 'fromlist'
        testobj.tolist = 'tolist'
        testobj.move_left('event')
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called dialog._moveitem(`tolist`, `fromlist`)\n')

    def test_moveitem(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog('parent', '')
        from_ = MockListBox()
        to = MockListBox()
        testobj._moveitem(from_, to)
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called ListBox.__init__()\n'
                                           'called ListBox.__init__()\n'
                                           'delete item 1 from listbox\n'
                                           'called listbox.GetCount()\n'
                                           "insert `['value 1 from listbox']` into listbox\n")

    def test_add_trefw(self, monkeypatch, capsys):
        "test adding new keyword"
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
            self.parent = args[0]
        def mock_textinit(self, *args, **kwargs):
            print('called MockTextDialog.__init__() with args `{}`'.format(kwargs))
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(MockTextDialog, '__init__', mock_textinit)
        monkeypatch.setattr(gui.wx, 'TextEntryDialog', MockTextDialog)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.tolist = MockListBox()
        testobj.add_trefw('event')
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called ListBox.__init__()\n'
                                           'called MockTextDialog.__init__() with args'
                                           " `{'caption': 'title', 'message': 't_newtag'}`\n"
                                           'called listbox.append() with arg `entered value`\n'
                                           'called dialog.Destroy()\n')

    def test_add_trefw_2(self, monkeypatch, capsys):
        "test canceling adding new keyword"
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
            self.parent = args[0]
        def mock_textinit(self, *args, **kwargs):
            print('called MockTextDialog.__init__() with args `{}`'.format(kwargs))
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(MockTextDialog, '__init__', mock_textinit)
        monkeypatch.setattr(MockTextDialog, 'ShowModal', lambda x: gui.wx.ID_CANCEL)
        monkeypatch.setattr(gui.wx, 'TextEntryDialog', MockTextDialog)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.tolist = MockListBox()
        testobj.add_trefw('event')
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called ListBox.__init__()\n'
                                           'called MockTextDialog.__init__() with args'
                                           " `{'caption': 'title', 'message': 't_newtag'}`\n"
                                           'called dialog.Destroy()\n')

    def test_keys_help(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
            self.parent = args[0]
            self.helptext = args[1]
        def mock_setaffirmativeid(self, *args):
            print('called dialog.SetAffirmativeId()')
        def mock_settitle(self, *args):
            print('called dialog.SetTitle()')
        def mock_setsizer(self, *args):
            print('called dialog.SetSizer()')
        def mock_setautolayout(self, *args):
            print('called dialog.SetAutoLayout()')
        def mock_showmodal(self, *args):
            print('called dialog.ShowModal()')
        def mock_layout(self, *args):
            print('called dialog.Layout()')
        monkeypatch.setattr(gui.wx.Dialog, 'SetAffirmativeId', mock_setaffirmativeid)
        monkeypatch.setattr(gui.wx.Dialog, 'SetTitle', mock_settitle)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_layout)
        monkeypatch.setattr(MockDialog, 'ShowModal', mock_showmodal)
        monkeypatch.setattr(gui.wx, 'Dialog', MockDialog)
        monkeypatch.setattr(gui.wx, 'BoxSizer', MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'FlexGridSizer', MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', MockStaticText)
        monkeypatch.setattr(gui.wx, 'Button', MockButton)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog(mockparent, (('x', 'y'), ('a', 'b')))
        testobj.keys_help('event')
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called MockDialog.__init__() with args `()`\n'
                                           'called GridSizer.__init__()\n'
                                           'called StaticText.__init__()\n'
                                           'called gridsizer.Add()\n'
                                           'called StaticText.__init__()\n'
                                           'called gridsizer.Add()\n'
                                           'called StaticText.__init__()\n'
                                           'called gridsizer.Add()\n'
                                           'called StaticText.__init__()\n'
                                           'called gridsizer.Add()\n'
                                           'called dialog.SetTitle()\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called vert sizer.Add()\n'
                                           'called Button.__init__()\n'
                                           'called Button.GetId()\n'
                                           'called dialog.SetAffirmativeId()\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.SetSizer()\n'
                                           'called dialog.SetAutoLayout()\n'
                                           'called vert sizer.Fit()\n'
                                           'called vert sizer.SetSizeHints()\n'
                                           'called dialog.Layout()\n'
                                           'called dialog.ShowModal()\n'
                                           'called dialog.Destroy()\n')

    def test_confirm(self, monkeypatch, capsys):    # def accept(self):
        def mock_init(self, *args, **kwargs):
            print('called dialog.__init__()')
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.tolist = MockListBox()
        assert testobj.confirm() == ['items from listbox']



class TestKeywordsManager:
    def test_init(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called wxDialog.__init__()')
        def mock_SetTitle(self, *args):
           print('called dialog.SetTitle() with args `{}`'.format(args))
        def mock_SetIcon(self, *args):
           print('called dialog.SetIcon() with args `{}`'.format(args))
        def mock_setaffirmativeid(self, *args):
            print('called dialog.SetAffirmativeId()')
        def mock_setsizer(self, *args):
            print('called dialog.SetSizer()')
        def mock_setautolayout(self, *args):
            print('called dialog.SetAutoLayout()')
        def mock_SetSize(self, *args):
            print('called dialog.SetSize()')
        def mock_Layout(self, *args):
            print('called dialog.Layout()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'SetTitle', mock_SetTitle)
        monkeypatch.setattr(gui.wx.Dialog, 'SetIcon', mock_SetIcon)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAffirmativeId', mock_setaffirmativeid)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSize', mock_SetSize)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_Layout)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx, 'BoxSizer', MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'FlexGridSizer', MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', MockStaticText)
        monkeypatch.setattr(gui.wx, 'Button', MockButton)
        monkeypatch.setattr(gui.wx, 'ComboBox', MockComboBox)
        monkeypatch.setattr(gui.wx, 'TextCtrl', MockTextCtrl)
        testobj = gui.KeywordsManager(mockparent)
        assert capsys.readouterr().out == ('called wxDialog.__init__()\n'
                                           "called dialog.SetTitle() with args "
                                           "`('title - t_tagman',)`\n"
                                           "called dialog.SetIcon() with args `('icon',)`\n"
                                           'called ComboBox.__init__()\n'
                                           'called TextCtrl.__init__()\n'
                                           'called combobox.clear()\n'
                                           "called combobox.appenditems() with arg `['x', 'y']`\n"
                                           'called combobox.SetValue(``)\n'
                                           'called text.clear()\n'
                                           'called Button.__init__()\n'
                                           'called Button.Bind()\n'
                                           'called Button.__init__()\n'
                                           'called Button.Bind()\n'
                                           'called Button.__init__()\n'
                                           'called Button.GetId()\n'
                                           'called dialog.SetAffirmativeId()\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called GridSizer.__init__()\n'
                                           'called StaticText.__init__()\n'
                                           'called gridsizer.Add()\n'
                                           'called gridsizer.Add()\n'
                                           'called gridsizer.Add()\n'
                                           'called StaticText.__init__()\n'
                                           'called gridsizer.Add()\n'
                                           'called gridsizer.Add()\n'
                                           'called gridsizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called StaticText.__init__()\n'
                                           'called hori sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called hori sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.SetSizer()\n'
                                           'called dialog.SetAutoLayout()\n'
                                           'called vert sizer.Fit()\n'
                                           'called vert sizer.SetSizeHints()\n'
                                           'called dialog.Layout()\n'
                                           'called dialog.SetSize()\n')

    def test_refresh_fields(self, monkeypatch, capsys):
        """niet per se nodig omdat dit integraal tijdens de init uitgevoerd wordt
        """
        def mock_init(self, *args, **kwargs):
            print('called manager.__init__()')
            self.parent = args[0]
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        testobj.newtag = MockTextCtrl()
        testobj.refresh_fields()
        assert capsys.readouterr().out == ('called manager.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called TextCtrl.__init__()\n'
                                           'called combobox.clear()\n'
                                           "called combobox.appenditems() with arg `['x', 'y']`\n"
                                           'called combobox.SetValue(``)\n'
                                           'called text.clear()\n')

    def test_update_items(self, monkeypatch, capsys):
        "test update/remove unused keyword"
        def mock_init(self, *args, **kwargs):
            print('called manager.__init__()')
            self.parent = args[0]
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        mockparent.tree = MockTree()
        mockparent.root = 'root'
        testobj.update_items('oldtext')
        assert capsys.readouterr().out == ('called manager.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.GetFirstChild()\n'
                                           'called MockTreeItem.__init__()\n'
                                           'called tree.GetNextChild()\n'
                                           'called MockTreeItem.__init__()\n'
                                           'called tree.GetNextChild()\n'
                                           'called MockTreeItem.__init__()\n')

    def test_update_items_2(self, monkeypatch, capsys):
        "test remove keyword from items"
        def mock_init(self, *args, **kwargs):
            print('called manager.__init__()')
            self.parent = args[0]
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        mockparent.tree = MockTree()
        mockparent.root = 'root'
        testobj.update_items('keyword')
        assert capsys.readouterr().out == ('called manager.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.GetFirstChild()\n'
                                           'called MockTreeItem.__init__()\n'
                                           'called tree.SetItemData() with args'
                                           " `('itemkey', 'itemtext', [])`\n"
                                           'called tree.GetNextChild()\n'
                                           'called MockTreeItem.__init__()\n'
                                           'called tree.SetItemData() with args'
                                           " `('itemkey', 'itemtext', [])`\n"
                                           'called tree.GetNextChild()\n'
                                           'called MockTreeItem.__init__()\n')

    def test_update_items_3(self, monkeypatch, capsys):
        "test update keyword in items"
        def mock_init(self, *args, **kwargs):
            print('called manager.__init__()')
            self.parent = args[0]
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        mockparent.tree = MockTree()
        mockparent.root = 'root'
        testobj.update_items('keyword', 'newtext')
        assert capsys.readouterr().out == ('called manager.__init__()\n'
                                           'called MockTree.__init__()\n'
                                           'called tree.GetFirstChild()\n'
                                           'called MockTreeItem.__init__()\n'
                                           'called tree.SetItemData() with args'
                                           " `('itemkey', 'itemtext', ['newtext'])`\n"
                                           'called tree.GetNextChild()\n'
                                           'called MockTreeItem.__init__()\n'
                                           'called tree.SetItemData() with args'
                                           " `('itemkey', 'itemtext', ['newtext'])`\n"
                                           'called tree.GetNextChild()\n'
                                           'called MockTreeItem.__init__()\n')

    def test_remove_keyword(self, monkeypatch, capsys):
        "test voor bevestigen verwijderen"
        def mock_init(self, *args, **kwargs):
            print('called manager.__init__()')
            self.parent = args[0]
        def mock_update(self, *args, **kwargs):
            print('called manager.update_items()')
        def mock_refresh(self, *args, **kwargs):
            print('called manager.refresh_fields()')
        def mock_messagebox(*args):
            print('called wx.MessageBox() with args `{}`, `{}`, `{}`'.format(
                args[0], args[1], args[2]))
            return gui.wx.YES
        monkeypatch.setattr(gui.wx, 'MessageBox', mock_messagebox)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        monkeypatch.setattr(gui.KeywordsManager, 'update_items', mock_update)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        monkeypatch.setattr(MockComboBox, 'GetValue', lambda x: 'x')
        testobj.oldtag = MockComboBox()
        testobj.remove_keyword('event')
        flags = gui.wx.YES_NO | gui.wx.ICON_QUESTION
        assert capsys.readouterr().out == ('called manager.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called wx.MessageBox() with args'
                                           " `t_remtag`, `title`, `{}`\n"
                                           'called manager.update_items()\n'
                                           'called manager.refresh_fields()\n').format(flags)

    def test_remove_keyword_2(self, monkeypatch, capsys):
        "test voor afbreken verwijderen"
        def mock_init(self, *args, **kwargs):
            print('called manager.__init__()')
            self.parent = args[0]
        def mock_update(self, *args, **kwargs):
            print('called manager.update_items()')
        def mock_refresh(self, *args, **kwargs):
            print('called manager.refresh_fields()')
        def mock_messagebox(*args):
            print('called wx.MessageBox() with args `{}`, `{}`, `{}`'.format(
                args[0], args[1], args[2]))
            return gui.wx.NO
        monkeypatch.setattr(gui.wx, 'MessageBox', mock_messagebox)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        monkeypatch.setattr(gui.KeywordsManager, 'update_items', mock_update)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        monkeypatch.setattr(MockComboBox, 'GetValue', lambda x: 'x')
        testobj.oldtag = MockComboBox()
        testobj.remove_keyword('event')
        flags = gui.wx.YES_NO | gui.wx.ICON_QUESTION
        assert capsys.readouterr().out == ('called manager.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called wx.MessageBox() with args'
                                           " `t_remtag`, `title`, `{}`\n").format(flags)

    def test_add_keyword(self, monkeypatch, capsys):
        "test adding keyword"
        def mock_init(self, *args, **kwargs):
            print('called manager.__init__()')
            self.parent = args[0]
        # def mock_update(self, *args, **kwargs):
        #    print('called manager.update_items()')
        def mock_refresh(self, *args, **kwargs):
            print('called manager.refresh_fields()')
        def mock_messagebox(*args):
            print('called wx.MessageBox() with args `{}`, `{}`, `{}`'.format(
                args[0], args[1], args[2]))
            return gui.wx.YES
        monkeypatch.setattr(gui.wx, 'MessageBox', mock_messagebox)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        monkeypatch.setattr(testobj.oldtag, 'GetValue', lambda: '')
        testobj.newtag = MockComboBox()
        monkeypatch.setattr(testobj.newtag, 'GetValue', lambda: 'z')
        testobj.add_keyword('event')
        assert testobj.parent.base.opts['Keywords'] == ['x', 'y', 'z']
        flags = gui.wx.YES_NO | gui.wx.ICON_QUESTION
        assert capsys.readouterr().out == ('called manager.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called wx.MessageBox() with args'
                                           " `t_addtag`, `title`, `{}`\n"
                                           'called manager.refresh_fields()\n').format(flags)

    def test_add_keyword_2(self, monkeypatch, capsys):
        "test canceling adding keyword"
        def mock_init(self, *args, **kwargs):
            print('called manager.__init__()')
            self.parent = args[0]
        def mock_refresh(self, *args, **kwargs):
            print('called manager.refresh_fields()')
        def mock_messagebox(*args):
            print('called wx.MessageBox() with args `{}`, `{}`, `{}`'.format(
                args[0], args[1], args[2]))
            return gui.wx.NO
        monkeypatch.setattr(gui.wx, 'MessageBox', mock_messagebox)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        monkeypatch.setattr(testobj.oldtag, 'GetValue', lambda: '')
        testobj.newtag = MockComboBox()
        monkeypatch.setattr(testobj.newtag, 'GetValue', lambda: 'z')
        testobj.add_keyword('event')
        assert testobj.parent.base.opts['Keywords'] == ['x', 'y']
        flags = gui.wx.YES_NO | gui.wx.ICON_QUESTION
        assert capsys.readouterr().out == ('called manager.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called wx.MessageBox() with args'
                                           " `t_addtag`, `title`, `{}`\n").format(flags)

    def test_add_keyword_3(self, monkeypatch, capsys):
        "test canceling replacing keyword"
        def mock_init(self, *args, **kwargs):
            print('called manager.__init__()')
            self.parent = args[0]
        def mock_showmodal(self):
            return gui.wx.ID_CANCEL
        def mock_refresh(self, *args, **kwargs):
            print('called manager.refresh_fields()')
        monkeypatch.setattr(gui.wx, 'MessageDialog', MockMessageDialog)
        monkeypatch.setattr(gui.wx.MessageDialog, 'ShowModal', mock_showmodal)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        monkeypatch.setattr(testobj.oldtag, 'GetValue', lambda: 'y')
        testobj.newtag = MockComboBox()
        monkeypatch.setattr(testobj.newtag, 'GetValue', lambda: 'z')
        testobj.add_keyword('event')
        assert testobj.parent.base.opts['Keywords'] == ['x', 'y']
        assert capsys.readouterr().out == ('called manager.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called MessageDialog.__init__()\n'
                                           'called dialog.SetExtendedMessage()\n'
                                           'called dialog.Destroy()\n'
                                           )

    def test_add_keyword_4(self, monkeypatch, capsys):
        "test replacing keyword, also in tree items"
        def mock_init(self, *args, **kwargs):
            print('called manager.__init__()')
            self.parent = args[0]
        def mock_showmodal(self):
            return gui.wx.ID_YES
        def mock_update(self, *args, **kwargs):
            print('called manager.update_items() with args `{}`'.format(args))
        def mock_refresh(self, *args, **kwargs):
            print('called manager.refresh_fields()')
        monkeypatch.setattr(gui.wx, 'MessageDialog', MockMessageDialog)
        monkeypatch.setattr(gui.wx.MessageDialog, 'ShowModal', mock_showmodal)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'update_items', mock_update)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        monkeypatch.setattr(testobj.oldtag, 'GetValue', lambda: 'y')
        testobj.newtag = MockComboBox()
        monkeypatch.setattr(testobj.newtag, 'GetValue', lambda: 'z')
        testobj.add_keyword('event')
        assert testobj.parent.base.opts['Keywords'] == ['x', 'z']
        assert capsys.readouterr().out == ('called manager.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called MessageDialog.__init__()\n'
                                           'called dialog.SetExtendedMessage()\n'
                                           'called dialog.Destroy()\n'
                                           "called manager.update_items() with args `('y', 'z')`\n"
                                           'called manager.refresh_fields()\n')

    def test_add_keyword_5(self, monkeypatch, capsys):
        "test replacing keyword, deleting from tree items"
        def mock_init(self, *args, **kwargs):
            print('called manager.__init__()')
            self.parent = args[0]
        def mock_showmodal(self):
            return gui.wx.ID_NO
        def mock_update(self, *args, **kwargs):
            print('called manager.update_items() with args `{}`'.format(args))
        def mock_refresh(self, *args, **kwargs):
            print('called manager.refresh_fields()')
        monkeypatch.setattr(gui.wx, 'MessageDialog', MockMessageDialog)
        monkeypatch.setattr(gui.wx.MessageDialog, 'ShowModal', mock_showmodal)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'update_items', mock_update)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        monkeypatch.setattr(testobj.oldtag, 'GetValue', lambda: 'y')
        testobj.newtag = MockComboBox()
        monkeypatch.setattr(testobj.newtag, 'GetValue', lambda: 'z')
        testobj.add_keyword('event')
        assert testobj.parent.base.opts['Keywords'] == ['x', 'z']
        assert capsys.readouterr().out == ('called manager.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called ComboBox.__init__()\n'
                                           'called MessageDialog.__init__()\n'
                                           'called dialog.SetExtendedMessage()\n'
                                           'called dialog.Destroy()\n'
                                           "called manager.update_items() with args `('y',)`\n"
                                           'called manager.refresh_fields()\n')

    def confirm(self, monkeypatch, capsys):
        "not implemented, so no test needed"


class TestGetTextDialog:
    def test_init(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called wxDialog.__init__()')
        def mock_createbuttons(self, *args):
            print('called dialog.CreateButtonSizer()')
        def mock_settitle(self, *args):
            print('called dialog.SetTitle()')
        def mock_seticon(self, *args):
            print('called dialog.SetIcon()')
        def mock_setsizer(self, *args):
            print('called dialog.SetSizer()')
        def mock_setautolayout(self, *args):
            print('called dialog.SetAutoLayout()')
        def mock_layout(self, *args):
            print('called dialog.Layout()')
        def mock_inputwin(self, *args):
            print('called dialog.create_inputwin()')
            self.inputwin = MockTextCtrl()
            self.use_case = MockCheckBox()
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'SetTitle', mock_settitle)
        monkeypatch.setattr(gui.wx.Dialog, 'SetIcon', mock_seticon)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'CreateButtonSizer', mock_createbuttons)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_layout)
        monkeypatch.setattr(gui.wx, 'BoxSizer', MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'FlexGridSizer', MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', MockStaticText)
        monkeypatch.setattr(gui.wx, 'CheckBox', MockCheckBox)
        monkeypatch.setattr(gui.wx, 'TextCtrl', MockTextCtrl)
        monkeypatch.setattr(gui.wx, 'Icon', MockIcon)
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.GetTextDialog, 'create_inputwin', mock_inputwin)
        testobj = gui.GetTextDialog(mockparent, 0, 'seltext', 'labeltext', True)
        assert testobj.parent == mockparent
        assert hasattr(testobj, 'in_exclude')
        assert hasattr(testobj, 'inputwin')
        assert hasattr(testobj, 'use_case')
        assert capsys.readouterr().out == ('called wxDialog.__init__()\n'
                                           'called dialog.SetTitle()\n'
                                           'called dialog.SetIcon()\n'
                                           'called dialog.create_inputwin()\n'
                                           'called TextCtrl.__init__()\n'
                                           'called CheckBox.__init__()\n'
        #                                  'called checkbox.SetValue(`False`)\n'
                                           'called CheckBox.__init__()\n'
                                           'called checkbox.SetValue(`False`)\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called StaticText.__init__()\n'
                                           'called hori sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called hori sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called hori sizer.Add()\n'
                                           'called hori sizer.Add()\n'
                                           'called checkbox.SetValue(`True`)\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.CreateButtonSizer()\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.SetSizer()\n'
                                           'called dialog.SetAutoLayout()\n'
                                           'called vert sizer.Fit()\n'
                                           'called vert sizer.SetSizeHints()\n'
                                           'called dialog.Layout()\n')

    def test_init_2(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called wxDialog.__init__()')
        def mock_createbuttons(self, *args):
            print('called dialog.CreateButtonSizer()')
        def mock_settitle(self, *args):
            print('called dialog.SetTitle()')
        def mock_seticon(self, *args):
            print('called dialog.SetIcon()')
        def mock_setsizer(self, *args):
            print('called dialog.SetSizer()')
        def mock_setautolayout(self, *args):
            print('called dialog.SetAutoLayout()')
        def mock_layout(self, *args):
            print('called dialog.Layout()')
        def mock_inputwin(self, *args):
            print('called dialog.create_inputwin()')
            self.inputwin = MockTextCtrl()
            self.use_case = MockCheckBox()
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'SetTitle', mock_settitle)
        monkeypatch.setattr(gui.wx.Dialog, 'SetIcon', mock_seticon)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'CreateButtonSizer', mock_createbuttons)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_layout)
        monkeypatch.setattr(gui.wx, 'BoxSizer', MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'FlexGridSizer', MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', MockStaticText)
        monkeypatch.setattr(gui.wx, 'CheckBox', MockCheckBox)
        monkeypatch.setattr(gui.wx, 'TextCtrl', MockTextCtrl)
        monkeypatch.setattr(gui.wx, 'Icon', MockIcon)
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.GetTextDialog, 'create_inputwin', mock_inputwin)
        testobj = gui.GetTextDialog(mockparent, -1, 'seltext', 'labeltext', False)
        assert testobj.parent == mockparent
        assert hasattr(testobj, 'in_exclude')
        assert hasattr(testobj, 'inputwin')
        assert hasattr(testobj, 'use_case')
        assert capsys.readouterr().out == ('called wxDialog.__init__()\n'
                                           'called dialog.SetTitle()\n'
                                           'called dialog.SetIcon()\n'
                                           'called dialog.create_inputwin()\n'
                                           'called TextCtrl.__init__()\n'
                                           'called CheckBox.__init__()\n'
        #                                  'called checkbox.SetValue(`False`)\n'
                                           'called CheckBox.__init__()\n'
                                           'called checkbox.SetValue(`False`)\n'
                                           'called checkbox.SetValue(`True`)\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called StaticText.__init__()\n'
                                           'called hori sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called hori sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called BoxSizer.__init__(`hori`)\n'
                                           'called hori sizer.Add()\n'
                                           'called hori sizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.CreateButtonSizer()\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.SetSizer()\n'
                                           'called dialog.SetAutoLayout()\n'
                                           'called vert sizer.Fit()\n'
                                           'called vert sizer.SetSizeHints()\n'
                                           'called dialog.Layout()\n')

    def test_create_inputwin(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called textdialog.__init__()')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx, 'CheckBox', MockCheckBox)
        monkeypatch.setattr(gui.wx, 'TextCtrl', MockTextCtrl)
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.GetTextDialog(mockparent)  # , 0, 'seltext', 'labeltext', True)
        testobj.create_inputwin('seltext')
        assert hasattr(testobj, 'inputwin')
        assert hasattr(testobj, 'use_case')
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called TextCtrl.__init__(`seltext`)\n'
                                           'called CheckBox.__init__()\n'
                                           'called checkbox.SetValue(`False`)\n')

    def test_confirm(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called textdialog.__init__()')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.GetTextDialog(mockparent, 0, 'seltext', 'labeltext', True)
        testobj.in_exclude = MockCheckBox()
        testobj.inputwin = MockTextCtrl()
        testobj.use_case = MockCheckBox()
        assert testobj.confirm() == ['value from checkbox', 'value from textctrl',
                                     'value from checkbox']


class TestGetItemDialog:
    def test_create_inputwin(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called textdialog.__init__()')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx, 'ComboBox', MockComboBox)
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.GetItemDialog(mockparent, 0, 'seltext', 'labeltext', True)
        testobj.create_inputwin((['sel1', 'sel2'], 1))
        assert hasattr(testobj, 'inputwin')
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called ComboBox.__init__() '
                                           "with arg `['sel1', 'sel2']`\n"
                                           'called combobox.SetSelection(`1`)\n')

    def test_confirm(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called textdialog.__init__()')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.GetItemDialog(mockparent, 0, 'seltext', 'labeltext', True)
        testobj.in_exclude = MockCheckBox()
        testobj.inputwin = MockComboBox()
        assert testobj.confirm() == ['value from checkbox', 'value from combobox']


class TestGridDialog:
    def test_init(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called wxDialog.__init__()')
        def mock_createbuttons(self, *args):
            print('called dialog.CreateButtonSizer()')
        def mock_setsizer(self, *args):
            print('called dialog.SetSizer()')
        def mock_setautolayout(self, *args):
            print('called dialog.SetAutoLayout()')
        def mock_layout(self, *args):
            print('called dialog.Layout()')
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'CreateButtonSizer', mock_createbuttons)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_layout)
        monkeypatch.setattr(gui.wx, 'BoxSizer', MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'FlexGridSizer', MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', MockStaticText)
        testobj = gui.GridDialog('parent', (('1', '2'), ('3', '4')), 'title')
        assert capsys.readouterr().out == ('called wxDialog.__init__()\n'
                                           'called BoxSizer.__init__(`vert`)\n'
                                           'called GridSizer.__init__()\n'
                                           'called StaticText.__init__()\n'
                                           'called gridsizer.Add()\n'
                                           'called StaticText.__init__()\n'
                                           'called gridsizer.Add()\n'
                                           'called StaticText.__init__()\n'
                                           'called gridsizer.Add()\n'
                                           'called StaticText.__init__()\n'
                                           'called gridsizer.Add()\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.CreateButtonSizer()\n'
                                           'called vert sizer.Add()\n'
                                           'called dialog.SetSizer()\n'
                                           'called dialog.SetAutoLayout()\n'
                                           'called vert sizer.Fit()\n'
                                           'called vert sizer.SetSizeHints()\n'
                                           'called dialog.Layout()\n')

    def confirm(self):  # te testen methode niet geïmplementeerd
        pass


class TestTaskbarIcon:
    def test_init(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called trayicon.__init__()')
        def mock_seticon(self, *args, **kwargs):
            print('called trayicon.SetIcon()')
        def mock_bind(self, *args, **kwargs):
            print('called trayicon.Bind()')
        monkeypatch.setattr(gui.wx.adv.TaskBarIcon, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.adv.TaskBarIcon, 'SetIcon', mock_seticon)
        monkeypatch.setattr(gui.wx.adv.TaskBarIcon, 'Bind', mock_bind)
        monkeypatch.setattr(gui.wx, 'Icon', MockIcon)
        mockparent = setup_mainwindow(monkeypatch)
        mockparent.nt_icon = gui.wx.Icon()
        mockparent.revive = lambda x: 'revive'
        testobj = gui.TaskbarIcon(mockparent)
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called Icon.__init__()\n'
                                           'called trayicon.__init__()\n'
                                           'called trayicon.SetIcon()\n'
                                           'called trayicon.Bind()\n'
                                           'called trayicon.Bind()\n')

    def test_createpopupmenu(self, monkeypatch, capsys):
        def mock_init(self, *args, **kwargs):
            print('called trayicon.__init__()')
        monkeypatch.setattr(gui.wx, 'Menu', MockMenu)
        monkeypatch.setattr(gui.TaskbarIcon, '__init__', mock_init)
        mockparent = setup_mainwindow(monkeypatch)
        menu = gui.TaskbarIcon(mockparent).CreatePopupMenu()
        assert isinstance(menu, gui.wx.Menu)
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called app.__init__()\n'
                                           'called trayicon.__init__()\n'
                                           'called Menu.__init__()\n'
                                           'called menu.Append()\n')

