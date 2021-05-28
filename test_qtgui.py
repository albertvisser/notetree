""" unittests voor qt_gui.py
"""
import os
import types
import pytest
import gettext
import notetree.qt_gui as gui
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gettext.install("NoteTree", os.path.join(HERE, 'locale'))


def setup_mainwindow(monkeypatch):
    monkeypatch.setattr(gui.qtw, 'QApplication', MockApplication)
    monkeypatch.setattr(gui.qtw, 'QMainWindow', MockMainWindow)
    return gui.MainWindow(MockNoteTree())


#--- redefine gui elements to make testing easier (or possible at all)
class MockApplication:
    def __init__(self, *args):
        print('called MockApplication.__init__()')
    def exec_(self):
        print('called MockApplication.exec_()')


class MockNoteTree:
    def __init__(self):
        print('called MockNoteTree.__init__()')
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


class MockMainWindow:
    def __init__(self, *args):
        print('called MockMainWindow.__init__()')


class MockIcon:
    def __init__(self, *args):
        print('called MockIcon.__init__() for `{}`'.format(args[0]))


class MockMenuBar:
    def __init__(self):
        self.menus = []
    def clear(self):
        self.menus = []
    def addMenu(self, text):
        newmenu = MockMenu(text)
        self.menus.append(newmenu)
        return newmenu


class MockMenu:
    def __init__(self, text):
        self.menutext = text
        self.actions = []
    def addAction(self, text, func):
        newaction = MockAction(text, func)
        self.actions.append(newaction)
        return newaction
    def addSeparator(self):
        newaction = MockAction('-----', None)
        self.actions.append(newaction)
        return newaction


class MockSplitter:
    def __init__(self, *args):
        print('called MockSplitter.__init__()')
    def addWidget(self, *args):
        print('called splitter.addWidget() with arg `{}`'.format(args[0]))
    def setSizes(self, *args):
        print('called splitter.setSizes() with args `{}`'.format(args))
    def sizes(self, *args):
        return 'left this wide', 'right that wide'


class MockTreeWidget:
    SingleSelection = 1
    def __init__(self, *args):
        print('called MockTreeWidget.__init__()')
        self.itemSelectionChanged = MockSignal()
    def setColumnCount(self, *args):
        print('called tree.setColumnCount()')
    def hideColumn(self, *args):
        print('called tree.hideColumn()')
    def headerItem(self):
        return MockTreeWidgetItem()
    def setSelectionMode(self, *args):
        print('called tree.setSelectionMode()')
    def selectedItems(self):
        print('called tree.selectedItems()')
    def setCurrentItem(self, *args):
        print('called tree.setCurrentItem(`{}`)'.format(args[0]))
    def currentItem(self):
        return 'current item'
    def takeTopLevelItem(self, *args):
        print('called tree.takeTopLevelItem()')
    def addTopLevelItem(self, *args):
        print('called tree.addTopLevelItem()')
    def setFocus(self, *args):
        print('called tree.setFocus()')


class MockTreeWidgetItem:
    def __init__(self, text='', data=''):
        self._text = {}
        self._data = {}
        if text:
            self._text[0] = text
        if data:
            self._data[0] = data
        self.subitems = []
    def setText(self, col, text):
        self._text[col] = text
    def setData(self, col, role, data):
        self._data[col] = data
    def text(self, col):
        return self._text[col]
    def data(self, col, *args):
        return self._data[col]
    def addChild(self, item):
        print('called treeitem.addChild()')
        self.subitems.append(item)
    def insertChild(self, index, item):
        print('called treeitem.insertChild()')
        self.subitems.insert(index, item)
    def childCount(self):
        return len(self.subitems)
    def child(self, num):
        return self.subitems[num]
    def indexOfChild(self, item):
        return self.subitems.index(item)
    def removeChild(self, item):
        print('called item.removeChild()')
    def setHidden(self, *args):
        print("called (header)item.setHidden({})".format(args[0]))
    def setExpanded(self, *args):
        print("called item.setExpanded({})".format(args[0]))
    def font(self, *args):
        return MockFont()
    def setFont(self, *args):
        print('called item.setFont()')


class MockFont:
    def __init__(self):
        print('called font.__init__()')
    def setBold(self, value):
        print('called font.setBold({})'.format(value))


class MockEditorWidget:
    WrapWord = 1
    SloppyBraceMatch = 2
    PlainFoldStyle = 3
    def __init__(self, *args):
        print('called editor.__init__()')
    def setWrapMode(self, *args):
        print('called editor.setWrapMode()')
    def setBraceMatching(self, *args):
        print('called editor.setBraceMatching()')
    def setAutoIndent(self, *args):
        print('called editor.setAutoIndent()')
    def setFolding(self, *args):
        print('called editor.setFolding()')
    def setCaretLineVisible(self, *args):
        print('called editor.setCaretLineVisible()')
    def setCaretLineBackgroundColor(self, *args):
        print('called editor.setCaretLineBackgroundColor()')
    def setLexer(self, *args):
        print('called editor.setLexer()')
    def clear(self, *args):
        print('called editor.clear()')
    def setEnabled(self, *args):
        print('called editor.setEnabled({})'.format(args[0]))
    def isModified(self, *args):
        return 'x'
    def setText(self, *args):
        print('called editor.setText(`{}`)'.format(args[0]))
    def text(self, *args):
        return 'editor text'
    def toPlainText(self, *args):
        return 'editor text'
    def setFocus(self, *args):
        print('called editor.setFocus()')


class MockSysTrayIcon:
    def __init__(self, *args):
        print('called trayicon.__init__()')
        self.activated = MockSignal()
    def showMessage(self, *args):
        print('called trayicon.showMessage()')
    def setToolTip(self, *args):
        print('called trayicon.setToolTip()')
    def hide(self):
        print('called trayicon.hide()')
    def show(self):
        print('called trayicon.show()')


class MockSignal:
    def __init__(self, *args):
        print('called signal.__init__()')
    def connect(self, *args):
        print('called signal.connect()')


class MockAction:
    triggered = MockSignal()
    def __init__(self, text, func):
        self.label = text
        self.callback = func
        self.shortcuts = []
        self.checkable = self.checked = False
        self.statustip = ''
    def setCheckable(self, state):
        self.checkable = state
    def setChecked(self, state):
        self.checked = state
    def setShortcut(self, data):
        print('call action.setShortcut with arg `{}`'.format(data))
    def setShortcuts(self, data):
        self.shortcuts = data
    def setStatusTip(self, data):
        self.statustip = data


class MockStatusBar:
    def showMessage(self, *args):
        print('called statusbar.showMessage({})'.format(args[0]))


class MockDialog:
    def __init__(self, parent, *args):
        self.parent = parent
        print('called dialog.__init()__ with args `{}`'.format(args))
    def exec_(self):
        self.parent.dialog_data = {'x': 'y'}
        return gui.qtw.QDialog.Accepted
    def setWindowTitle(self, *args):
        print('called dialog.setWindowTitle() with args `{}`'.format(args))
    def setLayout(self, *args):
        print('called dialog.setLayout()')
    def accept(self):
        print('called dialog.accept()')
        return gui.qtw.QDialog.Accepted
    def reject(self):
        print('called dialog.reject()')
        return gui.qtw.QDialog.Rejected


class MockVBoxLayout:
    def __init__(self, *args):
        print('called MockVBoxLayout.__init__()')
    def addWidget(self, *args):
        print('called vbox.addWidget()')
    def addLayout(self, *args):
        print('called vbox.addLayout()')
    def addStretch(self, *args):
        print('called vbox.addStretch()')
    def addSpacing(self, *args):
        print('called vbox.addSpacing()')


class MockHBoxLayout:
    def __init__(self, *args):
        print('called MockHBoxLayout.__init__()')
    def addWidget(self, *args):
        print('called hbox.addWidget()')
    def addLayout(self, *args):
        print('called hbox.addLayout()')
    def addStretch(self, *args):
        print('called hbox.addStretch()')
    def insertStretch(self, *args):
        print('called hbox.insertStretch()')


class MockGridLayout:
    def __init__(self, *args):
        print('called MockGridLayout.__init__()')
    def addWidget(self, *args):
        print('called grid.addWidget()')
    def addLayout(self, *args):
        print('called grid.addLayout()')
    def addStretch(self, *args):
        print('called grid.addStretch()')


class MockLabel:
    def __init__(self, *args):
        print('called MockLabel.__init__()')


class MockCheckBox:
    def __init__(self, *args):
        print('called MockCheckBox.__init__()')
        self.checked = None
    def setChecked(self, value):
        print('called check.setChecked({})'.format(value))
        self.checked = value
    def isChecked(self):
        print('called check.isChecked()')
        return self.checked


