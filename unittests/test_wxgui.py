"""unittests for ./notetree/wx_gui.py
"""
import types
from mockgui import mockwxwidgets as mockwx
from notetree import wx_gui as testee


def setup_mainwindow(monkeypatch, capsys):
    """stub for setting up MainWindow object
    """
    monkeypatch.setattr(testee.wx, 'Frame', mockwx.MockFrame)
    monkeypatch.setattr(testee.wx, 'App', mockwx.MockApp)
    testobj = testee.MainWindow(MockNoteTree())
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
        monkeypatch.setattr(testee.wx.Frame, '__init__', mock_init)
        monkeypatch.setattr(testee.wx, 'Icon', mockwx.MockIcon)
        monkeypatch.setattr(testee.wx.Frame, 'SetIcon', mock_seticon)
        monkeypatch.setattr(testee.wx, 'MenuBar', mockwx.MockMenuBar)
        monkeypatch.setattr(testee.wx.Frame, 'SetMenuBar', mock_setmenubar)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.init_screen(title='title', iconame='ico')
        assert capsys.readouterr().out == ('called frame.__init__\n'
                                           "called Icon.__init__ with args ('ico', 3)\n"
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
        monkeypatch.setattr(testee.wx.Frame, 'CreateStatusBar', mock_createstatusbar)
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
        monkeypatch.setattr(testee.wx, 'SplitterWindow', mockwx.MockSplitter)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.setup_split_screen()
        assert capsys.readouterr().out == (
                f'called Splitter.__init__ with args ({testobj},) {{}}\n'
                'called splitter.SetMinimumPaneSize with args (1,)\n')

    def test_setup_tree(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_tree
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.splitter = 'splitter'
        monkeypatch.setattr(testee.wx, 'TreeCtrl', mockwx.MockTree)
        tree = testobj.setup_tree()
        # assert tree == testobj.tree
        assert hasattr(testobj, 'root')
        assert capsys.readouterr().out == (
                "called Tree.__init__ with args ('splitter',) {}\n"
                "called tree.AddRoot with args ('title',)\n"
                "called tree.Bind with args"
                f" ({testee.wx.EVT_TREE_SEL_CHANGING}, {testobj.OnSelChanging})\n"
                "called tree.Bind with args"
                f" ({testee.wx.EVT_TREE_SEL_CHANGED}, {testobj.OnSelChanged})\n")

    def test_setup_editor(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_editor
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.splitter = 'splitter'
        monkeypatch.setattr(testee.stc, 'StyledTextCtrl', mockwx.MockEditor)
        monkeypatch.setattr(testee.wx, 'Font', mockwx.MockFont)
        editor = testobj.setup_editor()
        # assert editor == testobj.editor
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
                f"called editor.Bind with args ({testee.wx.EVT_TEXT}, {testobj.OnEvtText})\n")

    def test_finish_screen(self, monkeypatch, capsys):
        """unittest for MainWindow.finish_screen
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
        testobj = setup_mainwindow(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'Show', mock_show)
        testobj.splitter = mockwx.MockSplitter()
        testobj.tree = mockwx.MockTree()
        testobj.editor = mockwx.MockEditor()
        assert capsys.readouterr().out == (
                f'called Splitter.__init__ with args ({testobj},) {{}}\n'
                "called Tree.__init__ with args ('splitter',) {}\n"
                "called Editor.__init__ with args ('splitter',)\n")
        testobj.finish_screen()
        assert capsys.readouterr().out == (
                f"called splitter.SplitVertically with args ({testobj.tree}, {testobj.editor})\n"
                'called splitter.SetSashPosition with args (180, True)\n'
                f'called app.SetTopWindow with args ({testobj},)\n'
                'called MainWindow.Show\n')

    def setup_text(self):
        """stub

        wordt uiitgevoerd als onderdeel van setup_editor, dus geen aparte test nodig
        """

    # tbv apart testen nieuwe opgeknipte versie
    def _test_create_menu(self, monkeypatch, capsys):
        """unittest for MainWindow.create_menu
        """
        def callback():
            "dummy callback, just for reference"
        def mock_getmenubar(*args):
            print('called MainWindow.GetMenuBar')
            return mockwx.MockMenuBar()
        def mock_get_menudata(self, *args):
            return ()
        def mock_get_menudata_2(self, *args):
            return (('menutitle', ()),)
        def mock_get_menudata_3(self, *args):
            return (('menutitle', (('menuitem', callback, 'iteminfo', 'keydef'),),),)
        def mock_menubar_append(self, *args):
            print(f'called menubar.Append with args (<menu>, {args[1]})')
        def mock_menu_append(self, *args):
            print('called menu.Append with arg <menuitem>')
        def mock_create_item(self, *args):
            print('called MainWindow.create_menuitem')
        def mock_create_accel(self, *args):
            print('called MainWindow.create_accelerator')
            return []
        def mock_set_accel(self, *args):
            print('called mainwindow.SetAcceleratorTable')
        monkeypatch.setattr(mockwx.MockMenuBar, 'GetMenus', lambda x: [])
        monkeypatch.setattr(MockNoteTree, 'get_menudata', mock_get_menudata)
        monkeypatch.setattr(mockwx.MockMenuBar, 'Append', mock_menubar_append)
        # monkeypatch.setattr(mockwx.MockMenuBar, 'Replace', mock_menubar_replace)
        monkeypatch.setattr(mockwx.MockMenu, 'Append', mock_menu_append)
        monkeypatch.setattr(testee.wx, 'Menu', mockwx.MockMenu)
        monkeypatch.setattr(testee.wx, 'AcceleratorTable', mockwx.MockAcceleratorTable)
        testobj = setup_mainwindow(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'GetMenuBar', mock_getmenubar)
        monkeypatch.setattr(testobj, 'create_menuitem', mock_create_item)
        monkeypatch.setattr(testobj, 'create_accelerators', mock_create_accel)
        monkeypatch.setattr(testobj, 'SetAcceleratorTable', mock_set_accel)
        testobj.base.opts['RevOrder'] = True
        testobj.base.opts['Selection'] = (1, True)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == 'called Tree.__init__ with args () {}\n'
        testobj.create_menu()
        assert not testobj.selactions
        assert not testobj.seltypes
        assert capsys.readouterr().out == (
                "called MainWindow.GetMenuBar\n"
                "called MenuBar.__init__ with args ()\n"
                "called AcceleratorTable.__init__ with 0 AcceleratorEntries\n"
                "called mainwindow.SetAcceleratorTable\n")
        monkeypatch.setattr(MockNoteTree, 'get_menudata', mock_get_menudata_2)
        testobj.create_menu()
        assert not testobj.selactions
        assert not testobj.seltypes
        assert capsys.readouterr().out == (
                "called MainWindow.GetMenuBar\n"
                "called MenuBar.__init__ with args ()\n"
                "called Menu.__init__ with args ()\n"
                "called menubar.Append with args (<menu>, menutitle)\n"
                "called AcceleratorTable.__init__ with 0 AcceleratorEntries\n"
                "called mainwindow.SetAcceleratorTable\n")
        monkeypatch.setattr(MockNoteTree, 'get_menudata', mock_get_menudata_3)
        testobj.create_menu()
        assert not testobj.selactions
        assert not testobj.seltypes
        assert capsys.readouterr().out == (
                "called MainWindow.GetMenuBar\n"
                "called MenuBar.__init__ with args ()\n"
                "called Menu.__init__ with args ()\n"
                "called MainWindow.create_menuitem\n"
                "called menu.Append with arg <menuitem>\n"
                "called MainWindow.create_accelerator\n"
                "called menubar.Append with args (<menu>, menutitle)\n"
                "called AcceleratorTable.__init__ with 0 AcceleratorEntries\n"
                "called mainwindow.SetAcceleratorTable\n")

    def _test_create_menuitem(self, monkeypatch, capsys):
        """unittest for MainWindow.create_menuitem
        """
        def mock_menuitem_init(self, *args, **kwargs):
            print('called menuitem.__init__ with args <menu>', args[1:], kwargs)
        monkeypatch.setattr(testee.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(mockwx.MockMenuItem, '__init__', mock_menuitem_init)
        # testobj = setup_mainwindow(monkeypatch, capsys)

    def _test_create_accelerators(self, monkeypatch, capsys):
        """unittest for MainWindow.create_accelerator
        """
        def mock_fromstring(self, *args):
            print('called AcceleratorEntry.FromString with args', args)
            return False
        monkeypatch.setattr(testee.wx, 'AcceleratorEntry', mockwx.MockAcceleratorEntry)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.create_menu()

    # alles in 1 keer (originele test voor niet-opgeknipte versie))
    def test_old_create_menu(self, monkeypatch, capsys):
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
        def mock_bind(self, *args):
            "stub"
            args = (args[0], '<menu item>')
            print('called MainWindow.Bind with args', args)
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
        monkeypatch.setattr(testee.wx, 'Menu', mockwx.MockMenu)
        monkeypatch.setattr(mockwx.MockMenu, 'Append', mock_menu_append)
        monkeypatch.setattr(testee.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(mockwx.MockMenuItem, '__init__', mock_menuitem_init)
        monkeypatch.setattr(testee.wx, 'AcceleratorEntry', mockwx.MockAcceleratorEntry)
        monkeypatch.setattr(testee.wx, 'AcceleratorTable', mockwx.MockAcceleratorTable)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.opts['RevOrder'] = True
        testobj.base.opts['Selection'] = (1, True)
        testobj.tree = mockwx.MockTree()
        assert capsys.readouterr().out == 'called Tree.__init__ with args () {}\n'
        monkeypatch.setattr(mockwx.MockMenuBar, 'GetMenus', lambda x: [])
        monkeypatch.setattr(testobj, 'GetMenuBar', mock_getmenubar)
        monkeypatch.setattr(testobj, 'Bind', mock_bind)
        monkeypatch.setattr(testobj, 'SetAcceleratorTable', mock_set_accel)
        testobj.create_menu()
        assert list(testobj.selactions.keys()) == ["m_revorder", "m_selall", "m_seltag", "m_seltxt"]
        assert testobj.seltypes == ["m_selall", "m_seltag", "m_seltxt"]
        assert capsys.readouterr().out == (
                'called MenuBar.__init__ with args ()\n'
                'called Menu.__init__ with args ()\n'
                "called menuitem.__init__ with args"
                " <menu> (-1, 'm_forward\\tCtrl+PgDn', 'forward') {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('Ctrl+PgDn',)\n"
                "called menuitem.__init__ with args <menu> (-1, 'm_back\\tCtrl+PgUp', 'back') {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('Ctrl+PgUp',)\n"
                "called menuitem.__init__ with args <menu> () {'text': 'm_back\\tCtrl+PgUp'}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('F2',)\n"
                "called menuitem.__init__ with args <menu> (-1, 'other\\tCtrl+D', 'other') {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> () {'text': 'other\\tCtrl+D'}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('Delete',)\n"
                'called AcceleratorTable.__init__ with 1 AcceleratorEntries\n'
                'called tree.SetAcceleratorTable\n'
                'called menubar.Append with args (<menu>, other)\n'
                'called Menu.__init__ with args ()\n'
                "called menuitem.__init__ with args"
                " <menu> (-1, 'm_revorder\\tF9', 'h_revorder', 1) {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-2,) {}\n"
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_selall', 'h_selall', 1) {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_seltag', 'h_seltag', 1) {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_seltxt', 'h_seltxt', 1) {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
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
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                'called AcceleratorEntry.FromString with args (None,)\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_back', 'back') {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                'called AcceleratorEntry.FromString with args (None,)\n'
                "called menuitem.__init__ with args <menu> (-1, 'other\\tding', 'other') {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> () {'text': 'other\\tding'}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
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
        def mock_bind(self, *args):
            "stub"
            args = (args[0], '<menu item>')
            print('called MainWindow.Bind with args', args)
        def mock_set_accel(*args):
            """stub
            """
            print('called mainwindow.SetAcceleratorTable')
        monkeypatch.setattr(MockNoteTree, 'get_menudata', mock_get_menudata)
        monkeypatch.setattr(testee.wx, 'Menu', mockwx.MockMenu)
        monkeypatch.setattr(testee.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(testee.wx, 'AcceleratorEntry', mockwx.MockAcceleratorEntry)
        monkeypatch.setattr(testee.wx, 'AcceleratorTable', mockwx.MockAcceleratorTable)
        monkeypatch.setattr(mockwx.MockMenuItem, '__init__', mock_menuitem_init)
        monkeypatch.setattr(mockwx.MockMenu, 'Append', mock_menu_append)
        monkeypatch.setattr(mockwx.MockMenuBar, 'Replace', mock_menubar_replace)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.opts['RevOrder'] = True
        testobj.base.opts['Selection'] = (1, True)
        testobj.tree = mockwx.MockTree()
        monkeypatch.setattr(testobj, 'Bind', mock_bind)
        assert capsys.readouterr().out == 'called Tree.__init__ with args () {}\n'
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
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('Ctrl+PgDn',)\n"
                "called menuitem.__init__ with args <menu> (-1, 'm_back\\tCtrl+PgUp', 'back') {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('Ctrl+PgUp',)\n"
                "called menuitem.__init__ with args <menu> () {'text': 'm_back\\tCtrl+PgUp'}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('F2',)\n"
                "called menuitem.__init__ with args <menu> (-1, 'other\\tCtrl+D', 'other') {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> () {'text': 'other\\tCtrl+D'}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('Delete',)\n"
                'called AcceleratorTable.__init__ with 1 AcceleratorEntries\n'
                'called tree.SetAcceleratorTable\n'
                "called menubar.Replace with args (0, <menu>, other)\n"
                'called menu.Destroy\n'
                "called Menu.__init__ with args ()\n"
                "called menuitem.__init__ with args"
                " <menu> (-1, 'm_revorder\\tF9', 'h_revorder', 1) {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                'called menuitem.__init__ with args <menu> (-2,) {}\n'
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_selall', 'h_selall', 1) {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_seltag', 'h_seltag', 1) {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
                'called menu.Append with arg <menuitem>\n'
                "called menuitem.__init__ with args <menu> (-1, 'm_seltxt', 'h_seltxt', 1) {}\n"
                f"called MainWindow.Bind with args ({testobj.base.callback}, '<menu item>')\n"
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
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
                                           'called tree.DeleteAllItems\n'
                                           "called tree.AddRoot with args ('title',)\n")

    def test_set_item_expanded(self, monkeypatch, capsys):
        """unittest for MainWindow.set_item_expanded
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.set_item_expanded('item')
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
                                           "called tree.Expand with args ('item',)\n")

    def test_emphasize_activeitem(self, monkeypatch, capsys):
        """unittest for MainWindow.emphasize_activeitem
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.emphasize_activeitem('value')
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
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
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
                                           "called tree.SelectItem with args ('item',)\n")

    def test_get_selected_item(self, monkeypatch, capsys):
        """unittest for MainWindow.get_selected_item
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert testobj.get_selected_item() == 'selection'
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
                                           'called tree.GetSelection\n')

    def test_remove_item_from_tree_any(self, monkeypatch, capsys):
        """unittest for MainWindow.remove_item_from_tree: removing any item except last one
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.remove_item_from_tree('item')
        assert testobj.activeitem is None
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
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
                'called Tree.__init__ with args () {}\n'
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
        def mock_get(*args):
            print('called tree.GetItemData with args', args)
            return 'itemkey', 'itemtext', ['keyword']
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.tree.GetItemData = mock_get
        assert testobj.get_key_from_item('item') == 'itemkey'
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
                                           "called tree.GetItemData with args ('item',)\n")

    def test_get_activeitem_title(self, monkeypatch, capsys):
        """unittest for MainWindow.get_activeitem_title
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        assert testobj.get_activeitem_title() == 'itemtext'
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
                                           "called tree.GetItemText with args (None,)\n")

    def test_set_activeitem_title(self, monkeypatch, capsys):
        """unittest for MainWindow.set_activeitem_title
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.set_activeitem_title('title')
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
                                           "called tree.SetItemText with args (None, 'title')\n")

    def test_set_focus_to_tree(self, monkeypatch, capsys):
        """unittest for MainWindow.set_focus_to_tree
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.set_focus_to_tree()
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
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
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
                                           "called tree.AppendItem with args ('root', 'tag')\n"
                                           "called tree.SetItemData() with args"
                                           " ('appended item', ('key', 'text', ['keywords']))\n")

    def test_add_item_to_tree_2(self, monkeypatch, capsys):
        """unittest for MainWindow.add_item_to_tre:e reversed (new-to-old) order"
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.opts['RevOrder'] = True
        testobj.tree = mockwx.MockTree()
        testobj.root = 'root'
        testobj.add_item_to_tree('key', 'tag', 'text', ['keywords'])
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
                                           "called tree.PrependItem with args ('root', 'tag')\n"
                                           'called tree.SetItemData() with args'
                                           " ('prepended item', ('key', 'text', ['keywords']))\n")

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
        def mock_get(*args):
            print('called tree.GetItemData with args', args)
            return 'itemkey', 'itemtext', ['keyword']
        monkeypatch.setattr(mockwx.MockTree, 'GetFirstChild', mock_GetFirstChild)
        monkeypatch.setattr(mockwx.MockTree, 'GetNextChild', mock_GetNextChild)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        first = mockwx.MockTreeItem('first')
        last = mockwx.MockTreeItem('not ok')
        item = mockwx.MockTreeItem('activeitem')
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
                                           "called TreeItem.__init__ with args ('first',)\n"
                                           "called TreeItem.__init__ with args ('not ok',)\n"
                                           "called TreeItem.__init__ with args ('activeitem',)\n")
        testobj.tree.GetItemData = mock_get
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
        monkeypatch.setattr(testee.wx.Frame, 'GetSize', mock_getsize)
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
        monkeypatch.setattr(testee.MainWindow, 'Hide', mock_hide)
        monkeypatch.setattr(testee, 'TaskbarIcon', mockwx.MockTrayIcon)
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
        monkeypatch.setattr(testee.MainWindow, 'Show', mock_show)
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
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
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
        def mock_get(*args):
            print('called tree.GetItemData with args', args)
            return 'itemkey', 'itemtext', ['keyword']
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.tree.GetItemData = mock_get
        testobj.set_item_text('item', 'text')
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
                                           "called tree.GetItemData with args ('item',)\n"
                                           'called tree.SetItemData() with args'
                                           " ('item', ('itemkey', 'text', ['keyword']))\n")

    def test_get_item_keywords(self, monkeypatch, capsys):
        """unittest for MainWindow.get_item_keywords
        """
        def mock_get(*args):
            print('called tree.GetItemData with args', args)
            return 'itemkey', 'itemtext', ['keyword']
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.tree.GetItemData = mock_get
        assert testobj.get_item_keywords('item') == ['keyword']

    def test_set_item_keywords(self, monkeypatch, capsys):
        """unittest for MainWindow.set_item_keywords
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockwx.MockTree()
        testobj.set_item_keywords('item', ['data'])
        assert capsys.readouterr().out == ('called Tree.__init__ with args () {}\n'
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
        monkeypatch.setattr(testee.wx, 'MessageBox', mock_messagebox)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'title'
        flags = testee.wx.OK | testee.wx.ICON_INFORMATION
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
            return testee.wx.YES
        monkeypatch.setattr(testee.wx, 'MessageBox', mock_messagebox)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'title'
        flags = testee.wx.YES_NO | testee.wx.ICON_QUESTION
        assert testobj.ask_question('question')
        assert capsys.readouterr().out == ('called wx.MessageBox() with args'
                                           f" `question`, `title`, `{flags}`\n")

    def test_show_dialog(self, monkeypatch, capsys):
        """unittest for MainWindow.show_dialog
        """
        class MockDialogParent:
            def __init__(self, *args):
                print('called DialogParent.__init__ with args', args)
                self.gui = mockwx.MockDialog(self, *args)
            def confirm(self):
                print('called DialogParent.confirm')
                return 'confirmation data'
        def mock_showmodal(self, *args):
            """stub
            """
            return testee.wx.ID_OK
        monkeypatch.setattr(testee.wx.Dialog, 'ShowModal', mock_showmodal)
        testobj = setup_mainwindow(monkeypatch, capsys)
        assert testobj.show_dialog(MockDialogParent, 'title') == (True, 'confirmation data')
        assert capsys.readouterr().out == (
                f"called DialogParent.__init__ with args ({testobj}, 'title')\n"
                f"called Dialog.__init__ with args ({testobj}, 'title') {{}}\n"
                "called DialogParent.confirm\n")

    def test_show_dialog_2(self, monkeypatch, capsys):
        """unittest for MainWindow.show_dialog: cancel
        """
        class MockDialogParent:
            def __init__(self, *args):
                print('called DialogParent.__init__ with args', args)
                self.gui = mockwx.MockDialog(self, *args)
            def confirm(self):
                print('called DialogParent.confirm')
                return 'confirmation data'
        def mock_showmodal(self, *args):
            """stub
            """
            return testee.wx.ID_CANCEL
        monkeypatch.setattr(mockwx.MockDialog, 'ShowModal', mock_showmodal)
        testobj = setup_mainwindow(monkeypatch, capsys)
        assert testobj.show_dialog(MockDialogParent, 'title') == (False, None)
        assert capsys.readouterr().out == (
                f"called DialogParent.__init__ with args ({testobj}, 'title')\n"
                f"called Dialog.__init__ with args ({testobj}, 'title') {{}}\n")

    def test_get_text_from_user(self, monkeypatch, capsys):
        """unittest for MainWindow.get_text_from_user
        """
        monkeypatch.setattr(testee.wx, 'TextEntryDialog', mockwx.MockTextDialog)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'title'
        assert testobj.get_text_from_user('prompt', 'default') == ('entered value', True)
        assert capsys.readouterr().out == ('called TextDialog.__init__ with args'
                                           " ('prompt', 'title', 'default') {}\n"
                                           'called TextDialog.ShowModal\n'
                                           'called TextDialog.GetValue\n')

    def test_get_text_from_user_2(self, monkeypatch, capsys):
        """unittest for MainWindow.get_text_from_user: cancel prompt
        """
        def mock_showmodal(self, *args):
            """stub
            """
            return testee.wx.ID_CANCEL
        monkeypatch.setattr(testee.wx, 'TextEntryDialog', mockwx.MockTextDialog)
        monkeypatch.setattr(mockwx.MockTextDialog, 'ShowModal', mock_showmodal)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'title'
        assert testobj.get_text_from_user('prompt', 'default') == ('entered value', False)
        assert capsys.readouterr().out == ('called TextDialog.__init__ with args'
                                           " ('prompt', 'title', 'default') {}\n"
                                           'called TextDialog.GetValue\n')

    def test_get_choice_from_user(self, monkeypatch, capsys):
        """unittest for MainWindow.get_choice_from_user
        """
        monkeypatch.setattr(testee.wx, 'SingleChoiceDialog', mockwx.MockChoiceDialog)
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
            return testee.wx.ID_CANCEL
        monkeypatch.setattr(testee.wx, 'SingleChoiceDialog', mockwx.MockChoiceDialog)
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
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'FlexGridSizer', mockwx.MockGridSizer)
        testobj = testee.OptionsDialog('master', 'parent', 'title')  # {'text': 'value'})
        assert testobj.master == 'master'
        assert testobj.parent == 'parent'
        assert isinstance(testobj.vsizer, testee.wx.BoxSizer)
        assert isinstance(testobj.gsizer, testee.wx.FlexGridSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args ('title',) {}\n"
                f'called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n'
                "called GridSizer.__init__ with args () {'cols': 2}\n"
                "called vert sizer.Add with args <item> (0, 2544, 5)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout with args ()\n")

    def setup_testobj(self, monkeypatch, capsys):
        """initialize testdouble for OptionsDialog object
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
        monkeypatch.setattr(testee.OptionsDialog, '__init__', mock_init)
        testobj = testee.OptionsDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called dialog.__init__\n'
        return testobj

    def test_add_checkbox_line_to_grid(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_checkbox_line_to_grid
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.add_checkbox_line_to_grid(1, 'xxx', 'yyy')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                "called GridSizer.Add with args <item> (1, 240, 5)\n"
                f"called CheckBox.__init__ with args ({testobj},) {{}}\n"
                "called checkbox.SetValue with args ('yyy',)\n"
                "called GridSizer.Add with args <item> (1, 240, 5)\n")

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_buttonbox
        """
        def mock_set(arg):
            print(f'called OptionsDialog.SetEscapeId with arg {arg}')
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.SetEscapeId = mock_set
        testobj.vsizer = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        testobj.add_buttonbox('xxx', 'yyy')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5100, 'label': 'xxx'}}\n"
                "called hori sizer.Add with args <item> (0, 8432, 2)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5001, 'label': 'yyy'}}\n"
                "called hori sizer.Add with args <item> (0, 8432, 2)\n"
                "called OptionsDialog.SetEscapeId with arg 5001\n"
                "called vert sizer.Add with args <item> (0, 2544, 5)\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for OptionsDialog.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockwx.MockCheckBox()
        check.SetValue(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__ with args () {}\n"
                                           "called checkbox.SetValue with args (True,)\n")
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == ("called checkbox.GetValue\n")


