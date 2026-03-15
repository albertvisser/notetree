"""unittests for ./notetree/qt_gui.py
"""
import types
import pytest
from mockgui import mockqtwidgets as mockqtw
from notetree import qt_gui as testee


class MockNoteTree:
    """stub for main.NoteTree object
    """
    def __init__(self):
        print('called MockNoteTree.__init__')
    def get_menudata(self):
        """stub
        """
    def callback(self):
        """stub
        """
    def check_active(self, *args):
        """stub
        """
        print('called Base.check_active')
    def activate_item(self, *args):
        """stub
        """
        print(f'called Base.activate_item with arg `{args[0]}`')
    def update(self):
        """stub
        """
        print('called Base.update')


def setup_mainwindow(monkeypatch, capsys):
    """stub for setting up MainWindow object
    """
    def mock_init(self):
        """stub
        """
        print('called Widget.__init__')
    monkeypatch.setattr(testee.qtw, 'QApplication', mockqtw.MockApplication)
    monkeypatch.setattr(testee.qtw.QWidget, '__init__', mock_init)
    # monkeypatch.setattr(testee.qtw, 'QWidget', mockqtw.MockWidget)
    monkeypatch.setattr(testee.qtw, 'QMainWindow', mockqtw.MockMainWindow)
    testobj = testee.MainWindow(MockNoteTree())
    assert capsys.readouterr().out == ('called MockNoteTree.__init__\n'
                                       'called Application.__init__\n')
    return testobj


