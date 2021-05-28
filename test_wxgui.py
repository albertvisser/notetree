""" unittests voor wx_gui.py
"""
import os
import pytest
import gettext
import notetree.wx_gui as gui
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gettext.install("NoteTree", os.path.join(HERE, 'locale'))


def setup_mainwindow(monkeypatch):
    monkeypatch.setattr(gui.wx, 'Frame', MockFrame)
    monkeypatch.setattr(gui.wx, 'App', MockApp)
    me = gui.MainWindow(MockNoteTree())
    return me


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


class MockIcon:
    def __init__(self, *args):
        print('called Icon.__init__()')


class MockMenuBar:
    def __init__(self, *args):
        print('called MenuBar.__init__()')


class MockSplitter:
    def __init__(self, *args):
        print('called MockSplitter.__init__()')
    def SetMinimumPaneSize(self, *args):
        print('called splitter.SetMinimumPaneSize()')
    def SplitVertically(self, *args):
        print('called splitter.SplitVertically()')
    def SetSashPosition(self, *args):
        print('called splitter.SetSashPosition()')


class MockTree:
    def __init__(self, *args):
        print('called MockTree.__init__()')
    def AddRoot(self, *args):
        print('called tree.AddRoot()')
    def Bind(self, *args):
        print('called tree.Bind() for method {}'.format(str(args[1]).split()[2]))


class MockEditor:
    def __init__(self, *args):
        print('called MockEditor.__init__()')
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


class MockFont:
    def __init__(self):
        print('called MockFont.__init__()')
    def SetFamily(self, *args):
        print('called font.SetFamily()')
    def SetPointSize(self, *args):
        print('called font.SetPointSize()')


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
        def mock_seticon(self, *args):
            print('called frame.SetIcon')
        def mock_setmenubar(self, *args):
            print('called frame.SetMenuBar()')
        monkeypatch.setattr(gui.wx, 'Icon', MockIcon)
        monkeypatch.setattr(gui.wx.Frame, 'SetIcon', mock_seticon)
        monkeypatch.setattr(gui.wx, 'MenuBar', MockMenuBar)
        monkeypatch.setattr(gui.wx.Frame, 'SetMenuBar', mock_setmenubar)
        testobj = setup_mainwindow(monkeypatch)
        testobj.init_screen(parent=None, title='', iconame='')
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

    def test_setup_text(self, monkeypatch, capsys):
        "wordt uitgevoerd als onderdeel van setup_editor, dus geen aparte test nodig"

    def create_menu(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.create_menu()
        pass
    def OnEvtText(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.OnEvtText(event)
        pass
    def OnSelChanging(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.OnSelChanging(event=None)
        pass
    def OnSelChanged(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.OnSelChanged(event=None)
        pass
    def close(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.close(event=None)
        pass
    def clear_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.clear_editor()
        pass
    def open_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.open_editor()
        pass
    def set_screen(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.set_screen(screensize)
        pass
    def set_splitter(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.set_splitter(split)
        pass
    def create_root(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.create_root(title)
        pass
    def set_item_expanded(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.set_item_expanded(item)
        pass
    def emphasize_activeitem(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.emphasize_activeitem(value)
        pass
    def editor_text_was_changed(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.editor_text_was_changed()
        pass
    def copy_text_from_editor_to_activeitem(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.copy_text_from_editor_to_activeitem()
        pass
    def copy_text_from_activeitem_to_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.copy_text_from_activeitem_to_editor()
        pass
    def select_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.select_item(item)
        pass
    def get_selected_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_selected_item()
        pass
    def remove_item_from_tree(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.remove_item_from_tree(item)
        pass
    def get_key_from_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_key_from_item(item)
        pass
    def get_activeitem_title(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_activeitem_title()
        pass
    def set_activeitem_title(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_key_from_item(item)
        pass
    def set_focus_to_tree(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.set_focus_to_tree()
        pass
    def set_focus_to_editor(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.set_focus_to_editor()
        pass
    def add_item_to_tree(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.add_item_to_tree(key, tag, text, keywords)
        pass
    def get_treeitems(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_treeitems()
        pass
    def get_screensize(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_screensize()
        pass
    def get_splitterpos(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_splitterpos()
        pass
    def sleep(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.sleep()
        pass
    def revive(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.revive(event=None)
        pass
    def get_next_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_next_item()
        pass
    def get_prev_item(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_prev_item()
        pass
    def get_rootitem_title(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_rootitem_title()
        pass
    def set_rootitem_title(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.set_rootitem_title(text)
        pass
    def get_item_text(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_item_text(item)
        pass
    def set_editor_text(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.set_editor_text(text)
        pass
    def get_editor_text(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_editor_text()
        pass
    def set_item_text(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.set_item_text(item, text)
        pass
    def get_item_keywords(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_item_keywords(item)
        pass
    def set_item_keywords(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.set_item_keywords(item, data)
        pass
    def show_statusbar_message(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.show_statusbar_message(text)
        pass
    def enable_selaction(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.enable_selaction(sactiontext)
        pass
    def disable_selaction(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.disable_selaction(actiontext)
        pass
    def showmsg(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.showmsg(message)
        pass
    def ask_question(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.ask_question(question)
        pass
    def show_dialog(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.show_dialog(cls, *args)
        pass
    def get_text_from_user(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_text_from_user(prompt, default)
        pass
    def get_choice_from_user(self, monkeypatch, capsys):
        testobj = setup_mainwindow(monkeypatch)
        testobj.get_choice_from_user(prompt, choices, default)
        pass

class OptionsDialog:
    def __init__(self, parent, text2valuedict):
        pass
    def confirm(self):
        pass
class CheckDialog:
    def __init__(self, parent, option, message):
        pass
    def confirm(self):
        pass
class KeywordsDialog:
    def __init__(self, parent, keywords=None):
        pass
    def create_actions(self):
        pass
    def activate_left(self, event):
        pass
    def activate_right(self, event):
        pass
    def _activate(self, win):
        pass
    def move_right(self, event):
        pass
    def move_left(self, event):
        pass
    def _moveitem(self, from_, to):
        pass
    def add_trefw(self, event):
        pass
    def keys_help(self, event):
        pass
    def confirm(self):    # def accept(self):
        pass
class KeywordsManager:
    def __init__(self, parent):
        pass
    def refresh_fields(self):
        pass
    def update_items(self, oldtext, newtext=''):
        pass
    def remove_keyword(self, event):
        pass
    def add_keyword(self, event):
        pass
    def confirm(self):
        pass
class GetTextDialog:
    def __init__(self, parent, seltype, seltext, labeltext='', use_case=None):
        pass
    def create_inputwin(self, seltext):
        pass
    def confirm(self):
        pass
class GetItemDialog:
    def create_inputwin(self, seldata):
        pass
class GridDialog:
    def __init__(self, parent, title):
        pass
    def confirm(self):
        pass
class TaskbarIcon:
    def __init__(self, parent):
        pass
    def CreatePopupMenu(self):
        pass