class TestCheckDialog:
    """unittests for wx_gui.CheckDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for CheckDialog.init
        """
        monkeypatch.setattr(testee.wx, 'Icon', mockwx.MockIcon)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetIcon', mockwx.MockDialog.SetIcon)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)

        parent = types.SimpleNamespace(nt_icon='nt_icon')
        testobj = testee.CheckDialog('master', parent, 'title')
        assert testobj.master == 'master'
        assert testobj.parent == parent
        assert isinstance(testobj.vsizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title', 'size': (-1, 120)}\n"
                "called Icon.__init__ with args ('nt_icon',)\n"
                "called Dialog.SetIcon with args (Icon created from 'nt_icon',)\n"
                f'called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n'
                'called dialog.SetSizer with args (vert sizer,)\n'
                'called dialog.SetAutoLayout with args (True,)\n'
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                'called dialog.Layout with args ()\n')

    def setup_testobj(self, monkeypatch, capsys):
        """initialize testdouble for CheckDialog object
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
        monkeypatch.setattr(testee.CheckDialog, '__init__', mock_init)
        testobj = testee.CheckDialog()
        assert capsys.readouterr().out == 'called dialog.__init__\n'
        return testobj

    def test_add_label(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_label
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        testobj.add_label('message')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (8,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'message'}}\n"
                'called vert sizer.Add with args <item> (1, 240, 5)\n')

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_checkbox
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        testobj.add_checkbox('hide_message')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (8,)\n"
                f'called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n'
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'hide_message'}}\n"
                'called hori sizer.Add with args <item> (0, 8192)\n'
                'called vert sizer.Add with args <item> (0, 256)\n')

    def test_add_ok_buttonbox(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_ok_buttonbox
        """
        monkeypatch.setattr(testee.wx.Dialog, 'CreateButtonSizer',
                            mockwx.MockDialog.CreateButtonSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vsizer = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        testobj.add_ok_buttonbox()
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (8,)\n"
                'called dialog.CreateButtonSizer with args (4,)\n'
                'called vert sizer.Add with args <item> (0, 256)\n')

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for OptionsDialog.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockwx.MockCheckBox()
        check.SetValue(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__ with args () {}\n"
                                           "called checkbox.SetValue with args (True,)\n")
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == ("called checkbox.GetValue\n")