class TestMainWindow:
    """unittests for qt_gui.MainWindow
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
        with pytest.raises(SystemExit):
            testobj.start()
        assert capsys.readouterr().out == 'called Application.exec\n'

    def test_init_screen(self, monkeypatch, capsys):
        """unittest for MainWindow.init_screen
        """
        def mock_setWindowTitle(self, *args):
            """stub
            """
            print('called setWindowTitle with args', args)
        def mock_setWindowIcon(self, *args):
            """stub
            """
            print('called setWindowIcon()`')
        def mock_resize(self, *args):
            """stub
            """
            print('called resize with args', args)
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mock_resize)
        # breakpoint()
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.init_screen('title', 'iconame')
        assert hasattr(testobj, 'nt_icon')
        assert capsys.readouterr().out == ('called Widget.__init__\n'
                                           "called setWindowTitle with args ('title',)\n"
                                           'called Icon.__init__ with arg `iconame`\n'
                                           'called setWindowIcon()`\n'
                                           'called resize with args (800, 500)\n')

    def test_setup_statusbar(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_statusbar
        """
        def mock_statusbar(self, *args):
            """stub
            """
            print('called MainWindow.statusbar')
        monkeypatch.setattr(testee.qtw.QMainWindow, 'statusBar', mock_statusbar)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.setup_statusbar()
        assert hasattr(testobj, 'sb')
        assert capsys.readouterr().out == 'called MainWindow.statusbar\n'

    def test_setup_trayicon(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_trayicon
        """
        monkeypatch.setattr(testee.qtw, 'QSystemTrayIcon', mockqtw.MockSysTrayIcon)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.nt_icon = 'nt_icon'
        testobj.setup_trayicon()
        assert capsys.readouterr().out == (
                'called TrayIcon.__init__\n'
                "called TrayIcon.setToolTip with args ('revive_message',)\n"
                f'called Signal.connect with args ({testobj.revive},)\n'
                'called TrayIcon.hide\n')
        assert hasattr(testobj, 'tray_icon')

    def test_setup_split_screen(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_split_screen
        """
        def mock_setcentralwidget(self, *args):
            """stub
            """
            print('called MockMainWindow.setCentralWidget')
        def mock_add(self, arg):
            print(f"called Splitter.addWidget with arg `{arg}`")
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setCentralWidget', mock_setcentralwidget)
        monkeypatch.setattr(testee.qtw, 'QSplitter', mockqtw.MockSplitter)
        monkeypatch.setattr(mockqtw.MockSplitter, 'addWidget', mock_add)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.setup_split_screen()
        assert hasattr(testobj, 'splitter')
        assert capsys.readouterr().out == ('called Splitter.__init__\n'
                                           'called MockMainWindow.setCentralWidget\n')

    def test_setup_tree(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_tree
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidget', mockqtw.MockTreeWidget)
        testobj = setup_mainwindow(monkeypatch, capsys)
        newstuff = testobj.setup_tree()
        # assert newstuff == testobj.tree
        assert capsys.readouterr().out == ('called Tree.__init__\n'
                                           'called Tree.setColumnCount with arg `2`\n'
                                           'called Tree.hideColumn\n'
                                           'called Tree.headerItem\n'
                                           'called TreeItem.__init__ with args ()\n'
                                           "called TreeItem.setHidden with arg `True`\n"
                                           'called Tree.setSelectionMode\n'
                                           'called Signal.connect with args'
                                           f' ({testobj.changeselection},)\n')

    def test_setup_editor(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_editor
        """
        monkeypatch.setattr(testee.qsc, 'QsciScintilla', mockqtw.MockEditorWidget)
        monkeypatch.setattr(testee.qsc, 'QsciLexerMarkdown', lambda: 'dummy lexer')
        monkeypatch.setattr(testee.gui, 'QColor', mockqtw.MockColor)
        testobj = setup_mainwindow(monkeypatch, capsys)
        newstuff = testobj.setup_editor()
        # assert newstuff == testobj.editor
        assert capsys.readouterr().out == (
                f'called Editor.__init__ with args ({testobj},)\n'
                'called Editor.setFont\n'
                'called Editor.setWrapMode with arg `1`\n'
                'called Editor.setBraceMatching with arg `2`\n'
                'called Editor.setAutoIndent with arg `True`\n'
                'called Editor.setFolding with arg `3`\n'
                'called Editor.setCaretLineVisible with arg `True`\n'
                "called Editor.setCaretLineBackgroundColor with arg 'color #ffe4e4'\n"
                'called Editor.setLexer\n'
                'called Editor.setEnabled with arg False\n')

    def test_finish_screen(self, monkeypatch, capsys):
        """unittest for MainWindow.finish_screen
        """
        def mock_show(self, *args):
            """stub
            """
            print('called MockMainWindow.show')
        monkeypatch.setattr(testee.qtw.QMainWindow, 'show', mock_show)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.splitter = mockqtw.MockSplitter()
        testobj.tree = mockqtw.MockTreeWidget()
        testobj.editor = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == ('called Splitter.__init__\n'
                                           f'called Tree.__init__\n'
                                           f'called Editor.__init__\n')
        testobj.finish_screen()
        assert capsys.readouterr().out == ('called Splitter.addWidget with arg MockTreeWidget\n'
                                           'called Splitter.addWidget with arg MockEditorWidget\n'
                                           'called MockMainWindow.show\n')

    def test_create_menu(self, monkeypatch, capsys):
        """unittest for MainWindow.create_menu
        """
        def mock_menubar(self, *args):
            """stub
            """
            print('called setMenuBar')
            return mockqtw.MockMenuBar()
        def mock_get_menudata(self):
            """stub
            """
            return ([_("m_view"), ((_("m_revorder"), self.callback, _("h_revorder"), 'F9'),
                                   ("", None, None, None),
                                   (_("m_selall"), self.callback, _("h_selall"), None),
                                   (_("m_seltag"), self.callback, _("h_seltag"), None),
                                   (_("m_seltxt"), self.callback, _("h_seltxt"), None))],
                    ('xxx', [('yy', self.callback, 'yyyy', None)]))
        # monkeypatch.setattr(testee.qtw, 'QMenuBar', MockMenuBar)  # Hm dit geeft al een runtimeerror
        monkeypatch.setattr(MockNoteTree, 'get_menudata', mock_get_menudata)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'menuBar', mock_menubar)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.opts = {'RevOrder': True, 'Selection': (1, 'find_me')}
        testobj.create_menu()
        assert list(testobj.selactions.keys()) == ["m_revorder", "m_selall", "m_seltag", "m_seltxt"]
        assert testobj.seltypes == ["m_selall", "m_seltag", "m_seltxt"]
        assert capsys.readouterr().out == (
                'called setMenuBar\n'
                'called MenuBar.__init__\n'
                'called MenuBar.clear\n'
                'called MenuBar.addMenu with arg  m_view\n'
                "called Menu.__init__ with args ('m_view',)\n"
                f'called Menu.addAction with args `m_revorder` {testobj.base.callback}\n'
                f"called Action.__init__ with args ('m_revorder', {testobj.base.callback})\n"
                "called Action.setCheckable with arg `True`\n"
                "called Action.setShortcuts with arg `['F9']`\n"
                "called Action.setStatusTip with arg 'h_revorder'\n"
                "called Menu.addSeparator\n"
                "called Action.__init__ with args ('-----', None)\n"
                f'called Menu.addAction with args `m_selall` {testobj.base.callback}\n'
                f"called Action.__init__ with args ('m_selall', {testobj.base.callback})\n"
                "called Action.setCheckable with arg `True`\n"
                "called Action.setStatusTip with arg 'h_selall'\n"
                f'called Menu.addAction with args `m_seltag` {testobj.base.callback}\n'
                f"called Action.__init__ with args ('m_seltag', {testobj.base.callback})\n"
                "called Action.setCheckable with arg `True`\n"
                "called Action.setStatusTip with arg 'h_seltag'\n"
                f'called Menu.addAction with args `m_seltxt` {testobj.base.callback}\n'
                f"called Action.__init__ with args ('m_seltxt', {testobj.base.callback})\n"
                "called Action.setCheckable with arg `True`\n"
                "called Action.setStatusTip with arg 'h_seltxt'\n"
                'called MenuBar.addMenu with arg  xxx\n'
                "called Menu.__init__ with args ('xxx',)\n"
                f'called Menu.addAction with args `yy` {testobj.base.callback}\n'
                f"called Action.__init__ with args ('yy', {testobj.base.callback})\n"
                "called Action.setStatusTip with arg 'yyyy'\n"
                "called Action.setChecked with arg `False`\n"
                "called Action.setChecked with arg `False`\n"
                "called Action.setChecked with arg `False`\n"
                "called Action.setChecked with arg `False`\n"
                "called Action.setChecked with arg `True`\n"
                "called Action.setChecked with arg `True`\n")

    def test_changeselection(self, monkeypatch, capsys):
        """unittest for MainWindow.changeselection
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = 'root'
        testobj.tree = mockqtw.MockTreeWidget()
        testobj.changeselection()
        assert capsys.readouterr().out == ('called Tree.__init__\n'
                                           # 'called Tree.selectedItems\n'
                                           'called Base.check_active\n'
                                           'called Base.activate_item with arg'
                                           ' `called Tree.currentItem`\n')

    def test_closeevent(self, monkeypatch, capsys):
        """unittest for MainWindow.closeevent
        """
        def mock_accept(self, *args):
            """stub
            """
            print('called Event.accept')
        testobj = setup_mainwindow(monkeypatch, capsys)
        monkeypatch.setattr(testee.gui.QCloseEvent, 'accept', mock_accept)
        testobj.activeitem = None
        testobj.closeEvent(testee.gui.QCloseEvent())
        assert capsys.readouterr().out == 'called Event.accept\n'
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.activeitem = 'active item'
        testobj.closeEvent(testee.gui.QCloseEvent())
        assert capsys.readouterr().out == ('called Base.update\n'
                                           'called Event.accept\n')

    def test_clear_editor(self, monkeypatch, capsys):
        """unittest for MainWindow.clear_editor
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockqtw.MockEditorWidget()
        testobj.clear_editor()
        assert capsys.readouterr().out == ('called Editor.__init__\n'
                                           'called Editor.clear\n'
                                           'called Editor.setEnabled with arg False\n')

    def test_open_editor(self, monkeypatch, capsys):
        """unittest for MainWindow.open_editor
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = 'root'
        testobj.editor = mockqtw.MockEditorWidget()
        testobj.activeitem = 'root'
        testobj.open_editor()
        assert capsys.readouterr().out == 'called Editor.__init__\n'
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = 'root'
        testobj.editor = mockqtw.MockEditorWidget()
        testobj.activeitem = 'not root'
        testobj.open_editor()
        assert capsys.readouterr().out == ('called Editor.__init__\n'
                                           'called Editor.setEnabled with arg True\n')

    def test_set_screen(self, monkeypatch, capsys):
        """unittest for MainWindow.set_screen
        """
        def mock_resize(self, *args):
            """stub
            """
            print('called resize with args', args)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mock_resize)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.set_screen(('x', 'y'))
        assert capsys.readouterr().out == "called resize with args ('x', 'y')\n"

    def test_set_splitter(self, monkeypatch, capsys):
        """unittest for MainWindow.set_splitter
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.splitter = mockqtw.MockSplitter()  # testee.qtw.QSplitter()
        testobj.set_splitter('split')
        assert capsys.readouterr().out == ('called Splitter.__init__\n'
                                           "called Splitter.setSizes with args ('split',)\n")

    def test_create_root(self, monkeypatch, capsys):
        """unittest for MainWindow.create_root
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        newroot = testobj.create_root('title')
        assert newroot.text(0) == 'title'
        assert testobj.activeitem == testobj.root
        assert capsys.readouterr().out == ('called Tree.__init__\n'
                                           'called Tree.takeTopLevelItem with arg `0`\n'
                                           'called TreeItem.__init__ with args ()\n'
                                           "called TreeItem.setText with args (0, 'title')\n"
                                           'called Tree.addTopLevelItem\n'
                                           'called TreeItem.text with arg 0\n')

    def test_set_item_expanded(self, monkeypatch, capsys):
        """unittest for MainWindow.set_item_expanded
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_item_expanded(item)
        assert capsys.readouterr().out == "called TreeItem.setExpanded with arg `True`\n"

    def test_emphasize_activeitem(self, monkeypatch, capsys):
        """unittest for MainWindow.emphasize_activeitem
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.activeitem = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.emphasize_activeitem('x')
        assert capsys.readouterr().out == ('called TreeItem.font\n'
                                           'called Font.__init__\n'
                                           'called Font.setBold with arg `x`\n'
                                           'called TreeItem.setFont\n')

    def test_editor_text_was_changed(self, monkeypatch, capsys):
        """unittest for MainWindow.editor_text_was_changed
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == 'called Editor.__init__\n'
        assert testobj.editor_text_was_changed() == 'x'
        assert capsys.readouterr().out == 'called Editor.isModified\n'

    def test_copy_text_from_editor_to_activeitem(self, monkeypatch, capsys):
        """unittest for MainWindow.copy_text_from_editor_to_activeitem
        """
        def mock_settext(self, *args):
            """stub
            """
            print(f'called TreeItem.setText with args `{args[0]}`, `{args[1]}`')
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.activeitem = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.editor = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == 'called Editor.__init__\n'
        monkeypatch.setattr(mockqtw.MockTreeItem, 'setText', mock_settext)
        testobj.copy_text_from_editor_to_activeitem()
        assert capsys.readouterr().out == ('called Editor.text\n'
                                           'called TreeItem.setText with args `1`, `editor text`\n')

    def test_copy_text_from_activeitem_to_editor(self, monkeypatch, capsys):
        """unittest for MainWindow.copy_text_from_activeitem_to_editor
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.activeitem = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.editor = mockqtw.MockEditorWidget()
        monkeypatch.setattr(mockqtw.MockTreeItem, 'text', lambda x, y: 'item text')
        testobj.copy_text_from_activeitem_to_editor()
        assert capsys.readouterr().out == ('called Editor.__init__\n'
                                           'called Editor.setText with arg `item text`\n')

    def test_select_item(self, monkeypatch, capsys):
        """unittest for MainWindow.select_item
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        testobj.select_item('item')
        assert capsys.readouterr().out == ('called Tree.__init__\n'
                                           'called Tree.setCurrentItem with arg `item`\n')

    def test_get_selected_item(self, monkeypatch, capsys):
        """unittest for MainWindow.get_selected_item
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        assert testobj.get_selected_item() == 'called Tree.currentItem'
        assert capsys.readouterr().out == 'called Tree.__init__\n'

    def test_remove_item_from_tree(self, monkeypatch, capsys):
        """unittest for MainWindow.remove_item_from_tree
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.remove_item_from_tree('item')
        assert capsys.readouterr().out == 'called TreeItem.removeChild\n'

    def test_get_key_from_item(self, monkeypatch, capsys):
        """unittest for MainWindow.get_key_from_item
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        item._data = {0: 'key'}
        assert testobj.get_key_from_item(item) == 'key'
        assert capsys.readouterr().out == (
                f'called TreeItem.data with args (0, {testee.core.Qt.ItemDataRole.UserRole!r})\n')

    def test_get_activeitem_title(self, monkeypatch, capsys):
        """unittest for MainWindow.get_activeitem_title
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.activeitem = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.activeitem._text = {0: 'title'}
        assert testobj.get_activeitem_title() == 'title'
        assert capsys.readouterr().out == 'called TreeItem.text with arg 0\n'

    def test_set_activeitem_title(self, monkeypatch, capsys):
        """unittest for MainWindow.set_activeitem_title
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.activeitem = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_activeitem_title('text')
        assert testobj.activeitem._text == ['text']
        assert capsys.readouterr().out == "called TreeItem.setText with args (0, 'text')\n"

    def test_set_focus_to_tree(self, monkeypatch, capsys):
        """unittest for MainWindow.set_focus_to_tree
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.set_focus_to_tree()
        assert capsys.readouterr().out == 'called Tree.setFocus\n'

    def test_set_focus_to_editor(self, monkeypatch, capsys):
        """unittest for MainWindow.set_focus_to_editor
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockqtw.MockEditorWidget()
        assert capsys.readouterr().out == 'called Editor.__init__\n'
        testobj.set_focus_to_editor()
        assert capsys.readouterr().out == 'called Editor.setFocus\n'

    def test_add_item_to_tree(self, monkeypatch, capsys):
        """unittest for MainWindow.add_item_to_tree
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        expected = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        expected._text = ['tag', 'text']
        expected._data = ['key', 'keywords']

        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = testee.qtw.QTreeWidgetItem()  # waarom niet mockqtw.MockTreeItem()?
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.base.opts = {'RevOrder': False}
        result = testobj.add_item_to_tree('key', 'tag', 'text', 'keywords')
        assert result._text == expected._text
        assert result._data == expected._data
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setText with args (0, 'tag')\n"
                "called TreeItem.setData with args"
                f" (0, {testee.core.Qt.ItemDataRole.UserRole!r}, 'key')\n"
                "called TreeItem.setText with args (1, 'text')\n"
                "called TreeItem.setData with args"
                f" (1, {testee.core.Qt.ItemDataRole.UserRole!r}, 'keywords')\n"
                'called TreeItem.addChild\n')

        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = testee.qtw.QTreeWidgetItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.base.opts = {'RevOrder': True}
        testobj.add_item_to_tree('key', 'tag', 'text', 'keywords')
        assert result._text == expected._text
        assert result._data == expected._data
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setText with args (0, 'tag')\n"
                "called TreeItem.setData with args"
                f" (0, {testee.core.Qt.ItemDataRole.UserRole!r}, 'key')\n"
                "called TreeItem.setText with args (1, 'text')\n"
                "called TreeItem.setData with args"
                f" (1, {testee.core.Qt.ItemDataRole.UserRole!r}, 'keywords')\n"
                'called TreeItem.insertChild at pos 0\n')

    def test_get_treeitems(self, monkeypatch, capsys):
        """unittest for MainWindow.get_treeitems
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        subitem1 = mockqtw.MockTreeItem()
        subitem1._text = ['tag1', 'text1']
        subitem1._data = ['key1', 'keywords1']
        subitem2 = mockqtw.MockTreeItem()
        subitem2._text = ['tag2', 'text2']
        subitem2._data = ['key2', 'keywords2']
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.__init__ with args ()\n")
        testobj.root.subitems = [subitem1, subitem2]
        testobj.activeitem = None
        assert testobj.get_treeitems() == ([('key1', 'tag1', 'text1', 'keywords1'),
                                            ('key2', 'tag2', 'text2', 'keywords2')], 0)
        assert capsys.readouterr().out == (
                "called TreeItem.childCount\n"
                "called TreeItem.child with arg 0\n"
                "called TreeItem.text with arg 0\n"
                "called TreeItem.child with arg 0\n"
                f"called TreeItem.data with args (0, {testee.core.Qt.ItemDataRole.UserRole!r})\n"
                "called TreeItem.child with arg 0\n"
                "called TreeItem.child with arg 0\n"
                "called TreeItem.text with arg 1\n"
                "called TreeItem.child with arg 0\n"
                f"called TreeItem.data with args (1, {testee.core.Qt.ItemDataRole.UserRole!r})\n"
                "called TreeItem.child with arg 1\n"
                "called TreeItem.text with arg 0\n"
                "called TreeItem.child with arg 1\n"
                f"called TreeItem.data with args (0, {testee.core.Qt.ItemDataRole.UserRole!r})\n"
                "called TreeItem.child with arg 1\n"
                "called TreeItem.child with arg 1\n"
                "called TreeItem.text with arg 1\n"
                "called TreeItem.child with arg 1\n"
                f"called TreeItem.data with args (1, {testee.core.Qt.ItemDataRole.UserRole!r})\n")
        testobj.activeitem = subitem2
        assert testobj.get_treeitems() == ([('key1', 'tag1', 'text1', 'keywords1'),
                                            ('key2', 'tag2', 'text2', 'keywords2')], 'key2')
        assert capsys.readouterr().out == (
                "called TreeItem.childCount\n"
                "called TreeItem.child with arg 0\n"
                "called TreeItem.text with arg 0\n"
                "called TreeItem.child with arg 0\n"
                f"called TreeItem.data with args (0, {testee.core.Qt.ItemDataRole.UserRole!r})\n"
                "called TreeItem.child with arg 0\n"
                "called TreeItem.child with arg 0\n"
                "called TreeItem.text with arg 1\n"
                "called TreeItem.child with arg 0\n"
                f"called TreeItem.data with args (1, {testee.core.Qt.ItemDataRole.UserRole!r})\n"
                "called TreeItem.child with arg 1\n"
                "called TreeItem.text with arg 0\n"
                "called TreeItem.child with arg 1\n"
                f"called TreeItem.data with args (0, {testee.core.Qt.ItemDataRole.UserRole!r})\n"
                "called TreeItem.child with arg 1\n"
                "called TreeItem.child with arg 1\n"
                "called TreeItem.text with arg 1\n"
                "called TreeItem.child with arg 1\n"
                f"called TreeItem.data with args (1, {testee.core.Qt.ItemDataRole.UserRole!r})\n")

    def test_get_screensize(self, monkeypatch, capsys):
        """unittest for MainWindow.get_screensize
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'width', lambda x: 'yay wide')
        monkeypatch.setattr(testee.qtw.QMainWindow, 'height', lambda x: 'yay high')
        testobj = setup_mainwindow(monkeypatch, capsys)
        assert testobj.get_screensize() == ('yay wide', 'yay high')
        assert capsys.readouterr().out == ''

    def test_get_splitterpos(self, monkeypatch, capsys):
        """unittest for MainWindow.get_splitterpos
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.splitter = mockqtw.MockSplitter()
        assert capsys.readouterr().out == 'called Splitter.__init__\n'
        assert testobj.get_splitterpos() == ('left this wide', 'right that wide')
        assert capsys.readouterr().out == 'called Splitter.sizes\n'

    def test_sleep(self, monkeypatch, capsys):
        """unittest for MainWindow.sleep
        """
        def mock_hide(self, *args):
            """stub
            """
            print('called MockMainWindow.hide')
        monkeypatch.setattr(testee.qtw.QMainWindow, 'hide', mock_hide)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tray_icon = mockqtw.MockSysTrayIcon()
        testobj.sleep()
        assert capsys.readouterr().out == ('called TrayIcon.__init__\n'
                                           'called TrayIcon.show\n'
                                           'called MockMainWindow.hide\n')

    def test_revive(self, monkeypatch, capsys):
        """unittest for MainWindow.revive
        """
        def mock_show(self, *args):
            """stub
            """
            print('called MainWindow.show')
        monkeypatch.setattr(testee.qtw.QMainWindow, 'show', mock_show)
        testobj = setup_mainwindow(monkeypatch, capsys)
        assert capsys.readouterr().out == ''
        testobj.base.app_title = ''
        testobj.tray_icon = mockqtw.MockSysTrayIcon()
        testobj.revive(testee.qtw.QSystemTrayIcon.ActivationReason.Unknown)
        assert capsys.readouterr().out == (
                'called TrayIcon.__init__\n'
                "called TrayIcon.showMessage with args ('', 'revive_message')\n")
        testobj.revive(testee.qtw.QSystemTrayIcon.ActivationReason.Context)
        assert capsys.readouterr().out == ''
        testobj.revive()
        assert capsys.readouterr().out == ('called MainWindow.show\n'
                                           'called TrayIcon.hide\n')

    def test_get_next_item(self, monkeypatch, capsys):
        """unittest for MainWindow.get_next_item
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        subitem1 = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        subitem2 = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.root.subitems = [subitem1, subitem2]
        testobj.activeitem = subitem1
        assert testobj.get_next_item() == subitem2
        assert capsys.readouterr().out == ("called TreeItem.indexOfChild\n"
                                           "called TreeItem.childCount\n"
                                           "called TreeItem.child with arg 1\n")
        testobj.activeitem = subitem2
        assert testobj.get_next_item() is None
        assert capsys.readouterr().out == ("called TreeItem.indexOfChild\n"
                                           "called TreeItem.childCount\n")

    def test_get_prev_item(self, monkeypatch, capsys):
        """unittest for MainWindow.get_prev_item
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        subitem1 = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        subitem2 = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.root = mockqtw.MockTreeItem()
        testobj.root.subitems = [subitem1, subitem2]
        testobj.activeitem = subitem2
        assert testobj.get_prev_item() == subitem1
        testobj.activeitem = subitem1
        assert testobj.get_prev_item() is None

    def test_get_itempos(self, monkeypatch, capsys):
        """unittest for MainWindow.get_itempos
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.root.subitems = ['cheddar', 'stilton', 'gouda']
        assert testobj.get_itempos('gouda') == testobj.root.subitems.index('gouda')

    def test_get_itemcount(self, monkeypatch, capsys):
        """unittest for MainWindow.get_itemcount
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.root.subitems = ['cheddar', 'stilton', 'gouda']
        assert testobj.get_itemcount() == len(testobj.root.subitems)
        assert capsys.readouterr().out == "called TreeItem.childCount\n"

    def test_get_item_at_pos(self, monkeypatch, capsys):
        """unittest for MainWindow.get_item_at_pos
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.root.subitems = ['cheddar', 'stilton', 'gouda']
        assert testobj.get_item_at_pos(1) == 'stilton'

    def test_get_rootitem_title(self, monkeypatch, capsys):
        """unittest for MainWindow.get_rootitem_title
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.root._text = {0: 'title'}
        assert testobj.get_rootitem_title() == 'title'

    def test_set_rootitem_title(self, monkeypatch, capsys):
        """unittest for MainWindow.set_rootitem_title
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_rootitem_title('text')
        assert testobj.root._text == ['text']

    def test_get_item_text(self, monkeypatch, capsys):
        """unittest for MainWindow.get_item_text
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        item._text = {1: 'full item text'}
        assert testobj.get_item_text(item) == 'full item text'

    def test_set_editor_text(self, monkeypatch, capsys):
        """unittest for MainWindow.set_editor_text
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockqtw.MockEditorWidget()
        testobj.set_editor_text('new editor text')
        assert capsys.readouterr().out == ('called Editor.__init__\n'
                                           'called Editor.setText with arg `new editor text`\n')

    def test_get_editor_text(self, monkeypatch, capsys):
        """unittest for MainWindow.get_editor_text
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockqtw.MockEditorWidget()
        testobj.get_editor_text()
        assert capsys.readouterr().out == ('called Editor.__init__\n'
                                           'called Editor.toPlainText\n')

    def test_set_item_text(self, monkeypatch, capsys):
        """unittest for MainWindow.set_item_text
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_item_text(item, 'new item text')
        assert item._text[1] == 'new item text'
        assert capsys.readouterr().out == (
                "called TreeItem.setText with args (1, 'new item text')\n")

    def test_get_item_keywords(self, monkeypatch, capsys):
        """unittest for MainWindow.get_item_keywords
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        item._data = ['', ['some', 'words']]
        assert testobj.get_item_keywords(item) == ['some', 'words']
        assert capsys.readouterr().out == (
                f'called TreeItem.data with args (1, {testee.core.Qt.ItemDataRole.UserRole!r})\n')

    def test_set_item_keywords(self, monkeypatch, capsys):
        """unittest for MainWindow.set_item_keywords
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_item_keywords(item, ['keyword', 'list'])
        assert item._data == [['keyword', 'list']]
        assert capsys.readouterr().out == (
                "called TreeItem.setData with args"
                f" (1, {testee.core.Qt.ItemDataRole.UserRole!r}, ['keyword', 'list'])\n")

    def test_show_statusbar_message(self, monkeypatch, capsys):
        """unittest for MainWindow.show_statusbar_message
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.sb = mockqtw.MockStatusBar()
        testobj.show_statusbar_message('text')
        assert capsys.readouterr().out == ('called StatusBar.__init__ with args ()\n'
                                           'called StatusBar.showMessage with arg `text`\n')

    def test_enable_selaction(self, monkeypatch, capsys):
        """unittest for MainWindow.enable_selaction
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        action = mockqtw.MockAction('text', 'action')
        testobj.selactions = {'actiontext': action}
        testobj.enable_selaction('actiontext')
        assert action.checked
        assert capsys.readouterr().out == ("called Action.__init__ with args ('text', 'action')\n"
                                           "called Action.setChecked with arg `True`\n")

    def test_disable_selaction(self, monkeypatch, capsys):
        """unittest for MainWindow.disable_selaction
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        action = mockqtw.MockAction('text', 'action')
        action.checked = True
        testobj.selactions = {'actiontext': action}
        testobj.disable_selaction('actiontext')
        assert not action.checked

    def test_showmsg(self, monkeypatch, capsys):
        """unittest for MainWindow.showmsg
        """
        def mock_info(self, *args):
            """stub
            """
            print(f'called MessageBox.information with args `{args[0]}`, `{args[1]}`')
        monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_info)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'app_title'
        testobj.showmsg('message')
        assert capsys.readouterr().out == ('called MessageBox.information with args'
                                           ' `app_title`, `message`\n')

    def test_ask_question(self, monkeypatch, capsys):
        """unittest for MainWindow.ask_question
        """
        def mock_ask(self, *args):
            """stub
            """
            print('called MessageBox.question with args', args)
            return 'x'
        monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_ask)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'app_title'
        assert not testobj.ask_question('question')
        assert capsys.readouterr().out == ('called MessageBox.question with args'
                                           " ('app_title', 'question')\n")

    def test_show_dialog(self, monkeypatch, capsys):
        """unittest for MainWindow.show_dialog
        """
        class MockDialogParent:
            """stub for a class generating a dialog
            """
            def __init__(self, master, *args, **kwargs):
                print("called DialogParent.__init__ with args", args)
                self.master = master
                self.gui = MockDialog(self, *args, **kwargs)
        class MockDialog:
            "stub for a Dialog generated by a Dialog parent"
            def __init__(self, parent, *args, **kwargs):
                print("called Dialog.__init__ with args", args)
                self.parent = parent
            def exec(self):
                print("called Dialog.exec")
                self.parent.master.dialog_data = {'x': 'y'}
                return testee.qtw.QDialog.DialogCode.Accepted
        testobj = setup_mainwindow(monkeypatch, capsys)
        assert testobj.show_dialog(MockDialogParent, self, 'arg') == (True, {'x': 'y'})
        assert capsys.readouterr().out == (
                f"called DialogParent.__init__ with args ({self}, 'arg')\n"
                f"called Dialog.__init__ with args ({self}, 'arg')\n"
                "called Dialog.exec\n")

    def test_get_text_from_user(self, monkeypatch, capsys):
        """unittest for MainWindow.get_text_from_user
        """
        def mock_gettext(self, *args, **kwargs):
            """stub
            """
            print('called InputDialog.getText with args', args, kwargs)
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_gettext)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'app_title'
        testobj.get_text_from_user('prompt', 'default')
        assert capsys.readouterr().out == ("called InputDialog.getText with args"
                                           " ('app_title', 'prompt') {'text': 'default'}\n")

    def test_get_choice_from_user(self, monkeypatch, capsys):
        """unittest for MainWindow.get_choice_from_user
        """
        def mock_getitem(self, *args, **kwargs):
            """stub
            """
            print('called InputDialog.getItem with args', args, kwargs)
        monkeypatch.setattr(testee.qtw.QInputDialog, 'getItem', mock_getitem)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'app_title'
        testobj.get_choice_from_user('prompt', ['choices'], 0)
        assert capsys.readouterr().out == ("called InputDialog.getItem with args"
                                           " ('app_title', 'prompt', ['choices'])"
                                           " {'current': 0, 'editable': False}\n")


