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
                "NotifyOnLoad": True,
                "NotifyOnSave": True,
                "SashPosition": (180,),
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
        self.sett2text = {'AskBeforeHide': _('t_hide'),
                          'NotifyOnLoad': _('t_load'),
                          'NotifyOnSave': _('t_save')}
        self.project_file = filename
        self.gui = gui.MainWindow(self)
        self.define_screen()
        mld = self.open(first_time=True)
        if mld:
            self.gui.showmsg(mld)
            self.gui.close()
        else:
            self.gui.start()

    def define_screen(self):
        "setup main application window"
        title = " - ".join((self.project_file, self.app_title))
        iconame = os.path.join(os.path.dirname(__file__), "notetree.ico")
        self.gui.init_screen(title=title, iconame=iconame)
        self.gui.setup_statusbar()
        self.gui.setup_trayicon()
        self.gui.setup_split_screen()

    def get_menudata(self):
        """define of menu options and callbacks
        """
        return (
            (_("m_main"), (
                (_("m_reload"), self.reread, _("h_reload"), 'F5'),
                (_("m_save"), self.update, _("h_save"), 'Ctrl+S'),
                ("", None, None, None),
                (_("m_root"), self.rename, _("h_root"), 'Shift+F2'),
                (_('m_tagman'), self.manage_keywords, _('h_tagman'), 'Shift+F6'),
                ("", None, None, None),
                (_("m_hide"), self.hide_me, _("h_hide"), 'Ctrl+H'),
                (_("m_lang"), self.choose_language, _("h_lang"), 'Ctrl+L'),
                (_('m_opts'), self.set_options, _('h_opts'), 'Ctrl+O'),
                ("", None, None, None),
                (_("m_exit"), self.gui.close, _("h_exit"), 'Ctrl+Q,Escape'), ), ),
            (_("m_note"), (
                (_("m_new"), self.new_item, _("h_new"), 'Ctrl+N'),
                (_("m_delete"), self.delete_item, _("h_delete"), 'Ctrl+D,Delete'),
                (_("m_name"), self.ask_title, _("h_name"), 'F2'),
                ("", None, None, None),
                (_("m_tags"), self.link_keywords, _("h_tags"), 'F6'),
                ("", None, None, None),
                (_("m_forward"), self.goto_next_note, _("h_forward"), 'Ctrl+PgDown'),
                (_("m_back"), self.goto_prev_note, _("h_back"), 'Ctrl+PgUp'), ), ),
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
        ok = self.gui.ask_question(_('ask_reload').format(self.project_file))
        if ok:
            self.open()

    def update(self, *args):
        """resave the notes to a file
        """
        # TODO check of gewijzigd
        self.tree_to_dict()  # check for changed values in tree not in dict
        self.opts["ScreenSize"] = self.gui.get_screensize()
        self.opts["SashPosition"] = self.gui.get_splitterpos()
        # self.opts["ActiveItem"] = self.get_activeitem()  already done in self.tree_to_dict
        self.save()

    def rename(self, *args):
        """ask for a new title for the root item
        """
        text, ok = self.gui.get_text_from_user(_("t_root"), self.gui.get_rootitem_title())
        if ok:
            self.opts["RootTitle"] = text
            self.gui.set_rootitem_title(text)

    def manage_keywords(self, *args):
        """Open a dialog where keywords can be renamed, removed or added
        """
        self.gui.show_dialog(gui.KeywordsManager)

    def hide_me(self, *args):
        """Minimize application to an icon in the system tray
        """
        if self.opts["AskBeforeHide"]:
            ok, value = self.gui.show_dialog(gui.CheckDialog, "AskBeforeHide", _("sleep_message"))
            if ok:
                self.opts["AskBeforeHide"] = value
        self.gui.sleep()

    def choose_language(self, *args):
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        langcodes = ('nl', 'en')
        langnames = [_('t_{}'.format(code)) for code in langcodes]
        text, ok = self.gui.get_choice_from_user(_("t_lang"), langnames,
                                                 langcodes.index(self.opts["Language"]))
        if ok:
            code = langcodes[langnames.index(text)]
            self.opts["Language"] = code
            self.languages[code].install()
            self.gui.create_menu()

    def set_options(self, *args):
        "manage options for messages"
        data = {self.sett2text[x]: y for x, y in self.opts.items() if x in self.sett2text}
        text2sett = {y: x for x,y in self.sett2text.items()}
        ok, dialog_data = self.gui.show_dialog(gui.OptionsDialog, data)
        if ok:
            for sett_text, settvalue in dialog_data.items():
                self.opts[text2sett[sett_text]] = settvalue

    def new_item(self, *args):
        """add a new item to the tree after asking for a title
        """
        start = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        text, ok = self.gui.get_text_from_user(_("t_new"), start)
        if ok:
            item = self.gui.add_item_to_tree(start, text, '', [])
            self.nt_data[start] = ""
            self.gui.select_item(item)  # or activate_item?
            self.gui.set_item_expanded(self.gui.root)
            self.gui.open_editor()
            self.gui.set_focus_to_editor()

    def delete_item(self, *args):
        """remove item from tree
        """
        item = self.gui.get_selected_item()
        if item != self.gui.root:
            ky = self.gui.get_key_from_item(item)
            item = self.gui.remove_item_from_tree(item)
            del self.nt_data[ky]
        else:
            self.gui.showmsg(_("no_delete_root"))

    def ask_title(self, *args):
        """Get/change a title for this note
        """
        text, ok = self.gui.get_text_from_user(_("t_name"), self.gui.get_activeitem_title())
        if ok:
            self.gui.set_activeitem_title(text)

    def link_keywords(self, *args):
        """Open a dialog where keywords can be assigned to the text
        """
        item = self.gui.activeitem
        if item is not None:
            keywords = self.gui.get_item_keywords(item)
        if item is None or keywords is None:
            return
        ok, new_keywords = self.gui.show_dialog(gui.KeywordsDialog, keywords)
        if ok:
            self.gui.set_item_keywords(item, new_keywords)

    def goto_next_note(self, *args):
        """Go to next
        """
        item = self.gui.get_next_item()
        if item:
            self.gui.select_item(item)
        else:
            self.gui.showmsg(_("no_next_item"))

    def goto_prev_note(self, *args):
        """Go to previous
        """
        item = self.gui.get_prev_item()
        if item:
            self.gui.select_item(item)
        else:
            self.gui.showmsg(_("no_prev_item"))

    def reverse(self, *args):
        """set to "newest first"
        """
        self.opts['RevOrder'] = not self.opts['RevOrder']
        item_to_activate = self.build_tree()
        self.gui.select_item(item_to_activate)
        self.gui.set_item_expanded(self.gui.root)
        self.gui.open_editor()

    def no_selection(self, *args):
        """make sure nothing is selected
        """
        self.set_selection((0, ""), _("m_selall"))
        self.gui.show_statusbar_message(_("h_selall"))

    def keyword_select(self, *args):
        """Open a dialog where a keyword can be chosen to select texts that it's assigned to
        """
        if self.opts['Keywords']:
            seltype, seldata = self.opts['Selection'][:2]
            if abs(seltype) == 1:
                selection_list = self.opts['Keywords']
                try:
                    selindex = selection_list.index(seltext)
                except ValueError:
                    selindex = -1
                seldata = (selection_list, selindex)
            else:
                seldata = ''
            ok, data = self.gui.show_dialog(gui.GetItemDialog, seltype, seldata, _("i_seltag"))
        else:
            self.gui.showmsg('No keywords defined yet')
            ok = False
        if not ok:
            # bij Cancel menukeuze weer aan/uitzetten
            self.set_option(1, _("m_seltag"))
            return
        exclude, text = data
        if exclude:
            seltype, in_ex = -1, "all except"
        else:
            seltype, in_ex = 1, 'only'
        self.set_selection((seltype, text), _("m_seltag"))
        self.gui.show_statusbar_message(_("h_seltag").format(in_ex, text))

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
        ok, data = self.gui.show_dialog(gui.GetTextDialog, seltype, seltext, _("i_seltxt"),
                                        use_case)
        if ok:
            exclude, text, use_case = data
            if exclude:
                seltype, in_ex = -2, "all except"
            else:
                seltype, in_ex = 2, 'only'
            self.set_selection((seltype, text, use_case), _("m_seltxt"))
            self.gui.show_statusbar_message(_("h_seltxt").format(in_ex, text))
        else:
            # bij Cancel menukeuze weer aan/uitzetten
            self.set_option(2, _("m_seltxt"))

    def info_page(self, *args):
        """show program info
        """
        self.gui.showmsg(_('info_text'))

    def help_page(self, *args):
        """show keyboard shortcuts
        """
        self.gui.show_dialog(gui.GridDialog, self.app_title + " " + _("t_keys"))

    def open(self, first_time=False):  # , version):
        """initialize and read data file
        """
        self.opts = initial_opts
        self.opts['Version'] = gui.toolkit.title()  # version
        self.opts['RootTitle'] = self.root_title
        self.nt_data = collections.OrderedDict()
        try:
            self.nt_data = dml.load_file(self.project_file)
        except EOFError as e:
            return _(str(e)).format(self.project_file)
        if not self.nt_data:
            ok = self.gui.ask_question(_('ask_create').format(self.project_file))
            if not ok:
                self.project_file = ''
                return _('404_message')
        options = self.nt_data.get(0, [])
        if "AskBeforeHide" in options:
            for key, val in options.items():
                self.opts[key] = val
        languages[self.opts["Language"]].install()
        # recreate menu after loading (because of language)
        self.gui.create_menu()
        self.gui.set_screen(self.opts["ScreenSize"])
        if len(self.opts['SashPosition']) == 1:
            righthand_size = self.opts["ScreenSize"][0] - self.opts['SashPosition'][0]
            self.opts['SashPosition'] = tuple((self.opts['SashPosition'][0], righthand_size))
        try:
            self.gui.set_splitter(self.opts['SashPosition'])
        except TypeError:
            self.gui.showmsg(_('m_ignore'))
        self.gui.clear_editor()
        self.gui.select_item(self.build_tree(first_time=True))
        self.gui.set_item_expanded(self.gui.root)
        self.gui.open_editor()
        if self.opts["NotifyOnLoad"] and not first_time:
            self.gui.showmsg('\n'.join((_("load_message"), _('hide_me'))))
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

        return item_to_activate

    def check_active(self, message=None):
        """if there's a suitable "active" item, make sure its text is saved to the tree structure
        """
        if self.gui.activeitem and self.gui.activeitem != self.gui.root:
            self.gui.emphasize_activeitem(False)
            if self.gui.editor_text_was_changed():
                # print('in check_active: text in editpr was changed')
                if message:
                    self.showmsg(message)
                self.gui.copy_text_from_editor_to_activeitem()

    def activate_item(self, item):
        """make the new item "active" and get the text for itfrom the tree structure
        """
        if not item:
            return
        self.gui.clear_editor()
        self.gui.activeitem = item
        if item != self.gui.root:
            self.gui.emphasize_activeitem(True)
            self.gui.copy_text_from_activeitem_to_editor()
            self.gui.open_editor()
        # over uit wx versie
        # self.tree.EnsureVisible(item)

    def tree_to_dict(self):
        """translate the entire tree structure to a dictionary suitable for saving
        """
        self.check_active()  # even zorgen dat de editor inhoud geassocieerd wordt
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
        if self.opts["NotifyOnSave"]:
            self.gui.showmsg('\n'.join((_("save_message"), _('hide_me'))))

    def set_selection(self, opts, seltext):
        """selectie aanpassen
        """
        self.opts["Selection"] = opts
        self.gui.select_item(self.build_tree())
        self.gui.set_item_expanded(self.gui.root)
        self.gui.open_editor()
        for actiontext in(_("m_selall"), _("m_seltag"), _("m_seltxt")):
            if actiontext == seltext:
                self.gui.enable_selaction(actiontext)
            else:
                self.gui.disable_selaction(actiontext)

    def set_option(self, seltype, actiontext):
        """bij cancelen selectiedialoog de juiste menukeuze weer aan/uitzetten
        """
        if abs(self.opts['Selection'][0]) == seltype:
            self.gui.enable_selaction(actiontext)
        else:
            self.gui.disable_selaction(actiontext)
