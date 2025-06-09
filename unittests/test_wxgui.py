"""unittests for ./notetree/wx_gui.py
"""
import types
from mockgui import mockwxwidgets as mockwx
import notetree.wx_gui as gui


def setup_mainwindow(monkeypatch, capsys):
    """stub for setting up MainWindow object
    """
    monkeypatch.setattr(gui.wx, 'Frame', mockwx.MockFrame)
    monkeypatch.setattr(gui.wx, 'App', mockwx.MockApp)
    testobj = gui.MainWindow(MockNoteTree())
    assert capsys.readouterr().out == ('called NoteTree.__init__\n'
                                       'called app.__init__ with args (False,)\n')
    return testobj


class MockNoteTree:
    """stub for main.NoteTree object
    """
    def __init__(self):
        print('called NoteTree.__init__')
        self.root_title = 'title'
        self.opts = {}
    def get_menudata(self):
        """stub
        """
    def callback(self):
        """stub
        """
    def check_active(self, *args):
        """stub
        """
        print('called base.check_active')
    def activate_item(self, *args):
        """stub
        """
        print(f'called base.activate_item with arg `{args[0]}`')
    def update(self):
        """stub
        """
        print('called base.update')


class TestMainWindow:
    """unittests for wx_gui.MainWindow
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for MainWindow.init
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        assert hasattr(testobj, 'base')
        assert hasattr(testobj, 'app')
        assert testobj.activeitem is None

    def test_start(self, monkeypatch, capsys):
        """unittest for MainWindow.start
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.start()
        assert capsys.readouterr().out == 'called app.MainLoop\n'

    def test_init_screen(self, monkeypatch, capsys):
        """unittest for MainWindow.init_screen
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called frame.__init__')
        def mock_seticon(self, *args):
            """stub
            """
            print('called frame.SetIcon')
        def mock_setmenubar(self, *args):
            """stub
            """
            print('called frame.SetMenuBar')
        monkeypatch.setattr(gui.wx.Frame, '__init__', mock_init)
        monkeypatch.setattr(gui.wx, 'Icon', mockwx.MockIcon)
        monkeypatch.setattr(gui.wx.Frame, 'SetIcon', mock_seticon)
        monkeypatch.setattr(gui.wx, 'MenuBar', mockwx.MockMenuBar)
        monkeypatch.setattr(gui.wx.Frame, 'SetMenuBar', mock_setmenubar)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.init_screen()
        assert capsys.readouterr().out == ('called frame.__init__\n'
                                           'called MenuBar.__init__ with args ()\n'
                                           'called frame.SetMenuBar\n')
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.init_screen(parent=None, title='', iconame='x')
        assert capsys.readouterr().out == ('called frame.__init__\n'
                                           "called Icon.__init__ with args ('x', 3)\n"
                                           'called frame.SetIcon\n'
                                           'called MenuBar.__init__ with args ()\n'
                                           'called frame.SetMenuBar\n')

    def test_setup_statusbar(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_statusbar
        """
        def mock_createstatusbar(self, *args):
            """stub
            """
            print('called frame.CreateStatusBar')
            return 'x'
        monkeypatch.setattr(gui.wx.Frame, 'CreateStatusBar', mock_createstatusbar)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.setup_statusbar()
        assert capsys.readouterr().out == ('called frame.CreateStatusBar\n')
        assert hasattr(testobj, 'sb')

    def test_setup_trayicon(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_trayicon
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.setup_trayicon()  # eigenlijk overbodg want deze doet niks

    def test_setup_split_screen(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_split_screen
        """
        def mock_setup_tree(*args):
            """stub
            """
            print('called MainWindow.setup_tree')
            return 'tree'
        def mock_setup_editor(*args):
            """stub
            """
            print('called MainWindow.setup_editor')
            return 'editor'
        def mock_show(*args):
            """stub
            """
            print('called MainWindow.Show')
        monkeypatch.setattr(gui.wx, 'SplitterWindow', mockwx.MockSplitter)
        testobj = setup_mainwindow(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'setup_tree', mock_setup_tree)
        monkeypatch.setattr(testobj, 'setup_editor', mock_setup_editor)
        monkeypatch.setattr(testobj, 'Show', mock_show)
        testobj.setup_split_screen()
        assert capsys.readouterr().out == (
                f'called Splitter.__init__ with args ({testobj}, -1)\n'
                'called splitter.SetMinimumPaneSize with args (1,)\n'
                'called MainWindow.setup_tree\n'
                'called MainWindow.setup_editor\n'
                "called splitter.SplitVertically with args ('tree', 'editor')\n"
                'called splitter.SetSashPosition with args (180, True)\n'
                f'called app.SetTopWindow with args ({testobj},)\n'
                'called MainWindow.Show\n')

    def test_setup_tree(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_tree
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.splitter = 'splitter'
        monkeypatch.setattr(gui.wx, 'TreeCtrl', mockwx.MockTree)
        tree = testobj.setup_tree()
        assert tree == testobj.tree
        assert hasattr(testobj, 'root')
        assert capsys.readouterr().out == (
                "called Tree.__init__ with args ('splitter',)\n"
                "called tree.AddRoot with args ('title',)\n"
                "called tree.Bind with args"
                f" ({gui.wx.EVT_TREE_SEL_CHANGING}, {testobj.OnSelChanging})\n"
                "called tree.Bind with args"
                f" ({gui.wx.EVT_TREE_SEL_CHANGED}, {testobj.OnSelChanged})\n")

    def test_setup_editor(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_editor
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.splitter = 'splitter'
        monkeypatch.setattr(gui.stc, 'StyledTextCtrl', mockwx.MockEditor)
        monkeypatch.setattr(gui.wx, 'Font', mockwx.MockFont)
        editor = testobj.setup_editor()
        assert editor == testobj.editor
        assert capsys.readouterr().out == (
                "called Editor.__init__ with args ('splitter',)\n"
                "called editor.Enable with args (False,)\n"
                "called Font.__init__ with args ()\n"
                "called font.SetFamily with args (76,)\n"
                'called font.SetPointSize with args (10,)\n'
                'called editor.SetWrapMode with args (1,)\n'
                'called editor.SetCaretLineVisible with args (True,)\n'
                'called editor.SetCaretLineBackground with args (wx.Colour(255, 244, 244, 255),)\n'
                'called editor.SetLexer with args (98,)\n'
                'called editor.StyleSetForeground with args (2, wx.Colour(34, 68, 102, 255))\n'
                'called editor.StyleSetBold with args (2, True)\n'
                'called editor.StyleSetForeground with args (3, wx.Colour(34, 68, 102, 255))\n'
                'called editor.StyleSetBold with args (3, True)\n'
                'called editor.StyleSetForeground with args (4, wx.Colour(70, 51, 0, 255))\n'
                'called editor.StyleSetItalic with args (4, True)\n'
                'called editor.StyleSetForeground with args (5, wx.Colour(70, 51, 0, 255))\n'
                'called editor.StyleSetItalic with args (5, True)\n'
                'called editor.StyleSetForeground with args (6, wx.Colour(81, 131, 196, 255))\n'
                'called editor.StyleSetBold with args (6, True)\n'
                'called editor.StyleSetForeground with args (7, wx.Colour(81, 131, 196, 255))\n'
                'called editor.StyleSetBold with args (7, True)\n'
                'called editor.StyleSetForeground with args (8, wx.Colour(81, 131, 196, 255))\n'
                'called editor.StyleSetBold with args (8, True)\n'
                'called editor.StyleSetForeground with args (9, wx.Colour(81, 131, 196, 255))\n'
                'called editor.StyleSetBold with args (9, True)\n'
                'called editor.StyleSetForeground with args (10, wx.Colour(81, 131, 196, 255))\n'
                'called editor.StyleSetBold with args (10, True)\n'
                'called editor.StyleSetForeground with args (11, wx.Colour(81, 131, 196, 255))\n'
                'called editor.StyleSetBold with args (11, True)\n'
                'called editor.StyleSetBackground with args (12, wx.Colour(253, 253, 170, 255))\n'
                'called editor.StyleSetForeground with args (12, wx.Colour(0, 0, 0, 255))\n'
                'called editor.StyleSetForeground with args (13, wx.Colour(85, 85, 85, 255))\n'
                'called editor.StyleSetForeground with args (14, wx.Colour(85, 85, 85, 255))\n'
                'called editor.StyleSetForeground with args (15, wx.Colour(0, 0, 136, 255))\n'
                'called editor.StyleSetBackground with args (16, wx.Colour(169, 186, 157, 255))\n'
                'called editor.StyleSetForeground with args (16, wx.Colour(24, 69, 59, 255))\n'
                'called editor.StyleSetForeground with args (17, wx.Colour(85, 85, 85, 255))\n'
                'called editor.StyleSetBold with args (17, True)\n'
                'called editor.StyleSetForeground with args (18, wx.Colour(0, 0, 170, 255))\n'
                'called editor.StyleSetUnderline with args (11, True)\n'
                'called editor.StyleSetBackground with args (19, wx.Colour(253, 253, 253, 255))\n'
                'called editor.StyleSetForeground with args (19, wx.Colour(0, 0, 136, 255))\n'
                'called editor.StyleSetBackground with args (20, wx.Colour(253, 253, 253, 255))\n'
                'called editor.StyleSetForeground with args (20, wx.Colour(0, 0, 136, 255))\n'
                'called editor.StyleSetBackground with args (21, wx.Colour(253, 253, 253, 255))\n'
                'called editor.StyleSetForeground with args (21, wx.Colour(0, 0, 136, 255))\n'
                f"called editor.Bind with args ({gui.wx.EVT_TEXT}, {testobj.OnEvtText})\n")

    def setup_text(self):
        """stub

        wordt uiitgevoerd als onderdeel van setup_editor, dus geen aparte test nodig
        """

    def test_create_menu(self, monkeypatch, capsys):
        """unittest for MainWindow.create_menu: initial creation of menubar
        """
        def mock_getmenubar(*args):
            """stub
            """
            return mockwx.MockMenuBar()
        def mock_get_menudata(*args):
            """stub
            """
            self = args[0]
            return (('other', ((_('m_forward'), self.callback, 'forward', 'Ctrl+PgDown'),
                               (_('m_back'), self.callback, 'back', 'Ctrl+PgUp,F2'),
                               ('other', self.callback, 'other', 'Ctrl+D,Delete'), ), ),
                    (_("m_view"), ((_("m_revorder"), self.callback, _("h_revorder"), 'F9'),
                                   ("", None, None, None),
                                   (_("m_selall"), self.callback, _("h_selall"), None),
                                   (_("m_seltag"), self.callback, _("h_seltag"), None),
                                   (_("m_seltxt"), self.callback, _("h_seltxt"), None), ), ), )
        def mock_get_menudata_2(*args):
            """stub
            """
            self = args[0]
            return (('any', ((_('m_forward'), self.callback, 'forward', ''),
                             (_('m_back'), self.callback, 'back', ''),
                             ('other', self.callback, 'other', 'ding,invalid'), ), ), )
        def mock_menubar_append(self, *args):
            """stub
            """
            print(f'called menubar.Append with args (<menu>, {args[1]})')
        # def mock_menubar_replace(self, *args):
        #     """stub
        #     """
        #     print(f'called menubar.Replace with args ({args[0]}, <menu>, {args[2]})')
        def mock_menu_append(self, *args):
            """stub
            """
            print('called menu.Append with arg <menuitem>')
        def mock_menuitem_init(self, *args, **kwargs):
            """stub
            """
            print('called menuitem.__init__ with args <menu>', args[1:], kwargs)
        def mock_set_accel(self, *args):
            """stub
            """
            print('called mainwindow.SetAcceleratorTable')
        def mock_fromstring(self, *args):
            print('called AcceleratorEntry.FromString with args', args)
            return False
        monkeypatch.setattr(MockNoteTree, 'get_menudata', mock_get_menudata)
        monkeypatch.setattr(mockwx.MockMenuBar, 'Append', mock_menubar_append)
        # monkeypatch.setattr(mockwx.MockMenuBar, 'Replace', mock_menubar_replace)
        monkeypatch.setattr(gui.wx, 'Menu', mockwx.MockMenu)
        monkeypatch.setattr(mockwx.MockMenu, 'Append', mock_menu_append)
        monkeypatch.setattr(gui.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(mockwx.MockMenuItem, '__init__', mock_menuitem_init)
        monkeypatch.setattr(gui.wx, 'AcceleratorEntry', mockwx.MockAcceleratorEntry)
        monkeypatch.setattr(gui.wx, 'AcceleratorTable', mockwx.MockAcceleratorTable)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.opts['RevOrder'] = True
        testobj.base.opts['Selection'] = (1, True)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == 'called Tree.__init__ with args ()\n'
        monkeypatch.setattr(mockwx.MockMenuBar, 'GetMenus', lambda x: [])
        monkeypatch.setattr(testobj, 'GetMenuBar', mock_getmenubar)
        monkeypatch.setattr(testobj, 'SetAcceleratorTable', mock_set_accel)
        testobj.create_menu()
        assert list(testobj.selactions.keys()) == ["m_revorder", "m_selall", "m_seltag", "m_seltxt"]
        assert testobj.seltypes == ["m_selall", "m_seltag", "m_seltxt"]
        assert capsys.readouterr().out == (
                'called MenuBar.__init__ with args ()\n'
                'called Menu.__init__ with args ()\n'
                "called menuitem.__init__ with args"
                " <menu> (-1, 'm_forward\\tCtrl+PgDn', 'forward') {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+PgDn',)\n"
                "called menuitem.__init__ with args <menu> (-1, 'm_back\\tCtrl+PgUp', 'back') {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+PgUp',)\n"
                "called menuitem.__init__ with args <menu> () {'text': 'm_back\\tCtrl+PgUp'}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('F2',)\n"
                "called menuitem.__init__ with args <menu> (-1, 'other\\tCtrl+D', 'other') {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> () {'text': 'other\\tCtrl+D'}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Delete',)\n"
                'called AcceleratorTable.__init__ with 1 AcceleratorEntries\n'
                'called tree.SetAcceleratorTable\n'
                'called menubar.Append with args (<menu>, other)\n'
                'called Menu.__init__ with args ()\n'
                "called menuitem.__init__ with args"
                " <menu> (-1, 'm_revorder\\tF9', 'h_revorder', 1) {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-2,) {}\n"
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_selall', 'h_selall', 1) {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_seltag', 'h_seltag', 1) {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_seltxt', 'h_seltxt', 1) {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                'called menubar.Append with args (<menu>, m_view)\n'
                'called AcceleratorTable.__init__ with 3 AcceleratorEntries\n'
                'called mainwindow.SetAcceleratorTable\n'
                'called menuitem.Check with arg False\n'
                'called menuitem.Check with arg False\n'
                'called menuitem.Check with arg False\n'
                'called menuitem.Check with arg False\n'
                'called menuitem.Check with arg True\n'
                'called menuitem.Check with arg True\n')
        testobj.selactions = {}
        testobj.seltypes = []
        monkeypatch.setattr(MockNoteTree, 'get_menudata', mock_get_menudata_2)
        monkeypatch.setattr(mockwx.MockAcceleratorEntry, 'FromString', mock_fromstring)
        testobj.create_menu()
        assert not testobj.selactions
        assert not testobj.seltypes
        assert capsys.readouterr().out == (
                'called MenuBar.__init__ with args ()\n'
                'called Menu.__init__ with args ()\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_forward', 'forward') {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                'called AcceleratorEntry.FromString with args (None,)\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_back', 'back') {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                'called AcceleratorEntry.FromString with args (None,)\n'
                "called menuitem.__init__ with args <menu> (-1, 'other\\tding', 'other') {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> () {'text': 'other\\tding'}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('invalid',)\n"
                'called menubar.Append with args (<menu>, any)\n'
                'called AcceleratorTable.__init__ with 0 AcceleratorEntries\n'
                'called mainwindow.SetAcceleratorTable\n')

    def test_create_menu_2(self, monkeypatch, capsys):
        """unittest for MainWindow.create_menu: recreation of menubar
        """
        def mock_getmenubar(*args):
            """stub
            """
            return mockwx.MockMenuBar()
        def mock_get_menudata(*args):
            """stub
            """
            self = args[0]
            return (('other', ((_('m_forward'), self.callback, 'forward', 'Ctrl+PgDown'),
                               (_('m_back'), self.callback, 'back', 'Ctrl+PgUp,F2'),
                               ('other', self.callback, 'other', 'Ctrl+D,Delete'), ), ),
                    (_("m_view"), ((_("m_revorder"), self.callback, _("h_revorder"), 'F9'),
                                   ("", None, None, None),
                                   (_("m_selall"), self.callback, _("h_selall"), None),
                                   (_("m_seltag"), self.callback, _("h_seltag"), None),
                                   (_("m_seltxt"), self.callback, _("h_seltxt"), None), ), ), )
        def mock_menu_append(self, *args):
            """stub
            """
            print('called menu.Append with arg <menuitem>')
        def mock_menubar_replace(self, *args):
            """stub
            """
            print(f'called menubar.Replace with args ({args[0]}, <menu>, {args[2]})')
        def mock_menuitem_init(self, *args, **kwargs):
            """stub
            """
            print('called menuitem.__init__ with args <menu>', args[1:], kwargs)
        def mock_set_accel(*args):
            """stub
            """
            print('called mainwindow.SetAcceleratorTable')
        monkeypatch.setattr(MockNoteTree, 'get_menudata', mock_get_menudata)
        monkeypatch.setattr(gui.wx, 'Menu', mockwx.MockMenu)
        monkeypatch.setattr(gui.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(gui.wx, 'AcceleratorEntry', mockwx.MockAcceleratorEntry)
        monkeypatch.setattr(gui.wx, 'AcceleratorTable', mockwx.MockAcceleratorTable)
        monkeypatch.setattr(mockwx.MockMenuItem, '__init__', mock_menuitem_init)
        monkeypatch.setattr(mockwx.MockMenu, 'Append', mock_menu_append)
        monkeypatch.setattr(mockwx.MockMenuBar, 'Replace', mock_menubar_replace)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.opts['RevOrder'] = True
        testobj.base.opts['Selection'] = (1, True)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == 'called Tree.__init__ with args ()\n'
        monkeypatch.setattr(testobj, 'GetMenuBar', mock_getmenubar)
        monkeypatch.setattr(testobj, 'SetAcceleratorTable', mock_set_accel)
        testobj.create_menu()
        assert list(testobj.selactions.keys()) == ["m_revorder", "m_selall", "m_seltag", "m_seltxt"]
        assert testobj.seltypes == ["m_selall", "m_seltag", "m_seltxt"]
        assert capsys.readouterr().out == (
                'called MenuBar.__init__ with args ()\n'
                'called menubar.GetMenus with args ()\n'
                'called Menu.__init__ with args ()\n'
                'called Menu.__init__ with args ()\n'
                'called Menu.__init__ with args ()\n'
                'called menuitem.__init__ with args'
                " <menu> (-1, 'm_forward\\tCtrl+PgDn', 'forward') {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+PgDn',)\n"
                "called menuitem.__init__ with args <menu> (-1, 'm_back\\tCtrl+PgUp', 'back') {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+PgUp',)\n"
                "called menuitem.__init__ with args <menu> () {'text': 'm_back\\tCtrl+PgUp'}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('F2',)\n"
                "called menuitem.__init__ with args <menu> (-1, 'other\\tCtrl+D', 'other') {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> () {'text': 'other\\tCtrl+D'}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Delete',)\n"
                'called AcceleratorTable.__init__ with 1 AcceleratorEntries\n'
                'called tree.SetAcceleratorTable\n'
                "called menubar.Replace with args (0, <menu>, other)\n"
                'called menu.Destroy\n'
                "called Menu.__init__ with args ()\n"
                "called menuitem.__init__ with args"
                " <menu> (-1, 'm_revorder\\tF9', 'h_revorder', 1) {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.__init__ with args <menu> (-2,) {}\n'
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_selall', 'h_selall', 1) {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_seltag', 'h_seltag', 1) {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_seltxt', 'h_seltxt', 1) {}\n"
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.base.callback})\n'
                'called menu.Append with arg <menuitem>\n'
                "called menubar.Replace with args (1, <menu>, m_view)\n"
                'called menu.Destroy\n'
                'called AcceleratorTable.__init__ with 3 AcceleratorEntries\n'
                'called mainwindow.SetAcceleratorTable\n'
                'called menuitem.Check with arg False\n'
                'called menuitem.Check with arg False\n'
                'called menuitem.Check with arg False\n'
                'called menuitem.Check with arg False\n'
                'called menuitem.Check with arg True\n'
                'called menuitem.Check with arg True\n')

    def test_OnEvtText(self, monkeypatch, capsys):
        """unittest for MainWindow.OnEvtText
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockwx.MockEditor()
        testobj.OnEvtText('x')
        assert testobj.editor.IsModified

    def _test_OnSelChanging(self):
        """unittest for MainWindow.OnSelChanging

        deze methode is wel gedefinieerd maar leeggelaten
        """

    def test_OnSelChanged(self, monkeypatch, capsys):
        """unittest for MainWindow.OnSelChanged
        """
        # def mock_check_active(*args):
        #     print('called notetree.check_active')
        # def mock_activate_item(*args):
        #     print('called notetree.activate_item(`{args[0]}`)')
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = 'root'
        testobj.OnSelChanged(mockwx.MockEvent())
        assert capsys.readouterr().out == ('called event.__init__ with args ()\n'
                                           'called event.GetItem\n'
                                           'called base.check_active\n'
                                           'in onselchanged: item is treeitem, root is root\n'
                                           'called base.activate_item with arg `treeitem`\n'
                                           'called event.Skip\n')

    def test_close(self, monkeypatch, capsys):
        """unittest for MainWindow.close
        """
        def mock_close(*args):
            """stub
            """
            print('called mainwindow.Close')
        def mock_update(*args):
            """stub
            """
            print('called notetree.update')
        testobj = setup_mainwindow(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'Close', mock_close)
        monkeypatch.setattr(testobj.base, 'update', mock_update)
        testobj.activeitem = None
        testobj.close('event')
        assert capsys.readouterr().out == ('called mainwindow.Close\n')
        testobj = setup_mainwindow(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'Close', mock_close)
        monkeypatch.setattr(testobj.base, 'update', mock_update)
        testobj.activeitem = 'item'
        testobj.close('event')
        assert capsys.readouterr().out == ('called notetree.update\n'
                                           'called mainwindow.Close\n')

    def test_clear_editor(self, monkeypatch, capsys):
        """unittest for MainWindow.clear_editor
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockwx.MockEditor()
        testobj.clear_editor()
        assert capsys.readouterr().out == ('called Editor.__init__ with args ()\n'
                                           'called editor.Clear\n'
                                           'called editor.Enable with args (False,)\n')

    def test_open_editor(self, monkeypatch, capsys):
        """unittest for MainWindow.open_editor
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockwx.MockEditor()
        testobj.open_editor()
        assert capsys.readouterr().out == ('called Editor.__init__ with args ()\n'
                                           'called editor.Enable with args (True,)\n')

    def test_set_screen(self, monkeypatch, capsys):
        """unittest for MainWindow.set_screen
        """
        def mock_setsize(*args):
            """stub
            """
            print(f'called frame.SetSize({args[0]})')
        testobj = setup_mainwindow(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'SetSize', mock_setsize)
        testobj.set_screen('screensize')
        assert capsys.readouterr().out == ('called frame.SetSize(screensize)\n')

    def test_set_splitter(self, monkeypatch, capsys):
        """unittest for MainWindow.set_splitter
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.splitter = mockwx.MockSplitter()
        testobj.set_splitter('split')
        assert capsys.readouterr().out == ('called Splitter.__init__ with args ()\n'
                                           "called splitter.SetSashPosition with args ('s', True)\n")

    def test_create_root(self, monkeypatch, capsys):
        """unittest for MainWindow.create_root
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert testobj.create_root('title') == testobj.root
        assert testobj.activeitem == testobj.root
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           'called tree.DeleteAllItems\n'
                                           "called tree.AddRoot with args ('title',)\n")

    def test_set_item_expanded(self, monkeypatch, capsys):
        """unittest for MainWindow.set_item_expanded
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.set_item_expanded('item')
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           "called tree.Expand with args ('item',)\n")

    def test_emphasize_activeitem(self, monkeypatch, capsys):
        """unittest for MainWindow.emphasize_activeitem
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.emphasize_activeitem('value')
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           "called tree.SetItemBold with args (None, 'value')\n")

    def test_editor_text_was_changed(self, monkeypatch, capsys):
        """unittest for MainWindow.editor_text_was_changed
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockwx.MockEditor()
        assert testobj.editor_text_was_changed() == 'ismodified'
        assert capsys.readouterr().out == ('called Editor.__init__ with args ()\n')

    def test_copy_text_from_editor_to_activeitem(self, monkeypatch, capsys):
        """unittest for MainWindow.copy_text_from_editor_to_activeitem
        """
        def mock_set_itemtext(*args):
            """stub
            """
            print(f'set text of `{args[0]}` to `{args[1]}`')
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.activeitem = 'active item'
        testobj.editor = mockwx.MockEditor()
        monkeypatch.setattr(testobj, 'set_item_text', mock_set_itemtext)
        testobj.copy_text_from_editor_to_activeitem()
        assert capsys.readouterr().out == ('called Editor.__init__ with args ()\n'
                                           'called editor.GetValue\n'
                                           'set text of `active item` to `fake editor value`\n')

    def test_copy_text_from_activeitem_to_editor(self, monkeypatch, capsys):
        """unittest for MainWindow.copy_text_from_activeitem_to_editor
        """
        def mock_get_itemtext(*args):
            """stub
            """
            return 'item text'
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.activeitem = 'active item'
        testobj.editor = mockwx.MockEditor()
        monkeypatch.setattr(testobj, 'get_item_text', mock_get_itemtext)
        testobj.copy_text_from_activeitem_to_editor()
        assert capsys.readouterr().out == ('called Editor.__init__ with args ()\n'
                                           'called editor.SetValue with arg `item text`\n')

    def test_select_item(self, monkeypatch, capsys):
        """unittest for MainWindow.select_item
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.select_item('item')
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           "called tree.SelectItem with args ('item',)\n")

    def test_get_selected_item(self, monkeypatch, capsys):
        """unittest for MainWindow.get_selected_item
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert testobj.get_selected_item() == 'selection'
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           'called tree.GetSelection\n')

    def test_remove_item_from_tree_any(self, monkeypatch, capsys):
        """unittest for MainWindow.remove_item_from_tree: removing any item except last one
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.remove_item_from_tree('item')
        assert testobj.activeitem is None
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           'called tree.GetNextSibling\n'
                                           "called TreeItem.__init__ with args ('next treeitem',)\n"
                                           "called TreeItem.IsOk\n"
                                           "called tree.Delete with args ('item',)\n")

    def test_remove_item_from_tree_last(self, monkeypatch, capsys):
        """unittest for MainWindow.remove_item_from_tree: removing last item
        """
        def mock_get_next(self, *args):
            """stub
            """
            print('called tree.GetNextSibling')
            return mockwx.MockTreeItem('not ok')
        def mock_select(item):
            print('called tree.select_item')
        testobj = setup_mainwindow(monkeypatch, capsys)
        monkeypatch.setattr(mockwx.MockTree, 'GetNextSibling', mock_get_next)
        testobj.tree = mockwx.MockTree()
        testobj.select_item = mock_select
        testobj.remove_item_from_tree('item')
        assert testobj.activeitem is None
        assert capsys.readouterr().out == (
                'called Tree.__init__ with args ()\n'
                'called tree.GetNextSibling\n'
                "called TreeItem.__init__ with args ('not ok',)\n"
                "called TreeItem.IsOk\n"
                'called tree.GetPrevSibling\n'
                "called TreeItem.__init__ with args ('previous treeitem',)\n"
                "called tree.Delete with args ('item',)\n"
                'called tree.select_item\n')

    def test_get_key_from_item(self, monkeypatch, capsys):
        """unittest for MainWindow.get_key_from_item
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert testobj.get_key_from_item('item') == 'itemkey'
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           "called tree.GetItemData with args ('item',)\n")

    def test_get_activeitem_title(self, monkeypatch, capsys):
        """unittest for MainWindow.get_activeitem_title
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert testobj.get_activeitem_title() == 'itemtext'
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           "called tree.GetItemText with args (None,)\n")

    def test_set_activeitem_title(self, monkeypatch, capsys):
        """unittest for MainWindow.set_activeitem_title
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.set_activeitem_title('title')
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           "called tree.SetItemText with args (None, 'title')\n")

    def test_set_focus_to_tree(self, monkeypatch, capsys):
        """unittest for MainWindow.set_focus_to_tree
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.set_focus_to_tree()
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           'called tree.SetFocus\n')

    def test_set_focus_to_editor(self, monkeypatch, capsys):
        """unittest for MainWindow.set_focus_to_editor
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockwx.MockEditor()
        testobj.set_focus_to_editor()
        assert capsys.readouterr().out == ('called Editor.__init__ with args ()\n'
                                           'called editor.SetFocus\n')

    def test_add_item_to_tree(self, monkeypatch, capsys):
        """unittest for MainWindow.add_item_to_tree: old-to-new order"
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.opts['RevOrder'] = False
        testobj.tree = mockwx.MockTree()
        testobj.root = 'root'
        testobj.add_item_to_tree('key', 'tag', 'text', ['keywords'])
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           "called tree.AppendItem with args ('root', 'tag')\n"
                                           "called tree.SetItemData() with args"
                                           " (None, ('key', 'text', ['keywords']))\n")

    def test_add_item_to_tree_2(self, monkeypatch, capsys):
        """unittest for MainWindow.add_item_to_tre:e reversed (new-to-old) order"
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.opts['RevOrder'] = True
        testobj.tree = mockwx.MockTree()
        testobj.root = 'root'
        testobj.add_item_to_tree('key', 'tag', 'text', ['keywords'])
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           "called tree.PrependItem with args ('root', 'tag')\n"
                                           'called tree.SetItemData() with args'
                                           " (None, ('key', 'text', ['keywords']))\n")

    def test_get_treeitems(self, monkeypatch, capsys):
        """unittest for MainWindow.get_treeitems
        """
        def mock_GetFirstChild(self, *args):
            """stub
            """
            print('called tree.GetFirstChild')
            return first, 0
        def mock_GetNextChild(self, *args):
            """stub
            """
            cookie = args[1]
            print('called tree.GetNextChild')
            if cookie == 0:
                return item, 1
            return last, -1
        monkeypatch.setattr(mockwx.MockTree, 'GetFirstChild', mock_GetFirstChild)
        monkeypatch.setattr(mockwx.MockTree, 'GetNextChild', mock_GetNextChild)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        first = mockwx.MockTreeItem('first')
        last = mockwx.MockTreeItem('not ok')
        item = mockwx.MockTreeItem('activeitem')
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called TreeItem.__init__ with args ('not ok',)\n"
                                           "called TreeItem.__init__ with args ('activeitem',)\n")
        testobj.root = 'root'
        testobj.activeitem = item
        itemlist, activeitem = testobj.get_treeitems()
        assert itemlist == [('itemkey', 'itemtext', 'itemtext', ['keyword']),
                            ('itemkey', 'itemtext', 'itemtext', ['keyword'])]
        assert activeitem == 'itemkey'
        assert capsys.readouterr().out == ('called tree.GetFirstChild\n'
                                           "called TreeItem.IsOk\n"
                                           f"called tree.GetItemText with args ({first},)\n"
                                           f"called tree.GetItemData with args ({first},)\n"
                                           'called tree.GetNextChild\n'
                                           "called TreeItem.IsOk\n"
                                           f"called tree.GetItemText with args ({item},)\n"
                                           f"called tree.GetItemData with args ({item},)\n"
                                           'called tree.GetNextChild\n'
                                           "called TreeItem.IsOk\n")

    def test_get_screensize(self, monkeypatch, capsys):
        """unittest for MainWindow.get_screensize
        """
        def mock_getsize(self):
            """stub
            """
            return mockwx.MockSize(1, 2)
        monkeypatch.setattr(gui.wx.Frame, 'GetSize', mock_getsize)
        testobj = setup_mainwindow(monkeypatch, capsys)
        assert testobj.get_screensize() == (1, 2)

    def test_get_splitterpos(self, monkeypatch, capsys):
        """unittest for MainWindow.get_splitterpos
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.splitter = mockwx.MockSplitter()
        assert testobj.get_splitterpos() == (55,)

    def test_sleep(self, monkeypatch, capsys):
        """unittest for MainWindow.sleep
        """
        def mock_hide(self, *args):
            """stub
            """
            print('called frame.Hide')
        monkeypatch.setattr(gui.MainWindow, 'Hide', mock_hide)
        monkeypatch.setattr(gui, 'TaskbarIcon', mockwx.MockTrayIcon)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.sleep()
        assert hasattr(testobj, 'tray_icon')
        assert capsys.readouterr().out == (f"called TrayIcon.__init__ with args ({testobj},)\n"
                                           'called frame.Hide\n')

    def test_revive(self, monkeypatch, capsys):
        """unittest for MainWindow.revive
        """
        def mock_show(self, *args):
            """stub
            """
            print('called frame.Show')
        monkeypatch.setattr(gui.MainWindow, 'Show', mock_show)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tray_icon = mockwx.MockTrayIcon()
        testobj.revive()
        assert capsys.readouterr().out == ('called TrayIcon.__init__ with args ()\n'
                                           'called frame.Show\n'
                                           'called trayicon.Destroy\n')

    def test_get_next_item(self, monkeypatch, capsys):
        """unittest for MainWindow.get_next_item: next item gevonden
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        item = testobj.get_next_item()
        assert item.tag == 'next treeitem'

    def test_get_next_item_nonext(self, monkeypatch, capsys):
        """unittest for MainWindow.get_next_item: next item niet gevonden
        """
        def mock_getnextsibling(self, *args):
            """stub
            """
            return mockwx.MockTreeItem('not ok')
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        monkeypatch.setattr(testobj.tree, 'GetNextSibling', mock_getnextsibling)
        assert testobj.get_next_item() is None

    def test_get_prev_item(self, monkeypatch, capsys):
        """unittest for MainWindow.get_prev_item: previous item gevonden
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        item = testobj.get_prev_item()
        assert item.tag == 'previous treeitem'

    def test_get_prev_item_2(self, monkeypatch, capsys):
        """unittest for MainWindow.get_prev_item: previous item niet gevonden
        """
        def mock_getprevsibling(self, *args):
            """stub
            """
            return mockwx.MockTreeItem('not ok')
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        monkeypatch.setattr(testobj.tree, 'GetPrevSibling', mock_getprevsibling)
        assert testobj.get_prev_item() is None

    def test_get_rootitem_title(self, monkeypatch, capsys):
        """unittest for MainWindow.get_rootitem_title
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.root = 'root'
        assert testobj.get_rootitem_title() == 'itemtext'

    def test_set_rootitem_title(self, monkeypatch, capsys):
        """unittest for MainWindow.set_rootitem_title
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.root = 'root'
        testobj.set_rootitem_title('text')
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           "called tree.SetItemText with args ('root', 'text')\n")

    def test_get_item_text(self, monkeypatch, capsys):
        """unittest for MainWindow.get_item_text
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert testobj.get_item_text('item') == 'itemtext'

    def test_set_editor_text(self, monkeypatch, capsys):
        """unittest for MainWindow.set_editor_text
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockwx.MockEditor()
        testobj.set_editor_text('text')
        assert capsys.readouterr().out == ('called Editor.__init__ with args ()\n'
                                           'called editor.SetValue with arg `text`\n')

    def test_get_editor_text(self, monkeypatch, capsys):
        """unittest for MainWindow.get_editor_text
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockwx.MockEditor()
        assert testobj.get_editor_text() == 'fake editor value'

    def test_set_item_text(self, monkeypatch, capsys):
        """unittest for MainWindow.set_item_text
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.set_item_text('item', 'text')
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           "called tree.GetItemData with args ('item',)\n"
                                           'called tree.SetItemData() with args'
                                           " ('item', ('itemkey', 'text', ['keyword']))\n")

    def test_get_item_keywords(self, monkeypatch, capsys):
        """unittest for MainWindow.get_item_keywords
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert testobj.get_item_keywords('item') == ['keyword']

    def test_set_item_keywords(self, monkeypatch, capsys):
        """unittest for MainWindow.set_item_keywords
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.set_item_keywords('item', ['data'])
        assert capsys.readouterr().out == ('called Tree.__init__ with args ()\n'
                                           "called tree.GetItemData with args ('item',)\n"
                                           'called tree.SetItemData() with args'
                                           " ('item', ('itemkey', 'itemtext', ['data']))\n")

    def test_show_statusbar_message(self, monkeypatch, capsys):
        """unittest for MainWindow.show_statusbar_message
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.sb = mockwx.MockStatusBar()
        testobj.show_statusbar_message('text')
        assert capsys.readouterr().out == ("called statusbar.SetStatusText with args ('text',)\n")

    def test_enable_selaction(self, monkeypatch, capsys):
        """unittest for MainWindow.enable_selaction
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.selactions = {'actiontext': mockwx.MockMenuItem()}
        testobj.enable_selaction('actiontext')
        assert capsys.readouterr().out == ('called MenuItem.__init__ with args ()\n'
                                           'called menuitem.Check with arg True\n')

    def test_disable_selaction(self, monkeypatch, capsys):
        """unittest for MainWindow.disable_selaction
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.selactions = {'actiontext': mockwx.MockMenuItem()}
        testobj.disable_selaction('actiontext')
        assert capsys.readouterr().out == ('called MenuItem.__init__ with args ()\n'
                                           'called menuitem.Check with arg False\n')

    def test_showmsg(self, monkeypatch, capsys):
        """unittest for MainWindow.showmsg
        """
        def mock_messagebox(*args):
            """stub
            """
            print(f'called wx.MessageBox() with args `{args[0]}`, `{args[1]}`, `{args[2]}`')
        monkeypatch.setattr(gui.wx, 'MessageBox', mock_messagebox)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'title'
        flags = gui.wx.OK | gui.wx.ICON_INFORMATION
        testobj.showmsg('message')
        assert capsys.readouterr().out == ('called wx.MessageBox() with args'
                                           f" `message`, `title`, `{flags}`\n")

    def test_ask_question(self, monkeypatch, capsys):
        """unittest for MainWindow.ask_question
        """
        def mock_messagebox(*args):
            """stub
            """
            print(f'called wx.MessageBox() with args `{args[0]}`, `{args[1]}`, `{args[2]}`')
            return gui.wx.YES
        monkeypatch.setattr(gui.wx, 'MessageBox', mock_messagebox)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'title'
        flags = gui.wx.YES_NO | gui.wx.ICON_QUESTION
        assert testobj.ask_question('question')
        assert capsys.readouterr().out == ('called wx.MessageBox() with args'
                                           f" `question`, `title`, `{flags}`\n")

    def test_show_dialog(self, monkeypatch, capsys):
        """unittest for MainWindow.show_dialog
        """
        def mock_showmodal(self, *args):
            """stub
            """
            return gui.wx.ID_OK
        monkeypatch.setattr(gui.wx.Dialog, 'ShowModal', mock_showmodal)
        testobj = setup_mainwindow(monkeypatch, capsys)
        assert testobj.show_dialog(mockwx.MockDialog, 'title') == (True, 'confirmation data')
        assert capsys.readouterr().out == "called Dialog.__init__() with args ('title',) {}\n"

    def test_show_dialog_2(self, monkeypatch, capsys):
        """unittest for MainWindow.show_dialog: cancel
        """
        def mock_showmodal(self, *args):
            """stub
            """
            return gui.wx.ID_CANCEL
        monkeypatch.setattr(mockwx.MockDialog, 'ShowModal', mock_showmodal)
        testobj = setup_mainwindow(monkeypatch, capsys)
        assert testobj.show_dialog(mockwx.MockDialog, ('title',)) == (False, None)
        assert capsys.readouterr().out == "called Dialog.__init__() with args (('title',),) {}\n"

    def test_get_text_from_user(self, monkeypatch, capsys):
        """unittest for MainWindow.get_text_from_user
        """
        monkeypatch.setattr(gui.wx, 'TextEntryDialog', mockwx.MockTextDialog)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'title'
        assert testobj.get_text_from_user('prompt', 'default') == ('entered value', True)
        assert capsys.readouterr().out == ('called TextDialog.__init__() with args'
                                           " ('prompt', 'title', 'default') {}\n"
                                           'called TextDialog.GetValue\n')

    def test_get_text_from_user_2(self, monkeypatch, capsys):
        """unittest for MainWindow.get_text_from_user: cancel prompt
        """
        def mock_showmodal(self, *args):
            """stub
            """
            return gui.wx.ID_CANCEL
        monkeypatch.setattr(gui.wx, 'TextEntryDialog', mockwx.MockTextDialog)
        monkeypatch.setattr(mockwx.MockTextDialog, 'ShowModal', mock_showmodal)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'title'
        assert testobj.get_text_from_user('prompt', 'default') == ('entered value', False)
        assert capsys.readouterr().out == ('called TextDialog.__init__() with args'
                                           " ('prompt', 'title', 'default') {}\n"
                                           'called TextDialog.GetValue\n')

    def test_get_choice_from_user(self, monkeypatch, capsys):
        """unittest for MainWindow.get_choice_from_user
        """
        monkeypatch.setattr(gui.wx, 'SingleChoiceDialog', mockwx.MockChoiceDialog)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'title'
        assert testobj.get_choice_from_user('prompt', ['choices'], 'default') == (
            'selected value', True)
        assert capsys.readouterr().out == ('called ChoiceDialog.__init__ with args'
                                           " ('prompt', 'title', ['choices'])\n"
                                           "called ChoiceDialog.SetSelection with arg 'default'\n"
                                           'called ChoiceDialog.GetStringSelection\n')

    def test_get_choice_from_user_2(self, monkeypatch, capsys):
        """unittest for MainWindow.get_choice_from_user: cancel
        """
        def mock_showmodal(self, *args):
            """stub
            """
            return gui.wx.ID_CANCEL
        monkeypatch.setattr(gui.wx, 'SingleChoiceDialog', mockwx.MockChoiceDialog)
        monkeypatch.setattr(mockwx.MockChoiceDialog, 'ShowModal', mock_showmodal)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'title'
        assert testobj.get_choice_from_user('prompt', ['choices'], 'default') == (
            'selected value', False)