class TestOptionsDialog:
    """unittests for qt_gui.OptionsDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for OptionsDialog.init
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
        # in methoden die een super() aanroep bevatten om een methode op aan te roepen moet ik de
        # overgeërfde methoden die via self worden aangeroepen ook op de superklasse patchen
        # de superklasse zelf patchen werkt blijkbaar niet
        def mock_setWindowTitle(self, *args):
            """stub
            """
            print('called Dialog.setWindowTitle with args', args)
        def mock_setLayout(self, *args):
            """stub
            """
            print('called Dialog.setLayout')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mock_setLayout)
        testobj = testee.OptionsDialog('master', 'parent', 'xxx')   # {'text': 'value'})
        assert testobj.master == 'master'
        assert testobj.parent == 'parent'
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.gbox, testee.qtw.QGridLayout)
        assert capsys.readouterr().out == (
            'called Dialog.__init__\n'
            "called Dialog.setWindowTitle with args ('xxx',)\n"
            'called VBox.__init__\n'
            'called Grid.__init__\n'
            "called VBox.addLayout with arg MockGridLayout\n"
            'called Dialog.setLayout\n')

    def setup_testobj(self, monkeypatch, capsys):
        "initialize testdouble"
        def mock_init(self, *args):
            print('called Dialog.__init__')
            self.parent = args[0]
        monkeypatch.setattr(testee.OptionsDialog, '__init__', mock_init)
        testobj = testee.OptionsDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called Dialog.__init__\n'
        return testobj

    def test_add_checkbox_line_to_grid(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_checkbox_line_to_grid
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        result = testobj.add_checkbox_line_to_grid(1, 'label', True)
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
            f"called Label.__init__ with args ('label', {testobj})\n"
            "called Grid.addWidget with arg MockLabel at (1, 0)\n"
            f"called CheckBox.__init__ with args ('', {testobj})\n"
            'called CheckBox.setChecked with arg True\n'
            "called Grid.addWidget with arg MockCheckBox at (1, 1)\n")

    def test_add_buttonbox(self, monkeypatch, capsys):
        """unittest for OptionsDialog.add_buttonbox
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        testobj.gbox = mockqtw.MockGridLayout()
        testobj.accept = lambda: 'dummy callback'
        testobj.reject = lambda: 'dummy callback'
        assert capsys.readouterr().out == "called VBox.__init__\ncalled Grid.__init__\n"
        testobj.add_buttonbox('yes', 'nooo')
        assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            'called HBox.addStretch\n'
            f"called PushButton.__init__ with args ('yes', {testobj}) {{}}\n"
            f'called Signal.connect with args ({testobj.accept},)\n'
            "called HBox.addWidget with arg MockPushButton\n"
            f"called PushButton.__init__ with args ('nooo', {testobj}) {{}}\n"
            f'called Signal.connect with args ({testobj.reject},)\n'
            "called HBox.addWidget with arg MockPushButton\n"
            'called HBox.addStretch\n'
            "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for OptionsDialog.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockqtw.MockCheckBox()
        check.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n")
        assert capsys.readouterr().out == ""
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == "called CheckBox.isChecked\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for OptionsDialog.accept
        """
        def mock_accept(self, *args):
            """stub
            """
            print('called Dialog.accept')
        def mock_confirm():
            print('called SetOptions.confirm')
            return {'text': False}
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert testobj.parent.dialog_data == {'text': False}
        assert capsys.readouterr().out == ('called SetOptions.confirm\n'
                                           'called Dialog.accept\n')


class TestCheckDialog:
    """unittests for qt_gui.CheckDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for CheckDialog.init
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
        def mock_setWindowTitle(self, *args):
            """stub
            """
            print('called Dialog.setWindowTitle with args', args)
        def mock_setWindowIcon(self, *args):
            """stub
            """
            print('called Dialog.setWindowIcon with args', args)
        def mock_setLayout(self, *args):
            """stub
            """
            print('called Dialog.setLayout')
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = testee.CheckDialog('master', mockparent, 'xxx')  # {}, 'message')
        assert testobj.parent == mockparent
        assert capsys.readouterr().out == (
            'called Dialog.__init__\n'
            "called Dialog.setWindowTitle with args ('xxx',)\n"
            "called Dialog.setWindowIcon with args ('icon',)\n"
            'called VBox.__init__\n'
            'called Dialog.setLayout\n')

    def setup_testobj(self, monkeypatch, capsys):
        "initialize testdouble"
        def mock_init(self, *args):
            print('called Dialog.__init__')
            self.parent = args[0]
        monkeypatch.setattr(testee.CheckDialog, '__init__', mock_init)
        testobj = testee.CheckDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called Dialog.__init__\n'
        return testobj

    def test_add_label(self, monkeypatch, capsys):
        """unittest for CheckDialog.add_label
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_label('xxx')
        assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            f"called Label.__init__ with args ('xxx', {testobj})\n"
            "called HBox.addWidget with arg MockLabel\n"
            "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for CheckDialog.add_checkbox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_checkbox('xxx')
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            f"called CheckBox.__init__ with args ('xxx', {testobj})\n"
            "called HBox.addWidget with arg MockCheckBox\n"
            "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_ok_buttonbox(self, monkeypatch, capsys):
        """unittest for CheckDialog.add_ok_buttonbox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_ok_buttonbox()
        assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            'called HBox.addStretch\n'
            f"called PushButton.__init__ with args ('&Ok', {testobj}) {{}}\n"
            f"called Signal.connect with args ({testobj.klaar},)\n"
            "called HBox.addWidget with arg MockPushButton\n"
            'called HBox.addStretch\n'
            "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for CheckDialog.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockqtw.MockCheckBox()
        check.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n")
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == "called CheckBox.isChecked\n"

    def test_klaar(self, monkeypatch, capsys):
        """unittest for CheckDialog.klaar
        """
        def mock_confirm():
            print('called SetCheck.confirm')
            return {'text': False}
        def mock_accept(self, *args):
            """stub
            """
            print('called Dialog.accept')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.klaar()
        assert testobj.parent.dialog_data == {'text': False}
        assert capsys.readouterr().out == ('called SetCheck.confirm\n'
                                           'called Dialog.accept\n')


