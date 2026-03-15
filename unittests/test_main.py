"""unittests for ./notetree/testee.py
"""
# import gettext
import types
from notetree import main as testee

# HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# gettext.install("NoteTree", os.path.join(HERE, 'locale'))


def mock_init(self, filename):
    """stub for NoteTree.__init__
    """
    self.app_title = "mock_app"
    self.root_title = "mock_root"
    self.languages = testee.languages  # {'en': 'en_translation'}
    self.sett2text = testee.sett2text
    self.project_file = filename
    self.gui = MockMainWindow(self)


class MockLanguage:
    """stub for simulating gettext
    """
    def __init__(self, lang):
        self.lang = lang

    def install(self):
        """stub
        """
        print(f"called language.install for language `{self.lang}`")


class MockMainWindow:
    """stub for gui.MainWindow

    method arguments are not used but we need to include them to properly mimic the original class
    """
    def __init__(self, root):
        print("called MainWindow.__init__()")

    def start(self):
        """stub
        """
        print("called MainWindow.start()")

    def init_screen(self, title, iconame):
        """stub
        """
        print("called MainWindow.init_screen()")

    def setup_statusbar(self):
        """stub
        """
        print("called MainWindow.setup_statusbar()")

    def setup_trayicon(self):
        """stub
        """
        print("called MainWindow.setup_trayicon()")

    def setup_split_screen(self):
        """stub
        """
        print("called MainWindow.setup_split_screen()")

    def setup_tree(self):
        """stub
        """
        print("called MainWindow.setup_tree()")

    def setup_editor(self):
        """stub
        """
        print("called MainWindow.setup_editor()")

    def finish_screen(self):
        """stub
        """
        print("called MainWindow.finish_screen()")

    def create_menu(self):
        """stub
        """
        print("called MainWindow.create_menu()")

    def changeselection(self):
        """stub
        """
        print("called MainWindow.changeselection()")

    def close(self):
        """stub
        """
        print("called MainWindow.close()")

    def clear_editor(self):
        """stub
        """
        print("called MainWindow.clear_editor()")

    def open_editor(self):
        """stub
        """
        print("called MainWindow.open_editor()")

    def set_screen(self, screensize):
        """stub
        """
        print("called MainWindow.set_screen()")

    def set_splitter(self, split):
        """stub
        """
        print("called MainWindow.set_splitter()")

    def create_root(self, title):
        """stub
        """
        print("called MainWindow.create_root()")
        return "fake_root"

    def set_item_expanded(self, item):
        """stub
        """
        print("called MainWindow.set_item_expanded()")

    def emphasize_activeitem(self, value):
        """stub
        """
        print("called MainWindow.emphasize_activeitem()")

    def editor_text_was_changed(self):
        """stub
        """
        print("called MainWindow.editor_text_was_changed()")

    def copy_text_from_editor_to_activeitem(self):
        """stub
        """
        print("called MainWindow.copy_text_from_editor_to_activeitem()")

    def copy_text_from_activeitem_to_editor(self):
        """stub
        """
        print("called MainWindow.copy_text_from_activeitem_to_editor()")

    def select_item(self, item):
        """stub
        """
        print("called MainWindow.select_item()")

    def get_selected_item(self):
        """stub
        """
        print("called MainWindow.get_selected_item()")

    def remove_item_from_tree(self, item):
        """stub
        """
        print("called MainWindow.remove_item_from_tree()")

    def get_key_from_item(self, item):
        """stub
        """
        print("called MainWindow.get_key_from_item()")
        return "x"

    def get_activeitem_title(self):
        """stub
        """
        print("called MainWindow.get_activeitem_title()")

    def set_activeitem_title(self, text):
        """stub
        """
        print("called MainWindow.set_activeitem_title()")

    def set_focus_to_tree(self):
        """stub
        """
        print("called MainWindow.set_focus_to_tree()")

    def set_focus_to_editor(self):
        """stub
        """
        print("called MainWindow.set_focus_to_editor()")

    def add_item_to_tree(self, key, tag, text, keywords):  # , revorder):
        """stub
        """
        print("called MainWindow.add_item_to_tree()")

    def get_treeitems(self):
        """stub
        """
        print("called MainWindow.get_treeitems()")
        return [], 0

    def get_screensize(self):
        """stub
        """
        print("called MainWindow.get_screensize()")

    def get_splitterpos(self):
        """stub
        """
        print("called MainWindow.get_splitterpos()")

    def sleep(self):
        """stub
        """
        print("called MainWindow.sleep()")

    def revive(self, event=None):
        """stub
        """
        print("called MainWindow.revive()")

    def get_next_item(self):
        """stub
        """
        print("called MainWindow.get_next_item()")

    def get_prev_item(self):
        """stub
        """
        print("called MainWindow.get_prev_item()")

    def get_itempos(self, item):
        """stub
        """
        print("called MainWindow.get_itempos()")

    def get_itemcount(self):
        """stub
        """
        print("called MainWindow.get_itemcount()")

    def get_item_at_pos(self, pos):
        """stub
        """
        print("called MainWindow.get_item_at_pos()")

    def get_rootitem_title(self):
        """stub
        """
        print("called MainWindow.get_rootitem_title()")

    def set_rootitem_title(self, text):
        """stub
        """
        print("called MainWindow.set_rootitem_title()")

    def get_item_text(self, item):
        """stub
        """
        print("called MainWindow.get_item_text()")

    def set_editor_text(self, text):
        """stub
        """
        print("called MainWindow.set_editor_text()")

    def get_editor_text(self):
        """stub
        """
        print("called MainWindow.get_editor_text()")

    def set_item_text(self, item, text):
        """stub
        """
        print("called MainWindow.set_item_text()")

    def get_item_keywords(self, item):
        """stub
        """
        print("called MainWindow.get_item_keywords()")

    def set_item_keywords(self, item, keyword_list):
        """stub
        """
        print("called MainWindow.set_item_keywords()")

    def show_statusbar_message(self, text):
        """stub
        """
        print("called MainWindow.show_statusbar_message()")

    def enable_selaction(self, actiontext):
        """stub
        """
        print("called MainWindow.enable_selaction()")

    def disable_selaction(self, actiontext):
        """stub
        """
        print("called MainWindow.disable_selaction()")

    def showmsg(self, message):
        """stub
        """
        print("called MainWindow.showmsg()")

    def ask_question(self, question):
        """stub
        """
        print("called MainWindow.ask_question()")

    def show_dialog(self, cls, *args):
        """stub
        """
        print("called MainWindow.show_dialog()")
        return "", False  # simuleer default: afgebroken

    def get_text_from_user(self, prompt, default):
        """stub
        """
        print("called MainWindow.get_text_from_user()")
        return "", False  # simuleer default: afgebroken

    def get_choice_from_user(self, prompt, choices, choice=0):
        """stub
        """
        print("called MainWindow.get_choice_from_user()")
        return "", False  # simuleer default: afgebroken


