"""unittests for main.py
"""
import os

# import gettext
import pytest
import notetree.main as main

# HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# gettext.install("NoteTree", os.path.join(HERE, 'locale'))


def setup_notetree_class(monkeypatch):
    monkeypatch.setattr(main.NoteTree, "__init__", mock_init)
    return main.NoteTree("test")


def mock_init(self, filename):
    self.app_title = "mock_app"
    self.root_title = "mock_root"
    self.languages = main.languages  # {'en': 'en_translation'}
    self.sett2text = main.sett2text
    self.project_file = filename
    self.gui = MockMainWindow(self)


class MockLanguage:
    def __init__(self, lang):
        self.lang = lang

    def install(self):
        print("called language.install for language `{}`".format(self.lang))


class MockMainWindow:
    """method arguments are not used but we need to include them to properly mimic the original
    class"""

    def __init__(self, root):
        print("called mainwindow.__init__()")

    def start(self):
        print("called mainwindow.start()")

    def init_screen(self, title, iconame):
        print("called mainwindow.init_screen()")

    def setup_statusbar(self):
        print("called mainwindow.setup_statusbar()")

    def setup_trayicon(self):
        print("called mainwindow.setup_trayicon()")

    def setup_split_screen(self):
        print("called mainwindow.setup_split_screen()")

    def setup_tree(self):
        print("called mainwindow.setup_tree()")

    def setup_editor(self):
        print("called mainwindow.setup_editor()")

    def create_menu(self):
        print("called mainwindow.create_menu()")

    def changeselection(self):
        print("called mainwindow.changeselection()")

    def close(self):
        print("called mainwindow.close()")

    def clear_editor(self):
        print("called mainwindow.clear_editor()")

    def open_editor(self):
        print("called mainwindow.open_editor()")

    def set_screen(self, screensize):
        print("called mainwindow.set_screen()")

    def set_splitter(self, split):
        print("called mainwindow.set_splitter()")

    def create_root(self, title):
        print("called mainwindow.create_root()")
        return "fake_root"

    def set_item_expanded(self, item):
        print("called mainwindow.set_item_expanded()")

    def emphasize_activeitem(self, value):
        print("called mainwindow.emphasize_activeitem()")

    def editor_text_was_changed(self):
        print("called mainwindow.editor_text_was_changed()")

    def copy_text_from_editor_to_activeitem(self):
        print("called mainwindow.copy_text_from_editor_to_activeitem()")

    def copy_text_from_activeitem_to_editor(self):
        print("called mainwindow.copy_text_from_activeitem_to_editor()")

    def select_item(self, item):
        print("called mainwindow.select_item()")

    def get_selected_item(self):
        print("called mainwindow.get_selected_item()")

    def remove_item_from_tree(self, item):
        print("called mainwindow.remove_item_from_tree()")

    def get_key_from_item(self, item):
        print("called mainwindow.get_key_from_item()")
        return "x"

    def get_activeitem_title(self):
        print("called mainwindow.get_activeitem_title()")

    def set_activeitem_title(self, text):
        print("called mainwindow.set_activeitem_title()")

    def set_focus_to_tree(self):
        print("called mainwindow.set_focus_to_tree()")

    def set_focus_to_editor(self):
        print("called mainwindow.set_focus_to_editor()")

    def add_item_to_tree(self, key, tag, text, keywords):  # , revorder):
        print("called mainwindow.add_item_to_tree()")

    def get_treeitems(self):
        print("called mainwindow.get_treeitems()")
        return [], 0

    def get_screensize(self):
        print("called mainwindow.get_screensize()")

    def get_splitterpos(self):
        print("called mainwindow.get_splitterpos()")

    def sleep(self):
        print("called mainwindow.sleep()")

    def revive(self, event=None):
        print("called mainwindow.revive()")

    def get_next_item(self):
        print("called mainwindow.get_next_item()")

    def get_prev_item(self):
        print("called mainwindow.get_prev_item()")

    def get_itempos(self, item):
        print("called mainwindow.get_itempos()")

    def get_itemcount(self):
        print("called mainwindow.get_itemcount()")

    def get_item_at_pos(self, pos):
        print("called mainwindow.get_item_at_pos()")

    def get_rootitem_title(self):
        print("called mainwindow.get_rootitem_title()")

    def set_rootitem_title(self, text):
        print("called mainwindow.set_rootitem_title()")

    def get_item_text(self, item):
        print("called mainwindow.get_item_text()")

    def set_editor_text(self, text):
        print("called mainwindow.set_editor_text()")

    def get_editor_text(self):
        print("called mainwindow.get_editor_text()")

    def set_item_text(self, item, text):
        print("called mainwindow.set_item_text()")

    def get_item_keywords(self, item):
        print("called mainwindow.get_item_keywords()")

    def set_item_keywords(self, item, keyword_list):
        print("called mainwindow.set_item_keywords()")

    def show_statusbar_message(self, text):
        print("called mainwindow.show_statusbar_message()")

    def enable_selaction(self, actiontext):
        print("called mainwindow.enable_selaction()")

    def disable_selaction(self, actiontext):
        print("called mainwindow.disable_selaction()")

    def showmsg(self, message):
        print("called mainwindow.showmsg()")

    def ask_question(self, question):
        print("called mainwindow.ask_question()")

    def show_dialog(self, cls, *args):
        print("called mainwindow.show_dialog()")
        return "", False  # simuleer default: afgebroken

    def get_text_from_user(self, prompt, default):
        print("called mainwindow.get_text_from_user()")
        return "", False  # simuleer default: afgebroken

    def get_choice_from_user(self, prompt, choices, choice=0):
        print("called mainwindow.get_choice_from_user()")
        return "", False  # simuleer default: afgebroken