class TestKeywordsDialog:
    """unittests for wx_gui.KeywordsDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.init: calling with no keywords associated yet
        """
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetTitle', mockwx.MockDialog.SetTitle)
        monkeypatch.setattr(testee.wx.Dialog, 'SetIcon', mockwx.MockDialog.SetIcon)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSize', mockwx.MockDialog.SetSize)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        # monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        parent = types.SimpleNamespace(nt_icon='icon')
        testobj = testee.KeywordsDialog('master', parent, 'xxx')
        assert testobj.master == 'master'
        assert testobj.parent == parent
        assert isinstance(testobj.vbox, testee.wx.BoxSizer)
        assert isinstance(testobj.hbox, testee.wx.BoxSizer)
        # assert isinstance(testobj.fromlist, testee.wx.ListBox)
        # assert isinstance(testobj.tolist, testee.wx.ListBox)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {}\n"
                "called dialog.SetTitle with arg 'xxx'\n"
                "called Dialog.SetIcon with args ('icon',)\n"
                f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
                f"called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n"
                "called vert sizer.Add with args <item> (0, 496, 5)\n"
                "called dialog.SetSizer with args (vert sizer,)\n"
                "called dialog.SetAutoLayout with args (True,)\n"
                f"called vert sizer.Fit with args ({testobj},)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.Layout with args ()\n"
                'called dialog.SetSize with args (400, 264)\n')

    def setup_testobj(self, monkeypatch, capsys):
        """initialize testdouble for KeywordsDialog object
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
        monkeypatch.setattr(testee.KeywordsDialog, '__init__', mock_init)
        testobj = testee.KeywordsDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called dialog.__init__\n'
        return testobj

    def test_add_list(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.add_list
        """
        def callback():
            "dummy function, just for reference"
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'ListBox', mockwx.MockListBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hbox = mockwx.MockBoxSizer(testee.wx.HORIZONTAL)
        assert capsys.readouterr().out == (
                f"called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n")
        testobj.add_list('xxx', ['yyy', 'zzz'], callback)
        assert capsys.readouterr().out == (
                f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                "called vert sizer.Add with args <item> ()\n"
                f"called ListBox.__init__ with args ({testobj},)"
                " {'size': (120, 156), 'style': 128}\n"
                f"called listbox.bind with args ({testee.wx.EVT_LISTBOX_DCLICK}, {callback})\n"
                "called listbox.Append with args (['yyy', 'zzz'],)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called hori sizer.Add with args <item> ()\n")
        testobj.add_list('xxx', ['yyy', 'zzz'], callback, True, True)
        assert capsys.readouterr().out == (
                "called hori sizer.AddStretchSpacer\n"
                f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                "called vert sizer.Add with args <item> ()\n"
                f"called ListBox.__init__ with args ({testobj},)"
                " {'size': (120, 156), 'style': 128}\n"
                f"called listbox.bind with args ({testee.wx.EVT_LISTBOX_DCLICK}, {callback})\n"
                "called listbox.Append with args (['yyy', 'zzz'],)\n"
                "called vert sizer.Add with args <item> ()\n"
                "called hori sizer.Add with args <item> ()\n"
                "called hori sizer.AddStretchSpacer\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.add_button
        """
        def callback():
            "dummy function, just for reference"
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hbox = mockwx.MockBoxSizer(testee.wx.HORIZONTAL)
        assert capsys.readouterr().out == (
                f"called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n")
        testobj.add_buttons([])
        assert capsys.readouterr().out == (
                f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
                "called vert sizer.AddStretchSpacer\n"
                "called vert sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args <item> ()\n")
        testobj.add_buttons([('xxx', callback), ('yyy', None)])
        assert capsys.readouterr().out == (
                f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
                "called vert sizer.AddStretchSpacer\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {callback}) {{}}\n"
                "called vert sizer.Add with args <item> ()\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'yyy'}}\n"
                "called vert sizer.Add with args <item> ()\n"
                "called vert sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args <item> ()\n")

    def test_create_buttonbox(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.create_buttonbox
        """
        monkeypatch.setattr(testee.wx.Dialog, 'CreateButtonSizer',
                            mockwx.MockDialog.CreateButtonSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == (
                f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n")
        testobj.create_buttonbox()
        assert capsys.readouterr().out == ("called dialog.CreateButtonSizer with args (20,)\n"
                                           "called vert sizer.Add with args <item> (0, 496, 10)\n")

    def test_create_actions(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.create_actions
        """
        def callback():
            "dummy function, just for reference"
        def mock_bind(self, *args):
            "stub"
            args = (args[0], '<menu item>')
            print('called KeywordsDialog.Bind with args', args)
        def mock_fromstring(self, *args):
            print('called AcceleratorEntry.FromString with args', args)
            return False
        monkeypatch.setattr(testee.KeywordsDialog, 'SetAcceleratorTable',
                            mockwx.MockDialog.SetAcceleratorTable)
        monkeypatch.setattr(testee.KeywordsDialog, 'Bind', mockwx.MockDialog.Bind)
        monkeypatch.setattr(testee.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(testee.wx, 'AcceleratorEntry', mockwx.MockAcceleratorEntry)
        monkeypatch.setattr(testee.wx, 'AcceleratorTable', mockwx.MockAcceleratorTable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'Bind', mock_bind)
        testobj.create_actions([])
        assert capsys.readouterr().out == (
                'called AcceleratorTable.__init__ with 0 AcceleratorEntries\n'
                'called dialog.SetAcceleratorTable\n')
        testobj.create_actions([('xxx', 'yyy', callback), ('zzz', 'qqq', callback)])
        assert capsys.readouterr().out == (
                'called MenuItem.__init__ with args ()\n'
                f"called KeywordsDialog.Bind with args ({callback}, '<menu item>')\n"
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('yyy',)\n"
                'called MenuItem.__init__ with args ()\n'
                f"called KeywordsDialog.Bind with args ({callback}, '<menu item>')\n"
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('qqq',)\n"
                'called AcceleratorTable.__init__ with 2 AcceleratorEntries\n'
                'called dialog.SetAcceleratorTable\n')
        monkeypatch.setattr(mockwx.MockAcceleratorEntry, 'FromString', mock_fromstring)
        testobj.create_actions([('xxx', 'yyy', callback), ('zzz', 'qqq', callback)])
        assert capsys.readouterr().out == (
                'called MenuItem.__init__ with args ()\n'
                f"called KeywordsDialog.Bind with args ({callback}, '<menu item>')\n"
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('yyy',)\n"
                'called MenuItem.__init__ with args ()\n'
                f"called KeywordsDialog.Bind with args ({callback}, '<menu item>')\n"
                'called menuitem.GetId\n'
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('qqq',)\n"
                'called AcceleratorTable.__init__ with 0 AcceleratorEntries\n'
                'called dialog.SetAcceleratorTable\n')

    def test_activate(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate: when list-to-activate can be activated
        """
        def mock_get():
            print('called listbox.GetSelections')
            return []
        mylist = mockwx.MockListBox()
        assert capsys.readouterr().out == 'called ListBox.__init__ with args () {}\n'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.activate(mylist)
        assert capsys.readouterr().out == ('called listbox.GetSelections\n'
                                           'called listbox.SetSelection with args (1,)\n'
                                           'called listbox.SetFocus\n')
        mylist.GetSelections = mock_get
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.activate(mylist)
        assert capsys.readouterr().out == ('called listbox.GetSelections\n'
                                           'called listbox.SetSelection with args (0,)\n'
                                           'called listbox.SetFocus\n')

    def test_moveitem(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.moveitem
        """
        def mock_sel():
            return []
        testobj = self.setup_testobj(monkeypatch, capsys)
        fromlist = mockwx.MockListBox()
        tolist = mockwx.MockListBox()
        testobj.moveitem(fromlist, tolist)
        assert capsys.readouterr().out == (
                'called ListBox.__init__ with args () {}\n'
                'called ListBox.__init__ with args () {}\n'
                'called listbox.GetSelections\n'
                'called listbox.Delete with args (1,)\n'
                'called listbox.GetCount\n'
                "called listbox.Insert with args (['value 1 from listbox'], None)\n")
        fromlist.GetSelections = mock_sel
        testobj.moveitem(fromlist, tolist)
        assert capsys.readouterr().out == ""

    def test_ask_for_tag(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.ask_for_tag
        """
        def mock_show(self):
            print('called TextDialog.ShowModal')
            return testee.wx.ID_CANCEL
        monkeypatch.setattr(testee.wx, 'TextEntryDialog', mockwx.MockTextDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_for_tag('xxx', 'yyy') == ('entered value', True)
        assert capsys.readouterr().out == (
                "called TextDialog.__init__ with args ('yyy', 'xxx') {}\n"
                "called TextDialog.ShowModal\n"
                "called TextDialog.GetValue\n")
        monkeypatch.setattr(mockwx.MockTextDialog, 'ShowModal', mock_show)
        assert testobj.ask_for_tag('xxx', 'yyy') == ('', False)
        assert capsys.readouterr().out == (
                "called TextDialog.__init__ with args ('yyy', 'xxx') {}\n"
                "called TextDialog.ShowModal\n")

    def test_add_tag_to_list(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.add_tag_to_list
        """
        mylist = mockwx.MockListBox()
        assert capsys.readouterr().out == "called ListBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_tag_to_list('tag', mylist)
        assert capsys.readouterr().out == "called listbox.Append with args ('tag',)\n"

    def test_get_listvalues(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.get_listvalues
        """
        mylist = mockwx.MockListBox()
        assert capsys.readouterr().out == "called ListBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_listvalues(mylist)
        assert capsys.readouterr().out == ("")


class TestKeywordsManager:
    """unittests for wx_gui.KeywordsManager
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for KeywordsManager.init
        """
        def mock_setaffirmativeid(self, *args):
            """stub
            """
            print('called dialog.SetAffirmativeId')
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetTitle', mockwx.MockDialog.SetTitle)
        monkeypatch.setattr(testee.wx.Dialog, 'SetIcon', mockwx.MockDialog.SetIcon)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSize', mockwx.MockDialog.SetSize)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAffirmativeId', mockwx.MockDialog.SetAffirmativeId)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'GridBagSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        parent = types.SimpleNamespace(nt_icon='nt_icon')
        testobj = testee.KeywordsManager('master', parent, 'xxxx', 'yyy')
        assert testobj.master == 'master'
        assert testobj.parent == parent
        assert isinstance(testobj.gbox, testee.wx.GridBagSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'xxxx'}\n"
                "called Dialog.SetIcon with args ('nt_icon',)\n"
                f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
                "called GridSizer.__init__ with args () {}\n"
                'called vert sizer.Add with args <item> (1, 240, 5)\n'
                f"called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'yyy'}}\n"
                'called Button.GetId\n'
                'called dialog.SetAffirmativeId with args (None,)\n'
                'called hori sizer.Add with args <item> ()\n'
                'called vert sizer.Add with args <item> (0, 384, 10)\n'
                'called dialog.SetSizer with args (vert sizer,)\n'
                'called dialog.SetAutoLayout with args (True,)\n'
                f'called vert sizer.Fit with args ({testobj},)\n'
                f'called vert sizer.SetSizeHints with args ({testobj},)\n'
                'called dialog.Layout with args ()\n'
                'called dialog.SetSize with args (408, 200)\n')

    def setup_testobj(self, monkeypatch, capsys):
        """initialize testdouble for OptionsDialog object
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
        monkeypatch.setattr(testee.KeywordsManager, '__init__', mock_init)
        testobj = testee.KeywordsManager(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called dialog.__init__\n'
        return testobj

    def test_add_label(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_label
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.add_label('message', 'row', 'col')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'message'}}\n"
                "called GridSizer.Add with args <item>"
                " (('row', 'col'),) {'flag': 2288, 'border': 5}\n")
        testobj.add_label('message', 'row', -1)
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'message'}}\n"
                "called GridSizer.Add with args <item> (('row', 0), (1, 3), 240, 5)\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest for KeywordsManager.add_combobox
        """
        monkeypatch.setattr(testee.wx, 'ComboBox', mockwx.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_combobox('x', 'y')
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                f'called ComboBox.__init__ with args ({testobj},) {{}}\n'
                "called GridSizer.Add with args <item>"
                " (('x', 'y'),) {'flag': 240, 'border': 5}\n")

    def test_add_lineinput(self, monkeypatch, capsys):
        """unittest for KeywordsManager.add_lineinput
        """
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_lineinput('x', 'y')
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                f"called TextCtrl.__init__ with args ({testobj},) {{'size': (180, -1)}}\n"
                "called GridSizer.Add with args <item>"
                " (('x', 'y'),) {'flag': 2288, 'border': 5}\n")

    def test_add_button(self, monkeypatch, capsys):
        """unittest for KeywordsManager.add_button
        """
        def callback():
            "dummy function, just for reference"
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.add_button('aaa', callback, 'x', 'y')
        assert capsys.readouterr().out == (
                f"called Button.__init__ with args ({testobj},) {{'label': 'aaa'}}\n"
                f'called Button.Bind with args ({testee.wx.EVT_BUTTON}, {callback}) {{}}\n'
                "called GridSizer.Add with args <item>"
                " (('x', 'y'),) {'flag': 240, 'border': 5}\n")

    def test_reset_combobox(self, monkeypatch, capsys):
        """unittest for KeywordsManager.reset_combobox
        """
        assert capsys.readouterr().out == ("")
        widget = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reset_combobox(widget, ['x', 'y'])
        assert capsys.readouterr().out == (
                'called combobox.clear\n'
                "called combobox.AppendItems with args (['x', 'y'],)\n"
                "called combobox.SetValue with args ('',)\n")

    def test_reset_lineinput(self, monkeypatch, capsys):
        """unittest for KeywordsManager.reset_lineinput
        """
        assert capsys.readouterr().out == ("")
        widget = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reset_lineinput(widget)
        assert capsys.readouterr().out == 'called text.Clear\n'

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for KeywordsManager.get_combobox_value
        """
        widget = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_combobox_value(widget)
        assert capsys.readouterr().out == ("called combobox.GetValue\n")

    def test_ask_question(self, monkeypatch, capsys):
        """unittest for KeywordsManager.ask_question
        """
        def mock_message(*args):
            "stub"
            print('called wx.MessageBox with args', args)
            return testee.wx.NO
        def mock_message_2(*args):
            "stub"
            print('called wx.MessageBox with args', args)
            return testee.wx.YES
        monkeypatch.setattr(testee.wx, 'MessageBox', mock_message)
        assert capsys.readouterr().out == ("")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.ask_question('xxx', 'yyy')
        assert capsys.readouterr().out == (
                f"called wx.MessageBox with args ('yyy', 'xxx', 1034, {testobj})\n")
        monkeypatch.setattr(testee.wx, 'MessageBox', mock_message_2)
        assert testobj.ask_question('xxx', 'yyy')
        assert capsys.readouterr().out == (
                f"called wx.MessageBox with args ('yyy', 'xxx', 1034, {testobj})\n")

    def test_get_lineinput_text(self, monkeypatch, capsys):
        """unittest for KeywordsManager.get_lineinput_text
        """
        widget = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_lineinput_text(widget)
        assert capsys.readouterr().out == ("called text.GetValue\n")

    def test_ask_question_w_cancel(self, monkeypatch, capsys):
        """unittest for KeywordsManager.ask_question_w_cancel
        """
        def mock_show(self):
            print('called MessageDialog.ShowModal')
            return testee.wx.ID_NO
        def mock_show_2(self):
            print('called MessageDialog.ShowModal')
            return testee.wx.ID_YES
        def mock_show_3(self):
            print('called MessageDialog.ShowModal')
            return testee.wx.ID_CANCEL
        monkeypatch.setattr(testee.wx, 'MessageDialog', mockwx.MockMessageDialog)
        monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_question_w_cancel('xxx', 'yyy') == (False, False)
        assert capsys.readouterr().out == (
                f"called MessageDialog.__init__ with args ({testobj}, 'xxx') {{'style': 26}}\n"
                "called MessageDialog.SetExtendedMessage with args ('yyy',)\n"
                "called MessageDialog.ShowModal\n")
        monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show_2)
        assert testobj.ask_question_w_cancel('xxx', 'yyy') == (True, False)
        assert capsys.readouterr().out == (
                f"called MessageDialog.__init__ with args ({testobj}, 'xxx') {{'style': 26}}\n"
                "called MessageDialog.SetExtendedMessage with args ('yyy',)\n"
                "called MessageDialog.ShowModal\n")
        monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show_3)
        assert testobj.ask_question_w_cancel('xxx', 'yyy') == (False, True)
        assert capsys.readouterr().out == (
                f"called MessageDialog.__init__ with args ({testobj}, 'xxx') {{'style': 26}}\n"
                "called MessageDialog.SetExtendedMessage with args ('yyy',)\n"
                "called MessageDialog.ShowModal\n")


class TestGetTextDialog:
    """unittests for wx_gui.GetTextDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for GetTextDialog.init
        """
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetTitle', mockwx.MockDialog.SetTitle)
        monkeypatch.setattr(testee.wx.Dialog, 'SetIcon', mockwx.MockDialog.SetIcon)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSize', mockwx.MockDialog.SetSize)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'GridBagSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        parent = types.SimpleNamespace(nt_icon='nt_icon')
        testobj = testee.GetTextDialog('master', parent, 'xxxx')
        assert testobj.master == 'master'
        assert testobj.parent == parent
        assert isinstance(testobj.vbox, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {}\n"
                "called dialog.SetTitle with arg 'xxxx'\n"
                "called Dialog.SetIcon with args ('nt_icon',)\n"
                f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
                'called dialog.SetSizer with args (vert sizer,)\n'
                'called dialog.SetAutoLayout with args (True,)\n'
                f'called vert sizer.Fit with args ({testobj},)\n'
                f'called vert sizer.SetSizeHints with args ({testobj},)\n'
                'called dialog.Layout with args ()\n')

    def setup_testobj(self, monkeypatch, capsys):
        """initialize testdouble for GetTextDialog object
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
        monkeypatch.setattr(testee.GetTextDialog, '__init__', mock_init)
        testobj = testee.GetTextDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called dialog.__init__\n'
        return testobj

    def test_add_label(self, monkeypatch, capsys):
        """unittest for GetTextDialog.add_label
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        testobj.add_label('message')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'message'}}\n"
                "called hori sizer.Add with args <item> (0, 240, 5)\n"
                "called vert sizer.Add with args <item> (0, 240, 5)\n")

    def test_add_lineinput(self, monkeypatch, capsys):
        """unittest for KeywordsManager.add_lineinput
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        result = testobj.add_lineinput('xxx')
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called TextCtrl.__init__ with args ({testobj},) {{'value': 'xxx'}}\n"
                "called hori sizer.Add with args <item> (1, 240, 5)\n"
                "called vert sizer.Add with args <item> (1, 240, 5)\n")

    def test_add_checkbox_line(self, monkeypatch, capsys):
        """unittest for GetTextDialog.add_checkbox
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        testobj.add_checkbox_line([])
        assert capsys.readouterr().out == (
                f'called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n'
                'called vert sizer.Add with args <item> (0, 240, 5)\n')
        testobj.add_checkbox_line([('xxx', True), ('yyy', False)])
        assert capsys.readouterr().out == (
                f'called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n'
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                "called checkbox.SetValue with args (True,)\n"
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'yyy'}}\n"
                "called checkbox.SetValue with args (False,)\n"
                'called hori sizer.Add with args <item> (0, 240, 5)\n'
                'called vert sizer.Add with args <item> (0, 240, 5)\n')

    def test_add_okcancel_buttonbox(self, monkeypatch, capsys):
        """unittest for GetTextDialog.add_ok_buttonbox
        """
        monkeypatch.setattr(testee.wx.Dialog, 'CreateButtonSizer',
                            mockwx.MockDialog.CreateButtonSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        testobj.add_okcancel_buttonbox()
        assert capsys.readouterr().out == (
                'called dialog.CreateButtonSizer with args (20,)\n'
                'called vert sizer.Add with args <item> (0, 496, 10)\n')

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for GetTextDialog.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockwx.MockCheckBox()
        check.SetValue(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__ with args () {}\n"
                                           "called checkbox.SetValue with args (True,)\n")
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == ("called checkbox.GetValue\n")

    def test_get_lineinput_value(self, monkeypatch, capsys):
        """unittest for KeywordsManager.get_lineinput_value
        """
        widget = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_lineinput_value(widget)
        assert capsys.readouterr().out == ("called text.GetValue\n")


class TestGetItemDialog:
    """unittests for wx_gui.GetItemDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for GetTextDialog.init
        """
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetTitle', mockwx.MockDialog.SetTitle)
        monkeypatch.setattr(testee.wx.Dialog, 'SetIcon', mockwx.MockDialog.SetIcon)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSize', mockwx.MockDialog.SetSize)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'GridBagSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        parent = types.SimpleNamespace(nt_icon='nt_icon')
        testobj = testee.GetItemDialog('master', parent, 'xxxx')
        assert testobj.master == 'master'
        assert testobj.parent == parent
        assert isinstance(testobj.vbox, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {}\n"
                "called dialog.SetTitle with arg 'xxxx'\n"
                "called Dialog.SetIcon with args ('nt_icon',)\n"
                f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
                'called dialog.SetSizer with args (vert sizer,)\n'
                'called dialog.SetAutoLayout with args (True,)\n'
                f'called vert sizer.Fit with args ({testobj},)\n'
                f'called vert sizer.SetSizeHints with args ({testobj},)\n'
                'called dialog.Layout with args ()\n')

    def setup_testobj(self, monkeypatch, capsys):
        """initialize testdouble for GetItemDialog object
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
        monkeypatch.setattr(testee.GetItemDialog, '__init__', mock_init)
        testobj = testee.GetItemDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called dialog.__init__\n'
        return testobj

    def test_add_label(self, monkeypatch, capsys):
        """unittest for GetItemDialog.add_label
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        testobj.add_label('message')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'message'}}\n"
                "called hori sizer.Add with args <item> (0, 240, 5)\n"
                "called vert sizer.Add with args <item> (0, 240, 5)\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest for KeywordsManager.add_combobox
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'ComboBox', mockwx.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        result = testobj.add_combobox(['x', 'y'], 'z')
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called ComboBox.__init__ with args ({testobj},) {{'choices': ['x', 'y']}}\n"
                "called combobox.SetSelection with args ('z',)\n"
                "called hori sizer.Add with args <item> (1, 240, 5)\n"
                "called vert sizer.Add with args <item> (1, 240, 5)\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for GetItemDialog.add_checkbox
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        testobj.add_checkbox('xxx', True)
        assert capsys.readouterr().out == (
                f'called BoxSizer.__init__ with args ({testee.wx.HORIZONTAL},)\n'
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                "called checkbox.SetValue with args (True,)\n"
                "called hori sizer.Add with args <item> (0, 240, 5)\n"
                "called vert sizer.Add with args <item> (0, 240, 5)\n")

    def test_add_okcancel_buttonbox(self, monkeypatch, capsys):
        """unittest for GetItemDialog.add_okcancel_buttonbox
        """
        monkeypatch.setattr(testee.wx.Dialog, 'CreateButtonSizer',
                            mockwx.MockDialog.CreateButtonSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer(testee.wx.VERTICAL)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"
        testobj.add_okcancel_buttonbox()
        assert capsys.readouterr().out == (
                'called dialog.CreateButtonSizer with args (20,)\n'
                'called vert sizer.Add with args <item> (0, 496, 10)\n')

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for GetItemDialog.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockwx.MockCheckBox()
        check.SetValue(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__ with args () {}\n"
                                           "called checkbox.SetValue with args (True,)\n")
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == ("called checkbox.GetValue\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for GetItemDialog.get_combobox_value
        """
        widget = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.get_combobox_value(widget)
        assert capsys.readouterr().out == ("called combobox.GetValue\n")


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
        monkeypatch.setattr(testee.wx, 'Icon', mockwx.MockIcon)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetIcon', mockwx.MockDialog.SetIcon)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAffirmativeId', mockwx.MockDialog.SetAffirmativeId)
        monkeypatch.setattr(testee.wx.Dialog, 'Layout', mockwx.MockDialog.Layout)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'FlexGridSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)

        testobj = testee.GridDialog('parent', 'title', 'donetext')
        assert isinstance(testobj.gbox, testee.wx.FlexGridSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title', 'size': (-1, 320)}\n"
                f"called BoxSizer.__init__ with args ({testee.wx.VERTICAL},)\n"
                "called GridSizer.__init__ with args () {'cols': 2, 'vgap': 2, 'hgap': 25}\n"
                'called vert sizer.Add with args <item> (0, 8432, 5)\n'
                f"called Button.__init__ with args ({testobj},) {{'label': 'donetext'}}\n"
                "called Button.GetId\n"
                "called dialog.SetAffirmativeId with args (None,)\n"
                'called vert sizer.Add with args <item> (0, 496, 5)\n'
                'called dialog.SetSizer with args (vert sizer,)\n'
                'called dialog.SetAutoLayout with args (True,)\n'
                f'called vert sizer.Fit with args ({testobj},)\n'
                f'called vert sizer.SetSizeHints with args ({testobj},)\n'
                'called dialog.Layout with args ()\n')

    def setup_testobj(self, monkeypatch, capsys):
        """initialize testdouble for OptionsDialog object
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
        monkeypatch.setattr(testee.GridDialog, '__init__', mock_init)
        testobj = testee.GridDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called dialog.__init__\n'
        return testobj

    def test_add_label(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_label
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.add_label('row', 'col', 'message')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'message'}}\n"
                "called GridSizer.Add with args <item> ()\n")

    def test_send(self, monkeypatch, capsys):
        """unittest for OptionsDialog.send
        """
        monkeypatch.setattr(testee.wx.Dialog, 'ShowModal', mockwx.MockDialog.ShowModal)
        monkeypatch.setattr(testee.wx.Dialog, 'Destroy', mockwx.MockDialog.Destroy)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.send()
        assert capsys.readouterr().out == ("called dialog.Destroy\n")


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
        monkeypatch.setattr(testee.wx.adv.TaskBarIcon, '__init__', mock_init)
        monkeypatch.setattr(testee.wx.adv.TaskBarIcon, 'SetIcon', mock_seticon)
        monkeypatch.setattr(testee.wx.adv.TaskBarIcon, 'Bind', mock_bind)
        monkeypatch.setattr(testee.wx, 'Icon', mockwx.MockIcon)
        mockparent = setup_mainwindow(monkeypatch, capsys)
        mockparent.nt_icon = testee.wx.Icon()
        mockparent.revive = lambda x: 'revive'
        testee.TaskbarIcon(mockparent)
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
        monkeypatch.setattr(testee.wx, 'Menu', mockwx.MockMenu)
        monkeypatch.setattr(testee.TaskbarIcon, '__init__', mock_init)
        mockparent = setup_mainwindow(monkeypatch, capsys)
        testobj = testee.TaskbarIcon(mockparent)
        menu = testobj.CreatePopupMenu()
        assert isinstance(menu, testee.wx.Menu)
        assert capsys.readouterr().out == (
                'called trayicon.__init__\n'
                'called Menu.__init__ with args ()\n'
                f"called menu.Append with args ({testobj.id_revive}, 'Revive NoteTree')\n")