class TestOptionsDialog:
    """unittests for wx_gui.OptionsDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for OptionsDialog.init
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called wxDialog.__init__')
        def mock_setescapeid(self, *args):
            """stub
            """
            print('called dialog.SetEscapeId')
        def mock_setsizer(self, *args):
            """stub
            """
            print('called dialog.SetSizer')
        def mock_setautolayout(self, *args):
            """stub
            """
            print('called dialog.SetAutoLayout')
        def mock_layout(self, *args):
            """stub
            """
            print('called dialog.Layout')
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'SetEscapeId', mock_setescapeid)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_layout)
        monkeypatch.setattr(gui.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'FlexGridSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(gui.wx, 'CheckBox', mockwx.MockCheckBox)
        monkeypatch.setattr(gui.wx, 'Button', mockwx.MockButton)
        testobj = gui.OptionsDialog('parent', {'text': 'value'})
        assert testobj.parent == 'parent'
        assert len(testobj.controls) == 1
        assert testobj.controls[0][0] == 'text'
        assert capsys.readouterr().out == (
                'called wxDialog.__init__\n'
                f'called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n'
                "called GridSizer.__init__ with args () {'cols': 2}\n"
                f"called StaticText.__init__ with args ({testobj}, -1, 'text')\n"
                "called gridsizer.Add with args <item> (1, 240, 5)\n"
                f"called CheckBox.__init__ with args ({testobj}, -1, '') {{}}\n"
                "called checkbox.SetValue with args ('value',)\n"
                "called gridsizer.Add with args <item> (1, 240, 5)\n"
                "called vert sizer.Add with args <item> (0, 2544, 5)\n"
                f'called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n'
                f"called Button.__init__ with args ({testobj},) {{'id': 5100, 'label': 'b_apply'}}\n"
                "called hori sizer.Add with args <item> (0, 8432, 2)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5001, 'label': 'b_close'}}\n"
                "called hori sizer.Add with args <item> (0, 8432, 2)\n"
                "called dialog.SetEscapeId\n"
                "called vert sizer.Add with args <item> (0, 2544, 5)\n"
                "called dialog.SetSizer\n"
                "called dialog.SetAutoLayout\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout\n")

    def test_confirm(self, monkeypatch):
        """unittest for OptionsDialog.confirm
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
            self.parent = args[0]
        monkeypatch.setattr(gui.OptionsDialog, '__init__', mock_init)
        testobj = gui.OptionsDialog(types.SimpleNamespace(dialog_data={}), {})
        testobj.controls = [('text', mockwx.MockCheckBox())]
        assert testobj.confirm() == {'text': 'value from checkbox'}