class MockComboBox:
    def __init__(self, *args, **kwargs):
        print('called MockComboBox.__init__()')
        self._items = []
    def clear(self):
        print('called combo.clear()')
    def clearEditText(self):
        print('called combo.clearEditText()')
    def addItems(self, itemlist):
        print('called combo.addItems({})'.format(itemlist))
    def height(self):
        return 100
    def setCurrentIndex(self, value):
        print('called combo.setCurrentIndex({})'.format(value))
        self.checked = value
    def currentText(self):
        print('called combo.currentText()')
        return 'current text'


class MockPushButton:
    def __init__(self, *args):
        print('called MockPushButton.__init__()')
        self.clicked = MockSignal()


class MockLineEdit:
    def __init__(self, *args):
        print('called lineedit.__init__()')
    def setText(self, *args):
        print('called lineedit.settext(`{}`)'.format(args[0]))
    def setMinimumHeight(self, *args):
        print('called lineedit.setMinHeight({})'.format(args[0]))
    def clear(self):
        print('called lineedit.clear()')
    def text(self):
        return 'new seltext'


class MockButtonBox:
    Ok = 1
    Cancel = 2
    accepted = MockSignal()
    rejected = MockSignal()
    def __init__(self, *args):
        print('called buttonbox.__init__(`{}`)'.format(args[0]))


class MockMessageBox:
    Yes = 1
    No = 2
    Cancel = 0
    def __init__(self, *args):
        print('called messagebox.__init__()')
    def setText(self, *args):
        print('called messagebox.setText()')
    def setInformativeText(self, *args):
        print('called messagebox.setInformativeText()')
    def setStandardButtons(self, *args):
        print('called messagebox.setStandardButtons()')
    def setDefaultButton(self, *args):
        print('called messagebox.setDefaultButton()')
    def exec_(self, *args):
        pass


class MockListWidget:
    itemDoubleClicked = MockSignal()
    def __init__(self, *args):
        print('called list.__init__()')
        try:
            self.list = args[0]
        except IndexError:
            self.list = []
    def __len__(self):
        return len(self.list)
    def setSelectionMode(self, *args):
        print('called list.setSelectionMode()')
    def addItems(self, *args):
        print('called list.addItems() with arg `{}`'.format(args[0]))
    def currentItem(self):
        pass
    def item(self, *args):
        return self.list[args[0]]
    def setFocus(self, *args):
        print('called list.setFocus({})'.format(args[0]))
    def selectedItems(self):
        print('called list.selectedItems() on `{}`'.format(self.list))
        return ['item1', 'item2']
    def takeItem(self, *args):
        print('called list.takeItem(`{}`) on `{}`'.format(args[0], self.list))
    def row(self, *args):
        print('called list.row() on `{}`'.format(self.list))
        return args[0]
    def addItem(self, *args):
        print('called list.addItem(`{}`) on `{}`'.format(args[0], self.list))


class MockListWidgetItem:
    def __init__(self, *args):
        print('called listitem.__init__()')
        self.name = args[0]
    def text(self):
        return self.name
    def setSelected(self, *args):
        print('called listitem.setSelected({}) for `{}`'.format(args[0], self.name))