class TestNoteTree:
    """unittests for testee.NoteTree
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for setting up NoteTree object
        """
        def mock_init(self, filename):
            """stub for NoteTree.__init__
            """
            print(f"called NoteTree.__init__ with args ('{filename}',)")
            self.app_title = "mock_app"
            self.root_title = "mock_root"
            self.languages = testee.languages  # {'en': 'en_translation'}
            self.sett2text = testee.sett2text
            self.project_file = filename
            self.gui = MockMainWindow(self)
        monkeypatch.setattr(testee.NoteTree, "__init__", mock_init)
        testobj = testee.NoteTree("test")
        assert capsys.readouterr().out == ("called NoteTree.__init__ with args ('test',)\n"
                                           "called MainWindow.__init__()\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for NoteTree.init
        """
        def mock_define_screen(*args):
            """stub
            """
            print("called define_screen()")
        def mock_open(self, **kwargs):
            """stub
            """
            arg = "first_time" if kwargs.get("first_time", None) else "not first"
            print(f"called open(`{arg}`)")
        def mock_open_err(self, **kwargs):
            """stub
            """
            arg = "first_time" if kwargs.get("first_time", None) else "not first"
            print(f"called open(`{arg}`)")
            return "error"
        monkeypatch.setattr(testee.gui, "MainWindow", MockMainWindow)
        monkeypatch.setattr(testee.NoteTree, "define_screen", mock_define_screen)
        monkeypatch.setattr(testee.NoteTree, "open", mock_open)
        testobj = testee.NoteTree("test")
        assert testobj.app_title == testee.app_title
        assert testobj.root_title == testee.root_title
        assert testobj.languages == testee.languages
        assert testobj.sett2text == testee.sett2text
        assert testobj.project_file == "test"
        assert capsys.readouterr().out == ("called MainWindow.__init__()\n"
                                           "called define_screen()\n"
                                           "called open(`first_time`)\n"
                                           "called MainWindow.start()\n")
        monkeypatch.setattr(testee.NoteTree, "define_screen", mock_define_screen)
        monkeypatch.setattr(testee.NoteTree, "open", mock_open_err)
        testobj = testee.NoteTree("test")
        assert testobj.app_title == testee.app_title
        assert testobj.root_title == testee.root_title
        assert testobj.languages == testee.languages
        assert testobj.sett2text == testee.sett2text
        assert testobj.project_file == "test"
        assert capsys.readouterr().out == ("called MainWindow.__init__()\n"
                                           "called define_screen()\n"
                                           "called open(`first_time`)\n"
                                           "called MainWindow.showmsg()\n"
                                           "called MainWindow.close()\n")

    def test_define_screen(self, monkeypatch, capsys):
        """unittest for NoteTree.define_screen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.define_screen()
        assert capsys.readouterr().out == ("called MainWindow.init_screen()\n"
            "called MainWindow.setup_statusbar()\n"
            "called MainWindow.setup_trayicon()\n"
            "called MainWindow.setup_split_screen()\n"
            "called MainWindow.setup_tree()\n"
            "called MainWindow.setup_editor()\n"
            "called MainWindow.finish_screen()\n")

    def test_get_menudata(self, monkeypatch, capsys):
        """unittest for NoteTree.get_menudata
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_menudata() is not None  # geen logica; inhoud niet zo interessant

    def test_reread(self, monkeypatch, capsys):
        """unittest for NoteTree.reread
        """
        def mock_ask_question(*args):
            """stub
            """
            print("called MainWindow.ask_question()")
            return True

        def mock_open(*args):
            """stub
            """
            print("called self.open()")

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reread()
        assert capsys.readouterr().out == "called MainWindow.ask_question()\n"
        monkeypatch.setattr(MockMainWindow, "ask_question", mock_ask_question)
        monkeypatch.setattr(testee.NoteTree, "open", mock_open)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reread()
        assert capsys.readouterr().out == ("called MainWindow.ask_question()\n"
            "called self.open()\n")

    def test_save_from_menu(self, monkeypatch, capsys):
        """unittest for NoteTree.save_from_menu
        """
        def mock_update(force_save):
            """stub
            """
            print(f"called update() with arg {force_save}")
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, "update", mock_update)
        testobj.save_from_menu()
        assert capsys.readouterr().out == 'called update() with arg True\n'

    def test_update(self, monkeypatch, capsys):
        """unittest for NoteTree.update
        """
        def mock_tree_to_dict(*args):
            """stub
            """
            print("called tree_to_dict()")
        def mock_tree_to_dict_2(self):
            """stub
            """
            print("called tree_to_dict()")
            self.nt_data = {'not': 'empty'}
        def mock_save(*args):
            """stub
            """
            print("called save()")
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, "tree_to_dict", mock_tree_to_dict)
        monkeypatch.setattr(testobj, "save", mock_save)
        testobj.nt_data = {}
        testobj.old_nt_data = {}
        testobj.opts = {}
        testobj.update()
        assert "ScreenSize" in testobj.opts
        assert "SashPosition" in testobj.opts
        assert capsys.readouterr().out == ("called tree_to_dict()\n"
            "called MainWindow.get_screensize()\n"
            "called MainWindow.get_splitterpos()\n")
        testobj.nt_data = {}
        testobj.old_nt_data = {}
        testobj.opts = {}
        testobj.update(force_save=True)
        assert "ScreenSize" in testobj.opts
        assert "SashPosition" in testobj.opts
        assert capsys.readouterr().out == ("called tree_to_dict()\n"
            "called MainWindow.get_screensize()\n"
            "called MainWindow.get_splitterpos()\n"
            "called save()\n")
        # monkeypatch.setattr(testee.NoteTree, "__init__", mock_init)
        monkeypatch.setattr(testee.NoteTree, "tree_to_dict", mock_tree_to_dict_2)
        # testobj = testee.NoteTree("test")
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(testobj, "save", mock_save)
        testobj.nt_data = {}
        testobj.old_nt_data = {}
        testobj.opts = {}
        testobj.update()
        assert "ScreenSize" in testobj.opts
        assert "SashPosition" in testobj.opts
        assert capsys.readouterr().out == ("called tree_to_dict()\n"
            "called MainWindow.get_screensize()\n"
            "called MainWindow.get_splitterpos()\n"
            "called save()\n")

    def test_rename(self, monkeypatch, capsys):
        """unittest for NoteTree.rename
        """
        def mock_get_text_from_user(*args):
            """stub
            """
            print("called MainWindow.get_text_from_user()")
            return "Hallo", True

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.rename()
        assert capsys.readouterr().out == ("called MainWindow.get_rootitem_title()\n"
            "called MainWindow.get_text_from_user()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(MockMainWindow, "get_text_from_user", mock_get_text_from_user)
        testobj.opts = {}
        testobj.rename()
        assert testobj.opts["RootTitle"] == "Hallo"
        assert capsys.readouterr().out == ("called MainWindow.get_rootitem_title()\n"
            "called MainWindow.get_text_from_user()\n"
            "called MainWindow.set_rootitem_title()\n")

    def test_manage_keywords(self, monkeypatch, capsys):
        """unittest for NoteTree.manage_keywords
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.manage_keywords()
        assert capsys.readouterr().out == "called MainWindow.show_dialog()\n"

    def test_hide_me(self, monkeypatch, capsys):
        """unittest for NoteTree.hide_me
        """
        def mock_show_dialog(*args):
            """stub
            """
            print("called MainWindow.show_dialog()")
            return True, False
        def mock_show_dialog_2(*args):
            """stub
            """
            print("called MainWindow.show_dialog()")
            return True, True

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"AskBeforeHide": False}
        testobj.hide_me()
        assert capsys.readouterr().out == "called MainWindow.sleep()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"AskBeforeHide": True}
        testobj.hide_me()
        assert capsys.readouterr().out == ("called MainWindow.show_dialog()\n"
            "called MainWindow.sleep()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"AskBeforeHide": True}
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog)
        testobj.hide_me()
        assert testobj.opts["AskBeforeHide"]
        assert capsys.readouterr().out == ("called MainWindow.show_dialog()\n"
            "called MainWindow.sleep()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"AskBeforeHide": True}
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog_2)
        testobj.hide_me()
        assert not testobj.opts["AskBeforeHide"]
        assert capsys.readouterr().out == ("called MainWindow.show_dialog()\n"
            "called MainWindow.sleep()\n")

    def test_choose_language(self, monkeypatch, capsys):
        """unittest for NoteTree.choose_language
        """
        def mock_get_choice_from_user(*args):
            """stub
            """
            print("called MainWindow.get_choice_from_user()")
            # return 'English', True
            return "t_en", True

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Language": "nl"}
        testobj.choose_language()
        assert capsys.readouterr().out == "called MainWindow.get_choice_from_user()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Language": "nl"}
        testobj.languages = {"en": MockLanguage("en"), "nl": MockLanguage("nl")}
        monkeypatch.setattr(MockMainWindow, "get_choice_from_user", mock_get_choice_from_user)
        testobj.choose_language()
        assert testobj.opts["Language"] == "en"
        assert capsys.readouterr().out == ("called MainWindow.get_choice_from_user()\n"
            "called language.install for language `en`\n"
            "called MainWindow.create_menu()\n")

    def test_set_options(self, monkeypatch, capsys):
        """unittest for NoteTree.set_options
        """
        def mock_show_dialog(*args):
            """stub
            """
            print("called MainWindow.show_dialog()")
            return True, {
                "option_1_text": True,
                "option_2_text": True,
                "option_3_text": False,
                "option_4_text": False,
            }

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"option_1": True, "option_2": False, "option_3": True, "option_4": False}
        testobj.sett2text = {"option_1": "option_1_text", "option_2": "option_2_text",
                             "option_3": "option_3_text", "option_4": "option_4_text"}
        testobj.set_options()
        assert testobj.opts == {"option_1": True, "option_2": False,
                                "option_3": True, "option_4": False}
        assert testobj.sett2text == {"option_1": "option_1_text", "option_2": "option_2_text",
                                     "option_3": "option_3_text", "option_4": "option_4_text"}
        assert capsys.readouterr().out == "called MainWindow.show_dialog()\n"
        # testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.opts = {"option_1": True, "option_2": False, "option_3": True, "option_4": False}
        # testobj.sett2text = {
        #     "option_1": "option_1_text",
        #     "option_2": "option_2_text",
        #     "option_3": "option_3_text",
        #     "option_4": "option_4_text",
        # }
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog)
        testobj.set_options()
        assert testobj.opts == {"option_1": True, "option_2": True,
                                "option_3": False, "option_4": False}
        assert testobj.sett2text == {"option_1": "option_1_text", "option_2": "option_2_text",
                                     "option_3": "option_3_text", "option_4": "option_4_text"}
        assert capsys.readouterr().out == "called MainWindow.show_dialog()\n"

    def test_new_item(self, monkeypatch, capsys):
        """unittest for NoteTree.new_item
        """
        def mock_get_text_from_user(*args):
            """stub
            """
            print("called MainWindow.get_text_from_user()")
            return "Hallo", True

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nt_data = {}
        testobj.new_item()
        assert testobj.nt_data == {}
        assert capsys.readouterr().out == "called MainWindow.get_text_from_user()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nt_data = {}
        monkeypatch.setattr(MockMainWindow, "get_text_from_user", mock_get_text_from_user)
        testobj.gui.root = "x"
        testobj.new_item()
        assert list(testobj.nt_data.values()) == [""]
        assert capsys.readouterr().out == ("called MainWindow.get_text_from_user()\n"
            "called MainWindow.add_item_to_tree()\n"
            "called MainWindow.select_item()\n"
            "called MainWindow.set_item_expanded()\n"
            "called MainWindow.open_editor()\n"
            "called MainWindow.set_focus_to_editor()\n")

    def test_delete_item(self, monkeypatch, capsys):
        """unittest for NoteTree.delete_item
        """
        def mock_get_selected_item(self, *args):
            """stub
            """
            print("called MainWindow.get_selected_item()")
            return self.root

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nt_data = {"x": "y"}
        testobj.gui.root = "q"
        testobj.delete_item()
        assert "x" not in testobj.nt_data
        assert capsys.readouterr().out == ("called MainWindow.get_selected_item()\n"
            "called MainWindow.get_key_from_item()\n"
            "called MainWindow.remove_item_from_tree()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.nt_data = {"x": "y"}
        testobj.gui.root = "q"
        monkeypatch.setattr(MockMainWindow, "get_selected_item", mock_get_selected_item)
        testobj.delete_item()
        assert "x" in testobj.nt_data  # not deleted
        assert capsys.readouterr().out == ("called MainWindow.get_selected_item()\n"
            "called MainWindow.showmsg()\n")

    def test_ask_title(self, monkeypatch, capsys):
        """unittest for NoteTree.ask_title
        """
        def mock_get_text_from_user(*args):
            """stub
            """
            print("called MainWindow.get_text_from_user()")
            return "Hallo", True

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ask_title()
        assert capsys.readouterr().out == ("called MainWindow.get_activeitem_title()\n"
            "called MainWindow.get_text_from_user()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        monkeypatch.setattr(MockMainWindow, "get_text_from_user", mock_get_text_from_user)
        testobj.opts = {}
        testobj.ask_title()
        assert capsys.readouterr().out == ("called MainWindow.get_activeitem_title()\n"
            "called MainWindow.get_text_from_user()\n"
            "called MainWindow.set_activeitem_title()\n")

    def test_link_keywords(self, monkeypatch, capsys):
        """unittest for NoteTree.link_keywords
        """
        def mock_get_item_keywords(self, item):
            """stub
            """
            print("called MainWindow.get_item_keywords()")
            return ["kw1", "kw2"]

        def mock_show_dialog(*args):
            """stub
            """
            print("called MainWindow.show_dialog()")
            return True, ["kw1", "kw3"]

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.activeitem = None
        testobj.link_keywords()
        assert capsys.readouterr().out == ""
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.activeitem = "x"
        testobj.link_keywords()
        assert capsys.readouterr().out == "called MainWindow.get_item_keywords()\n"
        monkeypatch.setattr(MockMainWindow, "get_item_keywords", mock_get_item_keywords)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.activeitem = "x"
        testobj.link_keywords()
        assert capsys.readouterr().out == ("called MainWindow.get_item_keywords()\n"
            "called MainWindow.show_dialog()\n")
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.activeitem = "x"
        testobj.link_keywords()
        assert capsys.readouterr().out == ("called MainWindow.get_item_keywords()\n"
            "called MainWindow.show_dialog()\n"
            "called MainWindow.set_item_keywords()\n")

    def test_goto_next_note(self, monkeypatch, capsys):
        """unittest for NoteTree.goto_next_note
        """
        def mock_get_next_item(*args):
            """stub
            """
            print("called MainWindow.get_next_item()")
            return "x"

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.goto_next_note()
        assert capsys.readouterr().out == ("called MainWindow.get_next_item()\n"
            "called MainWindow.showmsg()\n")
        monkeypatch.setattr(MockMainWindow, "get_next_item", mock_get_next_item)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.goto_next_note()
        assert capsys.readouterr().out == ("called MainWindow.get_next_item()\n"
            "called MainWindow.select_item()\n")

    def test_goto_prev_note(self, monkeypatch, capsys):
        """unittest for NoteTree.goto_prev_note
        """
        def mock_get_prev_item(*args):
            """stub
            """
            print("called MainWindow.get_prev_item()")
            return "y"

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.goto_prev_note()
        assert capsys.readouterr().out == ("called MainWindow.get_prev_item()\n"
            "called MainWindow.showmsg()\n")
        monkeypatch.setattr(MockMainWindow, "get_prev_item", mock_get_prev_item)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.goto_prev_note()
        assert capsys.readouterr().out == ("called MainWindow.get_prev_item()\n"
            "called MainWindow.select_item()\n")

    def test_reverse(self, monkeypatch, capsys):
        """unittest for NoteTree.reverse
        """
        def mock_build_tree(*args):
            """stub
            """
            print("called self.build_tree()")

        monkeypatch.setattr(testee.NoteTree, "build_tree", mock_build_tree)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"RevOrder": False}
        testobj.gui.root = "x"
        testobj.reverse()
        assert testobj.opts["RevOrder"]
        assert capsys.readouterr().out == ("called self.build_tree()\n"
            "called MainWindow.select_item()\n"
            "called MainWindow.set_item_expanded()\n"
            "called MainWindow.open_editor()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"RevOrder": True}
        testobj.gui.root = "x"
        testobj.reverse()
        assert not testobj.opts["RevOrder"]
        assert capsys.readouterr().out == ("called self.build_tree()\n"
            "called MainWindow.select_item()\n"
            "called MainWindow.set_item_expanded()\n"
            "called MainWindow.open_editor()\n")

    def test_no_selection(self, monkeypatch, capsys):
        """unittest for NoteTree.no_selection
        """
        def mock_set_selection(*args):
            """stub
            """
            print("called self.set_selection()")

        monkeypatch.setattr(testee.NoteTree, "set_selection", mock_set_selection)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.no_selection()
        assert capsys.readouterr().out == ("called self.set_selection()\n"
            "called MainWindow.show_statusbar_message()\n")

    def test_keyword_select(self, monkeypatch, capsys):
        """unittest for NoteTree.keyword_select
        """
        def mock_set_option(*args):
            """stub
            """
            print("called self.set_option()")

        def mock_set_selection(self, *args):
            """stub
            """
            seltype, text = args[0]
            print(f"called self.set_selection() seltype is {seltype}, tekst is `{text}`")

        def mock_show_dialog(*args):
            """stub
            """
            print("called MainWindow.show_dialog()")
            return True, (False, "for_real")

        def mock_show_dialog_2(*args):
            """stub
            """
            print("called MainWindow.show_dialog()")
            return True, (True, "test")

        monkeypatch.setattr(testee.NoteTree, "set_option", mock_set_option)
        monkeypatch.setattr(testee.NoteTree, "set_selection", mock_set_selection)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Keywords": []}
        testobj.keyword_select()
        assert capsys.readouterr().out == ("called MainWindow.showmsg()\n"
            "called self.set_option()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Keywords": ["test", "for_real"], "Selection": [0, ""]}
        testobj.keyword_select()
        assert capsys.readouterr().out == ("called MainWindow.show_dialog()\n"
            "called self.set_option()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Keywords": ["test", "for_real"], "Selection": [1, "x"]}  # kan dit wel?
        testobj.keyword_select()
        assert capsys.readouterr().out == ("called MainWindow.show_dialog()\n"
            "called self.set_option()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Keywords": ["test", "for_real"], "Selection": [-1, "test"]}
        testobj.keyword_select()
        assert capsys.readouterr().out == ("called MainWindow.show_dialog()\n"
            "called self.set_option()\n")
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Keywords": ["test", "for_real"], "Selection": [-1, "test"]}
        testobj.keyword_select()
        assert capsys.readouterr().out == (
            "called MainWindow.show_dialog()\n"
            "called self.set_selection() seltype is 1, tekst is `for_real`\n"
            "called MainWindow.show_statusbar_message()\n")
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog_2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Keywords": ["test", "for_real"], "Selection": [-1, "test"]}
        testobj.keyword_select()
        assert capsys.readouterr().out == (
            "called MainWindow.show_dialog()\n"
            "called self.set_selection() seltype is -1, tekst is `test`\n"
            "called MainWindow.show_statusbar_message()\n")

    def test_text_select(self, monkeypatch, capsys):
        """unittest for NoteTree.text_select
        """
        def mock_set_option(*args):
            """stub
            """
            print("called self.set_option()")

        def mock_set_selection(self, *args):
            """stub
            """
            seltype, text, use_case = args[0]
            print(f"called self.set_selection() seltype is {seltype}, tekst is `{text}`,"
                  f" use_case is {use_case}")

        def mock_show_dialog(*args):
            """stub
            """
            print("called MainWindow.show_dialog()")
            return True, (False, "for_real", True)

        def mock_show_dialog_2(*args):
            """stub
            """
            print("called MainWindow.show_dialog()")
            return True, (True, "test", False)

        monkeypatch.setattr(testee.NoteTree, "set_option", mock_set_option)
        monkeypatch.setattr(testee.NoteTree, "set_selection", mock_set_selection)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Selection": [0, ""]}
        testobj.text_select()
        assert capsys.readouterr().out == ("called MainWindow.show_dialog()\n"
                                           "called self.set_option()\n")
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Selection": [2, "zoek", False]}
        testobj.text_select()
        assert capsys.readouterr().out == (
            "called MainWindow.show_dialog()\n"
            "called self.set_selection() seltype is 2, tekst is `for_real`, use_case is True\n"
            "called MainWindow.show_statusbar_message()\n")
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog_2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Selection": [-2, "zoek", False]}
        testobj.text_select()
        assert capsys.readouterr().out == (
            "called MainWindow.show_dialog()\n"
            "called self.set_selection() seltype is -2, tekst is `test`, use_case is False\n"
            "called MainWindow.show_statusbar_message()\n")

    def test_info_page(self, monkeypatch, capsys):
        """unittest for NoteTree.info_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.info_page()
        assert capsys.readouterr().out == "called MainWindow.showmsg()\n"

    def test_help_page(self, monkeypatch, capsys):
        """unittest for NoteTree.help_page
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.help_page()
        assert capsys.readouterr().out == "called MainWindow.show_dialog()\n"

    def test_open(self, monkeypatch, capsys):
        """unittest for NoteTree.open
        """
        def mock_load_file(*args):
            """stub
            """
            print("called dml.load_file()")
            return {0: testee.initial_opts}

        def mock_load_file_2(*args):
            """stub
            """
            print("called dml.load_file()")
            data = testee.initial_opts
            data["NotifyOnLoad"] = False
            data["SashPosition"] = (180, 600)
            return {0: data}

        def mock_load_file_empty(*args):
            """stub
            """
            print("called dml.load_file()")
            return {}

        def mock_load_file_error(*args):
            """stub
            """
            print("called dml.load_file()")
            raise EOFError("{} not found")

        def mock_ask_question(*args):
            """stub
            """
            print("called MainWindow.ask_question()")
            return True

        def mock_build_tree(*args, **kwargs):
            """stub
            """
            print("called self.build_tree()")

        def mock_set_splitter(*args):
            """stub
            """
            print("called MainWindow.set_splitter()")
            raise TypeError

        monkeypatch.setattr(testee.dml, "load_file", mock_load_file_error)
        testee.gui.toolkit = "aa"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.open() == "test not found"
        assert capsys.readouterr().out == "called dml.load_file()\n"
        monkeypatch.setattr(testee.dml, "load_file", mock_load_file_empty)
        testobj = self.setup_testobj(monkeypatch, capsys)
        # import pdb; pdb.set_trace()
        # assert testobj.open() == 'File not found'
        assert testobj.open() == "404_message"
        for opt in testee.initial_opts:
            if opt == "Version":
                assert testobj.opts[opt] == "Aa"
            elif opt == "RootTitle":
                assert testobj.opts[opt] == "mock_root"
            else:
                assert testobj.opts[opt] == testee.initial_opts[opt]
        assert capsys.readouterr().out == ("called dml.load_file()\n"
            "called MainWindow.ask_question()\n")
        monkeypatch.setattr(MockMainWindow, "ask_question", mock_ask_question)
        monkeypatch.setattr(testee.NoteTree, "build_tree", mock_build_tree)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = "x"
        testobj.open()
        assert testobj.opts["SashPosition"] == (180, 620)
        assert testobj.nt_data == testobj.old_nt_data
        assert capsys.readouterr().out == ("called dml.load_file()\n"
            "called MainWindow.ask_question()\n"
            "called MainWindow.create_menu()\n"
            "called MainWindow.set_screen()\n"
            "called MainWindow.set_splitter()\n"
            "called MainWindow.clear_editor()\n"
            "called self.build_tree()\n"
            "called MainWindow.select_item()\n"
            "called MainWindow.set_item_expanded()\n"
            "called MainWindow.open_editor()\n"
            "called MainWindow.showmsg()\n"
            "called MainWindow.set_focus_to_tree()\n")
        monkeypatch.setattr(testee.dml, "load_file", mock_load_file)
        monkeypatch.setattr(MockMainWindow, "set_splitter", mock_set_splitter)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = "x"
        testobj.open()
        assert testobj.nt_data == testobj.old_nt_data
        assert capsys.readouterr().out == ("called dml.load_file()\n"
            "called MainWindow.create_menu()\n"
            "called MainWindow.set_screen()\n"
            "called MainWindow.set_splitter()\n"
            "called MainWindow.showmsg()\n"
            "called MainWindow.clear_editor()\n"
            "called self.build_tree()\n"
            "called MainWindow.select_item()\n"
            "called MainWindow.set_item_expanded()\n"
            "called MainWindow.open_editor()\n"
            "called MainWindow.showmsg()\n"
            "called MainWindow.set_focus_to_tree()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = "x"
        testobj.open(first_time=True)
        assert testobj.nt_data == testobj.old_nt_data
        assert capsys.readouterr().out == ("called dml.load_file()\n"
            "called MainWindow.create_menu()\n"
            "called MainWindow.set_screen()\n"
            "called MainWindow.set_splitter()\n"
            "called MainWindow.showmsg()\n"
            "called MainWindow.clear_editor()\n"
            "called self.build_tree()\n"
            "called MainWindow.select_item()\n"
            "called MainWindow.set_item_expanded()\n"
            "called MainWindow.open_editor()\n"
            "called MainWindow.set_focus_to_tree()\n")
        monkeypatch.setattr(testee.dml, "load_file", mock_load_file_2)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = "x"
        testobj.open()
        assert testobj.nt_data == testobj.old_nt_data
        data = testee.initial_opts
        data["NotifyOnLoad"] = False
        data["SashPosition"] = (180, 600)
        assert testobj.opts == data
        assert capsys.readouterr().out == ("called dml.load_file()\n"
            "called MainWindow.create_menu()\n"
            "called MainWindow.set_screen()\n"
            "called MainWindow.set_splitter()\n"
            "called MainWindow.showmsg()\n"
            "called MainWindow.clear_editor()\n"
            "called self.build_tree()\n"
            "called MainWindow.select_item()\n"
            "called MainWindow.set_item_expanded()\n"
            "called MainWindow.open_editor()\n"
            "called MainWindow.set_focus_to_tree()\n")

    def test_build_tree(self, monkeypatch, capsys):
        """unittest for NoteTree.build_tree
        """
        def mock_tree_to_dict(*args):
            """stub
            """
            print("called self.tree_to_dict()")

        def mock_add_item_to_tree(self, key, tag, text, keywords):  # , revorder):
            """stub
            """
            print(f"called MainWindow.add_item_to_tree(): `{key}` -> (`{tag}`, `{text}`,"
                  f" `{keywords}`)")
            return key

        def mock_selection_contains_item(*args):
            """stub
            """
            return True

        def mock_selection_contains_item_no(*args):
            """stub
            """
            return False

        monkeypatch.setattr(testee.NoteTree, "tree_to_dict", mock_tree_to_dict)
        monkeypatch.setattr(testee.NoteTree, "selection_contains_item", mock_selection_contains_item)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"RootTitle": "text", "Selection": (0, "", True)}
        testobj.nt_data = {}
        assert testobj.build_tree() == "fake_root"
        assert capsys.readouterr().out == ("called self.tree_to_dict()\n"
            "called MainWindow.create_root()\n")
        monkeypatch.setattr(MockMainWindow, "add_item_to_tree", mock_add_item_to_tree)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"RootTitle": "text", "Selection": (0, ""), "ActiveItem": "1"}
        testobj.nt_data = {
            0: "x",
            "0": ("0", "nul", ["x"]),
            "1": ("1", "een", ["x", "y"]),
            "2": ("3", "drie"),
        }
        assert testobj.build_tree(first_time=True) == "1"
        assert capsys.readouterr().out == (
            "called MainWindow.create_root()\n"
            "called MainWindow.add_item_to_tree(): `0` -> (`0`, `nul`, `['x']`)\n"
            "called MainWindow.add_item_to_tree(): `1` -> (`1`, `een`, `['x', 'y']`)\n"
            "called MainWindow.add_item_to_tree(): `2` -> (`3`, `drie`, `[]`)\n"
        )
        monkeypatch.setattr(testee.NoteTree, "selection_contains_item",
                            mock_selection_contains_item_no)
        monkeypatch.setattr(MockMainWindow, "add_item_to_tree", mock_add_item_to_tree)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"RootTitle": "text", "Selection": (0, ""), "ActiveItem": "1"}
        testobj.nt_data = {
            0: "x",
            "0": ("0", "nul", ["x"]),
            "1": ("1", "een", ["x", "y"]),
            "2": ("3", "drie"),
        }
        assert testobj.build_tree(first_time=True) == "fake_root"
        assert capsys.readouterr().out == "called MainWindow.create_root()\n"

    def test_check_active(self, monkeypatch, capsys):
        """unittest for NoteTree.check_active
        """
        def mock_editor_text_was_changed(*args):
            """stub
            """
            print("called MainWindow.editor_text_was_changed()")
            return True

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = "x"
        testobj.gui.activeitem = None
        testobj.check_active()
        assert capsys.readouterr().out == ""
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = "x"
        testobj.gui.activeitem = "x"
        testobj.check_active()
        assert capsys.readouterr().out == ""
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = "x"
        testobj.gui.activeitem = "y"
        testobj.check_active()
        assert capsys.readouterr().out == ("called MainWindow.emphasize_activeitem()\n"
                                           "called MainWindow.editor_text_was_changed()\n")
        monkeypatch.setattr(MockMainWindow, "editor_text_was_changed", mock_editor_text_was_changed)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = "x"
        testobj.gui.activeitem = "y"
        testobj.check_active()
        assert capsys.readouterr().out == (
            "called MainWindow.emphasize_activeitem()\n"
            "called MainWindow.editor_text_was_changed()\n"
            "called MainWindow.copy_text_from_editor_to_activeitem()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = "x"
        testobj.gui.activeitem = "y"
        testobj.check_active("oops")
        assert capsys.readouterr().out == (
            "called MainWindow.emphasize_activeitem()\n"
            "called MainWindow.editor_text_was_changed()\n"
            "called MainWindow.showmsg()\n"
            "called MainWindow.copy_text_from_editor_to_activeitem()\n")

    def test_activate_item(self, monkeypatch, capsys):
        """unittest for NoteTree.activate_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.activate_item(None)
        assert capsys.readouterr().out == ""
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = "x"
        testobj.activate_item("x")
        assert testobj.gui.activeitem == "x"
        assert capsys.readouterr().out == "called MainWindow.clear_editor()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.root = "x"
        testobj.activate_item("y")
        assert testobj.gui.activeitem == "y"
        assert capsys.readouterr().out == ("called MainWindow.clear_editor()\n"
                                           "called MainWindow.emphasize_activeitem()\n"
                                           "called MainWindow.copy_text_from_activeitem_to_editor()"
                                           "\ncalled MainWindow.open_editor()\n")

    def test_tree_to_dict(self, monkeypatch, capsys):
        """unittest for NoteTree.tree_to_dict
        """
        def mock_check_active(*args):
            """stub
            """
            print("called self.check_active()")

        def mock_get_treeitems(*args):
            """stub
            """
            print("called MainWindow.get_treeitems()")
            return [(1, "x", "y", ["z"]), (2, "a", "b", [])], "q"

        monkeypatch.setattr(testee.NoteTree, "check_active", mock_check_active)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {}
        testobj.nt_data = {}
        testobj.tree_to_dict()
        assert testobj.opts["ActiveItem"] == 0
        assert testobj.nt_data == {}
        assert capsys.readouterr().out == ("called self.check_active()\n"
                                           "called MainWindow.get_treeitems()\n")
        monkeypatch.setattr(MockMainWindow, "get_treeitems", mock_get_treeitems)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {}
        testobj.nt_data = {}
        testobj.tree_to_dict()
        assert testobj.opts["ActiveItem"] == "q"
        assert testobj.nt_data == {1: ("x", "y", ["z"]), 2: ("a", "b", [])}
        assert capsys.readouterr().out == ("called self.check_active()\n"
                                           "called MainWindow.get_treeitems()\n")

    def test_save(self, monkeypatch, capsys):
        """unittest for NoteTree.save
        """
        def mock_copyfile(*args):
            """stub
            """
            print(f"called shutil.copyfile(`{args[0]}`, `{args[1]}`)")

        def mock_copyfile_error(*args):
            """stub
            """
            print("called shutil.copyfile()")
            raise FileNotFoundError

        def mock_save_file(*args):
            """stub
            """
            print("called dml.save_file()")

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = ""
        testobj.save()
        assert capsys.readouterr().out == ""
        monkeypatch.setattr(testee.shutil, "copyfile", mock_copyfile_error)
        monkeypatch.setattr(testee.dml, "save_file", mock_save_file)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = "x"
        testobj.opts = {"NotifyOnSave": True}
        testobj.nt_data = {0: "r*x", "x": "y"}
        testobj.save()
        assert testobj.nt_data == {0: {"NotifyOnSave": True}, "x": "y"}
        assert testobj.old_nt_data == testobj.nt_data
        assert capsys.readouterr().out == ("called shutil.copyfile()\n"
                                           "called dml.save_file()\n"
                                           "called MainWindow.showmsg()\n")
        monkeypatch.setattr(testee.shutil, "copyfile", mock_copyfile)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.project_file = "x"
        testobj.opts = {"NotifyOnSave": False}
        testobj.nt_data = {0: "r*x", "x": "y"}
        testobj.save()
        assert testobj.nt_data == {0: {"NotifyOnSave": False}, "x": "y"}
        assert testobj.old_nt_data == testobj.nt_data
        assert capsys.readouterr().out == ("called shutil.copyfile(`x`, `x~`)\n"
                                           "called dml.save_file()\n")

    def test_set_selection(self, monkeypatch, capsys):
        """unittest for NoteTree.set_selection
        """
        def mock_build_tree(*args):
            """stub
            """
            print("called self.build_tree")

        monkeypatch.setattr(testee.NoteTree, "build_tree", mock_build_tree)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {}
        testobj.gui.root = "yx"
        testobj.set_selection("x", "Select &All")
        assert testobj.opts["Selection"] == "x"
        assert capsys.readouterr().out == ("called self.build_tree\n"
                                           "called MainWindow.select_item()\n"
                                           "called MainWindow.set_item_expanded()\n"
                                           "called MainWindow.open_editor()\n"
                                           "called MainWindow.enable_selaction()\n"
                                           "called MainWindow.disable_selaction()\n"
                                           "called MainWindow.disable_selaction()\n")

    def test_set_option(self, monkeypatch, capsys):
        """unittest for NoteTree.set_option
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Selection": (-1, "x")}
        testobj.set_option(1, "")
        assert capsys.readouterr().out == "called MainWindow.enable_selaction()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.opts = {"Selection": [-2, "x", False]}
        testobj.set_option(1, "")
        assert capsys.readouterr().out == "called MainWindow.disable_selaction()\n"

    def test_selection_contains_item(self, monkeypatch, capsys):
        """unittest for NoteTree.selection_contains_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.selection_contains_item("text", ["key", "word"], 0, "", None)
        assert testobj.selection_contains_item("text", ["key", "word"], 1, "word", None)
        assert not testobj.selection_contains_item("text", ["key", "word"], 1, "other", None)
        assert not testobj.selection_contains_item("text", ["key", "word"], -1, "word", None)
        assert testobj.selection_contains_item("text", ["key", "word"], -1, "other", None)
        assert testobj.selection_contains_item("text", ["key", "word"], 2, "Ex", False)
        assert not testobj.selection_contains_item("text", ["key", "word"], 2, "Ex", True)
        assert testobj.selection_contains_item("tExt", ["key", "word"], 2, "Ex", True)
        assert not testobj.selection_contains_item("text", ["key", "word"], 2, "oink", False)
        assert not testobj.selection_contains_item("text", ["key", "word"], -2, "Ex", False)
        assert testobj.selection_contains_item("text", ["key", "word"], -2, "Ex", True)
        assert not testobj.selection_contains_item("tExt", ["key", "word"], -2, "Ex", True)
        assert testobj.selection_contains_item("text", ["key", "word"], -2, "oink", False)
        # niet zeker of dit wel kan voorkomen:
        assert not testobj.selection_contains_item("text", ["key", "word"], 3, "xxx", "yyy")
        assert not testobj.selection_contains_item("text", ["key", "word"], -3, "xxx", "yyy")


class TestSetOptions:
    """unittests for testee.SetOptions
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for setting up SetOptions object
        """
        def mock_init(self, *args):
            """stub for SetOptions.__init__
            """
            print('called SetOptions.__init__ with args', args)
        monkeypatch.setattr(testee.SetOptions, "__init__", mock_init)
        testobj = testee.SetOptions()
        assert capsys.readouterr().out == "called SetOptions.__init__ with args ()\n"
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SetOptions.init
        """
        class MockOptionsDialog:
            def __init__(self, *args, **kwargs):
                print('called OptionsDialog.__init__ with args', args, kwargs)
            def add_checkbox_line_to_grid(self, *args, **kwargs):
                print('called OptionsDialog.add_checkbox_line_to_grid with args', args, kwargs)
                return 'checkbox'
            def add_buttonbox(self, *args, **kwargs):
                print('called OptionsDialog.add_buttonbox wth args', args, kwargs)
        monkeypatch.setattr(testee.gui, "OptionsDialog", MockOptionsDialog)
        testobj = testee.SetOptions("test", {})
        assert testobj.parent == 'test'
        assert isinstance(testobj.gui, testee.gui.OptionsDialog)
        assert testobj.controls == []
        assert capsys.readouterr().out == (
                f"called OptionsDialog.__init__ with args ({testobj}, 'test')"
                " {'title': 'NoteTree Settings'}\n"
                "called OptionsDialog.add_buttonbox wth args"
                " () {'okvalue': '&Apply', 'cancelvalue': '&Close'}\n")
        testobj = testee.SetOptions("test", {'x': 'a', 'y': 'b'})
        assert testobj.parent == 'test'
        assert isinstance(testobj.gui, testee.gui.OptionsDialog)
        assert testobj.controls == [('x', 'checkbox'), ('y', 'checkbox')]
        assert capsys.readouterr().out == (
                f"called OptionsDialog.__init__ with args ({testobj}, 'test')"
                " {'title': 'NoteTree Settings'}\n"
                "called OptionsDialog.add_checkbox_line_to_grid with args (1, 'x', 'a') {}\n"
                "called OptionsDialog.add_checkbox_line_to_grid with args (2, 'y', 'b') {}\n"
                "called OptionsDialog.add_buttonbox wth args"
                " () {'okvalue': '&Apply', 'cancelvalue': '&Close'}\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SetOptions.confirm
        """
        def mock_get(*args):
            print('called OptionsDialog.get_checkbox_value with args', args)
            return 'xxx'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get)
        testobj.controls = []
        assert testobj.confirm() == {}
        assert capsys.readouterr().out == ""
        testobj.controls = [('text1', 'control1'), ('text2', 'control2')]
        assert testobj.confirm() == {'text1': 'xxx', 'text2': 'xxx'}
        assert capsys.readouterr().out == (
                "called OptionsDialog.get_checkbox_value with args ('control1',)\n"
                "called OptionsDialog.get_checkbox_value with args ('control2',)\n")


class TestSetCheck:
    """unittests for testee.SetCheck
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for setting up SetCheck object
        """
        def mock_init(self, *args):
            """stub for SetCheck.__init__
            """
            print('called SetCheck.__init__ with args', args)
        monkeypatch.setattr(testee.SetCheck, "__init__", mock_init)
        testobj = testee.SetCheck("test")
        assert capsys.readouterr().out == "called SetCheck.__init__ with args ('test',)\n"
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SetCheck.init
        """
        class MockCheckDialog:
            def __init__(self, *args, **kwargs):
                print('called CheckDialog.__init__ with args', args, kwargs)
            def add_label(self, *args, **kwargs):
                print('called CheckDialog.add_label with args', args, kwargs)
            def add_checkbox(self, *args, **kwargs):
                print('called CheckDialog.add_checkbox with args', args, kwargs)
                return 'check'
            def add_ok_buttonbox(self, *args, **kwargs):
                print('called CheckDialog.add_ok_buttonbox with args', args, kwargs)
        monkeypatch.setattr(testee.gui, "CheckDialog", MockCheckDialog)
        parent = types.SimpleNamespace(base=types.SimpleNamespace(app_title='apptitle'))
        testobj = testee.SetCheck(parent, 'message')
        assert testobj.parent == parent
        assert isinstance(testobj.gui, testee.gui.CheckDialog)
        assert testobj.check == 'check'
        assert capsys.readouterr().out == (
            f"called CheckDialog.__init__ with args ({testobj}, {parent})"
            " {'title': 'apptitle'}\n"
            "called CheckDialog.add_label with args ('message',) {}\n"
            'called CheckDialog.add_checkbox with args ("Don\'t show this message anymore",) {}\n'
            "called CheckDialog.add_ok_buttonbox with args () {}\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SetOptions.confirm
        """
        def mock_get(*args):
            print('called OptionsDialog.get_checkbox_value with args', args)
            return 'xxx'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get)
        testobj.check = 'check'
        assert testobj.confirm() == 'xxx'
        assert capsys.readouterr().out == (
                "called OptionsDialog.get_checkbox_value with args ('check',)\n")


class TestAssignTags:
    """unittests for testee.AssignTags
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for setting up AssignTags object
        """
        def mock_init(self, *args):
            """stub for AssignTags.__init__
            """
            print('called AssignTags.__init__ with args', args)
        monkeypatch.setattr(testee.AssignTags, "__init__", mock_init)
        testobj = testee.AssignTags("test")
        assert capsys.readouterr().out == "called AssignTags.__init__ with args ('test',)\n"
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for AssignTags.init
        """
        class MockKeywordsDialog:
            def __init__(self, *args, **kwargs):
                print('called KeywordsDialog.__init__ with args', args, kwargs)
            def add_list(self, *args, **kwargs):
                print('called KeywordsDialog.add_list with args', args, kwargs)
                return 'listbox'
            def add_buttons(self, *args, **kwargs):
                print('called KeywordsDialog.add_buttons with args', args, kwargs)
                return ['button', 'list']
            def create_buttonbox(self, *args, **kwargs):
                print('called KeywordsDialog.create_buttonbox with args', args, kwargs)
            def create_actions(self, *args, **kwargs):
                print('called KeywordsDialog.create_actions with args', args, kwargs)
        monkeypatch.setattr(testee.gui, "KeywordsDialog", MockKeywordsDialog)
        parent = types.SimpleNamespace(base=types.SimpleNamespace(
            app_title='apptitle', opts={'Keywords': ['x', 'y', 'z']}))
        monkeypatch.setattr(testee.AssignTags, 'move_right', lambda: 'dummy callback')
        monkeypatch.setattr(testee.AssignTags, 'move_left', lambda: 'dummy callback')
        monkeypatch.setattr(testee.AssignTags, 'add_trefw', lambda: 'dummy callback')
        monkeypatch.setattr(testee.AssignTags, 'keys_help', lambda: 'dummy callback')
        monkeypatch.setattr(testee.AssignTags, 'activate_right', lambda: 'dummy callback')
        monkeypatch.setattr(testee.AssignTags, 'activate_left', lambda: 'dummy callback')
        testobj = testee.AssignTags(parent, "test")
        assert testobj.parent == parent
        assert testobj.helptext == 'test'
        assert testobj.fromlist == 'listbox'
        assert testobj.buttons == ['button', 'list']
        assert testobj.tolist == 'listbox'
        assert capsys.readouterr().out == (
                "called KeywordsDialog.__init__ with args"
                f" ({testobj}, {parent}, 'apptitle - assign tags') {{}}\n"
                "called KeywordsDialog.add_list with args ('Available:', ['x', 'y', 'z'],"
                f" {testobj.move_right}) {{'first': True}}\n"
                "called KeywordsDialog.add_buttons with args"
                f" ([('Tag(s):', None), ('&Assign', {testobj.move_right}),"
                f" ('&Unassign', {testobj.move_left}),"
                f" ('', None), ('&New', {testobj.add_trefw}),"
                f" ('&Keys ', {testobj.keys_help})],) {{}}\n"
                "called KeywordsDialog.add_list with args"
                f" ('Assigned:', [], {testobj.move_left}) {{'last': True}}\n"
                "called KeywordsDialog.create_buttonbox with args () {}\n"
                "called KeywordsDialog.create_actions with args"
                f" ([('Activate Left', 'Ctrl+L', {testobj.activate_left}),"
                f" ('&Assign', 'Ctrl+Right', {testobj.move_right}),"
                f" ('Activate Right', 'Ctrl+R', {testobj.activate_right}),"
                f" ('&Unassign', 'Ctrl+Left', {testobj.move_left}),"
                f" ('&New', 'Ctrl+N', {testobj.add_trefw})],) {{}}\n")
        testobj = testee.AssignTags(parent, "test", ['y'])
        assert testobj.parent == parent
        assert testobj.helptext == 'test'
        assert testobj.fromlist == 'listbox'
        assert testobj.buttons == ['button', 'list']
        assert testobj.tolist == 'listbox'
        assert capsys.readouterr().out == (
                "called KeywordsDialog.__init__ with args"
                f" ({testobj}, {parent}, 'apptitle - assign tags') {{}}\n"
                "called KeywordsDialog.add_list with args ('Available:', ['x', 'z'],"
                f" {testobj.move_right}) {{'first': True}}\n"
                "called KeywordsDialog.add_buttons with args"
                f" ([('Tag(s):', None), ('&Assign', {testobj.move_right}),"
                f" ('&Unassign', {testobj.move_left}),"
                f" ('', None), ('&New', {testobj.add_trefw}),"
                f" ('&Keys ', {testobj.keys_help})],) {{}}\n"
                "called KeywordsDialog.add_list with args"
                f" ('Assigned:', ['y'], {testobj.move_left}) {{'last': True}}\n"
                "called KeywordsDialog.create_buttonbox with args () {}\n"
                "called KeywordsDialog.create_actions with args"
                f" ([('Activate Left', 'Ctrl+L', {testobj.activate_left}),"
                f" ('&Assign', 'Ctrl+Right', {testobj.move_right}),"
                f" ('Activate Right', 'Ctrl+R', {testobj.activate_right}),"
                f" ('&Unassign', 'Ctrl+Left', {testobj.move_left}),"
                f" ('&New', 'Ctrl+N', {testobj.add_trefw})],) {{}}\n")

    def test_activate_left(self, monkeypatch, capsys):
        """unittest for SetOptions.activate_left
        """
        def mock_activate(arg):
            print(f"called KeywordsDialog.activate with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(activate=mock_activate)
        testobj.fromlist = 'fromlist'
        testobj.activate_left()
        assert capsys.readouterr().out == "called KeywordsDialog.activate with arg 'fromlist'\n"

    def test_activate_right(self, monkeypatch, capsys):
        """unittest for SetOptions.activate_right
        """
        def mock_activate(arg):
            print(f"called KeywordsDialog.activate with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(activate=mock_activate)
        testobj.tolist = 'tolist'
        testobj.activate_right()
        assert capsys.readouterr().out == "called KeywordsDialog.activate with arg 'tolist'\n"

    def test_move_right(self, monkeypatch, capsys):
        """unittest for SetOptions.move_right
        """
        def mock_move(*args):
            print('called KeywordsDialog.moveitem with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(moveitem=mock_move)
        testobj.fromlist = 'fromlist'
        testobj.tolist = 'tolist'
        testobj.move_right()
        assert capsys.readouterr().out == (
                "called KeywordsDialog.moveitem with args ('fromlist', 'tolist')\n")

    def test_move_left(self, monkeypatch, capsys):
        """unittest for SetOptions.move_left
        """
        def mock_move(*args):
            print('called KeywordsDialog.moveitem with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(moveitem=mock_move)
        testobj.fromlist = 'fromlist'
        testobj.tolist = 'tolist'
        testobj.move_left()
        assert capsys.readouterr().out == (
                "called KeywordsDialog.moveitem with args ('tolist', 'fromlist')\n")

    def test_add_trefw(self, monkeypatch, capsys):
        """unittest for SetOptions.add_trefw
        """
        def mock_ask(*args, **kwargs):
            print('called KeywordsDialog.ask_for_tag with args', args, kwargs)
            return '', False
        def mock_ask_2(*args, **kwargs):
            print('called KeywordsDialog.ask_for_tag with args', args, kwargs)
            return 'xxx', True
        def mock_add(*args):
            print('called KeywordsDialog.add_tag_to_list with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(base=types.SimpleNamespace(app_title='apptitle',
                                                                          opts={'Keywords': []}))
        testobj.gui = types.SimpleNamespace(ask_for_tag=mock_ask, add_tag_to_list=mock_add)
        testobj.tolist = 'tolist'
        testobj.add_trefw()
        assert capsys.readouterr().out == (
                "called KeywordsDialog.ask_for_tag with args"
                " () {'caption': 'apptitle', 'message': 'Enter new keyword'}\n")
        testobj.gui.ask_for_tag = mock_ask_2
        testobj.add_trefw()
        assert capsys.readouterr().out == (
                "called KeywordsDialog.ask_for_tag with args"
                " () {'caption': 'apptitle', 'message': 'Enter new keyword'}\n"
                "called KeywordsDialog.add_tag_to_list with args ('xxx', 'tolist')\n")

    def test_keys_help(self, monkeypatch, capsys):
        """unittest for SetOptions.keys_help
        """
        class MockGrid:
            def __init__(self, *args):
                print('called gui.GridDialog with args', args)
            def add_label(self, *args):
                print('called gui.GridDialog.add_label with args', args)
            def send(self):
                print('called gui.GridDialog.send')
        monkeypatch.setattr(testee.gui, 'GridDialog', MockGrid)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(base=types.SimpleNamespace(app_title='apptitle'))
        testobj.gui = types.SimpleNamespace()
        testobj.helptext = [('x', 'y'), ('a', 'b')]
        testobj.keys_help()
        assert capsys.readouterr().out == (
                "called gui.GridDialog with args"
                f" ({testobj.gui}, 'apptitle special keys', 'Done')\n"
                "called gui.GridDialog.add_label with args (0, 0, 'x')\n"
                "called gui.GridDialog.add_label with args (0, 1, 'y')\n"
                "called gui.GridDialog.add_label with args (1, 0, 'a')\n"
                "called gui.GridDialog.add_label with args (1, 1, 'b')\n"
                "called gui.GridDialog.send\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SetOptions.confirm
        """
        def mock_get(arg):
            print(f"called KeywordsDialog.get_listvalues with arg {arg}")
            return ['x']
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(get_listvalues=mock_get)
        testobj.tolist = 'tolist'
        assert testobj.confirm() == ['x']
        assert capsys.readouterr().out == ("called KeywordsDialog.get_listvalues with arg tolist\n")


class TestDefineTags:
    """unittests for testee.DefineTags
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for setting up DefineTags object
        """
        def mock_init(self, *args):
            """stub for DefineTags.__init__
            """
            print('called DefineTags.__init__ with args', args)
        monkeypatch.setattr(testee.DefineTags, "__init__", mock_init)
        testobj = testee.DefineTags("test")
        assert capsys.readouterr().out == "called DefineTags.__init__ with args ('test',)\n"
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for DefineTags.init
        """
        class MockKeywordsManager:
            def __init__(self, *args, **kwargs):
                print('called KeywordsManager.__init__ with args', args, kwargs)
            def add_label(self, *args):
                print('called KeywordsManager.add_label with args', args)
            def add_combobox(self, *args):
                print('called KeywordsManager.add_combobox with args', args)
                return 'combobox'
            def add_lineinput(self, *args):
                print('called KeywordsManager.add_lineinput with args', args)
                return 'lineinput'
            def add_button(self, *args):
                print('called KeywordsManager.add_button with args', args)
        def mock_refresh(self):
            print('called DefineTags.refresh_fields')
        monkeypatch.setattr(testee.gui, "KeywordsManager", MockKeywordsManager)
        monkeypatch.setattr(testee.DefineTags, 'remove_keyword', lambda: 'dummy callback')
        monkeypatch.setattr(testee.DefineTags, 'add_keyword', lambda: 'dummy callback')
        monkeypatch.setattr(testee.DefineTags, 'refresh_fields', mock_refresh)
        parent = types.SimpleNamespace(base=types.SimpleNamespace(app_title='apptitle'))
        testobj = testee.DefineTags(parent)
        assert isinstance(testobj.gui, testee.gui.KeywordsManager)
        assert testobj.oldtags == 'combobox'
        assert testobj.newtag == 'lineinput'
        assert capsys.readouterr().out == (
                "called KeywordsManager.__init__ with args"
                f" ({testobj}, {testobj.parent}, 'apptitle - Manage tags', 'Done') {{}}\n"
                "called KeywordsManager.add_label with args ('Current:', 0, 0)\n"
                "called KeywordsManager.add_combobox with args (0, 1)\n"
                "called KeywordsManager.add_button with args"
                f" ('Remove selected', {testobj.remove_keyword}, 0, 2)\n"
                "called KeywordsManager.add_label with args ('New value', 1, 0)\n"
                "called KeywordsManager.add_lineinput with args (1, 1)\n"
                "called KeywordsManager.add_button with args"
                f" ('Add/Update', {testobj.add_keyword}, 1, 2)\n"
                "called KeywordsManager.add_label with args"
                " ('Changes are applied immediately', 2, -1)\n"
                "called DefineTags.refresh_fields\n")

    def test_refresh_fields(self, monkeypatch, capsys):
        """unittest for SetOptions.refresh_fields
        """
        def mock_reset_combo(*args):
            print('called KeywordsManager._reset_combobox with args', args)
        def mock_reset_input(*args):
            print('called KeywordsManager._reset_lineinput with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(
                base=types.SimpleNamespace(opts={'Keywords': {'key': 'words'}}))
        testobj.gui = types.SimpleNamespace(reset_combobox=mock_reset_combo,
                                            reset_lineinput=mock_reset_input)
        testobj.oldtags = 'oldtags'
        testobj.newtag = 'newtag'
        testobj.refresh_fields()
        assert capsys.readouterr().out == (
                "called KeywordsManager._reset_combobox with args ('oldtags', {'key': 'words'})\n"
                "called KeywordsManager._reset_lineinput with args ('newtag',)\n")

    def test_remove_keyword(self, monkeypatch, capsys):
        """unittest for SetOptions.remove_keyword
        """
        def mock_get(arg):
            print(f'called KeywordsManager.get_combobox_value with arg {arg}')
            return 'oldvalue'
        def mock_ask(*args):
            print('called KeywordsManager.ask_question with args', args)
            return False
        def mock_ask_2(*args):
            print('called KeywordsManager.ask_question with args', args)
            return True
        def mock_update(arg):
            print(f'called DefineTags.update_items with arg {arg}')
        def mock_refresh():
            print('called DefineTags.refresh_fields')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(get_combobox_value=mock_get, ask_question=mock_ask)
        testobj.parent = types.SimpleNamespace(base=types.SimpleNamespace(
            app_title='xxx', opts={'Keywords': ['oldvalue']}))
        testobj.update_items = mock_update
        testobj.refresh_fields = mock_refresh
        testobj.oldtags = 'oldtags'
        testobj.remove_keyword()
        assert capsys.readouterr().out == (
                "called KeywordsManager.get_combobox_value with arg oldtags\n"
                "called KeywordsManager.ask_question with args"
                " (\'xxx\', \'About to remove keyword \"oldvalue\" - continue?\')\n")
        testobj.gui.ask_question = mock_ask_2
        testobj.remove_keyword()
        assert capsys.readouterr().out == (
                "called KeywordsManager.get_combobox_value with arg oldtags\n"
                "called KeywordsManager.ask_question with args"
                " (\'xxx\', \'About to remove keyword \"oldvalue\" - continue?\')\n"
                "called DefineTags.update_items with arg oldvalue\n"
                "called DefineTags.refresh_fields\n")

    def test_add_keyword(self, monkeypatch, capsys):
        """unittest for SetOptions.add_keyword
        """
        def mock_get(arg):
            print(f'called KeywordsManager.get_combobox_value with arg {arg}')
            return 'oldvalue'
        def mock_get_2(arg):
            print(f'called KeywordsManager.get_combobox_value with arg {arg}')
            return ''
        def mock_get_line(arg):
            print(f'called KeywordsManager.get_lineinput_text with arg {arg}')
            return 'newvalue'
        def mock_ask(*args):
            print('called KeywordsManager.ask_question with args', args)
            return False
        def mock_ask_2(*args):
            print('called KeywordsManager.ask_question with args', args)
            return True
        def mock_askc(*args):
            print('called KeywordsManager.ask_question_with_cancel with args', args)
            return False, True
        def mock_askc_2(*args):
            print('called KeywordsManager.ask_question_with_cancel with args', args)
            return True, True
        def mock_askc_3(*args):
            print('called KeywordsManager.ask_question_with_cancel with args', args)
            return False, False
        def mock_askc_4(*args):
            print('called KeywordsManager.ask_question_with_cancel with args', args)
            return True, False
        def mock_update(*args):
            print('called DefineTags.update_items with args', args)
        def mock_refresh():
            print('called DefineTags.refresh_fields')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(get_combobox_value=mock_get, ask_question=mock_ask,
                                            ask_question_w_cancel=mock_askc,
                                            get_lineinput_text=mock_get_line)
        testobj.parent = types.SimpleNamespace(base=types.SimpleNamespace(
            app_title='xxx', opts={'Keywords': ['oldvalue']}))
        testobj.update_items = mock_update
        testobj.refresh_fields = mock_refresh
        testobj.oldtags = 'oldtags'
        testobj.newtag = 'newtag'
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['oldvalue']}
        assert capsys.readouterr().out == (
                "called KeywordsManager.get_combobox_value with arg oldtags\n"
                "called KeywordsManager.get_lineinput_text with arg newtag\n"
                "called KeywordsManager.ask_question_with_cancel with args"
                " ('About to replace keyword \"oldvalue\" with \"newvalue\"',"
                " 'Also replace where used (if not, entries are removed)?')\n")
        testobj.parent.base.opts = {'Keywords': ['oldvalue']}
        testobj.gui.ask_question_w_cancel = mock_askc_2
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['oldvalue']}
        assert capsys.readouterr().out == (
                "called KeywordsManager.get_combobox_value with arg oldtags\n"
                "called KeywordsManager.get_lineinput_text with arg newtag\n"
                "called KeywordsManager.ask_question_with_cancel with args"
                " ('About to replace keyword \"oldvalue\" with \"newvalue\"',"
                " 'Also replace where used (if not, entries are removed)?')\n")
        testobj.parent.base.opts = {'Keywords': ['oldvalue']}
        testobj.gui.ask_question_w_cancel = mock_askc_3
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['newvalue']}
        assert capsys.readouterr().out == (
                "called KeywordsManager.get_combobox_value with arg oldtags\n"
                "called KeywordsManager.get_lineinput_text with arg newtag\n"
                "called KeywordsManager.ask_question_with_cancel with args"
                " ('About to replace keyword \"oldvalue\" with \"newvalue\"',"
                " 'Also replace where used (if not, entries are removed)?')\n"
                "called DefineTags.update_items with args ('oldvalue',)\n"
                "called DefineTags.refresh_fields\n")
        testobj.parent.base.opts = {'Keywords': ['oldvalue']}
        testobj.gui.ask_question_w_cancel = mock_askc_4
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['newvalue']}
        assert capsys.readouterr().out == (
                "called KeywordsManager.get_combobox_value with arg oldtags\n"
                "called KeywordsManager.get_lineinput_text with arg newtag\n"
                "called KeywordsManager.ask_question_with_cancel with args"
                " ('About to replace keyword \"oldvalue\" with \"newvalue\"',"
                " 'Also replace where used (if not, entries are removed)?')\n"
                "called DefineTags.update_items with args ('oldvalue', 'newvalue')\n"
                "called DefineTags.refresh_fields\n")
        testobj.parent.base.opts = {'Keywords': ['oldvalue']}
        testobj.gui.get_combobox_value = mock_get_2
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['oldvalue']}
        assert capsys.readouterr().out == (
                "called KeywordsManager.get_combobox_value with arg oldtags\n"
                "called KeywordsManager.get_lineinput_text with arg newtag\n"
                "called KeywordsManager.ask_question with args"
                " (\'xxx\', \'About to add new keyword \"newvalue\" - continue?\')\n"
                "called DefineTags.refresh_fields\n")
        testobj.parent.base.opts = {'Keywords': ['oldvalue']}
        testobj.gui.ask_question = mock_ask_2
        testobj.add_keyword()
        assert testobj.parent.base.opts == {'Keywords': ['oldvalue', 'newvalue']}
        assert capsys.readouterr().out == (
                "called KeywordsManager.get_combobox_value with arg oldtags\n"
                "called KeywordsManager.get_lineinput_text with arg newtag\n"
                "called KeywordsManager.ask_question with args"
                " (\'xxx\', \'About to add new keyword \"newvalue\" - continue?\')\n"
                "called DefineTags.refresh_fields\n")

    def test_update_items(self, monkeypatch, capsys):
        """unittest for SetOptions.update_items
        """
        def mock_getitems():
            print('called NoteTree.get_treeitems')
            return [], None
        def mock_getitems_2():
            print('called NoteTree.get_treeitems')
            return ['item1', 'item2', 'item3'], 'item2'
        def mock_getwords(arg):
            print(f"called NoteTree.get_item_keywords with arg '{arg}'")
            if arg == 'item1':
                return ['oldvalue', 'other_value']
            if arg == 'item2':
                return ['xxx']
            return []
        def mock_set(*args):
            print('called NoteTree.set_item_keywords with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(get_treeitems=mock_getitems,
                                               get_item_keywords=mock_getwords,
                                               set_item_keywords=mock_set)
        testobj.update_items('oldvalue')
        assert capsys.readouterr().out == "called NoteTree.get_treeitems\n"
        testobj.parent.get_treeitems = mock_getitems_2
        testobj.update_items('oldvalue')
        assert capsys.readouterr().out == (
            "called NoteTree.get_treeitems\n"
            "called NoteTree.get_item_keywords with arg 'item1'\n"
            "called NoteTree.set_item_keywords with args ('item1', ['other_value'])\n"
            "called NoteTree.get_item_keywords with arg 'item2'\n"
            "called NoteTree.set_item_keywords with args ('item2', ['xxx'])\n"
            "called NoteTree.get_item_keywords with arg 'item3'\n"
            "called NoteTree.set_item_keywords with args ('item3', [])\n")
        testobj.update_items('oldvalue', 'newvalue')
        assert capsys.readouterr().out == (
            "called NoteTree.get_treeitems\n"
            "called NoteTree.get_item_keywords with arg 'item1'\n"
            "called NoteTree.set_item_keywords with args ('item1', ['other_value', 'newvalue'])\n"
            "called NoteTree.get_item_keywords with arg 'item2'\n"
            "called NoteTree.set_item_keywords with args ('item2', ['xxx'])\n"
            "called NoteTree.get_item_keywords with arg 'item3'\n"
            "called NoteTree.set_item_keywords with args ('item3', [])\n")


class TestGetText:
    """unittests for testee.GetText
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for setting up GetText object
        """
        def mock_init(self, *args):
            """stub for GetText.__init__
            """
            print('called GetText.__init__ with args', args)
        monkeypatch.setattr(testee.GetText, "__init__", mock_init)
        testobj = testee.GetText("test")
        assert capsys.readouterr().out == "called GetText.__init__ with args ('test',)\n"
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for GetText.init
        """
        class MockGetTextDialog:
            def __init__(self, *args, **kwargs):
                print('called GetTextDialog.__init__ with args', args, kwargs)
            def add_label(self, text):
                print(f"called GetTextDialog.add_label with arg '{text}'")
            def add_lineinput(self, text):
                print(f"called GetTextDialog.add_lineinput with arg '{text}'")
                return 'text'
            def add_checkbox_line(self, arg):
                print(f"called GetTextDialog.add_checkbox_line with arg '{arg}'")
                return 'exclude', 'use case'
            def add_okcancel_buttonbox(self):
                print('called GetTextDialog.add_okcancel_buttonbox')
        monkeypatch.setattr(testee.gui, "GetTextDialog", MockGetTextDialog)
        parent = types.SimpleNamespace(base=types.SimpleNamespace(app_title='apptitle'))
        testobj = testee.GetText(parent, 0, 'xxx')
        assert testobj.parent == parent
        assert isinstance(testobj.gui, testee.gui.GetTextDialog)
        assert testobj.text == 'text'
        assert testobj.in_exclude == 'exclude'
        assert testobj.use_case == 'use case'
        assert capsys.readouterr().out == (
                "called GetTextDialog.__init__ with args"
                f" ({testobj}, {testobj.parent}, 'apptitle') {{}}\n"
                "called GetTextDialog.add_label with arg ''\n"
                "called GetTextDialog.add_lineinput with arg 'xxx'\n"
                "called GetTextDialog.add_checkbox_line with arg"
                " '[('exclude', False), ('case sensitive', False)]'\n"
                "called GetTextDialog.add_okcancel_buttonbox\n")
        testobj = testee.GetText(parent, -1, 'xxx', 'yyy', True)
        assert capsys.readouterr().out == (
                "called GetTextDialog.__init__ with args"
                f" ({testobj}, {testobj.parent}, 'apptitle') {{}}\n"
                "called GetTextDialog.add_label with arg 'yyy'\n"
                "called GetTextDialog.add_lineinput with arg 'xxx'\n"
                "called GetTextDialog.add_checkbox_line with arg"
                " '[('exclude', True), ('case sensitive', True)]'\n"
                "called GetTextDialog.add_okcancel_buttonbox\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SetOptions.confirm
        """
        def mock_get(arg):
            print(f'called KeywordsManager.get_checkbox_value with arg {arg}')
            return True
        def mock_get_line(arg):
            print(f'called KeywordsManager.get_lineinput_text with arg {arg}')
            return 'value'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get,
                                            get_lineinput_value=mock_get_line)
        testobj.in_exclude = 'in/ex'
        testobj.text = 'text'
        testobj.use_case = 'use'
        assert testobj.confirm() == [True, 'value', True]
        assert capsys.readouterr().out == (
                "called KeywordsManager.get_checkbox_value with arg in/ex\n"
                "called KeywordsManager.get_lineinput_text with arg text\n"
                "called KeywordsManager.get_checkbox_value with arg use\n")


class TestGetItem:
    """unittests for testee.GetItem
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for setting up GetItem object
        """
        def mock_init(self, *args):
            """stub for GetItem.__init__
            """
            print('called GetItem.__init__ with args', args)
        monkeypatch.setattr(testee.GetItem, "__init__", mock_init)
        testobj = testee.GetItem("test")
        assert capsys.readouterr().out == "called GetItem.__init__ with args ('test',)\n"
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for GetItem.init
        """
        class MockGetItemDialog:
            def __init__(self, *args, **kwargs):
                print('called GetItemDialog with args', args, kwargs)
            def add_label(self, text):
                print(f"called GetItemDialog.add_label with arg '{text}'")
            def add_checkbox(self, *args):
                print("called GetItemDialog.add_checkbox with args", args)
                return 'check'
            def add_combobox(self, *args):
                print("called GetItemDialog.add_combobox with args", args)
                return 'combo'
            def add_okcancel_buttonbox(self):
                print('called GetItemDialog.add_okcancel_buttonbox')
        monkeypatch.setattr(testee.gui, "GetItemDialog", MockGetItemDialog)
        parent = types.SimpleNamespace(base=types.SimpleNamespace(app_title='apptitle'))
        testobj = testee.GetItem(parent, 0, ['xxx'], 'yyy')
        assert testobj.parent == parent
        assert isinstance(testobj.gui, testee.gui.GetItemDialog)
        assert testobj.text == 'combo'
        assert testobj.in_exclude == 'check'
        assert capsys.readouterr().out == (
                "called GetItemDialog with args"
                f" ({testobj}, {testobj.parent}, 'apptitle') {{}}\n"
                "called GetItemDialog.add_label with arg ''\n"
                "called GetItemDialog.add_combobox with args (['xxx'], 'yyy')\n"
                "called GetItemDialog.add_checkbox with args ('exclude', False)\n"
                "called GetItemDialog.add_okcancel_buttonbox\n")
        testobj = testee.GetItem(parent, -1, ['xxx'], 'yyy', True)
        assert capsys.readouterr().out == (
                "called GetItemDialog with args"
                f" ({testobj}, {testobj.parent}, 'apptitle') {{}}\n"
                "called GetItemDialog.add_label with arg 'True'\n"
                "called GetItemDialog.add_combobox with args (['xxx'], 'yyy')\n"
                "called GetItemDialog.add_checkbox with args ('exclude', True)\n"
                "called GetItemDialog.add_okcancel_buttonbox\n")

    def test_confirm(self, monkeypatch, capsys):
        """unittest for SetOptions.confirm
        """
        def mock_get(arg):
            print(f'called KeywordsManager.get_checkbox_value with arg {arg}')
            return True
        def mock_getc(arg):
            print(f'called KeywordsManager.get_combobox_value with arg {arg}')
            return 'xxxx'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui = types.SimpleNamespace(get_checkbox_value=mock_get,
                                            get_combobox_value=mock_getc)
        testobj.in_exclude = 'in/ex'
        testobj.text = 'text'
        assert testobj.confirm() == [True, 'xxxx']
        assert capsys.readouterr().out == (
                "called KeywordsManager.get_checkbox_value with arg in/ex\n"
                "called KeywordsManager.get_combobox_value with arg text\n")


class TestKeyHelp:
    """unittests for testee.KeyHelp
    """
    def test_init(self, monkeypatch, capsys):
        """unittest for KeyHelp.init
        """
        def mock_init(self, *args):
            """stub for Dialog.__init__
            """
            print('called Dialog.__init__ with args', args)
        class MockGridDialog:
            def __init__(self, *args, **kwargs):
                print('called GridDialog with args', args, kwargs)
            def add_label(self, *args):
                print('called GridDialog.add_label with args', args)
        monkeypatch.setattr(testee.gui, "GridDialog", MockGridDialog)
        testobj = testee.KeyHelp("test", "title", [])
        assert isinstance(testobj.gui, testee.gui.GridDialog)
        assert capsys.readouterr().out == (
                "called GridDialog with args ('test', 'title', 'Done') {}\n")
        testobj = testee.KeyHelp("test", "title", [('a', 'b'), ('x', 'y')])
        assert isinstance(testobj.gui, testee.gui.GridDialog)
        assert capsys.readouterr().out == (
                "called GridDialog with args ('test', 'title', 'Done') {}\n"
                "called GridDialog.add_label with args (0, 0, 'a')\n"
                "called GridDialog.add_label with args (0, 1, 'b')\n"
                "called GridDialog.add_label with args (1, 0, 'x')\n"
                "called GridDialog.add_label with args (1, 1, 'y')\n")