class TestCheckDialog:
    """unittests for wx_gui.CheckDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for CheckDialog.init
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called wxDialog.__init__')
            self.parent = args[0]
        def mock_createbuttons(self, *args):
            """stub
            """
            print('called dialog.CreateButtonSizer')
        def mock_setsizer(self, *args):
            """stub
            """
            print('called dialog.SetSizer')
        def mock_setautolayout(self, *args):
            """stub
            """
            print('called dialog.SetAutoLayout')
        def mock_layout(self, *args):
            """stub
            """
            print('called dialog.Layout')
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'CreateButtonSizer', mock_createbuttons)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_layout)
        monkeypatch.setattr(gui.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(gui.wx, 'CheckBox', mockwx.MockCheckBox)
        monkeypatch.setattr(gui.wx, 'Button', mockwx.MockButton)
        testobj = gui.CheckDialog(mockparent, {}, 'message')
        assert testobj.parent == mockparent
        assert hasattr(testobj, 'check')
        assert capsys.readouterr().out == (
                'called wxDialog.__init__\n'
                f'called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n'
                f"called StaticText.__init__ with args ({testobj}, -1, 'message')\n"
                'called vert sizer.Add with args <item> (1, 240, 5)\n'
                f'called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n'
                f"called CheckBox.__init__ with args ({testobj}, -1, 'hide_message') {{}}\n"
                'called hori sizer.Add with args <item> (0, 8192)\n'
                'called vert sizer.Add with args <item> (0, 256)\n'
                'called dialog.CreateButtonSizer\n'
                'called vert sizer.Add with args <item> ()\n'
                'called dialog.SetSizer\n'
                'called dialog.SetAutoLayout\n'
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                'called dialog.Layout\n')

    def test_confirm(self, monkeypatch):
        """unittest for CheckDialog.confirm
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
            self.parent = args[0]
        monkeypatch.setattr(gui.CheckDialog, '__init__', mock_init)
        testobj = gui.CheckDialog(types.SimpleNamespace(dialog_data='x'), {}, '')
        testobj.check = mockwx.MockCheckBox()
        assert testobj.confirm() == 'value from checkbox'