#--- and now for the actual testing stuff ---
class TestMainWindow:
    def test_init(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        assert hasattr(testobj, 'base')
        assert hasattr(testobj, 'app')
        assert testobj.activeitem == None
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n')

    def test_start(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        with pytest.raises(SystemExit):
            testobj.start()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called MockApplication.exec_()\n')

    def test_init_screen(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called QMainWindow.__init__()')
        def mock_setWindowTitle(self, *args):
            print('called setWindowTitle() with args `{}`'.format(args))
        def mock_setWindowIcon(self, *args):
            print('called setWindowIcon()`')
        def mock_resize(self, *args):
            print('called resize() with args `{}`'.format(args))
        monkeypatch.setattr(gui.gui, 'QIcon', MockIcon)
        monkeypatch.setattr(gui.qtw.QMainWindow, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'resize', mock_resize)
        testobj = setup_mainwindow(monkeypatch)
        testobj.init_screen('title', 'iconame')
        assert hasattr(testobj, 'nt_icon')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called QMainWindow.__init__()\n'
                                           "called setWindowTitle() with args `('title',)`\n"
                                           'called MockIcon.__init__() for `iconame`\n'
                                           'called setWindowIcon()`\n'
                                           'called resize() with args `(800, 500)`\n')

    def test_setup_statusbar(self, monkeypatch, capsys):
        def mock_statusbar(self, *args):
            print('called MainWindow.statusbar()')
        monkeypatch.setattr(gui.qtw.QMainWindow, 'statusBar', mock_statusbar)
        testobj = setup_mainwindow(monkeypatch)
        testobj.setup_statusbar()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called MainWindow.statusbar()\n')
        assert hasattr(testobj, 'sb')

    def test_setup_trayicon(self, monkeypatch, capsys):
        monkeypatch.setattr(gui.qtw, 'QSystemTrayIcon', MockSysTrayIcon)
        testobj = setup_mainwindow(monkeypatch)
        testobj.nt_icon = 'nt_icon'
        testobj.setup_trayicon()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called trayicon.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called trayicon.setToolTip()\n'
                                           'called signal.connect()\n'
                                           'called trayicon.hide()\n')
        assert hasattr(testobj, 'tray_icon')

    def test_setup_split_screen(self, monkeypatch, capsys):
        def mock_setcentralwidget(self, *args):
            print('called MockMainWindow.setCentralWidget()')
        def mock_show(self, *args):
            print('called MockMainWindow.show()')
        monkeypatch.setattr(gui.qtw.QMainWindow, 'setCentralWidget', mock_setcentralwidget)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'show', mock_show)
        monkeypatch.setattr(gui.qtw, 'QSplitter', MockSplitter)
        testobj = setup_mainwindow(monkeypatch)
        monkeypatch.setattr(testobj, 'setup_tree', lambda: 'treewidget')
        monkeypatch.setattr(testobj, 'setup_editor', lambda: 'editorwidget')
        testobj.setup_split_screen()
        assert hasattr(testobj, 'splitter')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called MockSplitter.__init__()\n'
                                           'called MockMainWindow.setCentralWidget()\n'
                                           'called splitter.addWidget() with arg `treewidget`\n'
                                           'called splitter.addWidget() with arg `editorwidget`\n'
                                           'called MockMainWindow.show()\n')

    def test_setup_tree(self, monkeypatch, capsys):
        monkeypatch.setattr(gui.qtw, 'QTreeWidget', MockTreeWidget)
        testobj = setup_mainwindow(monkeypatch)
        newstuff = testobj.setup_tree()
        assert newstuff == testobj.tree
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called MockTreeWidget.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called tree.setColumnCount()\n'
                                           'called tree.hideColumn()\n'
                                           "called (header)item.setHidden(True)\n"
                                           'called tree.setSelectionMode()\n'
                                           'called signal.connect()\n')

    def test_setup_editor(self, monkeypatch, capsys):
        monkeypatch.setattr(gui.qsc, 'QsciScintilla', MockEditorWidget)
        monkeypatch.setattr(gui.qsc, 'QsciLexerMarkdown', lambda: 'dummy lexer')
        testobj = setup_mainwindow(monkeypatch)
        newstuff = testobj.setup_editor()
        assert newstuff == testobj.editor
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called editor.__init__()\n'
                                           'called editor.setWrapMode()\n'
                                           'called editor.setBraceMatching()\n'
                                           'called editor.setAutoIndent()\n'
                                           'called editor.setFolding()\n'
                                           'called editor.setCaretLineVisible()\n'
                                           'called editor.setCaretLineBackgroundColor()\n'
                                           'called editor.setLexer()\n'
                                           'called editor.setEnabled(False)\n')

    def test_create_menu(self, monkeypatch, capsys):
        def mock_menubar(self, *args):
            print('called setMenuBar()')
            return MockMenuBar()
        def mock_get_menudata(self):
            return ( (_("m_view"), (
                     (_("m_revorder"), self.callback, _("h_revorder"), 'F9'),
                     ("", None, None, None),
                     (_("m_selall"), self.callback, _("h_selall"), None),
                     (_("m_seltag"), self.callback, _("h_seltag"), None),
                     (_("m_seltxt"), self.callback, _("h_seltxt"), None), ), ), )
        #monkeypatch.setattr(gui.qtw, 'QMenuBar', MockMenuBar)  # Hm dit geeft al een runtimeerror
        monkeypatch.setattr(MockNoteTree, 'get_menudata', mock_get_menudata)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'menuBar', mock_menubar)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.opts = {'RevOrder': True, 'Selection': (1, 'find_me')}
        # import pdb; pdb.set_trace()
        testobj.create_menu()
        assert list(testobj.selactions.keys()) == ["m_revorder", "m_selall", "m_seltag", "m_seltxt"]
        assert testobj.seltypes == ["m_selall", "m_seltag", "m_seltxt"]
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called setMenuBar()\n')

    def test_changeselection(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = 'root'
        testobj.tree = MockTreeWidget()
        testobj.changeselection()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called MockTreeWidget.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called tree.selectedItems()\n'
                                           'called base.check_active()\n'
                                           'called base.activate_item() with arg `current item`\n')

    def test_closeevent(self, monkeypatch, capsys):
        def mock_accept(self, *args):
            print('called event.accept()')
        testobj = setup_mainwindow(monkeypatch)
        monkeypatch.setattr(gui.gui.QCloseEvent, 'accept', mock_accept)
        testobj.activeitem = None
        testobj.closeEvent(gui.gui.QCloseEvent())
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called event.accept()\n')
        testobj = setup_mainwindow(monkeypatch)
        testobj.activeitem = 'active item'
        testobj.closeEvent(gui.gui.QCloseEvent())
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called base.update()\n'
                                           'called event.accept()\n')

    def test_clear_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor = MockEditorWidget()
        testobj.clear_editor()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called editor.__init__()\n'
                                           'called editor.clear()\n'
                                           'called editor.setEnabled(False)\n')

    def test_open_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = 'root'
        testobj.editor = MockEditorWidget()
        testobj.activeitem = 'root'
        testobj.open_editor()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called editor.__init__()\n')
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = 'root'
        testobj.editor = MockEditorWidget()
        testobj.activeitem = 'not root'
        testobj.open_editor()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called editor.__init__()\n'
                                           'called editor.setEnabled(True)\n')

    def test_set_screen(self, monkeypatch, capsys):
        def mock_resize(self, *args):
            print('called resize() with args `{}`'.format(args))
        monkeypatch.setattr(gui.qtw.QMainWindow, 'resize', mock_resize)
        testobj = setup_mainwindow(monkeypatch)
        testobj.set_screen(('x', 'y'))
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           "called resize() with args `('x', 'y')`\n")

    def test_set_splitter(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.splitter = MockSplitter()  # gui.qtw.QSplitter()
        testobj.set_splitter('split')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called MockSplitter.__init__()\n'
                                           "called splitter.setSizes() with args `('split',)`\n")

    def test_create_root(self, monkeypatch, capsys):
        monkeypatch.setattr(gui.qtw, 'QTreeWidgetItem', MockTreeWidgetItem)
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTreeWidget()
        newroot = testobj.create_root('title')
        assert newroot.text(0) == 'title'
        assert testobj.activeitem == testobj.root
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called MockTreeWidget.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called tree.takeTopLevelItem()\n'
                                           'called tree.addTopLevelItem()\n')

    def test_set_item_expanded(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        item = MockTreeWidgetItem()
        testobj.set_item_expanded(item)
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           "called item.setExpanded(True)\n")

    def test_emphasize_activeitem(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.activeitem = MockTreeWidgetItem()
        testobj.emphasize_activeitem('x')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called font.__init__()\n'
                                           'called font.setBold(x)\n'
                                           'called item.setFont()\n')

    def test_editor_text_was_changed(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor = MockEditorWidget()
        assert testobj.editor_text_was_changed() == 'x'
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called editor.__init__()\n')

    def test_copy_text_from_editor_to_activeitem(self, monkeypatch, capsys):
        def mock_settext(self, *args):
            print('called item.setText() with args `{}`, `{}`'.format(args[0], args[1]))
        testobj = setup_mainwindow(monkeypatch)
        testobj.activeitem = MockTreeWidgetItem()
        testobj.editor = MockEditorWidget()
        monkeypatch.setattr(MockTreeWidgetItem, 'setText', mock_settext)
        testobj.copy_text_from_editor_to_activeitem()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called editor.__init__()\n'
                                           'called item.setText() with args `1`, `editor text`\n')

    def test_copy_text_from_activeitem_to_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.activeitem = MockTreeWidgetItem()
        testobj.editor = MockEditorWidget()
        monkeypatch.setattr(MockTreeWidgetItem, 'text', lambda x, y: 'item text')
        testobj.copy_text_from_activeitem_to_editor()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called editor.__init__()\n'
                                           'called editor.setText(`item text`)\n')

    def test_select_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTreeWidget()
        testobj.select_item('item')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called MockTreeWidget.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called tree.setCurrentItem(`item`)\n')

    def test_get_selected_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTreeWidget()
        assert testobj.get_selected_item() == 'current item'
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called MockTreeWidget.__init__()\n'
                                           'called signal.__init__()\n')

    def test_remove_item_from_tree(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = MockTreeWidgetItem()
        testobj.remove_item_from_tree('item')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called item.removeChild()\n')

    def test_get_key_from_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        item = MockTreeWidgetItem()
        item._data = {0: 'key'}
        assert testobj.get_key_from_item(item) == 'key'
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n')

    def test_get_activeitem_title(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.activeitem = MockTreeWidgetItem()
        testobj.activeitem._text = {0: 'title'}
        assert testobj.get_activeitem_title() == 'title'
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n')

    def test_set_activeitem_title(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.activeitem = MockTreeWidgetItem()
        testobj.set_activeitem_title('text')
        assert testobj.activeitem._text == {0: 'text'}
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n')

    def test_set_focus_to_tree(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.tree = MockTreeWidget()
        testobj.set_focus_to_tree()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called MockTreeWidget.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called tree.setFocus()\n')

    def test_set_focus_to_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor = MockEditorWidget()
        testobj.set_focus_to_editor()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called editor.__init__()\n'
                                           'called editor.setFocus()\n')

    def test_add_item_to_tree(self, monkeypatch, capsys):
        monkeypatch.setattr(gui.qtw, 'QTreeWidgetItem', MockTreeWidgetItem)
        expected = MockTreeWidgetItem()
        expected._text = {0: 'tag', 1: 'text'}
        expected._data = {0: 'key', 1: 'keywords'}

        testobj = setup_mainwindow(monkeypatch)
        testobj.root = gui.qtw.QTreeWidgetItem()
        testobj.base.opts = {'RevOrder': False}
        result = testobj.add_item_to_tree('key', 'tag', 'text', 'keywords')
        assert result._text == expected._text
        assert result._data == expected._data
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called treeitem.addChild()\n')

        testobj = setup_mainwindow(monkeypatch)
        testobj.root = gui.qtw.QTreeWidgetItem()
        testobj.base.opts = {'RevOrder': True}
        testobj.add_item_to_tree('key', 'tag', 'text', 'keywords')
        assert result._text == expected._text
        assert result._data == expected._data
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called treeitem.insertChild()\n')

    def test_get_treeitems(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = MockTreeWidgetItem()
        subitem1 = MockTreeWidgetItem()
        subitem1._text = {0: 'tag1', 1: 'text1'}
        subitem1._data = {0: 'key1', 1: 'keywords1'}
        subitem2 = MockTreeWidgetItem()
        subitem2._text = {0: 'tag2', 1: 'text2'}
        subitem2._data = {0: 'key2', 1: 'keywords2'}
        testobj.root.subitems = [subitem1, subitem2]
        testobj.activeitem = None
        assert testobj.get_treeitems() == ([('key1', 'tag1', 'text1', 'keywords1'),
                                            ('key2', 'tag2', 'text2', 'keywords2')], 0)
        testobj.activeitem = subitem2
        assert testobj.get_treeitems() == ([('key1', 'tag1', 'text1', 'keywords1'),
                                            ('key2', 'tag2', 'text2', 'keywords2')], 'key2')

    def test_get_screensize(self, monkeypatch, capsys):
        monkeypatch.setattr(gui.qtw.QMainWindow, 'width', lambda x: 'yay wide')
        monkeypatch.setattr(gui.qtw.QMainWindow, 'height', lambda x: 'yay high')
        testobj = setup_mainwindow(monkeypatch)
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n')
        assert testobj.get_screensize() == ('yay wide', 'yay high')

    def test_get_splitterpos(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.splitter = MockSplitter()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called MockSplitter.__init__()\n')
        assert testobj.get_splitterpos() == ('left this wide', 'right that wide')

    def test_sleep(self, monkeypatch, capsys):
        def mock_hide(self, *args):
            print('called MockMainWindow.hide()')
        monkeypatch.setattr(gui.qtw.QMainWindow, 'hide', mock_hide)
        testobj = setup_mainwindow(monkeypatch)
        testobj.tray_icon = MockSysTrayIcon()
        testobj.sleep()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called trayicon.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called trayicon.show()\n'
                                           'called MockMainWindow.hide()\n')

    def test_revive(self, monkeypatch, capsys):
        def mock_show(self, *args):
            print('called MockMainWindow.show()')
        monkeypatch.setattr(gui.qtw.QMainWindow, 'show', mock_show)
        testobj = setup_mainwindow(monkeypatch)
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n')
        testobj.base.app_title = ''
        testobj.tray_icon = MockSysTrayIcon()
        testobj.revive(gui.qtw.QSystemTrayIcon.Unknown)
        assert capsys.readouterr().out == ('called trayicon.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called trayicon.showMessage()\n')
        testobj.revive(gui.qtw.QSystemTrayIcon.Context)
        assert capsys.readouterr().out == ''
        testobj.revive()
        assert capsys.readouterr().out == ('called MockMainWindow.show()\n'
                                           'called trayicon.hide()\n')

    def test_get_next_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        subitem1 = MockTreeWidgetItem()
        subitem2 = MockTreeWidgetItem()
        testobj.root = MockTreeWidgetItem()
        testobj.root.subitems = [subitem1, subitem2]
        testobj.activeitem = subitem1
        assert testobj.get_next_item() == subitem2
        testobj.activeitem = subitem2
        assert testobj.get_next_item() == None

    def test_get_prev_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        subitem1 = MockTreeWidgetItem()
        subitem2 = MockTreeWidgetItem()
        testobj.root = MockTreeWidgetItem()
        testobj.root.subitems = [subitem1, subitem2]
        testobj.activeitem = subitem2
        assert testobj.get_prev_item() == subitem1
        testobj.activeitem = subitem1
        assert testobj.get_prev_item() == None

    def test_get_itempos(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = MockTreeWidgetItem()
        testobj.root.subitems = ['cheddar', 'stilton', 'gouda']
        assert testobj.get_itempos('gouda') == 2

    def test_get_itemcount(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = MockTreeWidgetItem()
        testobj.root.subitems = ['cheddar', 'stilton', 'gouda']
        assert testobj.get_itemcount() == 3

    def test_get_item_at_pos(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = MockTreeWidgetItem()
        testobj.root.subitems = ['cheddar', 'stilton', 'gouda']
        assert testobj.get_item_at_pos(1) == 'stilton'

    def test_get_rootitem_title(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = MockTreeWidgetItem()
        testobj.root._text = {0: 'title'}
        assert testobj.get_rootitem_title() == 'title'

    def test_set_rootitem_title(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = MockTreeWidgetItem()
        testobj.set_rootitem_title('text')
        assert testobj.root._text == {0: 'text'}

    def test_get_item_text(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        item = MockTreeWidgetItem()
        item._text = {1: 'full item text'}
        assert testobj.get_item_text(item) == 'full item text'

    def test_set_editor_text(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor = MockEditorWidget()
        testobj.set_editor_text('new editor text')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called editor.__init__()\n'
                                           'called editor.setText(`new editor text`)\n')

    def test_get_editor_text(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor = MockEditorWidget()
        testobj.get_editor_text()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called editor.__init__()\n')

    def test_set_item_text(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        item = MockTreeWidgetItem()
        testobj.set_item_text(item, 'new item text')
        assert item._text == {1: 'new item text'}

    def test_get_item_keywords(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        item = MockTreeWidgetItem()
        item._data = {1: ['some', 'words']}
        assert testobj.get_item_keywords(item) == ['some', 'words']

    def test_set_item_keywords(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        item = MockTreeWidgetItem()
        testobj.set_item_keywords(item, ['keyword', 'list'])
        assert item._data == {1: ['keyword', 'list']}

    def test_show_statusbar_message(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.sb = MockStatusBar()
        testobj.show_statusbar_message('text')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called statusbar.showMessage(text)\n')

    def test_enable_selaction(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        action = MockAction('text', 'action')
        testobj.selactions = {'actiontext': action}
        testobj.enable_selaction('actiontext')
        assert action.checked == True

    def test_disable_selaction(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        action = MockAction('text', 'action')
        action.checked = True
        testobj.selactions = {'actiontext': action}
        testobj.disable_selaction('actiontext')
        assert action.checked == False

    def test_showmsg(self, monkeypatch, capsys):
        def mock_info(self, *args):
            print('called messagebox.information() with args `{}`, `{}`'.format(args[0], args[1]))
        monkeypatch.setattr(gui.qtw.QMessageBox, 'information', mock_info)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.app_title = 'app_title'
        testobj.showmsg('message')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called messagebox.information() with args'
                                           ' `app_title`, `message`\n')

    def test_ask_question(self, monkeypatch, capsys):
        def mock_ask(self, *args):
            print('called messagebox.question() with args `{}`, `{}`'.format(args[0], args[1]))
            return 'x'
        monkeypatch.setattr(gui.qtw.QMessageBox, 'question', mock_ask)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.app_title = 'app_title'
        assert testobj.ask_question('question') == False
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called messagebox.question() with args'
                                           ' `app_title`, `question`\n')

    def test_show_dialog(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        assert testobj.show_dialog(MockDialog, 'arg') == (True, {'x': 'y'})
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           "called dialog.__init()__ with args `('arg',)`\n")

    def test_get_text_from_user(self, monkeypatch, capsys):
        def mock_gettext(self, *args):
            print('called inputdialog.getText() with args `{}`'.format(args))
        monkeypatch.setattr(gui.qtw.QInputDialog, 'getText', mock_gettext)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.app_title = 'app_title'
        testobj.get_text_from_user('prompt', 'default')
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           "called inputdialog.getText() with args"
                                           " `('app_title', 'prompt', 0, 'default')`\n")

    def test_get_choice_from_user(self, monkeypatch, capsys):
        def mock_getitem(self, *args, **kwargs):
            print('called inputdialog.getItem() with args `{}` kwargs `{}`'.format(args, kwargs))
        monkeypatch.setattr(gui.qtw.QInputDialog, 'getItem', mock_getitem)
        testobj = setup_mainwindow(monkeypatch)
        testobj.base.app_title = 'app_title'
        testobj.get_choice_from_user('prompt', ['choices'], 0)
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           "called inputdialog.getItem() with args"
                                           " `('app_title', 'prompt', ['choices'])`"
                                           " kwargs `{'current': 0, 'editable': False}`\n")


class TestOptionsDialog:
    def test_init(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called QDialog.__init__()')
        # in methoden die een super() aanroep bevatten om een methode op aan te roepen moet ik de
        # overgeërfde methoden die via self worden aangeroepen ook op de superklasse patchen
        def mock_setWindowTitle(self, *args):
           print('called dialog.setWindowTitle() with args `{}`'.format(args))
        def mock_setLayout(self, *args):
            print('called dialog.setLayout()')
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QGridLayout', MockGridLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', MockLabel)
        monkeypatch.setattr(gui.qtw, 'QCheckBox', MockCheckBox)
        monkeypatch.setattr(gui.qtw, 'QPushButton', MockPushButton)
        testobj = gui.OptionsDialog('parent', {'text': 'value'})
        assert testobj.parent == 'parent'
        assert len(testobj.controls) == 1
        assert testobj.controls[0][0] == 'text'
        assert capsys.readouterr().out == ('called QDialog.__init__()\n'
                                           "called dialog.setWindowTitle() with args"
                                           " `('t_sett',)`\n"
                                           'called MockVBoxLayout.__init__()\n'
                                           'called MockGridLayout.__init__()\n'
                                           'called MockLabel.__init__()\n'
                                           'called grid.addWidget()\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called check.setChecked(value)\n'
                                           'called grid.addWidget()\n'
                                           'called vbox.addLayout()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called hbox.addStretch()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called hbox.addWidget()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called hbox.addWidget()\n'
                                           'called hbox.addStretch()\n'
                                           'called vbox.addLayout()\n'
                                           'called dialog.setLayout()\n')

    def test_accept(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called dialog.__init__()')
            self.parent = args[0]
        def mock_accept(self, *args):
            print('called dialog.accept()')
        monkeypatch.setattr(gui.qtw.QDialog, 'accept', mock_accept)
        monkeypatch.setattr(gui.OptionsDialog, '__init__', mock_init)
        testobj = gui.OptionsDialog(types.SimpleNamespace(dialog_data={}), {})
        testobj.controls = [('text', MockCheckBox())]
        testobj.accept()
        assert testobj.parent.dialog_data == {'text': None}
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called check.isChecked()\n'
                                           'called dialog.accept()\n')


class TestCheckDialog:
    def test_init(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called QDialog.__init__()')
        def mock_setWindowTitle(self, *args):
           print('called dialog.setWindowTitle() with args `{}`'.format(args))
        def mock_setWindowIcon(self, *args):
           print('called dialog.setWindowIcon() with args `{}`'.format(args))
        def mock_setLayout(self, *args):
            print('called dialog.setLayout()')
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', MockLabel)
        monkeypatch.setattr(gui.qtw, 'QCheckBox', MockCheckBox)
        monkeypatch.setattr(gui.qtw, 'QPushButton', MockPushButton)
        testobj = gui.CheckDialog(mockparent, {}, 'message')
        assert testobj.parent == mockparent
        assert capsys.readouterr().out == ('called QDialog.__init__()\n'
                                           "called dialog.setWindowTitle() with args `('title',)`\n"
                                           "called dialog.setWindowIcon() with args `('icon',)`\n"
                                           'called MockLabel.__init__()\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called MockVBoxLayout.__init__()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called hbox.addWidget()\n'
                                           'called vbox.addLayout()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called hbox.addWidget()\n'
                                           'called vbox.addLayout()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called hbox.addWidget()\n'
                                           'called hbox.insertStretch()\n'
                                           'called hbox.addStretch()\n'
                                           'called vbox.addLayout()\n'
                                           'called dialog.setLayout()\n')

    def test_klaar(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called dialog.__init__()')
            self.parent = args[0]
        def mock_accept(self, *args):
            print('called dialog.accept()')
        monkeypatch.setattr(gui.qtw.QDialog, 'accept', mock_accept)
        monkeypatch.setattr(gui.CheckDialog, '__init__', mock_init)
        testobj = gui.CheckDialog(types.SimpleNamespace(dialog_data='x'), {}, '')
        testobj.check = MockCheckBox()
        testobj.klaar()
        assert testobj.parent.dialog_data is None
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called check.isChecked()\n'
                                           'called dialog.accept()\n')


class TestKeywordsDialog:
    def test_init(self, monkeypatch, capsys):
        "test start dialoog zonder keywords parameter"
        def mock_init(self, *args):
            print('called QDialog.__init__()')
        def mock_setWindowTitle(self, *args):
           print('called dialog.setWindowTitle() with args `{}`'.format(args))
        def mock_setWindowIcon(self, *args):
           print('called dialog.setWindowIcon() with args `{}`'.format(args))
        def mock_resize(self, *args):
            print('called dialog.resize()')
        def mock_create_actions(self, *args):
            print('called create_actions()')
        def mock_setLayout(self, *args):
            print('called dialog.setLayout()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QDialog, 'resize', mock_resize)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QListWidget', MockListWidget)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', MockLabel)
        monkeypatch.setattr(gui.qtw, 'QPushButton', MockPushButton)
        monkeypatch.setattr(gui.qtw, 'QDialogButtonBox', MockButtonBox)
        monkeypatch.setattr(gui.KeywordsDialog, 'create_actions', mock_create_actions)
        testobj = gui.KeywordsDialog(mockparent)
        assert capsys.readouterr().out == ('called QDialog.__init__()\n'
                                           "called dialog.setWindowTitle() with args "
                                           "`('title - w_tags',)`\n"
                                           "called dialog.setWindowIcon() with args `('icon',)`\n"
                                           'called dialog.resize()\n'
                                           'called list.__init__()\n'
                                           'called list.setSelectionMode()\n'
                                           'called signal.connect()\n'
                                           'called MockLabel.__init__()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called list.__init__()\n'
                                           'called list.setSelectionMode()\n'
                                           'called signal.connect()\n'
                                           'called buttonbox.__init__(`3`)\n'
                                           'called signal.connect()\n'
                                           'called signal.connect()\n'
                                           'called create_actions()\n'
                                           'called list.addItems() with arg `[]`\n'
                                           "called list.addItems() with arg `['x', 'y']`\n"
                                           'called MockVBoxLayout.__init__()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called MockVBoxLayout.__init__()\n'
                                           'called MockLabel.__init__()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addWidget()\n'
                                           'called hbox.addLayout()\n'
                                           'called MockVBoxLayout.__init__()\n'
                                           'called vbox.addStretch()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addSpacing()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addStretch()\n'
                                           'called hbox.addLayout()\n'
                                           'called MockVBoxLayout.__init__()\n'
                                           'called MockLabel.__init__()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addWidget()\n'
                                           'called hbox.addLayout()\n'
                                           'called vbox.addLayout()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called hbox.addStretch()\n'
                                           'called hbox.addWidget()\n'
                                           'called hbox.addStretch()\n'
                                           'called vbox.addLayout()\n'
                                           'called dialog.setLayout()\n')

    def test_init_2(self, monkeypatch, capsys):
        "test start dialoog met keywords parameter"
        def mock_init(self, *args, **kwargs):
            print('called QDialog.__init__()')
        def mock_setWindowTitle(self, *args):
           print('called dialog.setWindowTitle() with args `{}`'.format(args))
        def mock_setWindowIcon(self, *args):
           print('called dialog.setWindowIcon() with args `{}`'.format(args))
        def mock_resize(self, *args):
            print('called dialog.resize()')
        def mock_create_actions(self, *args):
            print('called create_actions()')
        def mock_setLayout(self, *args):
            print('called dialog.setLayout()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QDialog, 'resize', mock_resize)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QListWidget', MockListWidget)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', MockLabel)
        monkeypatch.setattr(gui.qtw, 'QPushButton', MockPushButton)
        monkeypatch.setattr(gui.qtw, 'QDialogButtonBox', MockButtonBox)
        monkeypatch.setattr(gui.KeywordsDialog, 'create_actions', mock_create_actions)
        testobj = gui.KeywordsDialog(mockparent, keywords=['x'])
        assert capsys.readouterr().out == ('called QDialog.__init__()\n'
                                           "called dialog.setWindowTitle() with args "
                                           "`('title - w_tags',)`\n"
                                           "called dialog.setWindowIcon() with args `('icon',)`\n"
                                           'called dialog.resize()\n'
                                           'called list.__init__()\n'
                                           'called list.setSelectionMode()\n'
                                           'called signal.connect()\n'
                                           'called MockLabel.__init__()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called list.__init__()\n'
                                           'called list.setSelectionMode()\n'
                                           'called signal.connect()\n'
                                           'called buttonbox.__init__(`3`)\n'
                                           'called signal.connect()\n'
                                           'called signal.connect()\n'
                                           'called create_actions()\n'
                                           "called list.addItems() with arg `['x']`\n"
                                           "called list.addItems() with arg `['y']`\n"
                                           'called MockVBoxLayout.__init__()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called MockVBoxLayout.__init__()\n'
                                           'called MockLabel.__init__()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addWidget()\n'
                                           'called hbox.addLayout()\n'
                                           'called MockVBoxLayout.__init__()\n'
                                           'called vbox.addStretch()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addSpacing()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addStretch()\n'
                                           'called hbox.addLayout()\n'
                                           'called MockVBoxLayout.__init__()\n'
                                           'called MockLabel.__init__()\n'
                                           'called vbox.addWidget()\n'
                                           'called vbox.addWidget()\n'
                                           'called hbox.addLayout()\n'
                                           'called vbox.addLayout()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called hbox.addStretch()\n'
                                           'called hbox.addWidget()\n'
                                           'called hbox.addStretch()\n'
                                           'called vbox.addLayout()\n'
                                           'called dialog.setLayout()\n')

    def test_create_actions(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called dialog.__init__()')
        def mock_addAction(self, *args):
            print('called dialog.addAction()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QAction', MockAction)
        monkeypatch.setattr(gui.KeywordsDialog, 'addAction', mock_addAction)
        testobj = gui.KeywordsDialog(mockparent)
        testobj.create_actions()
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                          'call action.setShortcut with arg `Ctrl+L`\n'
                                          'called signal.connect()\n'
                                          'called dialog.addAction()\n'
                                          'call action.setShortcut with arg `Ctrl+Right`\n'
                                          'called signal.connect()\n'
                                          'called dialog.addAction()\n'
                                          'call action.setShortcut with arg `Ctrl+R`\n'
                                          'called signal.connect()\n'
                                          'called dialog.addAction()\n'
                                          'call action.setShortcut with arg `Ctrl+Left`\n'
                                          'called signal.connect()\n'
                                          'called dialog.addAction()\n'
                                          'call action.setShortcut with arg `Ctrl+N`\n'
                                          'called signal.connect()\n'
                                          'called dialog.addAction()\n')

    def test_activate_left(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called dialog.__init__()')
        def mock_activate(self, *args):
            print('called dialog.activate(`{}`)'.format(args[0]))
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QAction', MockAction)
        monkeypatch.setattr(gui.KeywordsDialog, '_activate', mock_activate)
        testobj = gui.KeywordsDialog(mockparent)
        testobj.fromlist = 'fromlist'
        testobj.activate_left()
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                'called dialog.activate(`fromlist`)\n')

    def test_activate_right(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called dialog.__init__()')
        def mock_activate(self, *args):
            print('called dialog.activate(`{}`)'.format(args[0]))
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QAction', MockAction)
        monkeypatch.setattr(gui.KeywordsDialog, '_activate', mock_activate)
        testobj = gui.KeywordsDialog(mockparent)
        testobj.tolist = 'tolist'
        testobj.activate_right()
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                'called dialog.activate(`tolist`)\n')

    def test_activate(self, monkeypatch, capsys):
        "test met geselecteerd item"
        def mock_init(self, *args):
            print('called dialog.__init__()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog(mockparent)
        win = MockListWidget()
        monkeypatch.setattr(win, 'currentItem', lambda: None)
        monkeypatch.setattr(win, 'item', lambda x: MockListWidgetItem('first item'))
        testobj._activate(win)
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called list.__init__()\n'
                                           'called listitem.__init__()\n'
                                           'called listitem.setSelected(True) for `first item`\n'
                                           'called list.setFocus(True)\n')

    def test_activate_2(self, monkeypatch, capsys):
        "test zonder geselecteerd item"
        def mock_init(self, *args):
            print('called dialog.__init__()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog(mockparent)
        win = MockListWidget()
        monkeypatch.setattr(win, 'currentItem', lambda: MockListWidgetItem('current item'))
        testobj._activate(win)
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called list.__init__()\n'
                                           'called listitem.__init__()\n'
                                           'called listitem.setSelected(True) for `current item`\n'
                                           'called list.setFocus(True)\n')

    def test_move_right(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called dialog.__init__()')
        def mock_moveitem(self, *args):
            print('called dialog.moveitem(`{}`)'.format(args))
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, '_moveitem', mock_moveitem)
        testobj = gui.KeywordsDialog(mockparent)
        testobj.fromlist = 'fromlist'
        testobj.tolist = 'tolist'
        testobj.move_right()
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                "called dialog.moveitem(`('fromlist', 'tolist')`)\n")

    def test_move_left(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called dialog.__init__()')
        def mock_moveitem(self, *args):
            print('called dialog.moveitem(`{}`)'.format(args))
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.KeywordsDialog, '_moveitem', mock_moveitem)
        testobj = gui.KeywordsDialog(mockparent)
        testobj.fromlist = 'fromlist'
        testobj.tolist = 'tolist'
        testobj.move_left()
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                "called dialog.moveitem(`('tolist', 'fromlist')`)\n")

    def test_moveitem(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called dialog.__init__()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        testobj = gui.KeywordsDialog(mockparent)
        from_ = MockListWidget('fromlist')
        to = MockListWidget('tolist')
        testobj._moveitem(from_, to)
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called list.__init__()\n'
                                           'called list.__init__()\n'
                                           'called list.selectedItems() on `fromlist`\n'
                                           'called list.row() on `fromlist`\n'
                                           'called list.takeItem(`item1`) on `fromlist`\n'
                                           'called list.addItem(`item1`) on `tolist`\n'
                                           'called list.row() on `fromlist`\n'
                                           'called list.takeItem(`item2`) on `fromlist`\n'
                                           'called list.addItem(`item2`) on `tolist`\n')

    def test_add_trefw(self, monkeypatch, capsys):
        "test doorvoeren trefwoord toevoegen"
        def mock_init(self, *args):
            print('called dialog.__init__()')
            self.parent = args[0]
        def mock_gettext(self, *args):
            print('called inputdialog.getText() with args `{}`'.format(args))
            return 'text', True
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QInputDialog, 'getText', mock_gettext)
        testobj = gui.KeywordsDialog(mockparent)
        testobj.tolist = MockListWidget()
        testobj.add_trefw()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'y', 'text']}
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called list.__init__()\n'
                                           "called inputdialog.getText() with args"
                                           " `('title', 't_newtag')`\n"
                                           'called list.addItem(`text`) on `[]`\n')

    def test_add_trefw_2(self, monkeypatch, capsys):
        "test doorvoeren trefwoord afbreken"
        def mock_init(self, *args):
            print('called dialog.__init__()')
            self.parent = args[0]
        def mock_gettext(self, *args):
            print('called inputdialog.getText() with args `{}`'.format(args))
            return '', False
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QInputDialog, 'getText', mock_gettext)
        testobj = gui.KeywordsDialog(mockparent)
        testobj.tolist = MockListWidget()
        testobj.add_trefw()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'y']}
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called list.__init__()\n'
                                           "called inputdialog.getText() with args"
                                           " `('title', 't_newtag')`\n")

    def keys_help(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called dialog.__init__()')
            self.parent = args[0]
        def mock_init_dialog(self, *args):
            print('called QDialog.__init__()')
        def mock_setWindowTitle(self, *args):
           print('called dialog.setWindowTitle() with args `{}`'.format(args))
        def mock_setLayout(self, *args):
            print('called dialog.setLayout()')
        def mock_exec_(self, *args):
            print('called dialog.exec_()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init_dialog)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QGridLayout', MockGridLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', MockLabel)
        testobj = gui.KeywordsDialog(mockparent)
        testobj.keys_help()
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called QDialog.__init__()\n'
                                           'called MockGridLayout.__init__()\n'
                                           'called MockLabel.__init__()\n'
                                           'called grid.addWidget()\n'
                                           'called MockLabel.__init__()\n'
                                           'called grid.addWidget()\n'
                                           "called dialog.setWindowTitle() with args"
                                           " `('title t_keys',)`"
                                           'called dialog.setLayout()'
                                           'called dialog.exec_()')

    def test_accept(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called dialog.__init__()')
            self.parent = args[0]
        def mock_accept(self, *args):
            print('called dialog.accept()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'accept', mock_accept)
        testobj = gui.KeywordsDialog(mockparent)
        testobj.tolist = MockListWidget([MockListWidgetItem('1'), MockListWidgetItem('2')])
        testobj.accept()
        assert capsys.readouterr().out == ('called dialog.__init__()\n'
                                           'called listitem.__init__()\n'
                                           'called listitem.__init__()\n'
                                           'called list.__init__()\n'
                                           'called dialog.accept()\n')
        assert testobj.parent.dialog_data == ['1', '2']

class TestKeywordsManager:
    def test_init(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called QDialog.__init__()')
        def mock_setWindowTitle(self, *args):
           print('called dialog.setWindowTitle() with args `{}`'.format(args))
        def mock_setWindowIcon(self, *args):
           print('called dialog.setWindowIcon() with args `{}`'.format(args))
        def mock_resize(self, *args):
            print('called dialog.resize()')
        def mock_setLayout(self, *args):
            print('called dialog.setLayout()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QDialog, 'resize', mock_resize)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QGridLayout', MockGridLayout)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', MockLabel)
        monkeypatch.setattr(gui.qtw, 'QComboBox', MockComboBox)
        monkeypatch.setattr(gui.qtw, 'QLineEdit', MockLineEdit)
        monkeypatch.setattr(gui.qtw, 'QPushButton', MockPushButton)
        testobj = gui.KeywordsManager(mockparent)
        assert capsys.readouterr().out == ('called QDialog.__init__()\n'
                                           "called dialog.setWindowTitle() with args "
                                           "`('title - t_tagman',)`\n"
                                           "called dialog.setWindowIcon() with args `('icon',)`\n"
                                           'called dialog.resize()\n'
                                           'called MockComboBox.__init__()\n'
                                           'called lineedit.__init__()\n'
                                           'called lineedit.setMinHeight(100)\n'
                                           'called combo.clear()\n'
                                           "called combo.addItems(['x', 'y'])\n"
                                           'called combo.clearEditText()\n'
                                           'called lineedit.clear()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called MockPushButton.__init__()\n'
                                           'called signal.__init__()\n'
                                           'called signal.connect()\n'
                                           'called MockVBoxLayout.__init__()\n'
                                           'called MockGridLayout.__init__()\n'
                                           'called MockLabel.__init__()\n'
                                           'called grid.addWidget()\n'
                                           'called grid.addWidget()\n'
                                           'called grid.addWidget()\n'
                                           'called MockLabel.__init__()\n'
                                           'called grid.addWidget()\n'
                                           'called grid.addWidget()\n'
                                           'called grid.addWidget()\n'
                                           'called vbox.addLayout()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called MockLabel.__init__()\n'
                                           'called hbox.addWidget()\n'
                                           'called vbox.addLayout()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called hbox.addStretch()\n'
                                           'called hbox.addWidget()\n'
                                           'called hbox.addStretch()\n'
                                           'called vbox.addLayout()\n'
                                           'called dialog.setLayout()\n')

    def refresh_fields(self):
        # wordt uitgevoerd als onderdeel van __init__()
        pass

    def test_update_items(self, monkeypatch, capsys):
        "test trefwoord wijzigen in treeitems"
        def mock_init(self, *args):
            print('called textdialog.__init__()')
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager('parent')
        testobj.parent = types.SimpleNamespace(root=MockTreeWidgetItem())
        subitem1 = MockTreeWidgetItem()
        subitem1._text = {0: 'tag1', 1: 'text1'}
        subitem1._data = {0: 'key1', 1: ['keywords1', 'oldtext']}
        subitem2 = MockTreeWidgetItem()
        subitem2._text = {0: 'tag2', 1: 'text2'}
        subitem2._data = {0: 'key2', 1: ['keywords2']}
        subitem3 = MockTreeWidgetItem()
        subitem3._text = {0: 'tag3', 1: 'text3'}
        subitem3._data = {0: 'key3', 1: ['keywords3', 'oldtext']}
        testobj.parent.root.subitems = [subitem1, subitem2, subitem3]
        testobj.update_items('oldtext', 'newtext')
        assert testobj.parent.root.subitems[0]._data[1] == ['keywords1', 'newtext']
        assert testobj.parent.root.subitems[1]._data[1] == ['keywords2']
        assert testobj.parent.root.subitems[2]._data[1] == ['keywords3', 'newtext']
        assert capsys.readouterr().out == 'called textdialog.__init__()\n'

    def test_update_items_2(self, monkeypatch, capsys):
        "test trefwoord verwijderen uit treeitems"
        def mock_init(self, *args):
            print('called textdialog.__init__()')
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager('parent')
        testobj.parent = types.SimpleNamespace(root=MockTreeWidgetItem())
        subitem1 = MockTreeWidgetItem()
        subitem1._text = {0: 'tag1', 1: 'text1'}
        subitem1._data = {0: 'key1', 1: ['keywords1', 'oldtext']}
        subitem2 = MockTreeWidgetItem()
        subitem2._text = {0: 'tag2', 1: 'text2'}
        subitem2._data = {0: 'key2', 1: ['keywords2', 'oldtext']}
        testobj.parent.root.subitems = [subitem1, subitem2]
        testobj.update_items('oldtext')
        assert testobj.parent.root.subitems[0]._data[1] == ['keywords1']
        assert testobj.parent.root.subitems[1]._data[1] == ['keywords2']
        assert capsys.readouterr().out == 'called textdialog.__init__()\n'

    def test_remove_keyword(self, monkeypatch, capsys):
        "test verwijderen afbreken"
        def mock_init(self, *args):
            print('called textdialog.__init__()')
            self.parent = args[0]
        def mock_update(self, *args):
            print('called dialog.update_items()')
        def mock_refresh(self, *args):
            print('called dialog.refresh_fields()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        monkeypatch.setattr(MockComboBox, 'currentText', lambda x: 'y')
        # testobj.newtag = MockLineEdit()
        monkeypatch.setattr(gui.qtw.QMessageBox, 'question',
                lambda x, y, z: gui.qtw.QMessageBox.No)
        monkeypatch.setattr(testobj, 'update_items', mock_update)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.remove_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'y']}
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called MockComboBox.__init__()\n')

    def test_remove_keyword_2(self, monkeypatch, capsys):
        "test verwijderen doorvoeren"
        def mock_init(self, *args):
            print('called textdialog.__init__()')
            self.parent = args[0]
        def mock_update(self, *args):
            print('called dialog.update_items()')
        def mock_refresh(*args):
            print('called dialog.refresh_fields()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        monkeypatch.setattr(MockComboBox, 'currentText', lambda x: 'y')
        # testobj.newtag = MockLineEdit()
        monkeypatch.setattr(gui.qtw.QMessageBox, 'question',
                lambda x, y, z: gui.qtw.QMessageBox.Yes)
        monkeypatch.setattr(testobj, 'update_items', mock_update)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.remove_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x']}
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called MockComboBox.__init__()\n'
                                           'called dialog.update_items()\n'
                                           'called dialog.refresh_fields()\n')

    def test_add_keyword(self, monkeypatch, capsys):
        "test toevoegen afbreken"
        def mock_init(self, *args):
            print('called textdialog.__init__()')
            self.parent = args[0]
        def mock_refresh(self, *args):
            print('called dialog.refresh_fields()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        monkeypatch.setattr(MockComboBox, 'currentText', lambda x: '')
        testobj.newtag = MockLineEdit()
        monkeypatch.setattr(MockLineEdit, 'text', lambda x: 'z')
        monkeypatch.setattr(gui.qtw.QMessageBox, 'question',
                lambda x, y, z: gui.qtw.QMessageBox.No)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'y']}
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called MockComboBox.__init__()\n'
                                           'called lineedit.__init__()\n')

    def test_add_keyword_2(self, monkeypatch, capsys):
        "test toevoegen doorvoeren"
        def mock_init(self, *args):
            print('called textdialog.__init__()')
            self.parent = args[0]
        def mock_refresh(*args):
            print('called dialog.refresh_fields()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        monkeypatch.setattr(MockComboBox, 'currentText', lambda x: '')
        testobj.newtag = MockLineEdit()
        monkeypatch.setattr(MockLineEdit, 'text', lambda x: 'z')
        monkeypatch.setattr(gui.qtw.QMessageBox, 'question',
                lambda x, y, z: gui.qtw.QMessageBox.Yes)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'y', 'z']}
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called MockComboBox.__init__()\n'
                                           'called lineedit.__init__()\n'
                                           'called dialog.refresh_fields()\n')

    def test_change_keyword(self, monkeypatch, capsys):
        "test wijzigen afbreken"
        def mock_init(self, *args):
            print('called textdialog.__init__()')
            self.parent = args[0]
        def mock_update(self, *args):
            print('called dialog.update_items() with args `{}`'.format(args))
        def mock_refresh(*args):
            print('called dialog.refresh_fields()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        monkeypatch.setattr(MockComboBox, 'currentText', lambda x: 'y')
        testobj.newtag = MockLineEdit()
        monkeypatch.setattr(MockLineEdit, 'text', lambda x: 'z')
        monkeypatch.setattr(gui.qtw, 'QMessageBox', MockMessageBox)
        monkeypatch.setattr(gui.qtw.QMessageBox, 'exec_', lambda x: gui.qtw.QMessageBox.Cancel)
        monkeypatch.setattr(testobj, 'update_items', mock_update)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'y']}
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called MockComboBox.__init__()\n'
                                           'called lineedit.__init__()\n'
                                           'called messagebox.__init__()\n'
                                           'called messagebox.setText()\n'
                                           'called messagebox.setInformativeText()\n'
                                           'called messagebox.setStandardButtons()\n'
                                           'called messagebox.setDefaultButton()\n')

    def test_change_keyword_2(self, monkeypatch, capsys):
        "test wijzigen doorvoeren met vervangen in treeitems"
        def mock_init(self, *args):
            print('called textdialog.__init__()')
            self.parent = args[0]
        def mock_update(*args):
            print('called dialog.update_items() with args `{}`'.format(args))
        def mock_refresh(*args):
            print('called dialog.refresh_fields()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        monkeypatch.setattr(MockComboBox, 'currentText', lambda x: 'y')
        testobj.newtag = MockLineEdit()
        monkeypatch.setattr(MockLineEdit, 'text', lambda x: 'z')
        monkeypatch.setattr(gui.qtw, 'QMessageBox', MockMessageBox)
        monkeypatch.setattr(gui.qtw.QMessageBox, 'exec_', lambda x: gui.qtw.QMessageBox.Yes)
        monkeypatch.setattr(testobj, 'update_items', mock_update)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'z']}
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called MockComboBox.__init__()\n'
                                           'called lineedit.__init__()\n'
                                           'called messagebox.__init__()\n'
                                           'called messagebox.setText()\n'
                                           'called messagebox.setInformativeText()\n'
                                           'called messagebox.setStandardButtons()\n'
                                           'called messagebox.setDefaultButton()\n'
                                           "called dialog.update_items() with args `('y', 'z')`\n"
                                           'called dialog.refresh_fields()\n')

    def test_change_keyword_3(self, monkeypatch, capsys):
        "test wijzigen doorvoeren zonder vervangen in treeitems"
        def mock_init(self, *args):
            print('called textdialog.__init__()')
            self.parent = args[0]
        def mock_update(*args):
            print('called dialog.update_items() with args `{}`'.format(args))
        def mock_refresh(*args):
            print('called dialog.refresh_fields()')
        mockbase = types.SimpleNamespace(app_title='title', opts={'Keywords': ['x', 'y']})
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.KeywordsManager, '__init__', mock_init)
        testobj = gui.KeywordsManager(mockparent)
        testobj.oldtag = MockComboBox()
        monkeypatch.setattr(MockComboBox, 'currentText', lambda x: 'y')
        testobj.newtag = MockLineEdit()
        monkeypatch.setattr(MockLineEdit, 'text', lambda x: 'z')
        monkeypatch.setattr(gui.qtw, 'QMessageBox', MockMessageBox)
        monkeypatch.setattr(gui.qtw.QMessageBox, 'exec_', lambda x: gui.qtw.QMessageBox.No)
        monkeypatch.setattr(testobj, 'update_items', mock_update)
        monkeypatch.setattr(testobj, 'refresh_fields', mock_refresh)
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['x', 'z']}
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called MockComboBox.__init__()\n'
                                           'called lineedit.__init__()\n'
                                           'called messagebox.__init__()\n'
                                           'called messagebox.setText()\n'
                                           'called messagebox.setInformativeText()\n'
                                           'called messagebox.setStandardButtons()\n'
                                           'called messagebox.setDefaultButton()\n'
                                           "called dialog.update_items() with args `('y',)`\n"
                                           'called dialog.refresh_fields()\n')


