"""NoteTree GUI-independent stuff
"""
import gettext
import os.path
import collections
import shutil
from datetime import datetime

import notetree.dml as dml
import notetree.gui as gui

app_title = "NoteTree"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
locale = os.path.join(HERE, 'locale')
gettext.install(app_title, locale)
languages = {'nl': gettext.translation(app_title, locale, languages=['nl']),
             'en': gettext.translation(app_title, locale, languages=['en'])}
# dynamically built translatable string symbols resolved so that they can be recognized
_('t_nl')
_('t_en')

root_title = "MyNotes"
initial_opts = {"Application": "NoteTree",
                "Version": "",
                "AskBeforeHide": True,
                "ActiveItem": 0,
                "SashPosition": 180,
                "ScreenSize": (800, 500),
                'Language': 'en',
                "RootTitle": '',
                "Keywords": [],
                "Selection": (0, ''),
                "RevOrder": False}


# Main screen
#
class NoteTree:
    """general methods
    """
    def __init__(self, filename):
        self.app_title = app_title
        self.root_title = root_title
        self.languages = languages
        self.project_file = filename
        self.gui = gui.MainWindow(self)
        title = " - ".join((self.project_file, self.app_title))
        iconame = os.path.join(os.path.dirname(__file__), "notetree.ico")
        self.gui.build_screen(title=title, iconame=iconame)
        mld = self.open()
        if mld:
            self.gui.showmsg(mld)
            self.gui.close()
        else:
            self.gui.open()
            self.gui.start()

    def get_menudata(self):
        """define of menu options and callbacks
        """
        return (
            (_("m_main"), (
                (_("m_reload"), self.reread, _("h_reload"), 'Ctrl+L'),
                (_("m_save"), self.update, _("h_save"), 'Ctrl+S'),
                ("", None, None, None),
                (_("m_root"), self.rename, _("h_root"), 'Shift+F2'),
                (_('m_tagman'), self.manage_keywords, _('h_tagman'), 'Shift+F6'),
                ("", None, None, None),
                (_("m_hide"), self.hide_me, _("h_hide"), 'Ctrl+H'),
                (_("m_lang"), self.choose_language, _("h_lang"), 'Ctrl+F1'),
                (_('m_opts'), self.set_options, _('h_opts'), 'Ctrl+M'),
                ("", None, None, None),
                (_("m_exit"), self.gui.close, _("h_exit"), 'Ctrl+Q,Escape'), ), ),
            (_("m_note"), (
                (_("m_new"), self.new_item, _("h_new"), 'Ctrl+N'),
                (_("m_delete"), self.delete_item, _("h_delete"), 'Ctrl+D,Delete'),
                (_("m_name"), self.ask_title, _("h_name"), 'F2'),
                ("", None, None, None),
                (_("m_tags"), self.link_keywords, _("h_tags"), 'F6'),
                ("", None, None, None),
                (_("m_forward"), self.next_note, _("h_forward"), 'Ctrl+PgDown'),
                (_("m_back"), self.prev_note, _("h_back"), 'Ctrl+PgUp'), ), ),
            (_("m_view"), (
                (_("m_revorder"), self.reverse, _("h_revorder"), 'F9'),
                ("", None, None, None),
                (_("m_selall"), self.no_selection, _("h_selall"), None),
                (_("m_seltag"), self.keyword_select, _("h_seltag"), None),
                (_("m_seltxt"), self.text_select, _("h_seltxt"), None), ), ),
            (_("m_help"), (
                (_("m_about"), self.info_page, _("h_about"), None),
                (_("m_keys"), self.help_page, _("h_keys"), 'F1'), ), ), )

    def reread(self, *args):
        """revert to the saved version of the notes file
        """
        ok = self.gui.ask_question(self, _('ask_reload').format(self.project_file))
        if ok:
            self.open()

    def update(self, *args):
        """resave the notes to a file
        """
        self.tree_to_dict()  # check for changed values in tree not in dict
        self.opts["ScreenSize"] = self.gui.get_screensize()
        self.opts["SashPosition"] = self.gui.get_splitterpos()
        # self.opts["ActiveItem"] = self.get_activeitem()  already done in self.tree_to_dict
        self.save()

    def rename(self, *args):
        """ask for a new title for the root item
        """
        text, ok = self.gui.get_text_from_user(_("t_root"), self.gui.get_root_text())
               # qt: self.root.text(0))
               # wx: self.tree.GetItemText(self.root)
        if ok:
            self.opts["RootTitle"] = text
            self.gui.set_rootitem_text(text)
            # qt: self.root.setText(0, text)
            # wx: self.tree.SetItemText(self.root, text)

    def manage_keywords(self, *args):
        """Open a dialog where keywords can be renamed, removed or added
        """
        self.gui.show_dialog(gui.KeywordsManager)

    def hide_me(self, *args):
        """Minimize application to an icon in the system tray
        """
        if self.opts["AskBeforeHide"]:
            self.gui.show_dialog(gui.CheckDialog)
        self.gui.sleep()

    def choose_language(self):
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        langcodes = ('nl', 'en')
        langnames = (_('t_{}'.format(code)) for code in langcodes)
        text, ok = self.gui.get_choice_from_user(_("t_lang"), langnames,
                                                 langcodes.index(self.opts["Language"]))
        if ok:
            code = langcodes[langnames.index(text)]
            self.opts["Language"] = code
            self.languages[code].install()
            self.gui.create_menu()

    def set_options(self, *args):
        "manage options for messages"
        self.gui.show_dialog(gui.OptionsDialog)

    def new_item(self, *args):
        """add a new item to the tree after asking for a title
        """
        start = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        text, ok = self.gui.get_text_from_user(_("t_new"), text=start)
        if ok:
            item = self.gui.add_item_to_tree(start, text, '', [])
            self.nt_data[start] = ""
            self.gui.select_item(item)  # or activate_item?
            self.gui.set_item.expanded(self.gui.root)
            self.gui.init_editor()
            self.gui.focus_editor()

    def delete_item(self, *args):
        """remove item from tree
        """
        item = self.gui.get_selected_item()
        if item != self.gui.root:
            item = self.gui.remove_item_from_tree(item)
            ky = self.gui.get_key_from_item(item)
            del self.nt_data[ky]
            # TODO moet hier niet nog activeren van het voorafgaande item bij?
        else:
            self.gui.showmsg(_("no_delete_root"))

    def ask_title(self, *args):
        """Get/change a title for this note
        """
        text, ok = self.gui.get_text_from_user(_("t_name"),
                                               self.gui.get_itemtext(self.gui.activeitem))
                # qt: self.activeitem.text(0))
                # wx: self.tree.GetItemText(self.activeitem)
        if ok:
            self.gui.set_itemtext(self.gui.activeitem, text)
            # qt: self.activeitem.setText(0, text)
            # wx: self.tree.SetItemText(self.activeitem, text)

    def link_keywords(self, *args):
        """Open a dialog where keywords can be assigned to the text
        """
        item = self.gui.activeitem
        if item is not None:
            keywords = self.gui.get_item_keywords(item)
        if item is None or keywords is None:
            return
        ok, new_keywords = self.gui.show_dialog(gui.KeywordsDialog)  # , keywords
        if ok:
            self.gui.set_item_keywords(item, new_keywords)

    def next_note(self):
        """Go to next
        """
        if not self.gui.goto_next_item():
            self.gui.showmsg(_("no_next_item"))

    def prev_note(self):
        """Go to previous
        """
        if not self.gui.goto_next_item():
            self.gui.showmsg(_("no_prev_item"))

    def reverse(self, *args):
        """set to "newest first"
        """
        self.opts['RevOrder'] = not self.opts['RevOrder']
        item_to_activate = self.build_tree()
        self.gui.select_item(item_to_activate)

    def no_selection(self, *args):
        """make sure nothing is selected
        """
        self.set_selection((0, ""), _("h_selall"))

    def keyword_select(self, *args):
        """Open a dialog where a keyword can be chosen to select texts that it's assigned to
        """
        seltype, seltext = self.opts['Selection'][:2]
        if abs(seltype) != 1:
            seltext = ''
        ok = self.gui.show_dialog(gui.GetItemDialog, seltype, seltext, _("i_seltag"))
        if ok:
            exclude, text = self.gui.dialog_data
            if exclude:
                seltype, in_ex = -1, "all except"
            else:
                seltype, in_ex = 1, 'only'
            self.set_selection((seltype, text), _("h_seltag"))
            self.gui.show_statusbar_message(_("h_seltag").format(in_ex, text))
        # bij Cancel menukeuze weer aan/uitzetten
        else:
            self.set_option(1, _("m_seltag"))

    def text_select(self, *args):
        """Open a dialog box where text can be entered that the texts to be selected contain
        """
        try:
            seltype, seltext, use_case = self.opts['Selection']
        except ValueError:
            seltype, seltext = self.opts['Selection']
            use_case = None
        if abs(seltype) != 2:
            seltext = ''
        ok = self.gui.show_dialog(gui.GetItemDialog, seltype, seltext, _("i_seltxt"), use_case)
        if ok:
            exclude, text, use_case = self.gui.dialog_data
            if exclude:
                seltype, in_ex = -2, "all except"
            else:
                seltype, in_ex = 2, 'only'
            self.set_selection((seltype, text, use_case), _("h_seltxt"))
            self.gui.show_statusbar_message(_("h_seltxt").format(in_ex, text))
        # bij Cancel menukeuze weer aan/uitzetten
        else:
            self.set_option(2, _("m_seltxt"))

    def info_page(self, *args):
        """show program info
        """
        self.gui.showmsg(_('info_text'))

    def help_page(self, *args):
        """show keyboard shortcuts
        """
        self.gui.show_dialog(gui.GridDialog, title=self.app_title + " " + _("t_keys"))

    def open(self):  # , version):
        """initialize and read data file
        """
        self.opts = initial_opts
        self.opts['Version'] = gui.toolkit.title()  # version
        self.opts['RootTitle'] = self.root_title
        self.nt_data = collections.OrderedDict()
        try:
            self.nt_data = dml.load_file(self.project_file)
        except EOFError as e:
            self.gui.showmsg(_(str(e)).format(self.project_file))
            return
        if not self.nt_data:
            # return 'Bestand niet gevonden'
            ok = self.gui.ask_question(self, _('ask_create').format(self.project_file))
            if not ok:
                self.project_file = ''
                self.gui.showmsg(_('404_message'))
                return
        options = self.nt_data.get(0, [])
        if "AskBeforeHide" in options:
            for key, val in options.items():
                self.opts[key] = val
        languages[self.opts["Language"]].install()
        # de rest vervangt self.gui.open()
        # recreate menu after loading (because of language)
        self.gui.create_menu()
        self.gui.set_screen(self.opts["ScreenSize"])
        if len(self.opts['SashPosition']) == 1:
            righthand_size = self.opts["ScreenSize"][0] - self.opts['SashPosition']
            self.opts['SashPosition'] = tuple(self.opts['SashPosition'], righthand_size)
        try:
            self.gui.set_splitter(self.opts['SashPosition'])
        except TypeError:
            self.gui.showmsg(_('m_ignore'))
        root = self.build_tree(first_time=True)
        self.gui.activate_item(root)
        self.gui.set_item_expanded(root)
        self.gui.clear_editor()
        self.gui.open_editor()
        self.gui.set_focus_to_tree()

    def build_tree(self, first_time=False):
        """translate the dictionary read to a tree structure, applying the chosen filter
        """
        if not first_time:
            self.tree_to_dict()      # op commentaar in wx versie
            # wx versie: self.check_active()  # even zorgen dat de editor inhoud geassocieerd wordt
        root = self.gui.create_root(self.opts["RootTitle"])  # qt versie
        # wx versie: self.tree.DeleteChildren(self.root)
        item_to_activate = root    # wx versie: item_to_return = self.root
        seltype, seldata = self.opts["Selection"][:2]
        use_case = None
        if len(self.opts["Selection"]) > 2:
            use_case = self.opts["Selection"][2]

        for key, value in self.nt_data.items():
            if key == 0:
                continue
            try:
                tag, text, keywords = value
            except ValueError:
                tag, text = value
                keywords = []
            if seltype == 1 and seldata not in keywords:
                continue
            elif seltype == -1 and seldata in keywords:
                continue
            elif seltype == 2:
                ok = False
                if use_case and seldata in text:
                    ok = True
                elif not use_case and seldata.upper() in text.upper():
                    ok = True
                if not ok:
                    continue
            elif seltype == -2:
                ok = False
                if use_case and seldata not in text:
                    ok = True
                elif not use_case and seldata.upper() not in text.upper():
                    ok = True
                if not ok:
                    continue
            item = self.gui.add_item_to_tree(key, tag, text, keywords)  # , self.opts['RevOrder'])
            if not item_to_activate:
                item_to_activate = item
            if key == self.opts["ActiveItem"]:
                item_to_activate = item

        if not first_time:
            self.gui.set_item_expanded(self.gui.root)
        return item_to_activate

    def tree_to_dict(self):
        """translate the entire tree structure to a dictionary suitable for saving
        """
        self.gui.check_active()  # even zorgen dat de editor inhoud geassocieerd wordt
        items, activeitem = self.gui.get_treeitems()
        self.opts["ActiveItem"] = activeitem
        for ky, tag, text, trefw in items:
            self.nt_data[ky] = (str(tag), str(text), trefw)

    def save(self, *args):
        """finalize and write data file
        """
        if not self.project_file:
            return
        self.nt_data[0] = self.opts
        try:
            shutil.copyfile(self.project_file, self.project_file + '~')
        except FileNotFoundError:
            pass
        dml.save_file(self.project_file, self.nt_data)

    def set_selection(self, opts, seltext):
        """selectie aanpassen
        """
        self.opts["Selection"] = opts
        item_to_activate = self.build_tree()
        self.gui.select_item(item_to_activate)
        for actiontext in(_("m_selall"), _("m_seltag"), _("m_seltxt")):
            if actiontext == seltext:
                self.gui.enable_selaction(actiontext)
            else:
                self.gui.disable_selaction(actiontext)

    def set_option(self, seltype, actiontext):
        """bij cancelen selectiedialoog de juiste menukeuze weer aan/uitzetten
        """
        if abs(self.base.opts['Selection'][0]) == seltype:
            self.gui.enable_selaction(actiontext)
        else:
            self.gui.disable_selaction(actiontext)