class TestNoteTree:
    def test_init(self, monkeypatch, capsys):
        def mock_define_screen(*args):
            print("called define_screen()")

        def mock_open(self, **kwargs):
            arg = "first_time" if kwargs.get("first_time", None) else "not first"
            print("called open(`{}`)".format(arg))

        def mock_open_err(self, **kwargs):
            arg = "first_time" if kwargs.get("first_time", None) else "not first"
            print("called open(`{}`)".format(arg))
            return "error"

        monkeypatch.setattr(main.gui, "MainWindow", MockMainWindow)
        # import pdb; pdb.set_trace()
        monkeypatch.setattr(main.NoteTree, "define_screen", mock_define_screen)
        monkeypatch.setattr(main.NoteTree, "open", mock_open)
        testsubj = main.NoteTree("test")
        assert testsubj.app_title == main.app_title
        assert testsubj.root_title == main.root_title
        assert testsubj.languages == main.languages
        assert testsubj.sett2text == main.sett2text
        assert testsubj.project_file == "test"
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called define_screen()\n"
            "called open(`first_time`)\n"
            "called mainwindow.start()\n"
        )
        monkeypatch.setattr(main.NoteTree, "define_screen", mock_define_screen)
        monkeypatch.setattr(main.NoteTree, "open", mock_open_err)
        testsubj = main.NoteTree("test")
        assert testsubj.app_title == main.app_title
        assert testsubj.root_title == main.root_title
        assert testsubj.languages == main.languages
        assert testsubj.sett2text == main.sett2text
        assert testsubj.project_file == "test"
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called define_screen()\n"
            "called open(`first_time`)\n"
            "called mainwindow.showmsg()\n"
            "called mainwindow.close()\n"
        )

    def test_define_screen(self, monkeypatch, capsys):
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.define_screen()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.init_screen()\n"
            "called mainwindow.setup_statusbar()\n"
            "called mainwindow.setup_trayicon()\n"
            "called mainwindow.setup_split_screen()\n"
        )

    def test_get_menudata(self, monkeypatch, capsys):
        testsubj = setup_notetree_class(monkeypatch)
        assert testsubj.get_menudata() is not None  # geen logica; inhoud niet zo interessant

    def test_reread(self, monkeypatch, capsys):
        def mock_ask_question(*args):
            print("called mainwindow.ask_question()")
            return True

        def mock_open(*args):
            print("called self.open()")

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.reread()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.ask_question()\n"
        )
        monkeypatch.setattr(MockMainWindow, "ask_question", mock_ask_question)
        monkeypatch.setattr(main.NoteTree, "open", mock_open)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.reread()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.ask_question()\n"
            "called self.open()\n"
        )

    def test_save_from_menu(self, monkeypatch, capsys):
        def mock_update(force_save):
            print(f"called update() with arg {force_save}")
        testsubj = setup_notetree_class(monkeypatch)
        assert capsys.readouterr().out == "called mainwindow.__init__()\n"
        monkeypatch.setattr(testsubj, "update", mock_update)
        testsubj.save_from_menu()
        assert capsys.readouterr().out == 'called update() with arg True\n'

    def test_update(self, monkeypatch, capsys):
        def mock_tree_to_dict(*args):
            print("called tree_to_dict()")
        def mock_tree_to_dict_2(self):
            print("called tree_to_dict()")
            self.nt_data = {'not': 'empty'}
        def mock_save(*args):
            print("called save()")
        testsubj = setup_notetree_class(monkeypatch)
        assert capsys.readouterr().out == "called mainwindow.__init__()\n"
        monkeypatch.setattr(testsubj, "tree_to_dict", mock_tree_to_dict)
        monkeypatch.setattr(testsubj, "save", mock_save)
        testsubj.nt_data = {}
        testsubj.old_nt_data = {}
        testsubj.opts = {}
        testsubj.update()
        assert "ScreenSize" in testsubj.opts
        assert "SashPosition" in testsubj.opts
        assert capsys.readouterr().out == (
            "called tree_to_dict()\n"
            "called mainwindow.get_screensize()\n"
            "called mainwindow.get_splitterpos()\n")
        testsubj.nt_data = {}
        testsubj.old_nt_data = {}
        testsubj.opts = {}
        testsubj.update(force_save=True)
        assert "ScreenSize" in testsubj.opts
        assert "SashPosition" in testsubj.opts
        assert capsys.readouterr().out == (
            "called tree_to_dict()\n"
            "called mainwindow.get_screensize()\n"
            "called mainwindow.get_splitterpos()\n"
            "called save()\n")
        monkeypatch.setattr(main.NoteTree, "__init__", mock_init)
        monkeypatch.setattr(main.NoteTree, "tree_to_dict", mock_tree_to_dict_2)
        testsubj = main.NoteTree("test")
        monkeypatch.setattr(testsubj, "save", mock_save)
        testsubj.nt_data = {}
        testsubj.old_nt_data = {}
        testsubj.opts = {}
        testsubj.update()
        assert "ScreenSize" in testsubj.opts
        assert "SashPosition" in testsubj.opts
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called tree_to_dict()\n"
            "called mainwindow.get_screensize()\n"
            "called mainwindow.get_splitterpos()\n"
            "called save()\n")

    def test_rename(self, monkeypatch, capsys):
        def mock_get_text_from_user(*args):
            print("called mainwindow.get_text_from_user()")
            return "Hallo", True

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.rename()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_rootitem_title()\n"
            "called mainwindow.get_text_from_user()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        monkeypatch.setattr(MockMainWindow, "get_text_from_user", mock_get_text_from_user)
        testsubj.opts = {}
        testsubj.rename()
        assert testsubj.opts["RootTitle"] == "Hallo"
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_rootitem_title()\n"
            "called mainwindow.get_text_from_user()\n"
            "called mainwindow.set_rootitem_title()\n"
        )

    def test_manage_keywords(self, monkeypatch, capsys):
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.manage_keywords()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
        )

    def test_hide_me(self, monkeypatch, capsys):
        def mock_show_dialog(*args):
            print("called mainwindow.show_dialog()")
            return True, False

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"AskBeforeHide": False}
        testsubj.hide_me()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.sleep()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"AskBeforeHide": True}
        testsubj.hide_me()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
            "called mainwindow.sleep()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"AskBeforeHide": True}
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog)
        testsubj.hide_me()
        assert not testsubj.opts["AskBeforeHide"]
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
            "called mainwindow.sleep()\n"
        )

    def test_choose_language(self, monkeypatch, capsys):
        def mock_get_choice_from_user(*args):
            print("called mainwindow.get_choice_from_user()")
            # return 'English', True
            return "t_en", True

        def mock_gettext(*args):
            text = args[0]
            print("called gettext('{}')".format(text))
            return text

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Language": "nl"}
        testsubj.choose_language()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_choice_from_user()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Language": "nl"}
        testsubj.languages = {"en": MockLanguage("en"), "nl": MockLanguage("nl")}
        monkeypatch.setattr(MockMainWindow, "get_choice_from_user", mock_get_choice_from_user)
        testsubj.choose_language()
        assert testsubj.opts["Language"] == "en"
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_choice_from_user()\n"
            "called language.install for language `en`\n"
            "called mainwindow.create_menu()\n"
        )

    def test_set_options(self, monkeypatch, capsys):
        def mock_show_dialog(*args):
            print("called mainwindow.show_dialog()")
            return True, {
                "option_1_text": True,
                "option_2_text": True,
                "option_3_text": False,
                "option_4_text": False,
            }

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"option_1": True, "option_2": False, "option_3": True, "option_4": False}
        testsubj.sett2text = {
            "option_1": "option_1_text",
            "option_2": "option_2_text",
            "option_3": "option_3_text",
            "option_4": "option_4_text",
        }
        testsubj.set_options()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"option_1": True, "option_2": False, "option_3": True, "option_4": False}
        testsubj.sett2text = {
            "option_1": "option_1_text",
            "option_2": "option_2_text",
            "option_3": "option_3_text",
            "option_4": "option_4_text",
        }
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog)
        testsubj.set_options()
        assert testsubj.opts == {
            "option_1": True,
            "option_2": True,
            "option_3": False,
            "option_4": False,
        }
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n" "called mainwindow.show_dialog()\n"
        )

    def test_new_item(self, monkeypatch, capsys):
        def mock_get_text_from_user(*args):
            print("called mainwindow.get_text_from_user()")
            return "Hallo", True

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.nt_data = {}
        testsubj.new_item()
        assert testsubj.nt_data == {}
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n" "called mainwindow.get_text_from_user()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.nt_data = {}
        monkeypatch.setattr(MockMainWindow, "get_text_from_user", mock_get_text_from_user)
        testsubj.gui.root = "x"
        testsubj.new_item()
        assert list(testsubj.nt_data.values()) == [""]
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_text_from_user()\n"
            "called mainwindow.add_item_to_tree()\n"
            "called mainwindow.select_item()\n"
            "called mainwindow.set_item_expanded()\n"
            "called mainwindow.open_editor()\n"
            "called mainwindow.set_focus_to_editor()\n"
        )

    def test_delete_item(self, monkeypatch, capsys):
        def mock_get_selected_item(self, *args):
            print("called mainwindow.get_selected_item()")
            return self.root

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.nt_data = {"x": "y"}
        testsubj.gui.root = "q"
        testsubj.delete_item()
        assert "x" not in testsubj.nt_data
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_selected_item()\n"
            "called mainwindow.get_key_from_item()\n"
            "called mainwindow.remove_item_from_tree()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.nt_data = {"x": "y"}
        testsubj.gui.root = "q"
        monkeypatch.setattr(MockMainWindow, "get_selected_item", mock_get_selected_item)
        testsubj.delete_item()
        assert "x" in testsubj.nt_data  # not deleted
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_selected_item()\n"
            "called mainwindow.showmsg()\n"
        )

    def test_ask_title(self, monkeypatch, capsys):
        def mock_get_text_from_user(*args):
            print("called mainwindow.get_text_from_user()")
            return "Hallo", True

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.ask_title()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_activeitem_title()\n"
            "called mainwindow.get_text_from_user()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        monkeypatch.setattr(MockMainWindow, "get_text_from_user", mock_get_text_from_user)
        testsubj.opts = {}
        testsubj.ask_title()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_activeitem_title()\n"
            "called mainwindow.get_text_from_user()\n"
            "called mainwindow.set_activeitem_title()\n"
        )

    def test_link_keywords(self, monkeypatch, capsys):
        def mock_get_item_keywords(self, item):
            print("called mainwindow.get_item_keywords()")
            return ["kw1", "kw2"]

        def mock_show_dialog(*args):
            print("called mainwindow.show_dialog()")
            return True, ["kw1", "kw3"]

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.activeitem = None
        testsubj.link_keywords()
        assert capsys.readouterr().out == ("called mainwindow.__init__()\n")
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.activeitem = "x"
        testsubj.link_keywords()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_item_keywords()\n"
        )
        monkeypatch.setattr(MockMainWindow, "get_item_keywords", mock_get_item_keywords)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.activeitem = "x"
        testsubj.link_keywords()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_item_keywords()\n"
            "called mainwindow.show_dialog()\n"
        )
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.activeitem = "x"
        testsubj.link_keywords()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_item_keywords()\n"
            "called mainwindow.show_dialog()\n"
            "called mainwindow.set_item_keywords()\n"
        )

    def test_goto_next_note(self, monkeypatch, capsys):
        def mock_get_next_item(*args):
            print("called mainwindow.get_next_item()")
            return "x"

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.goto_next_note()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_next_item()\n"
            "called mainwindow.showmsg()\n"
        )
        monkeypatch.setattr(MockMainWindow, "get_next_item", mock_get_next_item)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.goto_next_note()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_next_item()\n"
            "called mainwindow.select_item()\n"
        )

    def test_goto_prev_note(self, monkeypatch, capsys):
        def mock_get_prev_item(*args):
            print("called mainwindow.get_prev_item()")
            return "y"

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.goto_prev_note()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_prev_item()\n"
            "called mainwindow.showmsg()\n"
        )
        monkeypatch.setattr(MockMainWindow, "get_prev_item", mock_get_prev_item)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.goto_prev_note()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.get_prev_item()\n"
            "called mainwindow.select_item()\n"
        )

    def test_reverse(self, monkeypatch, capsys):
        def mock_build_tree(*args):
            print("called self.build_tree()")

        monkeypatch.setattr(main.NoteTree, "build_tree", mock_build_tree)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"RevOrder": False}
        testsubj.gui.root = "x"
        testsubj.reverse()
        assert testsubj.opts["RevOrder"]
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called self.build_tree()\n"
            "called mainwindow.select_item()\n"
            "called mainwindow.set_item_expanded()\n"
            "called mainwindow.open_editor()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"RevOrder": True}
        testsubj.gui.root = "x"
        testsubj.reverse()
        assert not testsubj.opts["RevOrder"]
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called self.build_tree()\n"
            "called mainwindow.select_item()\n"
            "called mainwindow.set_item_expanded()\n"
            "called mainwindow.open_editor()\n"
        )

    def test_no_selection(self, monkeypatch, capsys):
        def mock_set_selection(*args):
            print("called self.set_selection()")

        monkeypatch.setattr(main.NoteTree, "set_selection", mock_set_selection)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.no_selection()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called self.set_selection()\n"
            "called mainwindow.show_statusbar_message()\n"
        )

    def test_keyword_select(self, monkeypatch, capsys):
        def mock_set_option(*args):
            print("called self.set_option()")

        def mock_set_selection(self, *args):
            seltype, text = args[0]
            print("called self.set_selection() seltype is {}, tekst is `{}`".format(seltype, text))

        def mock_show_dialog(*args):
            print("called mainwindow.show_dialog()")
            return True, (False, "for_real")

        def mock_show_dialog_2(*args):
            print("called mainwindow.show_dialog()")
            return True, (True, "test")

        monkeypatch.setattr(main.NoteTree, "set_option", mock_set_option)
        monkeypatch.setattr(main.NoteTree, "set_selection", mock_set_selection)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Keywords": []}
        testsubj.keyword_select()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.showmsg()\n"
            "called self.set_option()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Keywords": ["test", "for_real"], "Selection": [0, ""]}
        testsubj.keyword_select()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
            "called self.set_option()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Keywords": ["test", "for_real"], "Selection": [1, "x"]}  # kan dit wel?
        testsubj.keyword_select()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
            "called self.set_option()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Keywords": ["test", "for_real"], "Selection": [-1, "test"]}
        testsubj.keyword_select()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
            "called self.set_option()\n"
        )
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Keywords": ["test", "for_real"], "Selection": [-1, "test"]}
        testsubj.keyword_select()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
            "called self.set_selection() seltype is 1, tekst is"
            " `for_real`\n"
            "called mainwindow.show_statusbar_message()\n"
        )
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog_2)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Keywords": ["test", "for_real"], "Selection": [-1, "test"]}
        testsubj.keyword_select()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
            "called self.set_selection() seltype is -1, tekst is"
            " `test`\n"
            "called mainwindow.show_statusbar_message()\n"
        )

    def test_text_select(self, monkeypatch, capsys):
        def mock_set_option(*args):
            print("called self.set_option()")

        def mock_set_selection(self, *args):
            seltype, text, use_case = args[0]
            print(
                "called self.set_selection() seltype is {}, tekst is `{}`,"
                " use_case is {}".format(seltype, text, use_case)
            )

        def mock_show_dialog(*args):
            print("called mainwindow.show_dialog()")
            return True, (False, "for_real", True)

        def mock_show_dialog_2(*args):
            print("called mainwindow.show_dialog()")
            return True, (True, "test", False)

        monkeypatch.setattr(main.NoteTree, "set_option", mock_set_option)
        monkeypatch.setattr(main.NoteTree, "set_selection", mock_set_selection)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Selection": [0, ""]}
        testsubj.text_select()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
            "called self.set_option()\n"
        )
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Selection": [2, "zoek", False]}
        testsubj.text_select()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
            "called self.set_selection() seltype is 2,"
            " tekst is `for_real`, use_case is True\n"
            "called mainwindow.show_statusbar_message()\n"
        )
        monkeypatch.setattr(MockMainWindow, "show_dialog", mock_show_dialog_2)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Selection": [-2, "zoek", False]}
        testsubj.text_select()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
            "called self.set_selection() seltype is -2,"
            " tekst is `test`, use_case is False\n"
            "called mainwindow.show_statusbar_message()\n"
        )

    def test_info_page(self, monkeypatch, capsys):
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.info_page()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.showmsg()\n"
        )

    def test_help_page(self, monkeypatch, capsys):
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.help_page()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.show_dialog()\n"
        )

    def test_open(self, monkeypatch, capsys):
        def mock_load_file(*args):
            print("called dml.load_file()")
            return {0: main.initial_opts}

        def mock_load_file_2(*args):
            print("called dml.load_file()")
            data = main.initial_opts
            data["NotifyOnLoad"] = False
            data["SashPosition"] = (180, 600)
            return {0: data}

        def mock_load_file_empty(*args):
            print("called dml.load_file()")
            return {}

        def mock_load_file_error(*args):
            print("called dml.load_file()")
            raise EOFError("{} not found")

        def mock_ask_question(*args):
            print("called mainwindow.ask_question()")
            return True

        def mock_build_tree(*args, **kwargs):
            print("called self.build_tree()")

        def mock_set_splitter(*args):
            print("called mainwindow.set_splitter()")
            raise TypeError

        monkeypatch.setattr(main.dml, "load_file", mock_load_file_error)
        main.gui.toolkit = "aa"
        testsubj = setup_notetree_class(monkeypatch)
        assert testsubj.open() == "test not found"
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called dml.load_file()\n"
        )
        monkeypatch.setattr(main.dml, "load_file", mock_load_file_empty)
        testsubj = setup_notetree_class(monkeypatch)
        # import pdb; pdb.set_trace()
        # assert testsubj.open() == 'File not found'
        assert testsubj.open() == "404_message"
        for opt in main.initial_opts:
            if opt == "Version":
                assert testsubj.opts[opt] == "Aa"
            elif opt == "RootTitle":
                assert testsubj.opts[opt] == "mock_root"
            else:
                assert testsubj.opts[opt] == main.initial_opts[opt]
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called dml.load_file()\n"
            "called mainwindow.ask_question()\n"
        )
        monkeypatch.setattr(MockMainWindow, "ask_question", mock_ask_question)
        monkeypatch.setattr(main.NoteTree, "build_tree", mock_build_tree)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.root = "x"
        testsubj.open()
        assert testsubj.opts["SashPosition"] == (180, 620)
        assert testsubj.nt_data == testsubj.old_nt_data
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called dml.load_file()\n"
            "called mainwindow.ask_question()\n"
            "called mainwindow.create_menu()\n"
            "called mainwindow.set_screen()\n"
            "called mainwindow.set_splitter()\n"
            "called mainwindow.clear_editor()\n"
            "called self.build_tree()\n"
            "called mainwindow.select_item()\n"
            "called mainwindow.set_item_expanded()\n"
            "called mainwindow.open_editor()\n"
            "called mainwindow.showmsg()\n"
            "called mainwindow.set_focus_to_tree()\n"
        )
        monkeypatch.setattr(main.dml, "load_file", mock_load_file)
        monkeypatch.setattr(MockMainWindow, "set_splitter", mock_set_splitter)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.root = "x"
        testsubj.open()
        assert testsubj.nt_data == testsubj.old_nt_data
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called dml.load_file()\n"
            "called mainwindow.create_menu()\n"
            "called mainwindow.set_screen()\n"
            "called mainwindow.set_splitter()\n"
            "called mainwindow.showmsg()\n"
            "called mainwindow.clear_editor()\n"
            "called self.build_tree()\n"
            "called mainwindow.select_item()\n"
            "called mainwindow.set_item_expanded()\n"
            "called mainwindow.open_editor()\n"
            "called mainwindow.showmsg()\n"
            "called mainwindow.set_focus_to_tree()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.root = "x"
        testsubj.open(first_time=True)
        assert testsubj.nt_data == testsubj.old_nt_data
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called dml.load_file()\n"
            "called mainwindow.create_menu()\n"
            "called mainwindow.set_screen()\n"
            "called mainwindow.set_splitter()\n"
            "called mainwindow.showmsg()\n"
            "called mainwindow.clear_editor()\n"
            "called self.build_tree()\n"
            "called mainwindow.select_item()\n"
            "called mainwindow.set_item_expanded()\n"
            "called mainwindow.open_editor()\n"
            "called mainwindow.set_focus_to_tree()\n"
        )
        monkeypatch.setattr(main.dml, "load_file", mock_load_file_2)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.root = "x"
        testsubj.open()
        assert testsubj.nt_data == testsubj.old_nt_data
        data = main.initial_opts
        data["NotifyOnLoad"] = False
        data["SashPosition"] = (180, 600)
        assert testsubj.opts == data
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called dml.load_file()\n"
            "called mainwindow.create_menu()\n"
            "called mainwindow.set_screen()\n"
            "called mainwindow.set_splitter()\n"
            "called mainwindow.showmsg()\n"
            "called mainwindow.clear_editor()\n"
            "called self.build_tree()\n"
            "called mainwindow.select_item()\n"
            "called mainwindow.set_item_expanded()\n"
            "called mainwindow.open_editor()\n"
            "called mainwindow.set_focus_to_tree()\n"
        )

    def test_build_tree(self, monkeypatch, capsys):
        def mock_tree_to_dict(*args):
            print("called self.tree_to_dict()")

        def mock_add_item_to_tree(self, key, tag, text, keywords):  # , revorder):
            print(
                "called mainwindow.add_item_to_tree(): `{}` ->"
                " (`{}`, `{}`, `{}`)".format(key, tag, text, keywords)
            )
            return key

        def mock_selection_contains_item(*args):
            return True

        def mock_selection_contains_item_no(*args):
            return False

        monkeypatch.setattr(main.NoteTree, "tree_to_dict", mock_tree_to_dict)
        monkeypatch.setattr(main.NoteTree, "selection_contains_item", mock_selection_contains_item)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"RootTitle": "text", "Selection": (0, "", True)}
        testsubj.nt_data = {}
        assert testsubj.build_tree() == "fake_root"
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called self.tree_to_dict()\n"
            "called mainwindow.create_root()\n"
        )
        monkeypatch.setattr(MockMainWindow, "add_item_to_tree", mock_add_item_to_tree)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"RootTitle": "text", "Selection": (0, ""), "ActiveItem": "1"}
        testsubj.nt_data = {
            0: "x",
            "0": ("0", "nul", ["x"]),
            "1": ("1", "een", ["x", "y"]),
            "2": ("3", "drie"),
        }
        assert testsubj.build_tree(first_time=True) == "1"
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.create_root()\n"
            "called mainwindow.add_item_to_tree(): `0` -> (`0`, `nul`, `['x']`)\n"
            "called mainwindow.add_item_to_tree(): `1` -> (`1`, `een`, `['x', 'y']`)\n"
            "called mainwindow.add_item_to_tree(): `2` -> (`3`, `drie`, `[]`)\n"
        )
        monkeypatch.setattr(
            main.NoteTree, "selection_contains_item", mock_selection_contains_item_no
        )
        monkeypatch.setattr(MockMainWindow, "add_item_to_tree", mock_add_item_to_tree)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"RootTitle": "text", "Selection": (0, ""), "ActiveItem": "1"}
        testsubj.nt_data = {
            0: "x",
            "0": ("0", "nul", ["x"]),
            "1": ("1", "een", ["x", "y"]),
            "2": ("3", "drie"),
        }
        assert testsubj.build_tree(first_time=True) == "fake_root"
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.create_root()\n"
        )

    def test_check_active(self, monkeypatch, capsys):
        def mock_editor_text_was_changed(*args):
            print("called mainwindow.editor_text_was_changed()")
            return True

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.root = "x"
        testsubj.gui.activeitem = None
        testsubj.check_active()
        assert capsys.readouterr().out == ("called mainwindow.__init__()\n")
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.root = "x"
        testsubj.gui.activeitem = "x"
        testsubj.check_active()
        assert capsys.readouterr().out == ("called mainwindow.__init__()\n")
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.root = "x"
        testsubj.gui.activeitem = "y"
        testsubj.check_active()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.emphasize_activeitem()\n"
            "called mainwindow.editor_text_was_changed()\n"
        )
        monkeypatch.setattr(MockMainWindow, "editor_text_was_changed", mock_editor_text_was_changed)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.root = "x"
        testsubj.gui.activeitem = "y"
        testsubj.check_active()
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.emphasize_activeitem()\n"
            "called mainwindow.editor_text_was_changed()\n"
            "called mainwindow.copy_text_from_editor_to_activeitem()"
            "\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.root = "x"
        testsubj.gui.activeitem = "y"
        testsubj.check_active("oops")
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.emphasize_activeitem()\n"
            "called mainwindow.editor_text_was_changed()\n"
            "called mainwindow.showmsg()\n"
            "called mainwindow.copy_text_from_editor_to_activeitem()"
            "\n"
        )

    def test_activate_item(self, monkeypatch, capsys):
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.activate_item(None)
        assert capsys.readouterr().out == ("called mainwindow.__init__()\n")
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.root = "x"
        testsubj.activate_item("x")
        assert testsubj.gui.activeitem == "x"
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.clear_editor()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.gui.root = "x"
        testsubj.activate_item("y")
        assert testsubj.gui.activeitem == "y"
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.clear_editor()\n"
            "called mainwindow.emphasize_activeitem()\n"
            "called mainwindow.copy_text_from_activeitem_to_editor()"
            "\ncalled mainwindow.open_editor()\n"
        )

    def test_tree_to_dict(self, monkeypatch, capsys):
        def mock_check_active(*args):
            print("called self.check_active()")

        def mock_get_treeitems(*args):
            print("called mainwindow.get_treeitems()")
            return [(1, "x", "y", ["z"]), (2, "a", "b", [])], "q"

        monkeypatch.setattr(main.NoteTree, "check_active", mock_check_active)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {}
        testsubj.nt_data = {}
        testsubj.tree_to_dict()
        assert testsubj.opts["ActiveItem"] == 0
        assert testsubj.nt_data == {}
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called self.check_active()\n"
            "called mainwindow.get_treeitems()\n"
        )
        monkeypatch.setattr(MockMainWindow, "get_treeitems", mock_get_treeitems)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {}
        testsubj.nt_data = {}
        testsubj.tree_to_dict()
        assert testsubj.opts["ActiveItem"] == "q"
        assert testsubj.nt_data == {1: ("x", "y", ["z"]), 2: ("a", "b", [])}
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called self.check_active()\n"
            "called mainwindow.get_treeitems()\n"
        )

    def test_save(self, monkeypatch, capsys):
        def mock_copyfile(*args):
            print("called shutil.copyfile(`{}`, `{}`)".format(args[0], args[1]))

        def mock_copyfile_error(*args):
            print("called shutil.copyfile()")
            raise FileNotFoundError

        def mock_save_file(*args):
            print("called dml.save_file()")

        testsubj = setup_notetree_class(monkeypatch)
        testsubj.project_file = ""
        testsubj.save()
        assert capsys.readouterr().out == ("called mainwindow.__init__()\n")
        monkeypatch.setattr(main.shutil, "copyfile", mock_copyfile_error)
        monkeypatch.setattr(main.dml, "save_file", mock_save_file)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.project_file = "x"
        testsubj.opts = {"NotifyOnSave": True}
        testsubj.nt_data = {0: "r*x", "x": "y"}
        testsubj.save()
        assert testsubj.nt_data == {0: {"NotifyOnSave": True}, "x": "y"}
        assert testsubj.old_nt_data == testsubj.nt_data
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called shutil.copyfile()\n"
            "called dml.save_file()\n"
            "called mainwindow.showmsg()\n"
        )
        monkeypatch.setattr(main.shutil, "copyfile", mock_copyfile)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.project_file = "x"
        testsubj.opts = {"NotifyOnSave": False}
        testsubj.nt_data = {0: "r*x", "x": "y"}
        testsubj.save()
        assert testsubj.nt_data == {0: {"NotifyOnSave": False}, "x": "y"}
        assert testsubj.old_nt_data == testsubj.nt_data
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called shutil.copyfile(`x`, `x~`)\n"
            "called dml.save_file()\n"
        )

    def test_set_selection(self, monkeypatch, capsys):
        def mock_build_tree(*args):
            print("called self.build_tree")

        monkeypatch.setattr(main.NoteTree, "build_tree", mock_build_tree)
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {}
        testsubj.gui.root = "yx"
        testsubj.set_selection("x", "Select &All")
        assert testsubj.opts["Selection"] == "x"
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called self.build_tree\n"
            "called mainwindow.select_item()\n"
            "called mainwindow.set_item_expanded()\n"
            "called mainwindow.open_editor()\n"
            "called mainwindow.enable_selaction()\n"
            "called mainwindow.disable_selaction()\n"
            "called mainwindow.disable_selaction()\n"
        )

    def test_set_option(self, monkeypatch, capsys):
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Selection": (-1, "x")}
        testsubj.set_option(1, "")
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.enable_selaction()\n"
        )
        testsubj = setup_notetree_class(monkeypatch)
        testsubj.opts = {"Selection": [-2, "x", False]}
        testsubj.set_option(1, "")
        assert capsys.readouterr().out == (
            "called mainwindow.__init__()\n"
            "called mainwindow.disable_selaction()\n"
        )

    def test_selection_contains_item(self, monkeypatch, capsys):
        testsubj = setup_notetree_class(monkeypatch)
        assert testsubj.selection_contains_item("text", ["key", "word"], 0, "", None)
        assert testsubj.selection_contains_item("text", ["key", "word"], 1, "word", None)
        assert not testsubj.selection_contains_item("text", ["key", "word"], 1, "other", None)
        assert not testsubj.selection_contains_item("text", ["key", "word"], -1, "word", None)
        assert testsubj.selection_contains_item("text", ["key", "word"], -1, "other", None)
        assert testsubj.selection_contains_item("text", ["key", "word"], 2, "Ex", False)
        assert not testsubj.selection_contains_item("text", ["key", "word"], 2, "Ex", True)
        assert testsubj.selection_contains_item("tExt", ["key", "word"], 2, "Ex", True)
        assert not testsubj.selection_contains_item("text", ["key", "word"], 2, "oink", False)
        assert not testsubj.selection_contains_item("text", ["key", "word"], -2, "Ex", False)
        assert testsubj.selection_contains_item("text", ["key", "word"], -2, "Ex", True)
        assert not testsubj.selection_contains_item("tExt", ["key", "word"], -2, "Ex", True)
        assert testsubj.selection_contains_item("text", ["key", "word"], -2, "oink", False)