class TestGetTextDialog:
    def test_init(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called QDialog.__init__()')
        def mock_setWindowTitle(self, *args):
           print('called dialog.setWindowTitle() with args `{}`'.format(args))
        def mock_setWindowIcon(self, *args):
           print('called dialog.setWindowIcon() with args `{}`'.format(args))
        def mock_setLayout(self, *args):
            print('called dialog.setLayout()')
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', MockLabel)
        monkeypatch.setattr(gui.qtw, 'QCheckBox', MockCheckBox)
        monkeypatch.setattr(gui.qtw, 'QLineEdit', MockLineEdit)
        monkeypatch.setattr(gui.qtw, 'QPushButton', MockPushButton)
        monkeypatch.setattr(gui.qtw, 'QDialogButtonBox', MockButtonBox)
        testobj = gui.GetTextDialog(mockparent, 0, 'seltext', 'labeltext', True)
        assert capsys.readouterr().out == ('called QDialog.__init__()\n'
                                           "called dialog.setWindowTitle() with args `('title',)`\n"
                                           "called dialog.setWindowIcon() with args `('icon',)`\n"
                                           'called lineedit.__init__()\n'
                                           'called lineedit.settext(`seltext`)\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called check.setChecked(False)\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called check.setChecked(False)\n'
                                           'called MockVBoxLayout.__init__()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called MockLabel.__init__()\n'
                                           'called hbox.addWidget()\n'
                                           'called vbox.addLayout()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called hbox.addWidget()\n'
                                           'called vbox.addLayout()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called hbox.addWidget()\n'
                                           'called hbox.addWidget()\n'
                                           'called check.setChecked(True)\n'
                                           'called vbox.addLayout()\n'
                                           'called buttonbox.__init__(`3`)\n'
                                           'called signal.connect()\n'
                                           'called signal.connect()\n'
                                           'called vbox.addWidget()\n'
                                           'called dialog.setLayout()\n')

    def test_init_2(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called QDialog.__init__()')
        def mock_setWindowTitle(self, *args):
           print('called dialog.setWindowTitle() with args `{}`'.format(args))
        def mock_setWindowIcon(self, *args):
           print('called dialog.setWindowIcon() with args `{}`'.format(args))
        def mock_setLayout(self, *args):
            print('called dialog.setLayout()')
        mockbase = types.SimpleNamespace(app_title='title')
        mockparent = types.SimpleNamespace(nt_icon='icon', base=mockbase)
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QVBoxLayout', MockVBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QHBoxLayout', MockHBoxLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', MockLabel)
        monkeypatch.setattr(gui.qtw, 'QCheckBox', MockCheckBox)
        monkeypatch.setattr(gui.qtw, 'QLineEdit', MockLineEdit)
        monkeypatch.setattr(gui.qtw, 'QPushButton', MockPushButton)
        monkeypatch.setattr(gui.qtw, 'QDialogButtonBox', MockButtonBox)
        testobj = gui.GetTextDialog(mockparent, -1, 'seltext', 'labeltext', False)
        assert capsys.readouterr().out == ('called QDialog.__init__()\n'
                                           "called dialog.setWindowTitle() with args `('title',)`\n"
                                           "called dialog.setWindowIcon() with args `('icon',)`\n"
                                           'called lineedit.__init__()\n'
                                           'called lineedit.settext(`seltext`)\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called check.setChecked(False)\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called check.setChecked(False)\n'
                                           'called check.setChecked(True)\n'
                                           'called MockVBoxLayout.__init__()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called MockLabel.__init__()\n'
                                           'called hbox.addWidget()\n'
                                           'called vbox.addLayout()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called hbox.addWidget()\n'
                                           'called vbox.addLayout()\n'
                                           'called MockHBoxLayout.__init__()\n'
                                           'called hbox.addWidget()\n'
                                           'called hbox.addWidget()\n'
                                           'called vbox.addLayout()\n'
                                           'called buttonbox.__init__(`3`)\n'
                                           'called signal.connect()\n'
                                           'called signal.connect()\n'
                                           'called vbox.addWidget()\n'
                                           'called dialog.setLayout()\n')

    def test_create_inputwin(self, monkeypatch, capsys):
        # hier niet per se nodig omdat het ook al in de init doorgelopen wordt
        def mock_init(self, *args):
            print('called textdialog.__init__()')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QCheckBox', MockCheckBox)
        monkeypatch.setattr(gui.qtw, 'QLineEdit', MockLineEdit)
        testobj = gui.GetTextDialog('parent', 0, '')  # , 'labeltext', False)
        testobj.create_inputwin('seltext')
        assert hasattr(testobj, 'inputwin')
        assert hasattr(testobj, 'use_case')
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called lineedit.__init__()\n'
                                           'called lineedit.settext(`seltext`)\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called check.setChecked(False)\n')

    def test_get_dialog_data(self, monkeypatch, capsys):
        # hier niet per se nodig omdat het ook al in de init doorgelopen wordt
        def mock_init(self, *args):
            print('called textdialog.__init__()')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QLineEdit', MockLineEdit)
        testobj = gui.GetTextDialog('parent', 0, '')  # , 'labeltext', False)
        testobj.inputwin = MockLineEdit()
        testobj.in_exclude = MockCheckBox()
        testobj.use_case = MockCheckBox()
        testobj.parent = types.SimpleNamespace(dialog_data='x')
        testobj.get_dialog_data()
        assert testobj.parent.dialog_data == [None, 'new seltext', None]
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called lineedit.__init__()\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called check.isChecked()\n'
                                           'called check.isChecked()\n')


    def test_accept(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called textdialog.__init__()')
            self.parent = args[0]
        def mock_accept(self, *args):
            print('called dialog.accept()')
        monkeypatch.setattr(gui.qtw.QDialog, 'accept', mock_accept)
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        testobj = gui.GetTextDialog(types.SimpleNamespace(dialog_data='x'), 0, '')
        testobj.inputwin = MockLineEdit()
        testobj.in_exclude = MockCheckBox()
        testobj.use_case = MockCheckBox()
        testobj.accept()
        assert testobj.parent.dialog_data == [None, 'new seltext', None]
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called lineedit.__init__()\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called check.isChecked()\n'
                                           'called check.isChecked()\n'
                                           'called dialog.accept()\n')