class TestKeywordsDialog:
    """unittests for qt_gui.KeywordsDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.init
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
        def mock_setWindowTitle(self, *args):
            """stub
            """
            print('called Dialog.setWindowTitle with args', args)
        def mock_setWindowIcon(self, *args):
            """stub
            """
            print('called Dialog.setWindowIcon with args', args)
        def mock_resize(self, *args):
            """stub
            """
            print('called Dialog.resize')
        def mock_setLayout(self, *args):
            """stub
            """
            print('called Dialog.setLayout')
        parent = types.SimpleNamespace(nt_icon='icon', base=types.SimpleNamespace(
            app_title='title', opts={'Keywords': ['x', 'y']}))
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mock_resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mock_setLayout)
        # monkeypatch.setattr(gui.KeywordsDialog, 'create_actions', mock_create_actions)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = testee.KeywordsDialog('master', parent, 'xxx')
        assert testobj.master == 'master'
        assert testobj.parent == parent
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.hbox, testee.qtw.QHBoxLayout)
        assert capsys.readouterr().out == (
            'called Dialog.__init__\n'
            "called Dialog.setWindowTitle with args ('xxx',)\n"
            "called Dialog.setWindowIcon with args ('icon',)\n"
            'called Dialog.resize\n'
            'called VBox.__init__\n'
            'called HBox.__init__\n'
            "called VBox.addLayout with arg MockHBoxLayout\n"
            'called Dialog.setLayout\n')

    def setup_testobj(self, monkeypatch, capsys):
        "initialize testdouble"
        def mock_init(self, *args):
            print('called Dialog.__init__')
        monkeypatch.setattr(testee.KeywordsDialog, '__init__', mock_init)
        testobj = testee.KeywordsDialog()
        assert capsys.readouterr().out == 'called Dialog.__init__\n'
        return testobj

    def test_add_list(self, monkeypatch, capsys):
        "unittest for KeywordsDialog.add_list"
        def callback():
            "dummy callback"
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QListWidget', mockqtw.MockListBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == 'called HBox.__init__\n'
        result = testobj.add_list('xxx', [], callback)
        assert isinstance(result, testee.qtw.QListWidget)
        assert capsys.readouterr().out == (
            'called VBox.__init__\n'
            f"called Label.__init__ with args ('xxx', {testobj})\n"
            "called VBox.addWidget with arg MockLabel\n"
            'called List.__init__\n'
            'called List.setSelectionMode\n'
            f"called Signal.connect with args ({callback},)\n"
            'called List.addItems with arg `[]`\n'
            "called VBox.addWidget with arg MockListBox\n"
            "called HBox.addLayout with arg MockVBoxLayout\n")

        result = testobj.add_list('xxx', ['x', 'y'], callback, first=True, last=True)
        assert isinstance(result, testee.qtw.QListWidget)
        assert capsys.readouterr().out == (
            "called HBox.addStretch\n"
            'called VBox.__init__\n'
            f"called Label.__init__ with args ('xxx', {testobj})\n"
            "called VBox.addWidget with arg MockLabel\n"
            'called List.__init__\n'
            'called List.setSelectionMode\n'
            f"called Signal.connect with args ({callback},)\n"
            "called List.addItems with arg `['x', 'y']`\n"
            "called VBox.addWidget with arg MockListBox\n"
            "called HBox.addLayout with arg MockVBoxLayout\n"
            "called HBox.addStretch\n")

    def test_add_buttons(self, monkeypatch, capsys):
        "unittest for KeywordsDialog.add_buttons"
        def callback():
            "dummy callback"
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == 'called HBox.__init__\n'
        result = testobj.add_buttons([('xxxx', callback), ('yyyy', None)])
        assert len(result) == 1
        assert isinstance(result[0], testee.qtw.QPushButton)
        assert capsys.readouterr().out == (
            'called VBox.__init__\n'
            'called VBox.addStretch\n'
            f"called PushButton.__init__ with args ('xxxx', {testobj}) {{}}\n"
            f"called Signal.connect with args ({callback},)\n"
            "called VBox.addWidget with arg MockPushButton\n"
            f"called Label.__init__ with args ('yyyy', {testobj})\n"
            "called VBox.addWidget with arg MockLabel\n"
            'called VBox.addStretch\n'
            "called HBox.addLayout with arg MockVBoxLayout\n")

    def test_create_buttonbox(self, monkeypatch, capsys):
        "unittest for KeywordsDialog.create_buttonbox"
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == 'called VBox.__init__\n'
        testobj.create_buttonbox()
        assert capsys.readouterr().out == ('called HBox.__init__\n'
                                           'called HBox.addStretch\n'
                                           'called ButtonBox.__init__ with args (3,)\n'
                                           f"called Signal.connect with args ({testobj.accept},)\n"
                                           f"called Signal.connect with args ({testobj.reject},)\n"
                                           "called HBox.addWidget with arg MockButtonBox\n"
                                           'called HBox.addStretch\n'
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_create_actions(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.create_actions
        """
        def callback1():
            "dummy callback"
        def callback2():
            "dummy callback"
        def mock_addAction(self, *args):
            """stub
            """
            print('called Dialog.addAction')
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.gui, 'QAction', mockqtw.MockAction)
        monkeypatch.setattr(testee.KeywordsDialog, 'addAction', mock_addAction)
        testobj.create_actions([])
        assert capsys.readouterr().out == ""
        testobj.create_actions([('xx', 'Ctrl+X', callback1), ('yy', 'Ctrl+Y', callback2)])
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('xx', {testobj})\n"
                'called Action.setShortcut with arg `Ctrl+X`\n'
                f"called Signal.connect with args ({callback1},)\n"
                'called Dialog.addAction\n'
                f"called Action.__init__ with args ('yy', {testobj})\n"
                'called Action.setShortcut with arg `Ctrl+Y`\n'
                f"called Signal.connect with args ({callback2},)\n"
                'called Dialog.addAction\n')

    def test_activate(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate - test met geselecteerd item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        win = mockqtw.MockListBox()
        monkeypatch.setattr(win, 'currentItem', lambda: None)
        monkeypatch.setattr(win, 'item', lambda x: mockqtw.MockListItem('first item'))
        assert capsys.readouterr().out == 'called List.__init__\n'
        testobj.activate(win)
        assert capsys.readouterr().out == (
                "called ListItem.__init__ with args ('first item',)\n"
                'called ListItem.setSelected with arg `True` for `first item`\n'
                'called List.setFocus with arg `True`\n')

    def test_activate_2(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate: test zonder geselecteerd item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        win = mockqtw.MockListBox()
        monkeypatch.setattr(win, 'currentItem', lambda: mockqtw.MockListItem('current item'))
        assert capsys.readouterr().out == 'called List.__init__\n'
        testobj.activate(win)
        assert capsys.readouterr().out == (
                "called ListItem.__init__ with args ('current item',)\n"
                'called ListItem.setSelected with arg `True` for `current item`\n'
                'called List.setFocus with arg `True`\n')

    def test_moveitem(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.moveitem
        """
        def mock_selectedItems(self):
            """stub
            """
            print(f'called List.selectedItems on `{self.list}`')
            return [mockqtw.MockListItem('item 1'), mockqtw.MockListItem('item 2')]
        def mock_takeItem(self, rowno):
            """stub
            """
            print(f'called List.takeItem with arg `{rowno}` on `{self.list}`')
        def mock_row(self, item):
            """stub
            """
            print(f'called List.row with arg `{item._name}` on `{self.list}`')
            return item._name[-1]
        def mock_addItem(self, item):
            """stub
            """
            print(f'called List.addItem with arg `{item._name}` on `{self.list}`')
        monkeypatch.setattr(mockqtw.MockListBox, 'selectedItems', mock_selectedItems)
        monkeypatch.setattr(mockqtw.MockListBox, 'takeItem', mock_takeItem)
        monkeypatch.setattr(mockqtw.MockListBox, 'row', mock_row)
        testobj = self.setup_testobj(monkeypatch, capsys)
        from_ = mockqtw.MockListBox()
        from_.addItem('fromlist')
        assert capsys.readouterr().out == ('called List.__init__\n'
                                           'called List.addItem with arg `fromlist`\n')
        to = mockqtw.MockListBox()
        to.addItem('tolist')
        assert capsys.readouterr().out == ('called List.__init__\n'
                                           'called List.addItem with arg `tolist`\n')
        monkeypatch.setattr(mockqtw.MockListBox, 'addItem', mock_addItem)
        testobj.moveitem(from_, to)
        assert capsys.readouterr().out == ("called List.selectedItems on `['fromlist']`\n"
                                           "called ListItem.__init__ with args ('item 1',)\n"
                                           "called ListItem.__init__ with args ('item 2',)\n"
                                           "called List.row with arg `item 1` on `['fromlist']`\n"
                                           "called List.takeItem with arg `1` on `['fromlist']`\n"
                                           "called List.addItem with arg `item 1` on `['tolist']`\n"
                                           "called List.row with arg `item 2` on `['fromlist']`\n"
                                           "called List.takeItem with arg `2` on `['fromlist']`\n"
                                           "called List.addItem with arg `item 2` on `['tolist']`\n")

    def test_ask_for_tag(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.accept
        """
        monkeypatch.setattr(testee.qtw, 'QInputDialog', mockqtw.MockInputDialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_for_tag('xxx', 'yyy') == ('', False)
        assert capsys.readouterr().out == (
                f"called InputDialog.getText with args {testobj} ('xxx', 'yyy') {{}}\n")

    def test_add_tag_to_list(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.accept
        """
        listbox = mockqtw.MockListBox()
        assert capsys.readouterr().out == "called List.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_tag_to_list('xxx', listbox)
        assert capsys.readouterr().out == "called List.addItem with arg `xxx`\n"

    def test_get_listvalues(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.accept
        """
        tolist = mockqtw.MockListBox()
        item1 = mockqtw.MockListItem('1')
        item2 = mockqtw.MockListItem('2')
        tolist.addItem(item1)
        tolist.addItem(item2)
        assert capsys.readouterr().out == ('called List.__init__\n'
                                           "called ListItem.__init__ with args ('1',)\n"
                                           "called ListItem.__init__ with args ('2',)\n"
                                           f'called List.addItem with arg `{item1}`\n'
                                           f'called List.addItem with arg `{item2}`\n')
        testobj = self.setup_testobj(monkeypatch, capsys)
        # breakpoint()
        assert testobj.get_listvalues(tolist) == ['1', '2']
        assert capsys.readouterr().out == ('called ListItem.text\n'
                                           'called ListItem.text\n')

    def test_accept(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.accept
        """
        def mock_confirm():
            print('called DialogParent.confirm')
            return ['1', '2']
        def mock_accept(self, *args):
            """stub
            """
            print('called Dialog.accept')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.parent = types.SimpleNamespace()
        testobj.accept()
        assert capsys.readouterr().out == ('called DialogParent.confirm\n'
                                           'called Dialog.accept\n')
        assert testobj.parent.dialog_data == ['1', '2']


class TestKeywordsManager:
    """unittests for qt_gui.KeywordsManager
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for KeywordsManager.init
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
        def mock_setWindowTitle(self, *args):
            """stub
            """
            print('called Dialog.setWindowTitle with args', args)
        def mock_setWindowIcon(self, *args):
            """stub
            """
            print('called Dialog.setWindowIcon with args', args)
        def mock_resize(self, *args):
            """stub
            """
            print('called Dialog.resize')
        def mock_setLayout(self, *args):
            """stub
            """
            print('called Dialog.setLayout')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mock_resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        parent = types.SimpleNamespace(nt_icon='icon')
        testobj = testee.KeywordsManager('master', parent, 'xxx', 'yyy')
        assert testobj.master == 'master'
        assert testobj.parent == parent
        assert isinstance(testobj.gbox, testee.qtw.QGridLayout)
        assert capsys.readouterr().out == (
            'called Dialog.__init__\n'
            "called Dialog.setWindowTitle with args ('xxx',)\n"
            "called Dialog.setWindowIcon with args ('icon',)\n"
            'called Dialog.resize\n'
            'called VBox.__init__\n'
            'called Grid.__init__\n'
            "called VBox.addLayout with arg MockGridLayout\n"
            'called ButtonBox.__init__ with args (8,)\n'
            'called VBox.addWidget with arg MockButtonBox\n'
            'called Dialog.setLayout\n')

    def setup_testobj(self, monkeypatch, capsys):
        "initialize testdouble"
        def mock_init(self, *args):
            print('called Dialog.__init__')
            self.parent = args[0]
        monkeypatch.setattr(testee.KeywordsManager, '__init__', mock_init)
        testobj = testee.KeywordsManager(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called Dialog.__init__\n'
        return testobj

    def test_add_label(self, monkeypatch, capsys):
        """unittest voor KeywordsManager.add_label
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.add_label('xxx', 1, 2)
        assert capsys.readouterr().out == (
            "called Label.__init__ with args ('xxx',)\n"
            "called Grid.addWidget with arg MockLabel at (1, 2)\n")
        testobj.add_label('xxx', 1, -1)
        assert capsys.readouterr().out == (
            "called Label.__init__ with args ('xxx',)\n"
            "called Grid.columnCount\n"
            "called Grid.addWidget with arg MockLabel at (1, 0, 1, 1)\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest voor KeywordsManager.add_combobox
        """
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.add_combobox(1, 2)
        assert capsys.readouterr().out == (
            'called ComboBox.__init__\n'
            "called Grid.addWidget with arg MockComboBox at (1, 2)\n")

    def test_add_lineinput(self, monkeypatch, capsys):
        """unittest voor KeywordsManager.add_lineinput
        """
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.add_lineinput(1, 2)
        assert capsys.readouterr().out == (
            f'called LineEdit.__init__ with args ({testobj},)\n'
            "called Grid.addWidget with arg MockLineEdit at (1, 2)\n")

    def test_add_button(self, monkeypatch, capsys):
        """unittest voor KeywordsManager.add_button
        """
        def callback():
            "dummy callback"
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.add_button('xxx', callback, 1, 2)
        assert capsys.readouterr().out == (
            f"called PushButton.__init__ with args ('xxx', {testobj}) {{}}\n"
            f"called Signal.connect with args ({callback},)\n"
            "called Grid.addWidget with arg MockPushButton at (1, 2)\n")

    def test_reset_combobox(self, monkeypatch, capsys):
        """unittest voor KeywordsManager.reset_combobox
        """
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        combo = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.reset_combobox(combo, ['x', 'y'])
        assert capsys.readouterr().out == (
            'called ComboBox.clear\n'
            "called ComboBox.addItems with arg ['x', 'y']\n"
            'called ComboBox.clearEditText\n')

    def test_reset_lineinput(self, monkeypatch, capsys):
        """unittest voor KeywordsManager.reset_lineinput
        """
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        text = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == f"called LineEdit.__init__ with args ()\n"
        testobj.reset_lineinput(text)
        assert capsys.readouterr().out == 'called LineEdit.clear\n'

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittset for KeywordsManager.get_combobox_value
        """
        widget = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_combobox_value(widget) == 'current text'
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_get_lineinput_text(self, monkeypatch, capsys):
        """unittset for KeywordsManager.get_lineinput_text
        """
        widget = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_lineinput_text(widget) == ''
        assert capsys.readouterr().out == ("called LineEdit.text\n")

    def test_ask_question(self, monkeypatch, capsys):
        """unittset for KeywordsManager.ask_question
        """
        def mock_ask(*args):
            print('called MessageBox.question with args', args)
            return mockqtw.MockMessageBox.StandardButton.Yes
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.ask_question('xxx', 'yyy')
        assert capsys.readouterr().out == (
                f"called MessageBox.question with args `{testobj}` `xxx` `yyy` `12`\n")
        monkeypatch.setattr(mockqtw.MockMessageBox, 'question', mock_ask)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.ask_question('xxx', 'yyy')
        assert capsys.readouterr().out == (
                f"called MessageBox.question with args ({testobj}, 'xxx', 'yyy')\n")

    def test_ask_question_w_cancel(self, monkeypatch, capsys):
        """unittset for KeywordsManager.ask_question_w_cancel
        """
        def mock_clicked(self):
            print('called MessageBox.clickedButton')
            return mockqtw.MockMessageBox.StandardButton.No
        def mock_clicked_2(self):
            print('called MessageBox.clickedButton')
            return mockqtw.MockMessageBox.StandardButton.Yes
        def mock_clicked_3(self):
            print('called MessageBox.clickedButton')
            return mockqtw.MockMessageBox.StandardButton.Cancel
        monkeypatch.setattr(testee.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(mockqtw.MockMessageBox, 'clickedButton', mock_clicked)
        assert testobj.ask_question_w_cancel('xxx', 'yyy') == (False, False)
        assert capsys.readouterr().out == ("called MessageBox.__init__ with args () {}\n"
                                           "called MessageBox.setText with arg `xxx`\n"
                                           "called MessageBox.setInformativeText with arg `yyy`\n"
                                           "called MessageBox.setStandardButtons\n"
                                           "called MessageBox.setDefaultButton with arg `4`\n"
                                           "called MessageBox.exec\n"
                                           "called MessageBox.clickedButton\n")
        monkeypatch.setattr(mockqtw.MockMessageBox, 'clickedButton', mock_clicked_2)
        assert testobj.ask_question_w_cancel('xxx', 'yyy') == (True, False)
        assert capsys.readouterr().out == ("called MessageBox.__init__ with args () {}\n"
                                           "called MessageBox.setText with arg `xxx`\n"
                                           "called MessageBox.setInformativeText with arg `yyy`\n"
                                           "called MessageBox.setStandardButtons\n"
                                           "called MessageBox.setDefaultButton with arg `4`\n"
                                           "called MessageBox.exec\n"
                                           "called MessageBox.clickedButton\n")
        monkeypatch.setattr(mockqtw.MockMessageBox, 'clickedButton', mock_clicked_3)
        assert testobj.ask_question_w_cancel('xxx', 'yyy') == (False, True)
        assert capsys.readouterr().out == ("called MessageBox.__init__ with args () {}\n"
                                           "called MessageBox.setText with arg `xxx`\n"
                                           "called MessageBox.setInformativeText with arg `yyy`\n"
                                           "called MessageBox.setStandardButtons\n"
                                           "called MessageBox.setDefaultButton with arg `4`\n"
                                           "called MessageBox.exec\n"
                                           "called MessageBox.clickedButton\n")


class TestGetTextDialog:
    """unittests for qt_gui.GetTextDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for GetTextDialog.init
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
        def mock_setWindowTitle(self, *args):
            """stub
            """
            print('called Dialog.setWindowTitle with args', args)
        def mock_setWindowIcon(self, *args):
            """stub
            """
            print('called Dialog.setWindowIcon with args', args)
        def mock_setLayout(self, *args):
            """stub
            """
            print('called Dialog.setLayout')
        parent = types.SimpleNamespace(nt_icon='icon')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = testee.GetTextDialog('master', parent, 'title')
        assert testobj.master == 'master'
        assert testobj.parent == parent
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           "called Dialog.setWindowTitle with args ('title',)\n"
                                           "called Dialog.setWindowIcon with args ('icon',)\n"
                                           'called VBox.__init__\n'
                                           'called Dialog.setLayout\n')

    def setup_testobj(self, monkeypatch, capsys):
        "initialize testdouble"
        def mock_init(self, *args):
            print('called Dialog.__init__')
            self.parent = args[0]
        monkeypatch.setattr(testee.GetTextDialog, '__init__', mock_init)
        testobj = testee.GetTextDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called Dialog.__init__\n'
        return testobj

    def test_add_label(self, monkeypatch, capsys):
        """unittest voor GetTextDialog.add_label
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_label('xxx')
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Label.__init__ with args ('xxx', {testobj})\n"
                                           "called HBox.addWidget with arg MockLabel\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_lineinput(self, monkeypatch, capsys):
        """unittest voor GetTextDialog.add_lineinput
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_lineinput('xxx')
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f'called LineEdit.__init__ with args ({testobj},)\n'
                                           "called LineEdit.setText with arg `xxx`\n"
                                           "called HBox.addWidget with arg MockLineEdit\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_okcancel_buttonbox(self, monkeypatch, capsys):
        "unittest for GetTextDialog.add_okcancel_buttonbox"
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == 'called VBox.__init__\n'
        testobj.add_okcancel_buttonbox()
        assert capsys.readouterr().out == ('called ButtonBox.__init__ with args (3,)\n'
                                           f"called Signal.connect with args ({testobj.accept},)\n"
                                           f"called Signal.connect with args ({testobj.reject},)\n"
                                           "called VBox.addWidget with arg MockButtonBox\n")

    def test_add_checkbox_line(self, monkeypatch, capsys):
        """unittest for GetTextDialog.add_checkbox
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_checkbox_line([('xxx', False), ('yyy', True)])
        assert len(result) == 2
        assert isinstance(result[0], testee.qtw.QCheckBox)
        assert isinstance(result[1], testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            f"called CheckBox.__init__ with args ('xxx', {testobj})\n"
            "called CheckBox.setChecked with arg False\n"
            "called HBox.addWidget with arg MockCheckBox\n"
            f"called CheckBox.__init__ with args ('yyy', {testobj})\n"
            "called CheckBox.setChecked with arg True\n"
            "called HBox.addWidget with arg MockCheckBox\n"
            "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for GetTextDialog.get_checkbox_value
        """
        check = mockqtw.MockCheckBox()
        check.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == "called CheckBox.isChecked\n"

    def test_get_lineinput_value(self, monkeypatch, capsys):
        """unittset for GetTextDialog.get_lineinput_text
        """
        widget = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_lineinput_value(widget) == ''
        assert capsys.readouterr().out == ("called LineEdit.text\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for GetTextDialog.accept
        """
        def mock_confirm():
            """stub
            """
            print('called GetTextDialog.confirm')
            return [False, '', False]
        def mock_accept(self, *args):
            """stub
            """
            print('called DialogParent.accept')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace()
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert testobj.parent.dialog_data == [False, '', False]
        assert capsys.readouterr().out == ('called GetTextDialog.confirm\n'
                                           'called DialogParent.accept\n')


class TestGetItemDialog:
    """unittests for qt_gui.GetItemDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for GetItemDialog.init
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
        def mock_setWindowTitle(self, *args):
            """stub
            """
            print('called Dialog.setWindowTitle with args', args)
        def mock_setWindowIcon(self, *args):
            """stub
            """
            print('called Dialog.setWindowIcon with args', args)
        def mock_setLayout(self, *args):
            """stub
            """
            print('called Dialog.setLayout')
        parent = types.SimpleNamespace(nt_icon='icon')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = testee.GetItemDialog('master', parent, 'title')
        assert testobj.master == 'master'
        assert testobj.parent == parent
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           "called Dialog.setWindowTitle with args ('title',)\n"
                                           "called Dialog.setWindowIcon with args ('icon',)\n"
                                           'called VBox.__init__\n'
                                           'called Dialog.setLayout\n')

    def setup_testobj(self, monkeypatch, capsys):
        "initialize testdouble"
        def mock_init(self, *args):
            print('called Dialog.__init__')
            self.parent = args[0]
        monkeypatch.setattr(testee.GetItemDialog, '__init__', mock_init)
        testobj = testee.GetItemDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called Dialog.__init__\n'
        return testobj

    def test_add_label(self, monkeypatch, capsys):
        """unittest voor GetItemDialog.add_label
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_label('xxx')
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Label.__init__ with args ('xxx', {testobj})\n"
                                           "called HBox.addWidget with arg MockLabel\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_combobox(self, monkeypatch, capsys):
        """unittest for GetItemDialog.add_combobox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_combobox(['xxx', 'yyy'], 'xxx')
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            "called ComboBox.__init__\n"
            "called ComboBox.addItems with arg ['xxx', 'yyy']\n"
            "called ComboBox.setCurrentIndex with arg `xxx`\n"
            "called HBox.addWidget with arg MockComboBox\n"
            "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_checkbox(self, monkeypatch, capsys):
        """unittest for GetItemDialog.add_checkbox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_checkbox('xxx', 'yyy')
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
            'called HBox.__init__\n'
            f"called CheckBox.__init__ with args ('xxx', {testobj})\n"
            "called CheckBox.setChecked with arg yyy\n"
            "called HBox.addWidget with arg MockCheckBox\n"
            "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_okcancel_buttonbox(self, monkeypatch, capsys):
        "unittest for GetItemDialog.add_okcancel_buttonbox"
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == 'called VBox.__init__\n'
        testobj.add_okcancel_buttonbox()
        assert capsys.readouterr().out == ('called ButtonBox.__init__ with args (3,)\n'
                                           f"called Signal.connect with args ({testobj.accept},)\n"
                                           f"called Signal.connect with args ({testobj.reject},)\n"
                                           "called VBox.addWidget with arg MockButtonBox\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for GetItemDialog.get_checkbox_value
        """
        check = mockqtw.MockCheckBox()
        check.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_value(check)
        assert capsys.readouterr().out == "called CheckBox.isChecked\n"

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittset for qtgui.get_combobox_value
        """
        widget = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_combobox_value(widget) == 'current text'
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for GetItemDialog.accept
        """
        def mock_confirm():
            """stub
            """
            print('called GetItemDialog.confirm')
            return [False, '', False]
        def mock_accept(self, *args):
            """stub
            """
            print('called DialogParent.accept')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mock_accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace()
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert testobj.parent.dialog_data == [False, '', False]
        assert capsys.readouterr().out == ('called GetItemDialog.confirm\n'
                                           'called DialogParent.accept\n')


class TestGridDialog:
    """unittests for qt_gui.GridDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for GridDialog.init
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
        def mock_setWindowTitle(self, *args):
            """stub
            """
            print('called Dialog.setWindowTitle with args', args)
        def mock_setLayout(self, *args):
            """stub
            """
            print('called Dialog.setLayout')
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = testee.GridDialog('parent', 'xxx', 'yyy')  # (('x', 'y'), ('a', 'b')), 'title')
        assert capsys.readouterr().out == (
                'called Dialog.__init__\n'
                "called Dialog.setWindowTitle with args ('xxx',)\n"
                'called VBox.__init__\n'
                'called Grid.__init__\n'
                "called VBox.addLayout with arg MockGridLayout\n"
                "called HBox.__init__\ncalled HBox.addStretch\n"
                f"called PushButton.__init__ with args ('yyy', {testobj}) {{}}\n"
                f"called Signal.connect with args ({testobj.reject},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n"
                "called Dialog.setLayout\n")

    def setup_testobj(self, monkeypatch, capsys):
        "initialize testdouble"
        def mock_init(self, *args):
            print('called Dialog.__init__')
            self.parent = args[0]
        monkeypatch.setattr(testee.GridDialog, '__init__', mock_init)
        testobj = testee.GridDialog(types.SimpleNamespace(dialog_data={}), {})
        assert capsys.readouterr().out == 'called Dialog.__init__\n'
        return testobj

    def test_add_label(self, monkeypatch, capsys):
        """unittest voor GridDialog.add_label
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gbox = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.add_label(1, 2, 'xxx')
        assert capsys.readouterr().out == (
            f"called Label.__init__ with args ('xxx', {testobj})\n"
            "called Grid.addWidget with arg MockLabel at (1, 2)\n")

    def test_send(self, monkeypatch, capsys):
        """unittset for GridDialog.send
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'exec', mockqtw.MockDialog.exec)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.send()
        assert capsys.readouterr().out == ("called Dialog.exec\n")