class TestKeywordsDialog:
    """unittests for wx_gui.KeywordsDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.init: calling with no keywords associated yet
        """
        def mock_init(self, *args):
            """stub
            """
            print('called wxDialog.__init__')
        def mock_SetTitle(self, *args):
            """stub
            """
            print('called dialog.SetTitle() with args', args)
        def mock_SetIcon(self, *args):
            """stub
            """
            print('called dialog.SetIcon() with args', args)
        def mock_createbuttons(self, *args):
            """stub
            """
            print('called dialog.createbuttons')
        # def mock_setaffirmativeid(self, *args):
        #     """stub
        #     """
        #     print('called dialog.SetAffirmativeId')
        def mock_setsizer(self, *args):
            """stub
            """
            print('called dialog.SetSizer')
        def mock_setautolayout(self, *args):
            """stub
            """
            print('called dialog.SetAutoLayout')
        def mock_setsize(self, *args):
            """stub
            """
            print('called dialog.SetSize')
        def mock_Layout(self, *args):
            """stub
            """
            print('called dialog.Layout')
        def mock_create_actions(self, *args):
            """stub
            """
            print('called dialog.create_actions')
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
        monkeypatch.setattr(gui.wx, 'BoxSizer', mockwx.MockBoxSizer)
        # monkeypatch.setattr(gui.wx, 'FlexGridSizer', MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(gui.wx, 'Button', mockwx.MockButton)
        monkeypatch.setattr(gui.wx, 'ListBox', mockwx.MockListBox)
        # monkeypatch.setattr(gui.wx, 'TextCtrl', mockwx.MockTextCtrl)
        monkeypatch.setattr(gui.KeywordsDialog, 'create_actions', mock_create_actions)
        testobj = gui.KeywordsDialog(mockparent, '')
        assert testobj.parent == mockparent
        assert testobj.helptext == ''  # hasattr(testobj, 'helptext')
        assert isinstance(testobj.fromlist, gui.wx.ListBox)
        assert isinstance(testobj.tolist, gui.wx.ListBox)
        # testobj = gui.KeywordsDialog(mockparent, keywords)
        assert capsys.readouterr().out == (
                "called wxDialog.__init__\n"
                "called dialog.SetTitle() with args ('title - w_tags',)\n"
                "called dialog.SetIcon() with args ('icon',)\n"
                f"called ListBox.__init__ with args ({testobj},)\n"
                f"called listbox.bind with args ({gui.wx.EVT_LISTBOX_DCLICK}, {testobj.move_right})\n"
                f"called StaticText.__init__ with args ({testobj},)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'b_tag'}}\n"
                f"called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.move_right}) {{}}\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'b_untag'}}\n"
                f"called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.move_left}) {{}}\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'b_newtag'}}\n"
                f"called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.add_trefw}) {{}}\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'm_keys'}}\n"
                f"called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.keys_help}) {{}}\n"
                f"called ListBox.__init__ with args ({testobj},)\n"
                f"called listbox.bind with args ({gui.wx.EVT_LISTBOX_DCLICK}, {testobj.move_left})\n"
                "called dialog.create_actions\n"
                "called ListBox.InsertItems with args ([],)\n"
                "called ListBox.InsertItems with args (['x', 'y'],)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called StaticText.__init__ with args ({testobj},)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called hori sizer.Add with args <item> ()\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                "called vert sizer.AddStretchSpacer\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.AddSpacer with args (10,)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args <item> ()\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called StaticText.__init__ with args ({testobj},)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called hori sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> (0, 496, 10)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                "called dialog.createbuttons\n"
                "called vert sizer.Add with args <item> (0, 496, 10)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called dialog.SetSizer\n"
                "called dialog.SetAutoLayout\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout\n"
                'called dialog.SetSize\n')
        testobj.parent.base.opts['Keywords'] = []
        testobj = gui.KeywordsDialog(mockparent, 'qqqq', ['aa', 'bb'])
        assert testobj.parent == mockparent
        assert testobj.helptext == 'qqqq'  # hasattr(testobj, 'helptext')
        assert isinstance(testobj.fromlist, gui.wx.ListBox)
        assert isinstance(testobj.tolist, gui.wx.ListBox)
        # testobj = gui.KeywordsDialog(mockparent, keywords)
        assert capsys.readouterr().out == (
                "called wxDialog.__init__\n"
                "called dialog.SetTitle() with args ('title - w_tags',)\n"
                "called dialog.SetIcon() with args ('icon',)\n"
                f"called ListBox.__init__ with args ({testobj},)\n"
                f"called listbox.bind with args ({gui.wx.EVT_LISTBOX_DCLICK}, {testobj.move_right})\n"
                f"called StaticText.__init__ with args ({testobj},)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'b_tag'}}\n"
                f"called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.move_right}) {{}}\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'b_untag'}}\n"
                f"called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.move_left}) {{}}\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'b_newtag'}}\n"
                f"called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.add_trefw}) {{}}\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'm_keys'}}\n"
                f"called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.keys_help}) {{}}\n"
                f"called ListBox.__init__ with args ({testobj},)\n"
                f"called listbox.bind with args ({gui.wx.EVT_LISTBOX_DCLICK}, {testobj.move_left})\n"
                "called dialog.create_actions\n"
                "called ListBox.InsertItems with args (['aa', 'bb'],)\n"
                "called ListBox.InsertItems with args ([],)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called StaticText.__init__ with args ({testobj},)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called hori sizer.Add with args <item> ()\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                "called vert sizer.AddStretchSpacer\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.AddSpacer with args (10,)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args <item> ()\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called StaticText.__init__ with args ({testobj},)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called hori sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> (0, 496, 10)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                "called dialog.createbuttons\n"
                "called vert sizer.Add with args <item> (0, 496, 10)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called dialog.SetSizer\n"
                "called dialog.SetAutoLayout\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout\n"
                'called dialog.SetSize\n')

    def test_init_2(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.init: calling with keywordi(s) already associated
        """
        def mock_init(self, *args):
            """stub
            """
            print('called wxDialog.__init__')
        def mock_SetTitle(self, *args):
            """stub
            """
            print('called dialog.SetTitle() with args', args)
        def mock_SetIcon(self, *args):
            """stub
            """
            print('called dialog.SetIcon() with args', args)
        def mock_createbuttons(self, *args):
            """stub
            """
            print('called dialog.createbuttons')
        # def mock_setaffirmativeid(self, *args):
        #     """stub
        #     """
        #     print('called dialog.SetAffirmativeId')
        def mock_setsizer(self, *args):
            """stub
            """
            print('called dialog.SetSizer')
        def mock_setautolayout(self, *args):
            """stub
            """
            print('called dialog.SetAutoLayout')
        def mock_setsize(self, *args):
            """stub
            """
            print('called dialog.SetSize')
        def mock_Layout(self, *args):
            """stub
            """
            print('called dialog.Layout')
        def mock_create_actions(self, *args):
            """stub
            """
            print('called dialog.create_actions')
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
        monkeypatch.setattr(gui.wx, 'BoxSizer', mockwx.MockBoxSizer)
        # monkeypatch.setattr(gui.wx, 'FlexGridSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(gui.wx, 'Button', mockwx.MockButton)
        monkeypatch.setattr(gui.wx, 'ListBox', mockwx.MockListBox)
        # monkeypatch.setattr(gui.wx, 'TextCtrl', mockwx.MockTextCtrl)
        monkeypatch.setattr(gui.KeywordsDialog, 'create_actions', mock_create_actions)
        testobj = gui.KeywordsDialog(mockparent, '', ['y'])
        assert hasattr(testobj, 'helptext')
        assert capsys.readouterr().out == (
                "called wxDialog.__init__\n"
                "called dialog.SetTitle() with args ('title - w_tags',)\n"
                "called dialog.SetIcon() with args ('icon',)\n"
                f"called ListBox.__init__ with args ({testobj},)\n"
                f"called listbox.bind with args ({gui.wx.EVT_LISTBOX_DCLICK}, {testobj.move_right})\n"
                f"called StaticText.__init__ with args ({testobj},)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'b_tag'}}\n"
                f"called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.move_right}) {{}}\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'b_untag'}}\n"
                f"called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.move_left}) {{}}\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'b_newtag'}}\n"
                f"called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.add_trefw}) {{}}\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'm_keys'}}\n"
                f"called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.keys_help}) {{}}\n"
                f"called ListBox.__init__ with args ({testobj},)\n"
                f"called listbox.bind with args ({gui.wx.EVT_LISTBOX_DCLICK}, {testobj.move_left})\n"
                "called dialog.create_actions\n"
                "called ListBox.InsertItems with args (['y'],)\n"
                "called ListBox.InsertItems with args (['x'],)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called StaticText.__init__ with args ({testobj},)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called hori sizer.Add with args <item> ()\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                "called vert sizer.AddStretchSpacer\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.AddSpacer with args (10,)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args <item> ()\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called StaticText.__init__ with args ({testobj},)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> ()\n"
                "called hori sizer.Add with args <item> ()\n"
                "called vert sizer.Add with args <item> (0, 496, 10)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                "called dialog.createbuttons\n"
                "called vert sizer.Add with args <item> (0, 496, 10)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called dialog.SetSizer\n"
                "called dialog.SetAutoLayout\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout\n"
                'called dialog.SetSize\n')

    def test_create_actions(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.create_actions
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
        def mock_set_accels(self, *args, **kwargs):
            """stub
            """
            print('called dialog.SetAcceleratorTable')
        def mock_fromstring(self, *args):
            print('called AcceleratorEntry.FromString with args', args)
            return False
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, 'SetAcceleratorTable', mock_set_accels)
        monkeypatch.setattr(gui.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(gui.wx, 'AcceleratorEntry', mockwx.MockAcceleratorEntry)
        monkeypatch.setattr(gui.wx, 'AcceleratorTable', mockwx.MockAcceleratorTable)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsDialog(mockparent, '')
        assert capsys.readouterr().out == 'called dialog.__init__\n'
        testobj.create_actions()
        assert capsys.readouterr().out == (
                'called MenuItem.__init__ with args ()\n'
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.activate_left})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+L',)\n"
                'called MenuItem.__init__ with args ()\n'
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.move_right})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+Right',)\n"
                'called MenuItem.__init__ with args ()\n'
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.activate_right})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+R',)\n"
                'called MenuItem.__init__ with args ()\n'
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.move_left})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+Left',)\n"
                'called MenuItem.__init__ with args ()\n'
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.add_trefw})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+N',)\n"
                'called AcceleratorTable.__init__ with 5 AcceleratorEntries\n'
                'called dialog.SetAcceleratorTable\n')
        monkeypatch.setattr(mockwx.MockAcceleratorEntry, 'FromString', mock_fromstring)
        testobj.create_actions()
        assert capsys.readouterr().out == (
                'called MenuItem.__init__ with args ()\n'
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.activate_left})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+L',)\n"
                'called MenuItem.__init__ with args ()\n'
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.move_right})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+Right',)\n"
                'called MenuItem.__init__ with args ()\n'
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.activate_right})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+R',)\n"
                'called MenuItem.__init__ with args ()\n'
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.move_left})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+Left',)\n"
                'called MenuItem.__init__ with args ()\n'
                f'called menuitem.Bind with args ({gui.wx.EVT_MENU}, {testobj.add_trefw})\n'
                'called menuitem.GetId\n'
                'called AcceleratorEntry.__init__ with args ()\n'
                "called AcceleratorEntry.FromString with args ('Ctrl+N',)\n"
                'called AcceleratorTable.__init__ with 0 AcceleratorEntries\n'
                'called dialog.SetAcceleratorTable\n')

    def test_activate_left(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate_left
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
        def mock_activate(self, *args):
            """stub
            """
            print(f'called dialog._activate(`{args[0]}`)')
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, '_activate', mock_activate)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.fromlist = 'fromlist'
        testobj.activate_left('event')
        assert capsys.readouterr().out == ('called dialog.__init__\n'
                                           'called dialog._activate(`fromlist`)\n')

    def test_activate_right(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate_right
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
        def mock_activate(self, *args):
            """stub
            """
            print(f'called dialog._activate(`{args[0]}`)')
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, '_activate', mock_activate)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.tolist = 'tolist'
        testobj.activate_right('event')
        assert capsys.readouterr().out == ('called dialog.__init__\n'
                                           'called dialog._activate(`tolist`)\n')

    def test_activate(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate: when list-to-activate can be activated
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog('parent', '')
        testobj._activate(mockwx.MockListBox())
        assert capsys.readouterr().out == ('called dialog.__init__\n'
                                           'called ListBox.__init__ with args ()\n'
                                           'called listbox.SetSelection with args (1,)\n'
                                           'called listbox.SetFocus\n')

    def test_activate_2(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate: nothing was previously selected
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(mockwx.MockListBox, 'GetSelections', lambda x: None)
        testobj = gui.KeywordsDialog('parent', '')
        testobj._activate(mockwx.MockListBox())
        assert capsys.readouterr().out == ('called dialog.__init__\n'
                                           'called ListBox.__init__ with args ()\n'
                                           'called listbox.SetSelection with args (0,)\n'
                                           'called listbox.SetFocus\n')

    def test_activate_3(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate: activating fromlist fails
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
        def mock_activate_left(self, *args, **kwargs):
            """stub
            """
            print('called dialog.activate_left')
        def mock_activate_right(self, *args, **kwargs):
            """stub
            """
            print('called dialog.activate_right')
        def mock_setselection(self, *args):
            """stub
            """
            raise gui.wx._core.wxAssertionError
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, 'activate_left', mock_activate_left)
        monkeypatch.setattr(gui.KeywordsDialog, 'activate_right', mock_activate_right)
        monkeypatch.setattr(mockwx.MockListBox, 'SetSelection', mock_setselection)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.fromlist = mockwx.MockListBox()
        testobj.tolist = mockwx.MockListBox()
        testobj._activate(testobj.fromlist)
        assert capsys.readouterr().out == ('called dialog.__init__\n'
                                           'called ListBox.__init__ with args ()\n'
                                           'called ListBox.__init__ with args ()\n'
                                           'called dialog.activate_right\n')

    def test_activate_4(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate: activating tolist fails
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
        def mock_activate_left(self, *args, **kwargs):
            """stub
            """
            print('called dialog.activate_left')
        def mock_activate_right(self, *args, **kwargs):
            """stub
            """
            print('called dialog.activate_right')
        def mock_setselection(self, *args):
            """stub
            """
            raise gui.wx._core.wxAssertionError
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, 'activate_left', mock_activate_left)
        monkeypatch.setattr(gui.KeywordsDialog, 'activate_right', mock_activate_right)
        monkeypatch.setattr(mockwx.MockListBox, 'SetSelection', mock_setselection)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.fromlist = mockwx.MockListBox()
        testobj.tolist = mockwx.MockListBox()
        testobj._activate(testobj.tolist)
        assert capsys.readouterr().out == ('called dialog.__init__\n'
                                           'called ListBox.__init__ with args ()\n'
                                           'called ListBox.__init__ with args ()\n'
                                           'called dialog.activate_left\n')

    def test_move_right(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.move_right
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
        def mock_moveitem(self, *args):
            """stub
            """
            print(f'called dialog._moveitem(`{args[0]}`, `{args[1]}`)')
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, '_moveitem', mock_moveitem)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.fromlist = 'fromlist'
        testobj.tolist = 'tolist'
        testobj.move_right('event')
        assert capsys.readouterr().out == ('called dialog.__init__\n'
                                           'called dialog._moveitem(`fromlist`, `tolist`)\n')

    def test_move_left(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.move_left
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
        def mock_moveitem(self, *args):
            """stub
            """
            print(f'called dialog._moveitem(`{args[0]}`, `{args[1]}`)')
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, '_moveitem', mock_moveitem)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.fromlist = 'fromlist'
        testobj.tolist = 'tolist'
        testobj.move_left('event')
        assert capsys.readouterr().out == ('called dialog.__init__\n'
                                           'called dialog._moveitem(`tolist`, `fromlist`)\n')

    def test_moveitem(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.moveitem
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
        def mock_sel():
            return []
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog('parent', '')
        from_ = mockwx.MockListBox()
        to = mockwx.MockListBox()
        testobj._moveitem(from_, to)
        assert capsys.readouterr().out == (
                'called dialog.__init__\n'
                'called ListBox.__init__ with args ()\n'
                'called ListBox.__init__ with args ()\n'
                'called listbox.Delete with args (1,)\n'
                'called listbox.GetCount\n'
                "called listbox.Insert with args (['value 1 from listbox'], None)\n")
        from_.GetSelections = mock_sel
        testobj._moveitem(from_, to)
        assert capsys.readouterr().out == ""

    def test_add_trefw(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.add_trefw: adding new keyword
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
            self.parent = args[0]
        def mock_textinit(self, *args, **kwargs):
            """stub
            """
            print('called TextDialog.__init__ with args', kwargs)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(mockwx.MockTextDialog, '__init__', mock_textinit)
        monkeypatch.setattr(gui.wx, 'TextEntryDialog', mockwx.MockTextDialog)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.tolist = mockwx.MockListBox()
        testobj.add_trefw('event')
        assert capsys.readouterr().out == ('called dialog.__init__\n'
                                           'called ListBox.__init__ with args ()\n'
                                           'called TextDialog.__init__ with args'
                                           " {'caption': 'title', 'message': 't_newtag'}\n"
                                           'called TextDialog.GetValue\n'
                                           "called listbox.Append with args ('entered value',)\n")

    def test_add_trefw_2(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.add_trefw: cancel adding new keyword
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
            self.parent = args[0]
        def mock_textinit(self, *args, **kwargs):
            """stub
            """
            print('called TextDialog.__init__ with args', kwargs)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(mockwx.MockTextDialog, '__init__', mock_textinit)
        monkeypatch.setattr(mockwx.MockTextDialog, 'ShowModal', lambda x: gui.wx.ID_CANCEL)
        monkeypatch.setattr(gui.wx, 'TextEntryDialog', mockwx.MockTextDialog)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.tolist = mockwx.MockListBox()
        testobj.add_trefw('event')
        assert capsys.readouterr().out == ('called dialog.__init__\n'
                                           'called ListBox.__init__ with args ()\n'
                                           'called TextDialog.__init__ with args'
                                           " {'caption': 'title', 'message': 't_newtag'}\n")

    def test_keys_help(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.keys_help
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
            self.parent = args[0]
            self.helptext = args[1]
        def mock_setaffirmativeid(self, *args):
            """stub
            """
            print('called dialog.SetAffirmativeId')
        def mock_settitle(self, *args):
            """stub
            """
            print('called dialog.SetTitle')
        def mock_setsizer(self, *args):
            """stub
            """
            print('called dialog.SetSizer')
        def mock_setautolayout(self, *args):
            """stub
            """
            print('called dialog.SetAutoLayout')
        def mock_showmodal(self, *args):
            """stub
            """
            print('called dialog.ShowModal')
        def mock_layout(self, *args):
            """stub
            """
            print('called dialog.Layout')
        def mock_lbl_init(self, *args, **kwargs):
            "stub"
            print('called StaticText.__init__ with args', '<dlg>', args[1:], kwargs)
        def mock_btn_init(self, *args, **kwargs):
            "stub"
            print('called Button.__init__ with args', '<dlg>', args[1:], kwargs)
        def mock_setsizer(self, *args):
            print(f"called dialog.SetSizer")
        def mock_fit(self , *args):
            print(f'called sizer.Fit')
        def mock_sizehints(self, *args):
            print(f'called sizer.SetSizeHints')
        monkeypatch.setattr(gui.wx.Dialog, 'SetAffirmativeId', mock_setaffirmativeid)
        monkeypatch.setattr(gui.wx.Dialog, 'SetTitle', mock_settitle)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_layout)
        monkeypatch.setattr(mockwx.MockDialog, 'ShowModal', mock_showmodal)
        monkeypatch.setattr(gui.wx, 'Dialog', mockwx.MockDialog)
        monkeypatch.setattr(mockwx.MockDialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(mockwx.MockBoxSizer, 'Fit', mock_fit)
        monkeypatch.setattr(mockwx.MockBoxSizer, 'SetSizeHints', mock_sizehints)
        monkeypatch.setattr(gui.wx, 'FlexGridSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(mockwx.MockStaticText, '__init__', mock_lbl_init)
        monkeypatch.setattr(gui.wx, 'Button', mockwx.MockButton)
        monkeypatch.setattr(mockwx.MockButton, '__init__', mock_btn_init)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog(mockparent, (('x', 'y'), ('a', 'b')))
        assert capsys.readouterr().out == 'called dialog.__init__\n'
        testobj.keys_help('event')
        assert capsys.readouterr().out == (
                'called Dialog.__init__() with args () {}\n'
                "called GridSizer.__init__ with args () {'cols': 2, 'vgap': 2, 'hgap': 25}\n"
                f"called StaticText.__init__ with args <dlg> () {{'label': 'x'}}\n"
                'called gridsizer.Add with args <item> (0,)\n'
                f"called StaticText.__init__ with args <dlg> () {{'label': 'y'}}\n"
                'called gridsizer.Add with args <item> (0,)\n'
                f"called StaticText.__init__ with args <dlg> () {{'label': 'a'}}\n"
                'called gridsizer.Add with args <item> (0,)\n'
                f"called StaticText.__init__ with args <dlg> () {{'label': 'b'}}\n"
                'called gridsizer.Add with args <item> (0,)\n'
                "called dialog.SetTitle with arg 'title t_keys'\n"
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                'called vert sizer.Add with args <item> (0, 240, 10)\n'
                f"called Button.__init__ with args <dlg> () {{'label': 'b_done'}}\n"
                'called Button.GetId\n'
                'called dialog.SetAffirmativeId with args (None,)\n'
                'called vert sizer.Add with args <item> (0, 496, 5)\n'
                'called dialog.SetSizer\n'
                'called dialog.SetAutoLayout with args (True,)\n'
                'called sizer.Fit\n'
                'called sizer.SetSizeHints\n'
                'called dialog.Layout with args ()\n'
                'called dialog.ShowModal\n')

    def test_confirm(self, monkeypatch):    # def accept(self):
        """unittest for KeywordsDialog.confirm
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called dialog.__init__')
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog('parent', '')
        testobj.tolist = mockwx.MockListBox()
        assert testobj.confirm() == ['items from listbox']


class TestKeywordsManager:
    """unittests for wx_gui.KeywordsManager
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for KeywordsManager.init
        """
        def mock_init(self, *args):
            """stub
            """
            print('called wxDialog.__init__')
        def mock_SetTitle(self, *args):
            """stub
            """
            print('called dialog.SetTitle() with args', args)
        def mock_SetIcon(self, *args):
            """stub
            """
            print('called dialog.SetIcon() with args', args)
        def mock_setaffirmativeid(self, *args):
            """stub
            """
            print('called dialog.SetAffirmativeId')
        def mock_setsizer(self, *args):
            """stub
            """
            print('called dialog.SetSizer')
        def mock_setautolayout(self, *args):
            """stub
            """
            print('called dialog.SetAutoLayout')
        def mock_SetSize(self, *args):
            """stub
            """
            print('called dialog.SetSize')
        def mock_Layout(self, *args):
            """stub
            """
            print('called dialog.Layout')
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
        monkeypatch.setattr(gui.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'FlexGridSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(gui.wx, 'Button', mockwx.MockButton)
        monkeypatch.setattr(gui.wx, 'ComboBox', mockwx.MockComboBox)
        monkeypatch.setattr(gui.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = gui.KeywordsManager(mockparent)
        assert capsys.readouterr().out == (
                'called wxDialog.__init__\n'
                "called dialog.SetTitle() with args ('title - t_tagman',)\n"
                "called dialog.SetIcon() with args ('icon',)\n"
                f'called ComboBox.__init__ with args ({testobj},) {{}}\n'
                f'called TextCtrl.__init__ with args ({testobj},) {{}}\n'
                'called combobox.clear\n'
                "called combobox.AppendItems with args (['x', 'y'],)\n"
                "called combobox.SetValue with args ('',)\n"
                'called text.Clear\n'
                f"called Button.__init__ with args ({testobj},) {{'label': 'b_remtag'}}\n"
                f'called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.remove_keyword}) {{}}\n'
                f"called Button.__init__ with args ({testobj},) {{'label': 'b_addtag'}}\n"
                f'called Button.Bind with args ({gui.wx.EVT_BUTTON}, {testobj.add_keyword}) {{}}\n'
                f"called Button.__init__ with args ({testobj},) {{'label': 'b_done'}}\n"
                'called Button.GetId\n'
                'called dialog.SetAffirmativeId\n'
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                "called GridSizer.__init__ with args () {'cols': 3}\n"
                f'called StaticText.__init__ with args ({testobj},)\n'
                'called gridsizer.Add with args <item> (0, 2288, 5)\n'
                'called gridsizer.Add with args <item> (0, 240, 5)\n'
                'called gridsizer.Add with args <item> (0, 240, 5)\n'
                f'called StaticText.__init__ with args ({testobj},)\n'
                'called gridsizer.Add with args <item> (0, 2288, 5)\n'
                'called gridsizer.Add with args <item> (0, 240, 5)\n'
                'called gridsizer.Add with args <item> (0, 240, 5)\n'
                'called vert sizer.Add with args <item> (240, 5)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                f'called StaticText.__init__ with args ({testobj},)\n'
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called vert sizer.Add with args <item> (0, 240, 5)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                'called hori sizer.Add with args <item> (0,)\n'
                'called vert sizer.Add with args <item> (0, 496, 5)\n'
                'called dialog.SetSizer\n'
                'called dialog.SetAutoLayout\n'
                f'called vert sizer.Fit with args ({testobj},)\n'
                f'called vert sizer.SetSizeHints with args ({testobj},)\n'
                'called dialog.Layout\n'
                'called dialog.SetSize\n')

    def test_refresh_fields(self, monkeypatch, capsys):
        """unittest for KeywordsManager.refresh_fields

        niet per se nodig omdat dit integraal tijdens de init uitgevoerd wordt
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called manager.__init__')
            self.parent = args[0]
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockwx.MockComboBox()
        testobj.newtag = mockwx.MockTextCtrl()
        testobj.refresh_fields()
        assert capsys.readouterr().out == ('called manager.__init__\n'
                                           'called ComboBox.__init__ with args () {}\n'
                                           'called TextCtrl.__init__ with args () {}\n'
                                           'called combobox.clear\n'
                                           "called combobox.AppendItems with args (['x', 'y'],)\n"
                                           "called combobox.SetValue with args ('',)\n"
                                           'called text.Clear\n')

    def test_update_items(self, monkeypatch, capsys):
        """unittest for KeywordsManager.update_items: update/remove unused keyword
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called manager.__init__')
            self.parent = args[0]
        def mock_GetFirstChild(self, *args):
            """stub
            """
            print('called tree.GetFirstChild')
            return first, 0
        def mock_GetNextChild(self, *args):
            """stub
            """
            cookie = args[1]
            print('called tree.GetNextChild')
            if cookie == 0:
                return item, 1
            return last, -1
        monkeypatch.setattr(mockwx.MockTree, 'GetFirstChild', mock_GetFirstChild)
        monkeypatch.setattr(mockwx.MockTree, 'GetNextChild', mock_GetNextChild)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        mockparent.tree = mockwx.MockTree()
        first = mockwx.MockTreeItem('first')
        last = mockwx.MockTreeItem('not ok')
        item = mockwx.MockTreeItem('activeitem')
        assert capsys.readouterr().out == ('called manager.__init__\n'
                                           'called Tree.__init__ with args ()\n'
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called TreeItem.__init__ with args ('not ok',)\n"
                                           "called TreeItem.__init__ with args ('activeitem',)\n")
        mockparent.root = 'root'
        testobj.update_items('oldtext')
        assert capsys.readouterr().out == (
                "called tree.GetFirstChild\n"
                "called TreeItem.IsOk\n"
                f"called tree.GetItemData with args ({first},)\n"
                "called tree.GetNextChild\n"
                "called TreeItem.IsOk\n"
                f"called tree.GetItemData with args ({item},)\n"
                'called tree.GetNextChild\n'
                "called TreeItem.IsOk\n")

    def test_update_items_2(self, monkeypatch, capsys):
        """unittest for KeywordsManager.update_items: remove keyword from items
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called manager.__init__')
            self.parent = args[0]
        def mock_GetFirstChild(self, *args):
            """stub
            """
            print('called tree.GetFirstChild')
            return first, 0
        def mock_GetNextChild(self, *args):
            """stub
            """
            cookie = args[1]
            print('called tree.GetNextChild')
            if cookie == 0:
                return item, 1
            return last, -1
        monkeypatch.setattr(mockwx.MockTree, 'GetFirstChild', mock_GetFirstChild)
        monkeypatch.setattr(mockwx.MockTree, 'GetNextChild', mock_GetNextChild)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        mockparent.tree = mockwx.MockTree()
        first = mockwx.MockTreeItem('first')
        last = mockwx.MockTreeItem('not ok')
        item = mockwx.MockTreeItem('activeitem')
        assert capsys.readouterr().out == ('called manager.__init__\n'
                                           'called Tree.__init__ with args ()\n'
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called TreeItem.__init__ with args ('not ok',)\n"
                                           "called TreeItem.__init__ with args ('activeitem',)\n")
        mockparent.root = 'root'
        testobj.update_items('keyword')
        assert capsys.readouterr().out == (
                'called tree.GetFirstChild\n'
                "called TreeItem.IsOk\n"
                f"called tree.GetItemData with args ({first},)\n"
                f"called tree.SetItemData() with args ({first}, ('itemkey', 'itemtext', []))\n"
                'called tree.GetNextChild\n'
                "called TreeItem.IsOk\n"
                f"called tree.GetItemData with args ({item},)\n"
                f"called tree.SetItemData() with args ({item}, ('itemkey', 'itemtext', []))\n"
                'called tree.GetNextChild\n'
                "called TreeItem.IsOk\n"
                )

    def test_update_items_3(self, monkeypatch, capsys):
        """unittest for KeywordsManager.update_items: update keyword in items
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called manager.__init__')
            self.parent = args[0]
        def mock_GetFirstChild(self, *args):
            """stub
            """
            print('called tree.GetFirstChild')
            return first, 0
        def mock_GetNextChild(self, *args):
            """stub
            """
            cookie = args[1]
            print('called tree.GetNextChild')
            if cookie == 0:
                return item, 1
            return last, -1
        monkeypatch.setattr(mockwx.MockTree, 'GetFirstChild', mock_GetFirstChild)
        monkeypatch.setattr(mockwx.MockTree, 'GetNextChild', mock_GetNextChild)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        mockparent.tree = mockwx.MockTree()
        first = mockwx.MockTreeItem('first')
        last = mockwx.MockTreeItem('not ok')
        item = mockwx.MockTreeItem('activeitem')
        assert capsys.readouterr().out == ('called manager.__init__\n'
                                           'called Tree.__init__ with args ()\n'
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called TreeItem.__init__ with args ('not ok',)\n"
                                           "called TreeItem.__init__ with args ('activeitem',)\n")
        mockparent.root = 'root'
        testobj.update_items('keyword', 'newtext')
        assert capsys.readouterr().out == (
                'called tree.GetFirstChild\n'
                "called TreeItem.IsOk\n"
                f"called tree.GetItemData with args ({first},)\n"
                "called tree.SetItemData() with args"
                f" ({first}, ('itemkey', 'itemtext', ['newtext']))\n"
                'called tree.GetNextChild\n'
                "called TreeItem.IsOk\n"
                f"called tree.GetItemData with args ({item},)\n"
                "called tree.SetItemData() with args"
                f" ({item}, ('itemkey', 'itemtext', ['newtext']))\n"
                'called tree.GetNextChild\n'
                "called TreeItem.IsOk\n"
                )

    def test_remove_keyword(self, monkeypatch, capsys):
        """unittest for KeywordsManager.remove_keyword: verwijderen doorvoeren
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called manager.__init__')
            self.parent = args[0]
        def mock_update(self, *args, **kwargs):
            """stub
            """
            print('called manager.update_items')
        def mock_refresh(self, *args, **kwargs):
            """stub
            """
            print('called manager.refresh_fields')
        def mock_messagebox(*args):
            """stub
            """
            print(f'called wx.MessageBox() with args `{args[0]}`, `{args[1]}`, `{args[2]}`')
            return gui.wx.YES
        monkeypatch.setattr(gui.wx, 'MessageBox', mock_messagebox)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        monkeypatch.setattr(gui.KeywordsManager, 'update_items', mock_update)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        monkeypatch.setattr(mockwx.MockComboBox, 'GetValue', lambda x: 'x')
        testobj.oldtag = mockwx.MockComboBox()
        testobj.remove_keyword('event')
        flags = gui.wx.YES_NO | gui.wx.ICON_QUESTION
        assert capsys.readouterr().out == ('called manager.__init__\n'
                                           'called ComboBox.__init__ with args () {}\n'
                                           'called wx.MessageBox() with args'
                                           f" `t_remtag`, `title`, `{flags}`\n"
                                           'called manager.update_items\n'
                                           'called manager.refresh_fields\n')

    def test_remove_keyword_2(self, monkeypatch, capsys):
        """unittest for KeywordsManager.remove_keyword: voor verwijderen afbreken
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called manager.__init__')
            self.parent = args[0]
        def mock_update(self, *args, **kwargs):
            """stub
            """
            print('called manager.update_items')
        def mock_refresh(self, *args, **kwargs):
            """stub
            """
            print('called manager.refresh_fields')
        def mock_messagebox(*args):
            """stub
            """
            print(f'called wx.MessageBox() with args `{args[0]}`, `{args[1]}`, `{args[2]}`')
            return gui.wx.NO
        monkeypatch.setattr(gui.wx, 'MessageBox', mock_messagebox)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        monkeypatch.setattr(gui.KeywordsManager, 'update_items', mock_update)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        monkeypatch.setattr(mockwx.MockComboBox, 'GetValue', lambda x: 'x')
        testobj.oldtag = mockwx.MockComboBox()
        testobj.remove_keyword('event')
        flags = gui.wx.YES_NO | gui.wx.ICON_QUESTION
        assert capsys.readouterr().out == ('called manager.__init__\n'
                                           'called ComboBox.__init__ with args () {}\n'
                                           'called wx.MessageBox() with args'
                                           f" `t_remtag`, `title`, `{flags}`\n")

    def test_add_keyword(self, monkeypatch, capsys):
        """unittest for KeywordsManager.add_keyword: adding keyword
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called manager.__init__')
            self.parent = args[0]
        # def mock_update(self, *args, **kwargs):
        #    print('called manager.update_items')
        def mock_refresh(self, *args, **kwargs):
            """stub
            """
            print('called manager.refresh_fields')
        def mock_messagebox(*args):
            """stub
            """
            print(f'called wx.MessageBox() with args `{args[0]}`, `{args[1]}`, `{args[2]}`')
            return gui.wx.YES
        monkeypatch.setattr(gui.wx, 'MessageBox', mock_messagebox)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockwx.MockComboBox()
        monkeypatch.setattr(testobj.oldtag, 'GetValue', lambda: '')
        testobj.newtag = mockwx.MockComboBox()
        monkeypatch.setattr(testobj.newtag, 'GetValue', lambda: 'z')
        assert capsys.readouterr().out == ('called manager.__init__\n'
                                           'called ComboBox.__init__ with args () {}\n'
                                           'called ComboBox.__init__ with args () {}\n')
        testobj.add_keyword('event')
        assert testobj.parent.base.opts['Keywords'] == ['x', 'y', 'z']
        flags = gui.wx.YES_NO | gui.wx.ICON_QUESTION
        assert capsys.readouterr().out == (
                                           'called wx.MessageBox() with args'
                                           f" `t_addtag`, `title`, `{flags}`\n"
                                           'called manager.refresh_fields\n')

    def test_add_keyword_2(self, monkeypatch, capsys):
        """unittest for KeywordsManager.add_keyword: cancel adding keyword
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called manager.__init__')
            self.parent = args[0]
        def mock_refresh(self, *args, **kwargs):
            """stub
            """
            print('called manager.refresh_fields')
        def mock_messagebox(*args):
            """stub
            """
            print(f'called wx.MessageBox() with args `{args[0]}`, `{args[1]}`, `{args[2]}`')
            return gui.wx.NO
        monkeypatch.setattr(gui.wx, 'MessageBox', mock_messagebox)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockwx.MockComboBox()
        monkeypatch.setattr(testobj.oldtag, 'GetValue', lambda: '')
        testobj.newtag = mockwx.MockComboBox()
        monkeypatch.setattr(testobj.newtag, 'GetValue', lambda: 'z')
        assert capsys.readouterr().out == ('called manager.__init__\n'
                                           'called ComboBox.__init__ with args () {}\n'
                                           'called ComboBox.__init__ with args () {}\n')
        testobj.add_keyword('event')
        assert testobj.parent.base.opts['Keywords'] == ['x', 'y']
        flags = gui.wx.YES_NO | gui.wx.ICON_QUESTION
        assert capsys.readouterr().out == ('called wx.MessageBox() with args'
                                           f" `t_addtag`, `title`, `{flags}`\n")

    def test_add_keyword_3(self, monkeypatch, capsys):
        """unittest for KeywordsManager.add_keyword: cancel replacing keyword
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called manager.__init__')
            self.parent = args[0]
        def mock_showmodal(self):
            """stub
            """
            return gui.wx.ID_CANCEL
        def mock_refresh(self, *args, **kwargs):
            """stub
            """
            print('called manager.refresh_fields')
        monkeypatch.setattr(gui.wx, 'MessageDialog', mockwx.MockMessageDialog)
        monkeypatch.setattr(gui.wx.MessageDialog, 'ShowModal', mock_showmodal)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockwx.MockComboBox()
        monkeypatch.setattr(testobj.oldtag, 'GetValue', lambda: 'y')
        testobj.newtag = mockwx.MockComboBox()
        monkeypatch.setattr(testobj.newtag, 'GetValue', lambda: 'z')
        assert capsys.readouterr().out == ('called manager.__init__\n'
                                           'called ComboBox.__init__ with args () {}\n'
                                           'called ComboBox.__init__ with args () {}\n')
        testobj.add_keyword('event')
        assert testobj.parent.base.opts['Keywords'] == ['x', 'y']
        assert capsys.readouterr().out == (
                f"called MessageDialog.__init__ with args ({testobj}, 't_repltag')\n"
                "called MessageDialog.SetExtendedMessage with args ('t_repltag2',)\n")

    def test_add_keyword_4(self, monkeypatch, capsys):
        """unittest for KeywordsManager.add_keyword: replace keyword, also in tree items
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called manager.__init__')
            self.parent = args[0]
        def mock_showmodal(self):
            """stub
            """
            return gui.wx.ID_YES
        def mock_update(self, *args, **kwargs):
            """stub
            """
            print('called manager.update_items() with args', args)
        def mock_refresh(self, *args, **kwargs):
            """stub
            """
            print('called manager.refresh_fields')
        monkeypatch.setattr(gui.wx, 'MessageDialog', mockwx.MockMessageDialog)
        monkeypatch.setattr(gui.wx.MessageDialog, 'ShowModal', mock_showmodal)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'update_items', mock_update)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockwx.MockComboBox()
        monkeypatch.setattr(testobj.oldtag, 'GetValue', lambda: 'y')
        testobj.newtag = mockwx.MockComboBox()
        monkeypatch.setattr(testobj.newtag, 'GetValue', lambda: 'z')
        assert capsys.readouterr().out == ('called manager.__init__\n'
                                           'called ComboBox.__init__ with args () {}\n'
                                           'called ComboBox.__init__ with args () {}\n')
        testobj.add_keyword('event')
        assert testobj.parent.base.opts['Keywords'] == ['x', 'z']
        assert capsys.readouterr().out == (
                f"called MessageDialog.__init__ with args ({testobj}, 't_repltag')\n"
                "called MessageDialog.SetExtendedMessage with args ('t_repltag2',)\n"
                "called manager.update_items() with args ('y', 'z')\n"
                'called manager.refresh_fields\n')

    def test_add_keyword_5(self, monkeypatch, capsys):
        """unittest for KeywordsManager.add_keyword: replace keyword, deleting from tree items
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called manager.__init__')
            self.parent = args[0]
        def mock_showmodal(self):
            """stub
            """
            return gui.wx.ID_NO
        def mock_update(self, *args, **kwargs):
            """stub
            """
            print('called manager.update_items() with args', args)
        def mock_refresh(self, *args, **kwargs):
            """stub
            """
            print('called manager.refresh_fields')
        monkeypatch.setattr(gui.wx, 'MessageDialog', mockwx.MockMessageDialog)
        monkeypatch.setattr(gui.wx.MessageDialog, 'ShowModal', mock_showmodal)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsManager, 'update_items', mock_update)
        monkeypatch.setattr(gui.KeywordsManager, 'refresh_fields', mock_refresh)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockwx.MockComboBox()
        monkeypatch.setattr(testobj.oldtag, 'GetValue', lambda: 'y')
        testobj.newtag = mockwx.MockComboBox()
        monkeypatch.setattr(testobj.newtag, 'GetValue', lambda: 'z')
        assert capsys.readouterr().out == ('called manager.__init__\n'
                                           'called ComboBox.__init__ with args () {}\n'
                                           'called ComboBox.__init__ with args () {}\n')
        testobj.add_keyword('event')
        assert testobj.parent.base.opts['Keywords'] == ['x', 'z']
        assert capsys.readouterr().out == (
                f"called MessageDialog.__init__ with args ({testobj}, 't_repltag')\n"
                "called MessageDialog.SetExtendedMessage with args ('t_repltag2',)\n"
                "called manager.update_items() with args ('y',)\n"
                'called manager.refresh_fields\n')

    def _test_confirm(self):
        """not implemented, so no test needed
        """


class TestGetTextDialog:
    """unittests for wx_gui.GetTextDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for GetTextDialog.init
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called wxDialog.__init__')
        def mock_createbuttons(self, *args):
            """stub
            """
            print('called dialog.CreateButtonSizer')
        def mock_settitle(self, *args):
            """stub
            """
            print('called dialog.SetTitle')
        def mock_seticon(self, *args):
            """stub
            """
            print('called dialog.SetIcon')
        def mock_setsizer(self, *args):
            """stub
            """
            print('called dialog.SetSizer')
        def mock_setautolayout(self, *args):
            """stub
            """
            print('called dialog.SetAutoLayout')
        def mock_layout(self, *args):
            """stub
            """
            print('called dialog.Layout')
        def mock_inputwin(self, *args):
            """stub
            """
            print('called dialog.create_inputwin')
            self.inputwin = mockwx.MockTextCtrl()
            self.use_case = mockwx.MockCheckBox()
        def mock_inputwin_2(self, *args):
            """stub
            """
            print('called dialog.create_inputwin')
            self.inputwin = mockwx.MockTextCtrl()
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'SetTitle', mock_settitle)
        monkeypatch.setattr(gui.wx.Dialog, 'SetIcon', mock_seticon)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'CreateButtonSizer', mock_createbuttons)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_layout)
        monkeypatch.setattr(gui.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'FlexGridSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(gui.wx, 'CheckBox', mockwx.MockCheckBox)
        monkeypatch.setattr(gui.wx, 'TextCtrl', mockwx.MockTextCtrl)
        monkeypatch.setattr(gui.wx, 'Icon', mockwx.MockIcon)
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.GetTextDialog, 'create_inputwin', mock_inputwin)
        testobj = gui.GetTextDialog(mockparent, 0, 'seltext', 'labeltext', True)
        assert testobj.parent == mockparent
        assert hasattr(testobj, 'in_exclude')
        assert hasattr(testobj, 'inputwin')
        assert hasattr(testobj, 'use_case')
        assert capsys.readouterr().out == (
                'called wxDialog.__init__\n'
                'called dialog.SetTitle\n'
                'called dialog.SetIcon\n'
                'called dialog.create_inputwin\n'
                'called TextCtrl.__init__ with args () {}\n'
                'called CheckBox.__init__ with args () {}\n'
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'exclude'}}\n"
                'called checkbox.SetValue with args (False,)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                f'called StaticText.__init__ with args ({testobj},)\n'
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called vert sizer.Add with args <item> (0, 240, 5)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                'called hori sizer.Add with args <item> (1, 240, 5)\n'
                'called vert sizer.Add with args <item> (1, 240, 5)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called checkbox.SetValue with args (True,)\n'
                'called vert sizer.Add with args <item> (0, 240, 5)\n'
                'called dialog.CreateButtonSizer\n'
                'called vert sizer.Add with args <item> (0, 496, 10)\n'
                'called dialog.SetSizer\n'
                'called dialog.SetAutoLayout\n'
                f'called vert sizer.Fit with args ({testobj},)\n'
                f'called vert sizer.SetSizeHints with args ({testobj},)\n'
                'called dialog.Layout\n')

        testobj = gui.GetTextDialog(mockparent, 0, 'seltext', 'labeltext')
        assert testobj.parent == mockparent
        assert hasattr(testobj, 'in_exclude')
        assert hasattr(testobj, 'inputwin')
        assert hasattr(testobj, 'use_case')
        assert capsys.readouterr().out == (
                'called wxDialog.__init__\n'
                'called dialog.SetTitle\n'
                'called dialog.SetIcon\n'
                'called dialog.create_inputwin\n'
                'called TextCtrl.__init__ with args () {}\n'
                'called CheckBox.__init__ with args () {}\n'
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'exclude'}}\n"
                'called checkbox.SetValue with args (False,)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                f'called StaticText.__init__ with args ({testobj},)\n'
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called vert sizer.Add with args <item> (0, 240, 5)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                'called hori sizer.Add with args <item> (1, 240, 5)\n'
                'called vert sizer.Add with args <item> (1, 240, 5)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called vert sizer.Add with args <item> (0, 240, 5)\n'
                'called dialog.CreateButtonSizer\n'
                'called vert sizer.Add with args <item> (0, 496, 10)\n'
                'called dialog.SetSizer\n'
                'called dialog.SetAutoLayout\n'
                f'called vert sizer.Fit with args ({testobj},)\n'
                f'called vert sizer.SetSizeHints with args ({testobj},)\n'
                'called dialog.Layout\n')
        monkeypatch.setattr(gui.GetTextDialog, 'create_inputwin', mock_inputwin_2)
        testobj = gui.GetTextDialog(mockparent, 0, 'seltext', 'labeltext')
        assert testobj.parent == mockparent
        assert hasattr(testobj, 'in_exclude')
        assert hasattr(testobj, 'inputwin')
        assert hasattr(testobj, 'use_case')
        assert capsys.readouterr().out == (
                'called wxDialog.__init__\n'
                'called dialog.SetTitle\n'
                'called dialog.SetIcon\n'
                'called dialog.create_inputwin\n'
                'called TextCtrl.__init__ with args () {}\n'
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'exclude'}}\n"
                'called checkbox.SetValue with args (False,)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                f'called StaticText.__init__ with args ({testobj},)\n'
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called vert sizer.Add with args <item> (0, 240, 5)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                'called hori sizer.Add with args <item> (1, 240, 5)\n'
                'called vert sizer.Add with args <item> (1, 240, 5)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called vert sizer.Add with args <item> (0, 240, 5)\n'
                'called dialog.CreateButtonSizer\n'
                'called vert sizer.Add with args <item> (0, 496, 10)\n'
                'called dialog.SetSizer\n'
                'called dialog.SetAutoLayout\n'
                f'called vert sizer.Fit with args ({testobj},)\n'
                f'called vert sizer.SetSizeHints with args ({testobj},)\n'
                'called dialog.Layout\n')

    def test_init_2(self, monkeypatch, capsys):
        """unittest for GetTextDialog.init
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called wxDialog.__init__')
        def mock_createbuttons(self, *args):
            """stub
            """
            print('called dialog.CreateButtonSizer')
        def mock_settitle(self, *args):
            """stub
            """
            print('called dialog.SetTitle')
        def mock_seticon(self, *args):
            """stub
            """
            print('called dialog.SetIcon')
        def mock_setsizer(self, *args):
            """stub
            """
            print('called dialog.SetSizer')
        def mock_setautolayout(self, *args):
            """stub
            """
            print('called dialog.SetAutoLayout')
        def mock_layout(self, *args):
            """stub
            """
            print('called dialog.Layout')
        def mock_inputwin(self, *args):
            """stub
            """
            print('called dialog.create_inputwin')
            self.inputwin = mockwx.MockTextCtrl()
            self.use_case = mockwx.MockCheckBox()
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'SetTitle', mock_settitle)
        monkeypatch.setattr(gui.wx.Dialog, 'SetIcon', mock_seticon)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'CreateButtonSizer', mock_createbuttons)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_layout)
        monkeypatch.setattr(gui.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'FlexGridSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(gui.wx, 'CheckBox', mockwx.MockCheckBox)
        monkeypatch.setattr(gui.wx, 'TextCtrl', mockwx.MockTextCtrl)
        monkeypatch.setattr(gui.wx, 'Icon', mockwx.MockIcon)
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.GetTextDialog, 'create_inputwin', mock_inputwin)
        testobj = gui.GetTextDialog(mockparent, -1, 'seltext', 'labeltext', False)
        assert testobj.parent == mockparent
        assert hasattr(testobj, 'in_exclude')
        assert hasattr(testobj, 'inputwin')
        assert hasattr(testobj, 'use_case')
        assert capsys.readouterr().out == (
                'called wxDialog.__init__\n'
                'called dialog.SetTitle\n'
                'called dialog.SetIcon\n'
                'called dialog.create_inputwin\n'
                'called TextCtrl.__init__ with args () {}\n'
                'called CheckBox.__init__ with args () {}\n'
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'exclude'}}\n"
                'called checkbox.SetValue with args (False,)\n'
                'called checkbox.SetValue with args (True,)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                f'called StaticText.__init__ with args ({testobj},)\n'
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called vert sizer.Add with args <item> (0, 240, 5)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                'called hori sizer.Add with args <item> (1, 240, 5)\n'
                'called vert sizer.Add with args <item> (1, 240, 5)\n'
                f"called BoxSizer.__init__ with args ({gui.wx.HORIZONTAL},)\n"
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called vert sizer.Add with args <item> (0, 240, 5)\n'
                'called dialog.CreateButtonSizer\n'
                'called vert sizer.Add with args <item> (0, 496, 10)\n'
                'called dialog.SetSizer\n'
                'called dialog.SetAutoLayout\n'
                f'called vert sizer.Fit with args ({testobj},)\n'
                f'called vert sizer.SetSizeHints with args ({testobj},)\n'
                'called dialog.Layout\n')

    def test_create_inputwin(self, monkeypatch, capsys):
        """unittest for GetTextDialog.create_inputwin
        """
        def mock_init(self, *args):
            """stub
            """
            print('called textdialog.__init__')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx, 'CheckBox', mockwx.MockCheckBox)
        monkeypatch.setattr(gui.wx, 'TextCtrl', mockwx.MockTextCtrl)
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.GetTextDialog(mockparent)  # , 0, 'seltext', 'labeltext', True)
        testobj.create_inputwin('seltext')
        assert hasattr(testobj, 'inputwin')
        assert hasattr(testobj, 'use_case')
        assert capsys.readouterr().out == (
                'called textdialog.__init__\n'
                f"called TextCtrl.__init__ with args ({testobj},) {{'value': 'seltext'}}\n"
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'case sensitive'}}\n"
                'called checkbox.SetValue with args (False,)\n')

    def test_confirm(self, monkeypatch):
        """unittest for GetTextDialog.confirm
        """
        def mock_init(self, *args):
            """stub
            """
            print('called textdialog.__init__')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.GetTextDialog(mockparent, 0, 'seltext', 'labeltext', True)
        testobj.in_exclude = mockwx.MockCheckBox()
        testobj.inputwin = mockwx.MockTextCtrl()
        testobj.use_case = mockwx.MockCheckBox()
        assert testobj.confirm() == ['value from checkbox', 'value from textctrl',
                                     'value from checkbox']