class TestGetItemDialog:
    def test_create_inputwin(self, monkeypatch, capsys):
        def mock_init(self, *args):
            print('called textdialog.__init__()')
            self.parent = args[0]
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QComboBox', MockComboBox)
        mockbase = types.SimpleNamespace(opts={'Keywords': ['title']})
        mockparent = types.SimpleNamespace(base=mockbase)
        # import pdb; pdb.set_trace()
        testobj = gui.GetItemDialog(mockparent, 0, '')
        testobj.create_inputwin((['item0', 'item1'], 1))
        assert hasattr(testobj, 'inputwin')
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           "called MockComboBox.__init__()\n"
                                           "called combo.addItems(['item0', 'item1'])\n"
                                           'called combo.setCurrentIndex(1)\n')

    def test_get_dialog_data(self, monkeypatch, capsys):
        pass
        def mock_init(self, *args):
            print('called textdialog.__init__()')
        monkeypatch.setattr(gui.GetTextDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw, 'QLineEdit', MockLineEdit)
        testobj = gui.GetItemDialog('parent', 0, '')  # , 'labeltext', False)
        testobj.inputwin = MockComboBox()
        testobj.in_exclude = MockCheckBox()
        testobj.parent = types.SimpleNamespace(dialog_data='x')
        testobj.get_dialog_data()
        assert testobj.parent.dialog_data == [None, 'current text']
        assert capsys.readouterr().out == ('called textdialog.__init__()\n'
                                           'called MockComboBox.__init__()\n'
                                           'called MockCheckBox.__init__()\n'
                                           'called combo.currentText()\n'
                                           'called check.isChecked()\n')


