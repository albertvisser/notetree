""" unittests va=oor qt_gui.py
"""
import os
import pytest
import gettext
import notetree.qt_gui as gui
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gettext.install("NoteTree", os.path.join(HERE, 'locale'))


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


class MockAction:
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
    def setShortcuts(self, data):
        self.shortcuts = data
    def setStatusTip(self, data):
        self.statustip = data


class MockTreeWidget:
    def __init__(self, *args):
        print('called MockTreeWidget.__init__()')
    # def selectedItems(self): pass
    def selectedItems(self):
        print('called tree.selectedItems()')
    def currentItem(self):
        return 'current item'


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


class MockTextEdit:
    def __init__(self, *args):
        print('called editor.__init__()')
    def setEnabled(self, *args):
        print('called editor.setEnabled()')


class MockSysTrayIcon:
    def showMessage(self, *args):
        print('called trayicon.showMessage()')
    def hide(self):
        print('called trayicon.hide()')


def setup_mainwindow(monkeypatch):
        monkeypatch.setattr(gui.qtw, 'QApplication', MockApplication)
        monkeypatch.setattr(gui.qtw, 'QMainWindow', MockMainWindow)
        testobj = gui.MainWindow(MockNoteTree())
        return testobj


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
        def mock_setWindowTitle(self, *args):
            print('called setWindowTitle() with args `{}`'.format(args))
        def mock_setWindowIcon(self, *args):
            print('called setWindowIcon()`')
        def mock_resize(self, *args):
            print('called resize() with args `{}`'.format(args))
        monkeypatch.setattr(gui.gui, 'QIcon', MockIcon)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'setWindowTitle', mock_setWindowTitle)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'setWindowIcon', mock_setWindowIcon)
        monkeypatch.setattr(gui.qtw.QMainWindow, 'resize', mock_resize)
        # helaas, zo eenvoudig als dit is het niet
        # monkeypatch.setattr(__builtin__, 'super', lambda x: MockMainWindow)
        testobj = setup_mainwindow(monkeypatch)
        testobj.init_screen('title', 'iconame')  # de super() call die hier gedaan wordt failt
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called MockMainWindow.__init__()\n'
                                           "called setWindowTitle() with args `('title',)`\n"
                                           'called MockIcon.__init__() for `iconame`\n'
                                           'called setWindowIcon()`\n'
                                           'called resize() with args `(800, 500)`\n')

    def setup_statusbar(self): pass

    def setup_trayicon(self): pass

    def setup_split_screen(self): pass

    def setup_tree(self): pass

    def setup_editor(self): pass

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

    def clear_editor(self): pass

    def test_open_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = 'root'
        testobj.editor = MockTextEdit()
        testobj.activeitem = 'root'
        testobj.open_editor()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called editor.__init__()\n')
        testobj = setup_mainwindow(monkeypatch)
        testobj.root = 'root'
        testobj.editor = MockTextEdit()
        testobj.activeitem = 'not root'
        testobj.open_editor()
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n'
                                           'called editor.__init__()\n'
                                           'called editor.setEnabled()\n')

    def set_screen(self, screensize): pass

    def set_splitter(self, split): pass

    def create_root(self, title): pass

    def set_item_expanded(self, item): pass

    def emphasize_activeitem(self, value): pass

    def editor_text_was_changed(self): pass

    def copy_text_from_editor_to_activeitem(self): pass

    def copy_text_from_activeitem_to_editor(self): pass

    def select_item(self, item): pass

    def get_selected_item(self): pass

    def remove_item_from_tree(self, item): pass

    def get_key_from_item(self, item): pass

    def get_activeitem_title(self): pass

    def set_activeitem_title(self, text): pass

    def set_focus_to_tree(self): pass

    def set_focus_to_editor(self): pass

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

    def get_screensize(self): pass

    def get_splitterpos(self): pass

    def sleep(self): pass

    def test_revive(self, monkeypatch, capsys, event=None):
        def mock_show(self, *args):
            print('called MockMainWindow.show()')
        monkeypatch.setattr(gui.qtw.QMainWindow, 'show', mock_show)
        testobj = setup_mainwindow(monkeypatch)
        assert capsys.readouterr().out == ('called MockNoteTree.__init__()\n'
                                           'called MockApplication.__init__()\n')
        testobj.base.app_title = ''
        testobj.tray_icon = MockSysTrayIcon()
        testobj.revive(gui.qtw.QSystemTrayIcon.Unknown)
        assert capsys.readouterr().out == 'called trayicon.showMessage()\n'
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

    def get_itempos(self, item): pass

    def get_itemcount(self): pass

    def get_item_at_pos(self, pos): pass

    def get_rootitem_title(self): pass

    def set_rootitem_title(self, text): pass

    def get_item_text(self, item): pass

    def set_editor_text(self, text): pass

    def get_editor_text(self): pass

    def set_item_text(self, item, text): pass

    def get_item_keywords(self, item): pass

    def set_item_keywords(self, item, keyword_list): pass

    def show_statusbar_message(self, text): pass

    def enable_selaction(self, actiontext): pass

    def disable_selaction(self, actiontext): pass

    def showmsg(self, message): pass

    def ask_question(self, question): pass

    def show_dialog(self, cls, *args): pass

    def get_text_from_user(self, prompt, default): pass

    def get_choice_from_user(self, prompt, choices, choice=0): pass


class OptionsDialog:
    def __init__(self, parent, text2valuedict):
        pass  # loopen over settings

    def accept(self):
        pass  # uitlezen attributen


class CheckDialog:
    def __init__(self, parent, option, message):
        pass

    def klaar(self):
        pass


class KeywordsDialog:
    def __init__(self, parent, keywords=None):
        pass  # check input,

    def create_actions(self):
        pass  # loop over tabel

    def activate_left(self):
        pass  # relay call

    def activate_right(self):
        pass  # relay call

    def _activate(self, win):
        pass  # check "input"

    def move_right(self):
        pass  # relay call

    def move_left(self):
        pass  # ralay call

    def _moveitem(self, from_, to):
        pass  # loop over "input"

    def add_trefw(self):
        pass  # check uitkomst dialoog

    def keys_help(self):
        pass

    def accept(self):
        pass


class KeywordsManager:
    def __init__(self, parent):
        pass

    def refresh_fields(self):
        pass

    def update_items(self, oldtext, newtext=''):
        pass  # loop over "output"

    def remove_keyword(self):
        pass  # check "input"

    def add_keyword(self):
        pass  # check diverse "input"


class GetTextDialog:
    def __init__(self, parent, seltype, seltext, labeltext='', use_case=None):
        pass  # check "input"

    def create_inputwin(self, seltext):
        pass

    def accept(self):
        pass


class GetItemDialog:
    def create_inputwin(self, seldata):
        pass  # check "input"

    def accept(self):
        pass


class GridDialog:
    def __init__(self, parent, title=''):
        pass