class TestGetItemDialog:
    """unittests for wx_gui.GetItemDialog
    """
    def test_create_inputwin(self, monkeypatch, capsys):
        """unittest for GetItemDialog.create_inputwin
        """
        def mock_init(self, *args):
            """stub
            """
            print('called textdialog.__init__')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx, 'ComboBox', mockwx.MockComboBox)
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.GetItemDialog(mockparent, 0, 'seltext', 'labeltext', True)
        testobj.create_inputwin((['sel1', 'sel2'], 1))
        assert hasattr(testobj, 'inputwin')
        assert capsys.readouterr().out == (
                'called textdialog.__init__\n'
                f"called ComboBox.__init__ with args ({testobj},) {{'choices': ['sel1', 'sel2']}}\n"
                'called combobox.SetSelection with args (1,)\n')

    def test_confirm(self, monkeypatch):
        """unittest for GetItemDialog.confirm
        """
        def mock_init(self, *args):
            """stub
            """
            print('called textdialog.__init__')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        testobj = gui.GetItemDialog(mockparent, 0, 'seltext', 'labeltext', True)
        testobj.in_exclude = mockwx.MockCheckBox()
        testobj.inputwin = mockwx.MockComboBox()
        assert testobj.confirm() == ['value from checkbox', 'value from combobox']