class TestGridDialog:
    def test_init(self, monkeypatch, capsys):
        return  # ik kan de call via _() niet simuleren
        # gettext.install definieert een GNUTranslations object en herdefinieert de builtin _
        # om daarvan de gettext methode aan te roepen
        # maar omdat ik geen referentie naar dat object heb kan ik die call ook niet patchen
        # wat misschien wel kan is vóór de import gettext.install patchen zodat deze _ op iets
        # anders mapt
        def mock_init(self, *args):
            print('called QDialog.__init__()')
        def mock_setWindowTitle(self, *args):
           print('called dialog.setWindowTitle() with args `{}`'.format(args))
        def mock_translation(*args):
            return 'a - b\nc - d'
        def mock_setLayout(self, *args):
            print('called dialog.setLayout()')
        monkeypatch.setattr(gui.qtw.QDialog, '__init__', mock_init)
        monkeypatch.setattr(gui.qtw.QDialog, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QDialog, 'setLayout', mock_setLayout)
        monkeypatch.setattr(gui.qtw, 'QGridLayout', MockGridLayout)
        monkeypatch.setattr(gui.qtw, 'QLabel', MockLabel)
        # monkeypatch.setattr(gui.gettext, 'translation', mock_translation)
        testobj = gui.GridDialog('parent', 'title')
        assert capsys.readouterr().out == ('called QDialog.__init__()\n'
                                           'called MockGridLayout.__init__()\n'
                                           'called MockLabel.__init__()\n'
                                           'called grid.addWidget()\n'
                                           'called MockLabel.__init__()\n'
                                           'called grid.addWidget()\n'
                                           'called MockLabel.__init__()\n'
                                           'called grid.addWidget()\n'
                                           'called MockLabel.__init__()\n'
                                           'called grid.addWidget()\n'
                                           "called dialog.setWindowTitle() with args"
                                           " `('title',)`\n"
                                           'called dialog.setLayout()')

