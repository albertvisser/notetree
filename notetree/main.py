"""NoteTree GUI-independent stuff
"""
import gettext
import os.path
import collections
import shutil

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
                (_("m_root"), self.gui.rename, _("h_root"), 'Shift+F2'),
                (_('m_tagman'), self.gui.manage_keywords, _('h_tagman'), 'Shift+F6'),
                ("", None, None, None),
                (_("m_hide"), self.gui.hide_me, _("h_hide"), 'Ctrl+H'),
                (_("m_lang"), self.gui.choose_language, _("h_lang"), 'Ctrl+F1'),
                (_('m_opts'), self.set_options, _('h_opts'), 'Ctrl+M'),
                ("", None, None, None),
                (_("m_exit"), self.gui.close, _("h_exit"), 'Ctrl+Q,Escape'), ), ),
            (_("m_note"), (
                (_("m_new"), self.gui.new_item, _("h_new"), 'Ctrl+N'),
                (_("m_delete"), self.gui.delete_item, _("h_delete"), 'Ctrl+D,Delete'),
                (_("m_name"), self.gui.ask_title, _("h_name"), 'F2'),
                ("", None, None, None),
                (_("m_tags"), self.gui.link_keywords, _("h_tags"), 'F6'),
                ("", None, None, None),
                (_("m_forward"), self.gui.next_note, _("h_forward"), 'Ctrl+PgDown'),
                (_("m_back"), self.gui.prev_note, _("h_back"), 'Ctrl+PgUp'), ), ),
            (_("m_view"), (
                (_("m_revorder"), self.gui.reverse, _("h_revorder"), 'F9'),
                ("", None, None, None),
                (_("m_selall"), self.gui.no_selection, _("h_selall"), None),
                (_("m_seltag"), self.gui.keyword_select, _("h_seltag"), None),
                (_("m_seltxt"), self.gui.text_select, _("h_seltxt"), None), ), ),
            (_("m_help"), (
                (_("m_about"), self.info_page, _("h_about"), None),
                (_("m_keys"), self.help_page, _("h_keys"), 'F1'), ), ), )

    def open(self, version):
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
            righthand_size = self.opts["ScreenSize"][0] - self.opts['SashPosition'])
            self.opts['SashPosition'] = tuple(self.opts['SashPosition'], righthand_size)
        try:
            self.gui.set_splitter(self.opts['SashPosition'])
        except TypeError:
            self.gui.showmsg(_('m_ignore'))
        root = self.gui.create_root(self.base.opts["RootTitle"])
        self.activate_item(self.build_tree(first_time=True)
        self.gui.set_item_expanded(root)
        self.gui.clear_editor()
        self.gui.open_editor()
        self.focus_to_tree()

    def build_tree(self, first_time=False):
        """translate the dictionary read to a tree structure
        """
        if not first_time:
            self.tree_to_dict()      # op commentaar in wx versie
            root = self.gui.create_root(self.opts["RootTitle"])  # qt versie
            # wx versie: self.check_active()  # even zorgen dat de editor inhoud geassocieerd wordt
            #            self.tree.DeleteChildren(self.root)
        item_to_activate = self.root    # wx versie: item_to_return = self.root
        seltype, seldata = self.opts["Selection"][:2]
        use_case = None
        if len(self.opts["Selection"]) > 2:
            use_case = self.opts["Selection"][2]

        for key, value in self.base.nt_data.items():
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
            item = self.gui.add_item_to_tree(key, tag, text, keywords, self.opts['RevOrder'])
            if not item_to_activate:
                item_to_activate = item
            if key == self.base.opts["ActiveItem"]:
                item_to_activate = item

        if not first_time:
            self.tree.expandItem(self.root)
        return item_to_activate

    def reread(self, *args):
        ok = self.gui.ask_question(self, _('ask_reload').format(self.project_file))
        if ok:
            self.open()

    def update(self, *args):
        """resave the notes to a file
        """
        self.tree_to_dict()  # check for changed values in tree not in dict
        self.opts["ScreenSize"] = self.get_screensize()
        self.opts["SashPosition"] = self.get_splitterpos()
        # self.opts["ActiveItem"] = self.get_activeitem()  already done in self.tree_to_dict
        self.save()

    def tree_to_dict(self):
        """translate the entire tree structure to a dictionary suitable for saving
        """
        self.check_active()  # even zorgen dat de editor inhoud geassocieerd wordt
        items, activeitem = self.gui.get_treeitems()
        self.base.opts["ActiveItem"] = activeitem   # is dit nodig als ik na check_active?
        for ky, tag, text, trefw in items:
            self.base.nt_data[ky] = (str(tag), str(text), trefw)

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

    def ask_title(self, *args):
        """Get/change a title for this note
        """
        text, ok = self.gui.get_text_from_user(_("t_name"), self.gui.get_itemtext(self.activeitem))
                # qt: self.activeitem.text(0))
                # wx: self.tree.GetItemText(self.activeitem)
        if ok:
            self.gui.set_itemtext(self.activeitem)
            # qt: self.activeitem.setText(0, text)
            # wx: self.tree.SetItemText(self.activeitem, text)

    def info_page(self. *args):
        """show program info
        """
        self.gui.showmsg(_('info_text'))

    def help_page(self, *args):
        """show keyboard shortcuts
        """
        self.gui.show_dialog(gui.GridDialog, title=self.base.app_title + " " + _("t_keys"))


    def set_options(self, *args):
        "manage options for messages"
        self.gui.show_dialog(gui.OptionsDialog)
