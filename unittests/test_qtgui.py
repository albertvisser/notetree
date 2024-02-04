"""unittests for ./notetree/qt_gui.py
"""
import types
import pytest
from mockgui import mockqtwidgets as mockqtw
import notetree.qt_gui as gui


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
    monkeypatch.setattr(gui.qtw, 'QApplication', mockqtw.MockApplication)
    monkeypatch.setattr(gui.qtw.QWidget, '__init__', mock_init)
    # monkeypatch.setattr(gui.qtw, 'QWidget', mockqtw.MockWidget)
    monkeypatch.setattr(gui.qtw, 'QMainWindow', mockqtw.MockMainWindow)
    testobj = gui.MainWindow(MockNoteTree())
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
        assert capsys.readouterr().out == 'called Application.exec_\n'

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
        monkeypatch.setattr(gui.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'resize', mock_resize)
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
        monkeypatch.setattr(gui.qtw.QMainWindow, 'statusBar', mock_statusbar)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.setup_statusbar()
        assert hasattr(testobj, 'sb')
        assert capsys.readouterr().out == 'called MainWindow.statusbar\n'

    def test_setup_trayicon(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_trayicon
        """
        monkeypatch.setattr(gui.qtw, 'QSystemTrayIcon', mockqtw.MockSysTrayIcon)
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
        def mock_show(self, *args):
            """stub
            """
            print('called MockMainWindow.show')
        monkeypatch.setattr(gui.qtw.QMainWindow, 'setCentralWidget', mock_setcentralwidget)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'show', mock_show)
        monkeypatch.setattr(gui.qtw, 'QSplitter', mockqtw.MockSplitter)
        testobj = setup_mainwindow(monkeypatch, capsys)
        monkeypatch.setattr(testobj, 'setup_tree', lambda: 'treewidget')
        monkeypatch.setattr(testobj, 'setup_editor', lambda: 'editorwidget')
        testobj.setup_split_screen()
        assert hasattr(testobj, 'splitter')
        assert capsys.readouterr().out == ('called Splitter.__init__\n'
                                           'called MockMainWindow.setCentralWidget\n'
                                           'called Splitter.addWidget with arg `treewidget`\n'
                                           'called Splitter.addWidget with arg `editorwidget`\n'
                                           'called MockMainWindow.show\n')

    def test_setup_tree(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_tree
        """
        monkeypatch.setattr(gui.qtw, 'QTreeWidget', mockqtw.MockTreeWidget)
        testobj = setup_mainwindow(monkeypatch, capsys)
        newstuff = testobj.setup_tree()
        assert newstuff == testobj.tree
        assert capsys.readouterr().out == ('called Tree.__init__\n'
                                           'called Tree.setColumnCount with arg `2`\n'
                                           'called Tree.hideColumn\n'
                                           'called TreeItem.__init__ with args ()\n'
                                           "called TreeItem.setHidden with arg `True`\n"
                                           'called Tree.setSelectionMode\n'
                                           'called Signal.connect with args'
                                           f' ({testobj.changeselection},)\n')

    def test_setup_editor(self, monkeypatch, capsys):
        """unittest for MainWindow.setup_editor
        """
        monkeypatch.setattr(gui.qsc, 'QsciScintilla', mockqtw.MockEditorWidget)
        monkeypatch.setattr(gui.qsc, 'QsciLexerMarkdown', lambda: 'dummy lexer')
        testobj = setup_mainwindow(monkeypatch, capsys)
        newstuff = testobj.setup_editor()
        assert newstuff == testobj.editor
        assert capsys.readouterr().out == (f'called Editor.__init__ with args ({testobj},)\n'
                                           'called Editor.setFont\n'
                                           'called Editor.setWrapMode\n'
                                           'called Editor.setBraceMatching\n'
                                           'called Editor.setAutoIndent\n'
                                           'called Editor.setFolding\n'
                                           'called Editor.setCaretLineVisible\n'
                                           'called Editor.setCaretLineBackgroundColor\n'
                                           'called Editor.setLexer\n'
                                           'called Editor.setEnabled with arg False\n')

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
            return ((_("m_view"), (
                    (_("m_revorder"), self.callback, _("h_revorder"), 'F9'),
                    ("", None, None, None),
                    (_("m_selall"), self.callback, _("h_selall"), None),
                    (_("m_seltag"), self.callback, _("h_seltag"), None),
                    (_("m_seltxt"), self.callback, _("h_seltxt"), None), ), ), )
        # monkeypatch.setattr(gui.qtw, 'QMenuBar', MockMenuBar)  # Hm dit geeft al een runtimeerror
        monkeypatch.setattr(MockNoteTree, 'get_menudata', mock_get_menudata)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'menuBar', mock_menubar)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.opts = {'RevOrder': True, 'Selection': (1, 'find_me')}
        # import pdb; pdb.set_trace()
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
                "called Action.setShortcuts with arg `['F9']`\n"
                "called Menu.addSeparator\n"
                "called Action.__init__ with args ('-----', None)\n"
                f'called Menu.addAction with args `m_selall` {testobj.base.callback}\n'
                f"called Action.__init__ with args ('m_selall', {testobj.base.callback})\n"
                f'called Menu.addAction with args `m_seltag` {testobj.base.callback}\n'
                f"called Action.__init__ with args ('m_seltag', {testobj.base.callback})\n"
                f'called Menu.addAction with args `m_seltxt` {testobj.base.callback}\n'
                f"called Action.__init__ with args ('m_seltxt', {testobj.base.callback})\n")

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
        monkeypatch.setattr(gui.gui.QCloseEvent, 'accept', mock_accept)
        testobj.activeitem = None
        testobj.closeEvent(gui.gui.QCloseEvent())
        assert capsys.readouterr().out == 'called Event.accept\n'
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.activeitem = 'active item'
        testobj.closeEvent(gui.gui.QCloseEvent())
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
        monkeypatch.setattr(gui.qtw.QMainWindow, 'resize', mock_resize)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.set_screen(('x', 'y'))
        assert capsys.readouterr().out == "called resize with args ('x', 'y')\n"

    def test_set_splitter(self, monkeypatch, capsys):
        """unittest for MainWindow.set_splitter
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.splitter = mockqtw.MockSplitter()  # gui.qtw.QSplitter()
        testobj.set_splitter('split')
        assert capsys.readouterr().out == ('called Splitter.__init__\n'
                                           "called Splitter.setSizes with args ('split',)\n")

    def test_create_root(self, monkeypatch, capsys):
        """unittest for MainWindow.create_root
        """
        monkeypatch.setattr(gui.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.tree = mockqtw.MockTreeWidget()
        newroot = testobj.create_root('title')
        assert newroot.text(0) == 'title'
        assert testobj.activeitem == testobj.root
        assert capsys.readouterr().out == ('called Tree.__init__\n'
                                           'called Tree.takeTopLevelItem with arg `0`\n'
                                           'called TreeItem.__init__ with args ()\n'
                                           'called TreeItem.setText with arg `title` for col 0\n'
                                           'called Tree.addTopLevelItem\n'
                                           'called TreeItem.text for col 0\n')

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
        assert capsys.readouterr().out == ('called Font.__init__\n'
                                           'called Font.setBold with arg `x`\n'
                                           'called TreeItem.setFont\n')

    def test_editor_text_was_changed(self, monkeypatch, capsys):
        """unittest for MainWindow.editor_text_was_changed
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.editor = mockqtw.MockEditorWidget()
        assert testobj.editor_text_was_changed() == 'x'
        assert capsys.readouterr().out == 'called Editor.__init__\n'

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
        monkeypatch.setattr(mockqtw.MockTreeItem, 'setText', mock_settext)
        testobj.copy_text_from_editor_to_activeitem()
        assert capsys.readouterr().out == ('called Editor.__init__\n'
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
        assert capsys.readouterr().out == 'called TreeItem.data for col 0 role 256\n'

    def test_get_activeitem_title(self, monkeypatch, capsys):
        """unittest for MainWindow.get_activeitem_title
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.activeitem = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.activeitem._text = {0: 'title'}
        assert testobj.get_activeitem_title() == 'title'
        assert capsys.readouterr().out == 'called TreeItem.text for col 0\n'

    def test_set_activeitem_title(self, monkeypatch, capsys):
        """unittest for MainWindow.set_activeitem_title
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.activeitem = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_activeitem_title('text')
        assert testobj.activeitem._text == ['text']
        assert capsys.readouterr().out == 'called TreeItem.setText with arg `text` for col 0\n'

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
        monkeypatch.setattr(gui.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        expected = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        expected._text = ['tag', 'text']
        expected._data = ['key', 'keywords']

        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = gui.qtw.QTreeWidgetItem()  # waarom niet mockqtw.MockTreeItem()?
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.base.opts = {'RevOrder': False}
        result = testobj.add_item_to_tree('key', 'tag', 'text', 'keywords')
        assert result._text == expected._text
        assert result._data == expected._data
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with arg `tag` for col 0\n"
                                           "called TreeItem.setData to `key` with role 256"
                                           " for col 0\n"
                                           "called TreeItem.setText with arg `text` for col 1\n"
                                           "called TreeItem.setData to `keywords` with role 256"
                                           " for col 1\n"
                                           'called TreeItem.addChild\n')

        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.root = gui.qtw.QTreeWidgetItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.base.opts = {'RevOrder': True}
        testobj.add_item_to_tree('key', 'tag', 'text', 'keywords')
        assert result._text == expected._text
        assert result._data == expected._data
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with arg `tag` for col 0\n"
                                           "called TreeItem.setData to `key` with role 256"
                                           " for col 0\n"
                                           "called TreeItem.setText with arg `text` for col 1\n"
                                           "called TreeItem.setData to `keywords` with role 256"
                                           " for col 1\n"
                                           'called TreeItem.insertChild\n')

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
        testobj.root.subitems = [subitem1, subitem2]
        testobj.activeitem = None
        assert testobj.get_treeitems() == ([('key1', 'tag1', 'text1', 'keywords1'),
                                            ('key2', 'tag2', 'text2', 'keywords2')], 0)
        testobj.activeitem = subitem2
        assert testobj.get_treeitems() == ([('key1', 'tag1', 'text1', 'keywords1'),
                                            ('key2', 'tag2', 'text2', 'keywords2')], 'key2')

    def test_get_screensize(self, monkeypatch, capsys):
        """unittest for MainWindow.get_screensize
        """
        monkeypatch.setattr(gui.qtw.QMainWindow, 'width', lambda x: 'yay wide')
        monkeypatch.setattr(gui.qtw.QMainWindow, 'height', lambda x: 'yay high')
        testobj = setup_mainwindow(monkeypatch, capsys)
        assert testobj.get_screensize() == ('yay wide', 'yay high')
        assert capsys.readouterr().out == ''

    def test_get_splitterpos(self, monkeypatch, capsys):
        """unittest for MainWindow.get_splitterpos
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.splitter = mockqtw.MockSplitter()
        assert testobj.get_splitterpos() == ('left this wide', 'right that wide')
        assert capsys.readouterr().out == 'called Splitter.__init__\n'

    def test_sleep(self, monkeypatch, capsys):
        """unittest for MainWindow.sleep
        """
        def mock_hide(self, *args):
            """stub
            """
            print('called MockMainWindow.hide')
        monkeypatch.setattr(gui.qtw.QMainWindow, 'hide', mock_hide)
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
        monkeypatch.setattr(gui.qtw.QMainWindow, 'show', mock_show)
        testobj = setup_mainwindow(monkeypatch, capsys)
        assert capsys.readouterr().out == ''
        testobj.base.app_title = ''
        testobj.tray_icon = mockqtw.MockSysTrayIcon()
        testobj.revive(gui.qtw.QSystemTrayIcon.Unknown)
        assert capsys.readouterr().out == (
                'called TrayIcon.__init__\n'
                "called TrayIcon.showMessage with args ('', 'revive_message')\n")
        testobj.revive(gui.qtw.QSystemTrayIcon.Context)
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
        testobj.root.subitems = [subitem1, subitem2]
        testobj.activeitem = subitem1
        assert testobj.get_next_item() == subitem2
        testobj.activeitem = subitem2
        assert testobj.get_next_item() is None

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
        assert item._text == ['new item text']
        assert capsys.readouterr().out == ("called TreeItem.setText with arg"
                                           " `new item text` for col 1\n")

    def test_get_item_keywords(self, monkeypatch, capsys):
        """unittest for MainWindow.get_item_keywords
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        item._data = ['', ['some', 'words']]
        assert testobj.get_item_keywords(item) == ['some', 'words']
        assert capsys.readouterr().out == 'called TreeItem.data for col 1 role 256\n'

    def test_set_item_keywords(self, monkeypatch, capsys):
        """unittest for MainWindow.set_item_keywords
        """
        testobj = setup_mainwindow(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_item_keywords(item, ['keyword', 'list'])
        assert item._data == [['keyword', 'list']]
        assert capsys.readouterr().out == ("called TreeItem.setData to `['keyword', 'list']`"
                                           " with role 256 for col 1\n")

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
        assert capsys.readouterr().out == "called Action.__init__ with args ('text', 'action')\n"

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
        monkeypatch.setattr(gui.qtw.QMessageBox, 'information', mock_info)
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
        monkeypatch.setattr(gui.qtw.QMessageBox, 'question', mock_ask)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'app_title'
        assert not testobj.ask_question('question')
        assert capsys.readouterr().out == ('called MessageBox.question with args'
                                           " ('app_title', 'question')\n")

    def test_show_dialog(self, monkeypatch, capsys):
        """unittest for MainWindow.show_dialog
        """
        def mock_exec(self):
            """stub
            """
            self.parent.dialog_data = {'x': 'y'}
            return gui.qtw.QDialog.Accepted
        monkeypatch.setattr(mockqtw.MockDialog, 'exec_', mock_exec)
        testobj = setup_mainwindow(monkeypatch, capsys)
        assert testobj.show_dialog(mockqtw.MockDialog, 'arg') == (True, {'x': 'y'})
        assert capsys.readouterr().out == ("called Dialog.__init__ with args"
                                           f" {testobj} ('arg',) {{}}\n")

    def test_get_text_from_user(self, monkeypatch, capsys):
        """unittest for MainWindow.get_text_from_user
        """
        def mock_gettext(self, *args):
            """stub
            """
            print('called InputDialog.getText with args', args)
        monkeypatch.setattr(gui.qtw.QInputDialog, 'getText', mock_gettext)
        testobj = setup_mainwindow(monkeypatch, capsys)
        testobj.base.app_title = 'app_title'
        testobj.get_text_from_user('prompt', 'default')
        assert capsys.readouterr().out == ("called InputDialog.getText with args"
                                           " ('app_title', 'prompt', 0, 'default')\n")

    def test_get_choice_from_user(self, monkeypatch, capsys):
        """unittest for MainWindow.get_choice_from_user
        """
        def mock_getitem(self, *args, **kwargs):
            """stub
            """
            print('called InputDialog.getItem with args', args, kwargs)
        monkeypatch.setattr(gui.qtw.QInputDialog, 'getItem', mock_getitem)
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
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(gui.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(gui.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = gui.OptionsDialog('parent', {'text': 'value'})
        assert testobj.parent == 'parent'
        assert len(testobj.controls) == 1
        assert testobj.controls[0][0] == 'text'
        assert capsys.readouterr().out == (
            'called Dialog.__init__\n'
            "called Dialog.setWindowTitle with args ('t_sett',)\n"
            'called VBox.__init__\n'
            'called Grid.__init__\n'
            f"called Label.__init__ with args ('text', {testobj})\n"
            "called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>"
            " at (1, 0)\n"
            'called CheckBox.__init__\n'
            'called CheckBox.setChecked with arg value\n'
            "called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>"
            " at (1, 1)\n"
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>\n"
            'called HBox.__init__\n'
            'called HBox.addStretch\n'
            f"called PushButton.__init__ with args ('b_apply', {testobj}) {{}}\n"
            f'called Signal.connect with args ({testobj.accept},)\n'
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            f"called PushButton.__init__ with args ('b_close', {testobj}) {{}}\n"
            f'called Signal.connect with args ({testobj.reject},)\n'
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            'called HBox.addStretch\n'
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
            'called Dialog.setLayout\n')

    def test_accept(self, monkeypatch, capsys):
        """unittest for OptionsDialog.accept
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
            self.parent = args[0]
        def mock_accept(self, *args):
            """stub
            """
            print('called Dialog.accept')
        monkeypatch.setattr(gui.qtw.QDialog, 'accept', mock_accept)
        monkeypatch.setattr(gui.OptionsDialog, '__init__', mock_init)
        testobj = gui.OptionsDialog(types.SimpleNamespace(dialog_data={}), {})
        testobj.controls = [('text', mockqtw.MockCheckBox())]
        testobj.accept()
        assert testobj.parent.dialog_data == {'text': False}
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called CheckBox.isChecked\n'
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
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(gui.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(gui.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = gui.CheckDialog(mockparent, {}, 'message')
        assert testobj.parent == mockparent
        assert capsys.readouterr().out == (
            'called Dialog.__init__\n'
            "called Dialog.setWindowTitle with args ('title',)\n"
            "called Dialog.setWindowIcon with args ('icon',)\n"
            f"called Label.__init__ with args ('message', {testobj})\n"
            'called CheckBox.__init__\n'
            f"called PushButton.__init__ with args ('&Ok', {testobj}) {{}}\n"
            f"called Signal.connect with args ({testobj.klaar},)\n"
            'called VBox.__init__\n'
            'called HBox.__init__\n'
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
            'called HBox.__init__\n'
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
            'called HBox.__init__\n'
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            'called HBox.insertStretch\n'
            'called HBox.addStretch\n'
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
            'called Dialog.setLayout\n')

    def test_klaar(self, monkeypatch, capsys):
        """unittest for CheckDialog.klaar
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
            self.parent = args[0]
        def mock_accept(self, *args):
            """stub
            """
            print('called Dialog.accept')
        monkeypatch.setattr(gui.qtw.QDialog, 'accept', mock_accept)
        monkeypatch.setattr(gui.CheckDialog, '__init__', mock_init)
        testobj = gui.CheckDialog(types.SimpleNamespace(dialog_data='x'), {}, '')
        testobj.check = mockqtw.MockCheckBox()
        testobj.klaar()
        assert not testobj.parent.dialog_data
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called CheckBox.isChecked\n'
                                           'called Dialog.accept\n')


class TestKeywordsDialog:
    """unittests for qt_gui.KeywordsDialog
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.init - start dialoog zonder keywords parameter
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
        def mock_create_actions(self, *args):
            """stub
            """
            print('called create_actions')
        def mock_setLayout(self, *args):
            """stub
            """
            print('called Dialog.setLayout')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QDialog, 'resize', mock_resize)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QListWidget', mockqtw.MockListBox)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(gui.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(gui.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(gui.KeywordsDialog, 'create_actions', mock_create_actions)
        testobj = gui.KeywordsDialog(mockparent, '')
        assert testobj.parent == mockparent
        assert capsys.readouterr().out == (
            'called Dialog.__init__\n'
            "called Dialog.setWindowTitle with args ('title - w_tags',)\n"
            "called Dialog.setWindowIcon with args ('icon',)\n"
            'called Dialog.resize\n'
            'called List.__init__\n'
            'called List.setSelectionMode\n'
            f"called Signal.connect with args ({testobj.move_right},)\n"
            f"called Label.__init__ with args ('t_tags', {testobj})\n"
            f"called PushButton.__init__ with args ('b_tag',) {{}}\n"
            f"called Signal.connect with args ({testobj.move_right},)\n"
            f"called PushButton.__init__ with args ('b_untag',) {{}}\n"
            f"called Signal.connect with args ({testobj.move_left},)\n"
            f"called PushButton.__init__ with args ('b_newtag',) {{}}\n"
            f"called Signal.connect with args ({testobj.add_trefw},)\n"
            f"called PushButton.__init__ with args ('m_keys',) {{}}\n"
            f"called Signal.connect with args ({testobj.keys_help},)\n"
            'called List.__init__\n'
            'called List.setSelectionMode\n'
            f"called Signal.connect with args ({testobj.move_left},)\n"
            'called ButtonBox.__init__ with args (3,)\n'
            f"called Signal.connect with args ({testobj.accept},)\n"
            f"called Signal.connect with args ({testobj.reject},)\n"
            'called create_actions\n'
            'called List.addItems with arg `[]`\n'
            "called List.addItems with arg `['x', 'y']`\n"
            'called VBox.__init__\n'
            'called HBox.__init__\n'
            'called VBox.__init__\n'
            f"called Label.__init__ with args ('t_left', {testobj})\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockListBox'>\n"
            "called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>\n"
            'called VBox.__init__\n'
            'called VBox.addStretch\n'
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            'called VBox.addSpacing\n'
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            'called VBox.addStretch\n'
            "called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>\n"
            'called VBox.__init__\n'
            f"called Label.__init__ with args ('t_right', {testobj})\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockListBox'>\n"
            "called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>\n"
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
            'called HBox.__init__\n'
            'called HBox.addStretch\n'
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockButtonBox'>\n"
            'called HBox.addStretch\n'
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
            'called Dialog.setLayout\n')

    def test_init_2(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.init - start dialoog met keywords parameter
        """
        def mock_init(self, *args, **kwargs):
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
        def mock_create_actions(self, *args):
            """stub
            """
            print('called create_actions')
        def mock_setLayout(self, *args):
            """stub
            """
            print('called Dialog.setLayout')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QDialog, 'resize', mock_resize)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QListWidget', mockqtw.MockListBox)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(gui.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(gui.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(gui.KeywordsDialog, 'create_actions', mock_create_actions)
        testobj = gui.KeywordsDialog(mockparent, '', keywords=['x'])
        assert testobj.parent == mockparent
        assert capsys.readouterr().out == (
            'called Dialog.__init__\n'
            "called Dialog.setWindowTitle with args ('title - w_tags',)\n"
            "called Dialog.setWindowIcon with args ('icon',)\n"
            'called Dialog.resize\n'
            'called List.__init__\n'
            'called List.setSelectionMode\n'
            f"called Signal.connect with args ({testobj.move_right},)\n"
            f"called Label.__init__ with args ('t_tags', {testobj})\n"
            f"called PushButton.__init__ with args ('b_tag',) {{}}\n"
            f"called Signal.connect with args ({testobj.move_right},)\n"
            f"called PushButton.__init__ with args ('b_untag',) {{}}\n"
            f"called Signal.connect with args ({testobj.move_left},)\n"
            f"called PushButton.__init__ with args ('b_newtag',) {{}}\n"
            f"called Signal.connect with args ({testobj.add_trefw},)\n"
            f"called PushButton.__init__ with args ('m_keys',) {{}}\n"
            f"called Signal.connect with args ({testobj.keys_help},)\n"
            'called List.__init__\n'
            'called List.setSelectionMode\n'
            f"called Signal.connect with args ({testobj.move_left},)\n"
            'called ButtonBox.__init__ with args (3,)\n'
            f"called Signal.connect with args ({testobj.accept},)\n"
            f"called Signal.connect with args ({testobj.reject},)\n"
            'called create_actions\n'
            "called List.addItems with arg `['x']`\n"
            "called List.addItems with arg `['y']`\n"
            'called VBox.__init__\n'
            'called HBox.__init__\n'
            'called VBox.__init__\n'
            f"called Label.__init__ with args ('t_left', {testobj})\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockListBox'>\n"
            "called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>\n"
            'called VBox.__init__\n'
            'called VBox.addStretch\n'
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            'called VBox.addSpacing\n'
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            'called VBox.addStretch\n'
            "called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>\n"
            'called VBox.__init__\n'
            f"called Label.__init__ with args ('t_right', {testobj})\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockListBox'>\n"
            "called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>\n"
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
            'called HBox.__init__\n'
            'called HBox.addStretch\n'
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockButtonBox'>\n"
            'called HBox.addStretch\n'
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
            'called Dialog.setLayout\n')

    def test_create_actions(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.create_actions
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
        def mock_addAction(self, *args):
            """stub
            """
            print('called Dialog.addAction')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QAction', mockqtw.MockAction)
        monkeypatch.setattr(gui.KeywordsDialog, 'addAction', mock_addAction)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.create_actions()
        assert capsys.readouterr().out == (
                'called Dialog.__init__\n'
                f"called Action.__init__ with args ('a_from', {testobj})\n"
                'called Action.setShortcut with arg `Ctrl+L`\n'
                f"called Signal.connect with args ({testobj.activate_left},)\n"
                'called Dialog.addAction\n'
                f"called Action.__init__ with args ('b_tag', {testobj})\n"
                'called Action.setShortcut with arg `Ctrl+Right`\n'
                f"called Signal.connect with args ({testobj.move_right},)\n"
                'called Dialog.addAction\n'
                f"called Action.__init__ with args ('a_to', {testobj})\n"
                'called Action.setShortcut with arg `Ctrl+R`\n'
                f"called Signal.connect with args ({testobj.activate_right},)\n"
                'called Dialog.addAction\n'
                f"called Action.__init__ with args ('b_untag', {testobj})\n"
                'called Action.setShortcut with arg `Ctrl+Left`\n'
                f"called Signal.connect with args ({testobj.move_left},)\n"
                'called Dialog.addAction\n'
                f"called Action.__init__ with args ('b_newtag', {testobj})\n"
                'called Action.setShortcut with arg `Ctrl+N`\n'
                f"called Signal.connect with args ({testobj.add_trefw},)\n"
                'called Dialog.addAction\n')

    def test_activate_left(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate_left
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
        def mock_activate(self, *args):
            """stub
            """
            print('called dialog.activate with args', args)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QAction', mockqtw.MockAction)
        monkeypatch.setattr(gui.KeywordsDialog, '_activate', mock_activate)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.fromlist = 'fromlist'
        testobj.activate_left()
        assert capsys.readouterr().out == ('called dialog.__init__\n'
                                           "called dialog.activate with args ('fromlist',)\n")

    def test_activate_right(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate_right
        """
        def mock_init(self, *args):
            """stub
            """
            print('called dialog.__init__')
        def mock_activate(self, *args):
            """stub
            """
            print('called dialog.activate with args', args)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QAction', mockqtw.MockAction)
        monkeypatch.setattr(gui.KeywordsDialog, '_activate', mock_activate)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.tolist = 'tolist'
        testobj.activate_right()
        assert capsys.readouterr().out == ('called dialog.__init__\n'
                                           "called dialog.activate with args ('tolist',)\n")

    def test_activate(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate - test met geselecteerd item
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog(mockparent, '')
        win = mockqtw.MockListBox()
        monkeypatch.setattr(win, 'currentItem', lambda: None)
        monkeypatch.setattr(win, 'item', lambda x: mockqtw.MockListItem('first item'))
        testobj._activate(win)
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           'called List.__init__\n'
                                           'called ListItem.__init__\n'
                                           'called ListItem.setSelected with arg'
                                           ' `True` for `first item`\n'
                                           'called List.setFocus with arg `True`\n')

    def test_activate_2(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.activate: test zonder geselecteerd item
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog(mockparent, '')
        win = mockqtw.MockListBox()
        monkeypatch.setattr(win, 'currentItem', lambda: mockqtw.MockListItem('current item'))
        testobj._activate(win)
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           'called List.__init__\n'
                                           'called ListItem.__init__\n'
                                           'called ListItem.setSelected with arg'
                                           ' `True` for `current item`\n'
                                           'called List.setFocus with arg `True`\n')

    def test_move_right(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.move_right
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
        def mock_moveitem(self, *args):
            """stub
            """
            print('called Dialog.moveitem with args', args)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, '_moveitem', mock_moveitem)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.fromlist = 'fromlist'
        testobj.tolist = 'tolist'
        testobj.move_right()
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           "called Dialog.moveitem with args ('fromlist',"
                                           " 'tolist')\n")

    def test_move_left(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.move_left
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
        def mock_moveitem(self, *args):
            """stub
            """
            print('called Dialog.moveitem with args', args)
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, '_moveitem', mock_moveitem)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.fromlist = 'fromlist'
        testobj.tolist = 'tolist'
        testobj.move_left()
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           "called Dialog.moveitem with args ('tolist',"
                                           " 'fromlist')\n")

    def test_moveitem(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.moveitem
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
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
            print(f'called List.row with arg `{item.name}` on `{self.list}`')
            return item.name[-1]
        def mock_addItem(self, item):
            """stub
            """
            print(f'called List.addItem with arg `{item.name}` on `{self.list}`')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(mockqtw.MockListBox, 'selectedItems', mock_selectedItems)
        monkeypatch.setattr(mockqtw.MockListBox, 'takeItem', mock_takeItem)
        monkeypatch.setattr(mockqtw.MockListBox, 'row', mock_row)
        monkeypatch.setattr(mockqtw.MockListBox, 'addItem', mock_addItem)
        testobj = gui.KeywordsDialog(mockparent, '')
        assert capsys.readouterr().out == 'called Dialog.__init__\n'
        from_ = mockqtw.MockListBox(['fromlist'])
        assert capsys.readouterr().out == 'called List.__init__\n'
        to = mockqtw.MockListBox(['tolist'])
        assert capsys.readouterr().out == 'called List.__init__\n'
        testobj._moveitem(from_, to)
        assert capsys.readouterr().out == ("called List.selectedItems on `['fromlist']`\n"
                                           'called ListItem.__init__\n'
                                           'called ListItem.__init__\n'
                                           "called List.row with arg `item 1` on `['fromlist']`\n"
                                           "called List.takeItem with arg `1` on `['fromlist']`\n"
                                           "called List.addItem with arg `item 1` on `['tolist']`\n"
                                           "called List.row with arg `item 2` on `['fromlist']`\n"
                                           "called List.takeItem with arg `2` on `['fromlist']`\n"
                                           "called List.addItem with arg `item 2` on `['tolist']`\n")

    def test_add_trefw(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.add_trefw: test doorvoeren trefwoord toevoegen
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
            self.parent = args[0]
        def mock_gettext(self, *args):
            """stub
            """
            print('called InputDialog.getText with args', args)
            return 'text', True
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QInputDialog, 'getText', mock_gettext)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.tolist = mockqtw.MockListBox()
        testobj.add_trefw()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'y', 'text']}
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           'called List.__init__\n'
                                           "called InputDialog.getText with args"
                                           " ('title', 't_newtag')\n"
                                           'called List.addItem with arg `text` on `[]`\n')

    def test_add_trefw_2(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.add_trefw: test doorvoeren trefwoord afbreken
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
            self.parent = args[0]
        def mock_gettext(self, *args):
            """stub
            """
            print('called InputDialog.getText with args', args)
            return '', False
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QInputDialog, 'getText', mock_gettext)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.tolist = mockqtw.MockListBox()
        testobj.add_trefw()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'y']}
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           'called List.__init__\n'
                                           "called InputDialog.getText with args"
                                           " ('title', 't_newtag')\n")

    def test_keys_help(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.keys_help
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
            self.parent = args[0]
        def mock_init_dialog(self, *args):
            """stub
            """
            print('called QDialog.__init__')
        def mock_setWindowTitle(self, *args):
            """stub
            """
            print('called Dialog.setWindowTitle with args', args)
        def mock_setLayout(self, *args):
            """stub
            """
            print('called Dialog.setLayout')
        def mock_exec(self, *args):
            """stub
            """
            print('called Dialog.exec_')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init_dialog)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw.QDialog, 'exec_', mock_exec)
        monkeypatch.setattr(gui.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.helptext = (('x', 'y'), ('a', 'b'))
        testobj.keys_help()
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           'called QDialog.__init__\n'
                                           'called Grid.__init__\n'
                                           f"called Label.__init__ with args ('x', {testobj})\n"
                                           "called Grid.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)\n"
                                           f"called Label.__init__ with args ('y', {testobj})\n"
                                           "called Grid.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 1)\n"
                                           f"called Label.__init__ with args ('a', {testobj})\n"
                                           "called Grid.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'> at (1, 0)\n"
                                           f"called Label.__init__ with args ('b', {testobj})\n"
                                           "called Grid.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'> at (1, 1)\n"
                                           "called Dialog.setWindowTitle with args"
                                           " ('title t_keys',)\n"
                                           'called Dialog.setLayout\n'
                                           'called Dialog.exec_\n')

    def test_accept(self, monkeypatch, capsys):
        """unittest for KeywordsDialog.accept
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Dialog.__init__')
            self.parent = args[0]
        def mock_accept(self, *args):
            """stub
            """
            print('called Dialog.accept')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'accept', mock_accept)
        testobj = gui.KeywordsDialog(mockparent, '')
        testobj.tolist = mockqtw.MockListBox([mockqtw.MockListItem('1'),
                                              mockqtw.MockListItem('2')])
        testobj.accept()
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           'called ListItem.__init__\n'
                                           'called ListItem.__init__\n'
                                           'called List.__init__\n'
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
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QDialog, 'resize', mock_resize)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(gui.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(gui.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(gui.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = gui.KeywordsManager(mockparent)
        assert testobj.parent == mockparent
        assert capsys.readouterr().out == (
            'called Dialog.__init__\n'
            "called Dialog.setWindowTitle with args ('title - t_tagman',)\n"
            "called Dialog.setWindowIcon with args ('icon',)\n"
            'called Dialog.resize\n'
            'called ComboBox.__init__\n'
            'called LineEdit.__init__\n'
            'called LineEdit.setMinimumHeight with arg `100`\n'
            'called ComboBox.clear\n'
            "called ComboBox.addItems with arg ['x', 'y']\n"
            'called ComboBox.clearEditText\n'
            'called LineEdit.clear\n'
            f"called PushButton.__init__ with args ('b_remtag', {testobj}) {{}}\n"
            f"called Signal.connect with args ({testobj.remove_keyword},)\n"
            f"called PushButton.__init__ with args ('b_addtag', {testobj}) {{}}\n"
            f"called Signal.connect with args ({testobj.add_keyword},)\n"
            f"called PushButton.__init__ with args ('b_done', {testobj}) {{}}\n"
            f"called Signal.connect with args ({testobj.accept},)\n"
            'called VBox.__init__\n'
            'called Grid.__init__\n'
            "called Label.__init__ with args ('l_oldval',)\n"
            "called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>"
            " at (0, 0)\n"
            "called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>"
            " at (0, 1)\n"
            "called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>"
            " at (0, 2)\n"
            "called Label.__init__ with args ('l_newval',)\n"
            "called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>"
            " at (1, 0)\n"
            "called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>"
            " at (1, 1)\n"
            "called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>"
            " at (1, 2)\n"
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>\n"
            'called HBox.__init__\n'
            "called Label.__init__ with args ('t_applied',)\n"
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>\n"
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
            'called HBox.__init__\n'
            'called HBox.addStretch\n'
            "called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>\n"
            'called HBox.addStretch\n'
            "called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
            'called Dialog.setLayout\n')

    def _test_refresh_fields(self):
        """unittest for Keywordsmanager.refresh_fields

        not needed, is executed as part of __init__`
        """

    def test_update_items(self, monkeypatch, capsys):
        """unittest for KeywordsManager.update_items: trefwoord wijzigen in treeitems
        """
        def mock_init(self, *args):
            """stub
            """
            print('called KeywordsManager.__init__')
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager('parent')
        assert capsys.readouterr().out == 'called KeywordsManager.__init__\n'
        testobj.parent = types.SimpleNamespace(root=mockqtw.MockTreeItem())
        assert capsys.readouterr().out == 'called TreeItem.__init__ with args ()\n'
        subitem1 = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == 'called TreeItem.__init__ with args ()\n'
        subitem1._text = ['tag1', 'text1']
        subitem1._data = ['key1', ['keywords1', 'oldtext']]
        subitem2 = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == 'called TreeItem.__init__ with args ()\n'
        subitem2._text = ['tag2', 'text2']
        subitem2._data = ['key2', ['keywords2']]
        subitem3 = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == 'called TreeItem.__init__ with args ()\n'
        subitem3._text = ['tag3', 'text3']
        subitem3._data = ['key3', ['keywords3', 'oldtext']]
        testobj.parent.root.subitems = [subitem1, subitem2, subitem3]
        testobj.update_items('oldtext', 'newtext')
        assert testobj.parent.root.subitems[0]._data[1] == ['keywords1', 'newtext']
        assert testobj.parent.root.subitems[1]._data[1] == ['keywords2']
        assert testobj.parent.root.subitems[2]._data[1] == ['keywords3', 'newtext']
        assert capsys.readouterr().out == ("called TreeItem.data for col 1 role 256\n"
                                           "called TreeItem.setData to `['keywords1', 'newtext']`"
                                           " with role 256 for col 1\n"
                                           "called TreeItem.data for col 1 role 256\n"
                                           "called TreeItem.data for col 1 role 256\n"
                                           "called TreeItem.setData to `['keywords3', 'newtext']`"
                                           " with role 256 for col 1\n")

    def test_update_items_2(self, monkeypatch, capsys):
        """unittest for KeywordsManager.update_items: trefwoord verwijderen uit treeitems
        """
        def mock_init(self, *args):
            """stub
            """
            print('called KeywordsManager.__init__')
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager('parent')
        assert capsys.readouterr().out == 'called KeywordsManager.__init__\n'
        testobj.parent = types.SimpleNamespace(root=mockqtw.MockTreeItem())
        assert capsys.readouterr().out == 'called TreeItem.__init__ with args ()\n'
        subitem1 = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == 'called TreeItem.__init__ with args ()\n'
        subitem1._text = ['tag1', 'text1']
        subitem1._data = ['key1', ['keywords1', 'oldtext']]
        subitem2 = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == 'called TreeItem.__init__ with args ()\n'
        subitem2._text = ['tag2', 'text2']
        subitem2._data = ['key2', ['keywords2', 'oldtext']]
        testobj.parent.root.subitems = [subitem1, subitem2]
        testobj.update_items('oldtext')
        assert testobj.parent.root.subitems[0]._data[1] == ['keywords1']
        assert testobj.parent.root.subitems[1]._data[1] == ['keywords2']
        assert capsys.readouterr().out == ("called TreeItem.data for col 1 role 256\n"
                                           "called TreeItem.setData to `['keywords1']`"
                                           " with role 256 for col 1\n"
                                           "called TreeItem.data for col 1 role 256\n"
                                           "called TreeItem.setData to `['keywords2']`"
                                           " with role 256 for col 1\n")

    def test_remove_keyword(self, monkeypatch, capsys):
        """unittest for KeywordsManager.remove_keyword: verwijderen afbreken
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__')
            self.parent = args[0]
        def mock_update(self, *args):
            """stub
            """
            print('called Dialog.update_items')
        def mock_refresh(self, *args):
            """stub
            """
            print('called Dialog.refresh_fields')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockqtw.MockComboBox()
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentText', lambda x: 'y')
        # testobj.newtag = MockLineEdit()
        monkeypatch.setattr(gui.qtw.QMessageBox, 'question',
                            lambda x, y, z: gui.qtw.QMessageBox.No)
        monkeypatch.setattr(testobj, 'update_items', mock_update)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.remove_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'y']}
        assert capsys.readouterr().out == ('called TextDialog.__init__\n'
                                           'called ComboBox.__init__\n')

    def test_remove_keyword_2(self, monkeypatch, capsys):
        """unittest for KeywordsManager.remove_keyword: verwijderen doorvoeren
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__')
            self.parent = args[0]
        def mock_update(self, *args):
            """stub
            """
            print('called Dialog.update_items')
        def mock_refresh(*args):
            """stub
            """
            print('called Dialog.refresh_fields')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockqtw.MockComboBox()
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentText', lambda x: 'y')
        # testobj.newtag = MockLineEdit()
        monkeypatch.setattr(gui.qtw.QMessageBox, 'question',
                            lambda x, y, z: gui.qtw.QMessageBox.Yes)
        monkeypatch.setattr(testobj, 'update_items', mock_update)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.remove_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x']}
        assert capsys.readouterr().out == ('called TextDialog.__init__\n'
                                           'called ComboBox.__init__\n'
                                           'called Dialog.update_items\n'
                                           'called Dialog.refresh_fields\n')

    def test_add_keyword(self, monkeypatch, capsys):
        """unittest for KeywordsManager.add_keyword: toevoegen afbreken
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__')
            self.parent = args[0]
        def mock_refresh(self, *args):
            """stub
            """
            print('called Dialog.refresh_fields')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockqtw.MockComboBox()
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentText', lambda x: '')
        testobj.newtag = mockqtw.MockLineEdit()
        monkeypatch.setattr(mockqtw.MockLineEdit, 'text', lambda x: 'z')
        monkeypatch.setattr(gui.qtw.QMessageBox, 'question',
                            lambda x, y, z: gui.qtw.QMessageBox.No)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'y']}
        assert capsys.readouterr().out == ('called TextDialog.__init__\n'
                                           'called ComboBox.__init__\n'
                                           'called LineEdit.__init__\n')

    def test_add_keyword_2(self, monkeypatch, capsys):
        """unittest for KeywordsManager.add_keyword: toevoegen doorvoeren
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__')
            self.parent = args[0]
        def mock_refresh(*args):
            """stub
            """
            print('called Dialog.refresh_fields')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockqtw.MockComboBox()
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentText', lambda x: '')
        testobj.newtag = mockqtw.MockLineEdit()
        monkeypatch.setattr(mockqtw.MockLineEdit, 'text', lambda x: 'z')
        monkeypatch.setattr(gui.qtw.QMessageBox, 'question',
                            lambda x, y, z: gui.qtw.QMessageBox.Yes)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'y', 'z']}
        assert capsys.readouterr().out == ('called TextDialog.__init__\n'
                                           'called ComboBox.__init__\n'
                                           'called LineEdit.__init__\n'
                                           'called Dialog.refresh_fields\n')

    def test_change_keyword(self, monkeypatch, capsys):
        """unittest for KeywordsManager.change_keyword
         wijzigen afbreken
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__')
            self.parent = args[0]
        def mock_update(self, *args):
            """stub
            """
            print('called Dialog.update_items with args', args)
        def mock_refresh(*args):
            """stub
            """
            print('called Dialog.refresh_fields')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockqtw.MockComboBox()
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentText', lambda x: 'y')
        testobj.newtag = mockqtw.MockLineEdit()
        monkeypatch.setattr(mockqtw.MockLineEdit, 'text', lambda x: 'z')
        monkeypatch.setattr(gui.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        monkeypatch.setattr(gui.qtw.QMessageBox, 'exec_', lambda x: gui.qtw.QMessageBox.Cancel)
        monkeypatch.setattr(testobj, 'update_items', mock_update)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'y']}
        assert capsys.readouterr().out == (
                'called TextDialog.__init__\n'
                'called ComboBox.__init__\n'
                'called LineEdit.__init__\n'
                'called MessageBox.__init__ with args () {}\n'
                'called MessageBox.setText with arg `t_repltag`\n'
                'called MessageBox.setInformativeText with arg `t_repltag2`\n'
                'called MessageBox.setStandardButtons\n'
                'called MessageBox.setDefaultButton with arg `4`\n')

    def test_change_keyword_2(self, monkeypatch, capsys):
        """unittest for KeywordsManager.change_keyword: wijzigen met vervangen in treeitems
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__')
            self.parent = args[0]
        def mock_update(*args):
            """stub
            """
            print('called Dialog.update_items with args', args)
        def mock_refresh(*args):
            """stub
            """
            print('called Dialog.refresh_fields')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockqtw.MockComboBox()
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentText', lambda x: 'y')
        testobj.newtag = mockqtw.MockLineEdit()
        monkeypatch.setattr(mockqtw.MockLineEdit, 'text', lambda x: 'z')
        monkeypatch.setattr(gui.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        monkeypatch.setattr(gui.qtw.QMessageBox, 'exec_', lambda x: gui.qtw.QMessageBox.Yes)
        monkeypatch.setattr(testobj, 'update_items', mock_update)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'z']}
        assert capsys.readouterr().out == (
                'called TextDialog.__init__\n'
                'called ComboBox.__init__\n'
                'called LineEdit.__init__\n'
                'called MessageBox.__init__ with args () {}\n'
                'called MessageBox.setText with arg `t_repltag`\n'
                'called MessageBox.setInformativeText with arg `t_repltag2`\n'
                'called MessageBox.setStandardButtons\n'
                'called MessageBox.setDefaultButton with arg `4`\n'
                "called Dialog.update_items with args ('y', 'z')\n"
                'called Dialog.refresh_fields\n')

    def test_change_keyword_3(self, monkeypatch, capsys):
        """unittest for KeywordsManager.change_keyword: wijzigen zonder vervangen in treeitems
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__')
            self.parent = args[0]
        def mock_update(*args):
            """stub
            """
            print('called Dialog.update_items with args', args)
        def mock_refresh(*args):
            """stub
            """
            print('called Dialog.refresh_fields')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = mockqtw.MockComboBox()
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentText', lambda x: 'y')
        testobj.newtag = mockqtw.MockLineEdit()
        monkeypatch.setattr(mockqtw.MockLineEdit, 'text', lambda x: 'z')
        monkeypatch.setattr(gui.qtw, 'QMessageBox', mockqtw.MockMessageBox)
        monkeypatch.setattr(gui.qtw.QMessageBox, 'exec_', lambda x: gui.qtw.QMessageBox.No)
        monkeypatch.setattr(testobj, 'update_items', mock_update)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'z']}
        assert capsys.readouterr().out == (
                'called TextDialog.__init__\n'
                'called ComboBox.__init__\n'
                'called LineEdit.__init__\n'
                'called MessageBox.__init__ with args () {}\n'
                'called MessageBox.setText with arg `t_repltag`\n'
                'called MessageBox.setInformativeText with arg `t_repltag2`\n'
                'called MessageBox.setStandardButtons\n'
                'called MessageBox.setDefaultButton with arg `4`\n'
                "called Dialog.update_items with args ('y',)\n"
                'called Dialog.refresh_fields\n')


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
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(gui.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(gui.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(gui.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(gui.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = gui.GetTextDialog(mockparent, 0, 'seltext', 'labeltext', True)
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           "called Dialog.setWindowTitle with args ('title',)\n"
                                           "called Dialog.setWindowIcon with args ('icon',)\n"
                                           'called LineEdit.__init__\n'
                                           'called LineEdit.setText with arg `seltext`\n'
                                           'called CheckBox.__init__\n'
                                           'called CheckBox.setChecked with arg False\n'
                                           'called CheckBox.__init__\n'
                                           'called CheckBox.setChecked with arg False\n'
                                           'called VBox.__init__\n'
                                           'called HBox.__init__\n'
                                           "called Label.__init__ with args"
                                           f" ('labeltext', {testobj})\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'>\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
                                           'called HBox.__init__\n'
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLineEdit'>\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
                                           'called HBox.__init__\n'
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           'called CheckBox.setChecked with arg True\n'
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
                                           'called ButtonBox.__init__ with args (3,)\n'
                                           f"called Signal.connect with args ({testobj.accept},)\n"
                                           f"called Signal.connect with args ({testobj.reject},)\n"
                                           "called VBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockButtonBox'>\n"
                                           'called Dialog.setLayout\n')

    def test_init_2(self, monkeypatch, capsys):
        """unittest for GetTextDialog.init_2
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
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(gui.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(gui.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(gui.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(gui.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = gui.GetTextDialog(mockparent, -1, 'seltext', 'labeltext', False)
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           "called Dialog.setWindowTitle with args ('title',)\n"
                                           "called Dialog.setWindowIcon with args ('icon',)\n"
                                           'called LineEdit.__init__\n'
                                           'called LineEdit.setText with arg `seltext`\n'
                                           'called CheckBox.__init__\n'
                                           'called CheckBox.setChecked with arg False\n'
                                           'called CheckBox.__init__\n'
                                           'called CheckBox.setChecked with arg False\n'
                                           'called CheckBox.setChecked with arg True\n'
                                           'called VBox.__init__\n'
                                           'called HBox.__init__\n'
                                           "called Label.__init__ with args"
                                           f" ('labeltext', {testobj})\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'>\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
                                           'called HBox.__init__\n'
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLineEdit'>\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
                                           'called HBox.__init__\n'
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n"
                                           'called ButtonBox.__init__ with args (3,)\n'
                                           f"called Signal.connect with args ({testobj.accept},)\n"
                                           f"called Signal.connect with args ({testobj.reject},)\n"
                                           "called VBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockButtonBox'>\n"
                                           'called Dialog.setLayout\n')

    def test_create_inputwin(self, monkeypatch, capsys):
        """unittest for GetTextDialog.create_inputwin
        """
        # hier niet per se nodig omdat het ook al in de init doorgelopen wordt
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(gui.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = gui.GetTextDialog('parent', 0, '')  # , 'labeltext', False)
        testobj.create_inputwin('seltext')
        assert hasattr(testobj, 'inputwin')
        assert hasattr(testobj, 'use_case')
        assert capsys.readouterr().out == ('called TextDialog.__init__\n'
                                           'called LineEdit.__init__\n'
                                           'called LineEdit.setText with arg `seltext`\n'
                                           'called CheckBox.__init__\n'
                                           'called CheckBox.setChecked with arg False\n')

    def test_get_dialog_data(self, monkeypatch, capsys):
        """unittest for GetTextDialog.get_dialog_data
        """
        # hier niet per se nodig omdat het ook al in de init doorgelopen wordt
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = gui.GetTextDialog('parent', 0, '')  # , 'labeltext', False)
        testobj.inputwin = mockqtw.MockLineEdit()
        testobj.in_exclude = mockqtw.MockCheckBox()
        testobj.use_case = mockqtw.MockCheckBox()
        testobj.parent = types.SimpleNamespace(dialog_data='x')
        testobj.get_dialog_data()
        assert testobj.parent.dialog_data == [False, '', False]
        assert capsys.readouterr().out == ('called TextDialog.__init__\n'
                                           'called LineEdit.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called LineEdit.text\n'
                                           'called CheckBox.isChecked\n'
                                           'called CheckBox.isChecked\n')

    def test_accept(self, monkeypatch, capsys):
        """unittest for GetTextDialog.accept
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__')
            self.parent = args[0]
        def mock_accept(self, *args):
            """stub
            """
            print('called Dialog.accept')
        monkeypatch.setattr(gui.qtw.QDialog, 'accept', mock_accept)
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        testobj = gui.GetTextDialog(types.SimpleNamespace(dialog_data='x'), 0, '')
        testobj.inputwin = mockqtw.MockLineEdit()
        testobj.in_exclude = mockqtw.MockCheckBox()
        testobj.use_case = mockqtw.MockCheckBox()
        testobj.accept()
        assert testobj.parent.dialog_data == [False, '', False]
        assert capsys.readouterr().out == ('called TextDialog.__init__\n'
                                           'called LineEdit.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called LineEdit.text\n'
                                           'called CheckBox.isChecked\n'
                                           'called CheckBox.isChecked\n'
                                           'called Dialog.accept\n')


class TestGetItemDialog:
    """unittests for qt_gui.GetItemDialog
    """
    def test_create_inputwin(self, monkeypatch, capsys):
        """unittest for GetItemDialog.create_inputwin
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__')
            self.parent = args[0]
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QComboBox', mockqtw.MockComboBox)
        mockbase = types.SimpleNamespace(opts={'Keywords': ['title']})
        mockparent = types.SimpleNamespace(base=mockbase)
        # import pdb; pdb.set_trace()
        testobj = gui.GetItemDialog(mockparent, 0, '')
        testobj.create_inputwin((['item0', 'item1'], 1))
        assert hasattr(testobj, 'inputwin')
        assert capsys.readouterr().out == ('called TextDialog.__init__\n'
                                           "called ComboBox.__init__\n"
                                           "called ComboBox.addItems with arg ['item0', 'item1']\n"
                                           'called ComboBox.setCurrentIndex with arg `1`\n')

    def test_get_dialog_data(self, monkeypatch, capsys):
        """unittest for GetItemDialog.get_dialog_data
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TextDialog.__init__')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = gui.GetItemDialog('parent', 0, '')  # , 'labeltext', False)
        testobj.inputwin = mockqtw.MockComboBox()
        testobj.in_exclude = mockqtw.MockCheckBox()
        testobj.parent = types.SimpleNamespace(dialog_data='x')
        testobj.get_dialog_data()
        assert testobj.parent.dialog_data == [False, 'current text']
        assert capsys.readouterr().out == ('called TextDialog.__init__\n'
                                           'called ComboBox.__init__\n'
                                           'called CheckBox.__init__\n'
                                           'called ComboBox.currentText\n'
                                           'called CheckBox.isChecked\n')


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
        def mock_translation(*args):
            """stub
            """
            return 'a - b\nc - d'
        def mock_setLayout(self, *args):
            """stub
            """
            print('called Dialog.setLayout')
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', mockqtw.MockLabel)
        # monkeypatch.setattr(gui.gettext, 'translation', mock_translation)
        testobj = gui.GridDialog('parent', (('x', 'y'), ('a', 'b')), 'title')
        assert capsys.readouterr().out == ('called Dialog.__init__\n'
                                           'called Grid.__init__\n'
                                           f"called Label.__init__ with args ('x', {testobj})\n"
                                           "called Grid.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)\n"
                                           f"called Label.__init__ with args ('y', {testobj})\n"
                                           "called Grid.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 1)\n"
                                           f"called Label.__init__ with args ('a', {testobj})\n"
                                           "called Grid.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'> at (1, 0)\n"
                                           f"called Label.__init__ with args ('b', {testobj})\n"
                                           "called Grid.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'> at (1, 1)\n"
                                           "called Dialog.setWindowTitle with args ('title',)\n"
                                           'called Dialog.setLayout\n')