class TestGridDialog:
    """unittests for wx_gui.GridDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for GridDialog.init
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called wxDialog.__init__')
        def mock_createbuttons(self, *args):
            """stub
            """
            print('called dialog.CreateButtonSizer')
        def mock_setsizer(self, *args):
            """stub
            """
            print('called dialog.SetSizer')
        def mock_setautolayout(self, *args):
            """stub
            """
            print('called dialog.SetAutoLayout')
        def mock_layout(self, *args):
            """stub
            """
            print('called dialog.Layout')
        monkeypatch.setattr(gui.wx.Dialog, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.Dialog, 'SetSizer', mock_setsizer)
        monkeypatch.setattr(gui.wx.Dialog, 'CreateButtonSizer', mock_createbuttons)
        monkeypatch.setattr(gui.wx.Dialog, 'SetAutoLayout', mock_setautolayout)
        monkeypatch.setattr(gui.wx.Dialog, 'Layout', mock_layout)
        monkeypatch.setattr(gui.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(gui.wx, 'FlexGridSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(gui.wx, 'StaticText', mockwx.MockStaticText)
        testobj = gui.GridDialog('parent', (('1', '2'), ('3', '4')), 'title')
        assert capsys.readouterr().out == (
                'called wxDialog.__init__\n'
                f"called BoxSizer.__init__ with args ({gui.wx.VERTICAL},)\n"
                "called GridSizer.__init__ with args () {'cols': 2}\n"
                f'called StaticText.__init__ with args ({testobj},)\n'
                'called gridsizer.Add with args <item> ()\n'
                f'called StaticText.__init__ with args ({testobj},)\n'
                'called gridsizer.Add with args <item> ()\n'
                f'called StaticText.__init__ with args ({testobj},)\n'
                'called gridsizer.Add with args <item> ()\n'
                f'called StaticText.__init__ with args ({testobj},)\n'
                'called gridsizer.Add with args <item> ()\n'
                'called vert sizer.Add with args <item> (0, 8432, 5)\n'
                'called dialog.CreateButtonSizer\n'
                'called vert sizer.Add with args <item> ()\n'
                'called dialog.SetSizer\n'
                'called dialog.SetAutoLayout\n'
                f'called vert sizer.Fit with args ({testobj},)\n'
                f'called vert sizer.SetSizeHints with args ({testobj},)\n'
                'called dialog.Layout\n')

    def confirm(self):  # te testen methode niet geïmplementeerd
        """stub
        """


class TestTaskbarIcon:
    """unittests for wx_gui.TaskbarIcon
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for TaskbarIcon.init
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called trayicon.__init__')
        def mock_seticon(self, *args, **kwargs):
            """stub
            """
            print('called trayicon.SetIcon')
        def mock_bind(self, *args, **kwargs):
            """stub
            """
            print('called trayicon.Bind')
        monkeypatch.setattr(gui.wx.adv.TaskBarIcon, '__init__', mock_init)
        monkeypatch.setattr(gui.wx.adv.TaskBarIcon, 'SetIcon', mock_seticon)
        monkeypatch.setattr(gui.wx.adv.TaskBarIcon, 'Bind', mock_bind)
        monkeypatch.setattr(gui.wx, 'Icon', mockwx.MockIcon)
        mockparent = setup_mainwindow(monkeypatch, capsys)
        mockparent.nt_icon = gui.wx.Icon()
        mockparent.revive = lambda x: 'revive'
        gui.TaskbarIcon(mockparent)
        assert capsys.readouterr().out == ('called Icon.__init__ with args ()\n'
                                           'called trayicon.__init__\n'
                                           'called trayicon.SetIcon\n'
                                           'called trayicon.Bind\n'
                                           'called trayicon.Bind\n')

    def test_createpopupmenu(self, monkeypatch, capsys):
        """unittest for TaskbarIcon.createpopupmenu
        """
        def mock_init(self, *args, **kwargs):
            """stub
            """
            print('called trayicon.__init__')
        monkeypatch.setattr(gui.wx, 'Menu', mockwx.MockMenu)
        monkeypatch.setattr(gui.TaskbarIcon, '__init__', mock_init)
        mockparent = setup_mainwindow(monkeypatch, capsys)
        testobj = gui.TaskbarIcon(mockparent)
        menu = testobj.CreatePopupMenu()
        assert isinstance(menu, gui.wx.Menu)
        assert capsys.readouterr().out == (
                'called trayicon.__init__\n'
                'called Menu.__init__ with args ()\n'
                f"called menu.Append with args ({testobj.id_revive}, 'Revive NoteTree')\n")
