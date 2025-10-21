"""NoteTree GUI-independent stuff
"""
import gettext
import os.path
import collections
import shutil
import contextlib
from datetime import datetime

from notetree import dml
from notetree import gui

app_title = "NoteTree"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
locale = os.path.join(HERE, 'locale')
gettext.install(app_title, locale)
languages = {'nl': gettext.translation(app_title, locale, languages=['nl']),
             'en': gettext.translation(app_title, locale, languages=['en'])}
# dynamically built translatable string symbols resolved so that they can be recognized:
_('t_nl')
_('t_en')
# these ones aren't recognized the way they are defined in the code (sett2text dict):
_('t_hide')
_('t_load')
_('t_save')

root_title = "MyNotes"
initial_opts = {"Application": "NoteTree",
                "Version": "",
                "AskBeforeHide": True,
                "NotifyOnLoad": True,
                "NotifyOnSave": True,
                # "SaveOnEsc": True,
                "SashPosition": (180,),
                "ScreenSize": (800, 500),
                'Language': 'en',
                "RootTitle": '',
                "Keywords": [],
                "Selection": (0, ''),
                "RevOrder": False}
sett2text = {'AskBeforeHide': 't_hide',
             'NotifyOnLoad': 't_load',
             'NotifyOnSave': 't_save'}
             # 'SaveOnEsc': 't_svex'}
selectionmodes = ("m_selall", "m_seltag", "m_seltxt")


# Main screen
#
class NoteTree:
    """Main application class
    """
    def __init__(self, filename):
        self.app_title = app_title
        self.root_title = root_title
        self.languages = languages
        self.sett2text = sett2text
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
        title = f"{self.project_file} - {self.app_title}"
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
                (_("m_save"), self.save_from_menu, _("h_save"), 'Ctrl+S'),
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

    def save_from_menu(self, *args):
        "saving from the menu means saving should always happen"
        self.update(force_save=True)

    def update(self, *args, force_save=False):
        """resave the notes to a file
        """
        self.tree_to_dict()  # check for changed values in tree not in dict
        self.opts["ScreenSize"] = self.gui.get_screensize()
        self.opts["SashPosition"] = self.gui.get_splitterpos()
        # self.opts["ActiveItem"] = self.get_activeitem()  already done in self.tree_to_dict
        if self.nt_data != self.old_nt_data or force_save:
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
        self.gui.show_dialog(DefineTags)

    def hide_me(self, *args):
        """Minimize application to an icon in the system tray
        """
        if self.opts["AskBeforeHide"]:
            # als je in de dialoog het vinkje aanzet moet je het voor de optie juist uitzetten v.v.
            self.opts["AskBeforeHide"] = not self.gui.show_dialog(SetCheck, _("sleep_message"))[1]
        self.gui.sleep()

    def choose_language(self, *args):
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        langcodes = ('nl', 'en')
        langnames = [_(f't_{code}') for code in langcodes]
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
        text2sett = {y: x for x, y in self.sett2text.items()}
        ok, dialog_data = self.gui.show_dialog(SetOptions, data)
        if ok:
            for sett_text, settvalue in dialog_data.items():
                self.opts[text2sett[sett_text]] = settvalue

    def new_item(self, *args):
        """add a new item to the tree after asking for a title
        """
        start = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        text, ok = self.gui.get_text_from_user(_("t_new"), start)
        if ok:
            self.nt_data[start] = ""   # alvast toevoegen aan de data structuur
            item = self.gui.add_item_to_tree(start, text, '', [])
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
            self.gui.remove_item_from_tree(item)
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
        helptext = [x.split(' - ', 1) for x in _("tag_help").split('\n')]
        ok, new_keywords = self.gui.show_dialog(AssignTags, helptext, keywords)
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
            selection_list = self.opts['Keywords']
            seltype, seltext = self.opts['Selection'][:2]
            if abs(seltype) == 1:
                try:
                    selindex = selection_list.index(seltext)
                except ValueError:  # kan niet?bij seltype (-)1 is dit altijd een bestaand trefwoord
                    selindex = -1
                # seldata = (selection_list, selindex)
            else:
                selindex = -1
                # seldata = (selection_list, -1)  # ''
            ok, data = self.gui.show_dialog(GetItem, seltype, selection_list, selindex,
                                            _("i_seltag"))
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
            use_case = False
        if abs(seltype) != 2:
            seltext = ''
        ok, data = self.gui.show_dialog(GetText, seltype, seltext, _("i_seltxt"), use_case)
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
        data = [x.split(' - ', 1) for x in _("help_text").split('\n')]
        self.gui.show_dialog(KeyHelp, self.app_title + " " + _("t_keys"), data)

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
        self.old_nt_data = self.nt_data.copy()
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
        return ''

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
            if not self.selection_contains_item(text, keywords, seltype, seldata, use_case):
                continue
            item = self.gui.add_item_to_tree(key, tag, text, keywords)  # , self.opts['RevOrder'])
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
                    self.gui.showmsg(message)
                self.gui.copy_text_from_editor_to_activeitem()

    def activate_item(self, item):
        """make the new item "active" and get the text for it from the tree structure
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
        with contextlib.suppress(FileNotFoundError):
            shutil.copyfile(self.project_file, self.project_file + '~')
        dml.save_file(self.project_file, self.nt_data)
        self.old_nt_data = self.nt_data.copy()
        if self.opts["NotifyOnSave"]:
            self.gui.showmsg('\n'.join((_("save_message"), _('hide_me'))))

    def set_selection(self, opts, seltext):
        """selectie aanpassen
        """
        self.opts["Selection"] = opts
        self.gui.select_item(self.build_tree())
        self.gui.set_item_expanded(self.gui.root)
        self.gui.open_editor()
        for actiontext in selectionmodes:
            if _(actiontext) == seltext:
                self.gui.enable_selaction(_(actiontext))
            else:
                self.gui.disable_selaction(_(actiontext))

    def set_option(self, seltype, actiontext):
        """bij cancelen selectiedialoog de juiste menukeuze weer aan/uitzetten
        """
        if abs(self.opts['Selection'][0]) == seltype:
            self.gui.enable_selaction(actiontext)
        else:
            self.gui.disable_selaction(actiontext)

    def selection_contains_item(self, text, keywords, seltype, seldata, use_case):
        """determine if item should be added to the selection
        """
        exclude = -1
        if seltype == selectionmodes.index("m_selall"):  # 0:
            return True
        if seltype == selectionmodes.index("m_seltag"):  # 1:
            if seldata in keywords:
                return True
        elif seltype == exclude * selectionmodes.index("m_seltag"):  # -1:
            if seldata not in keywords:
                return True
        elif seltype == selectionmodes.index("m_seltxt"):  # 2:
            if use_case and seldata in text:
                return True
            if not use_case and seldata.upper() in text.upper():
                return True
        elif seltype == exclude * selectionmodes.index("m_seltxt"):  # -2:
            if use_case and seldata not in text:
                return True
            if not use_case and seldata.upper() not in text.upper():
                return True
        return False


class SetOptions:
    """Toon en wijzig desgewenst instellingen
    """
    def __init__(self, parent, text2valuedict):
        self.parent = parent
        self.gui = gui.OptionsDialog(self, parent, title=_('t_sett'))
        self.controls = []
        row = 0
        for labeltext, value in text2valuedict.items():
            row += 1
            check = self.gui.add_checkbox_line_to_grid(row, _(f'{labeltext}'), value)
            self.controls.append((labeltext, check))
        self.gui.add_buttonbox(okvalue=_('b_apply'), cancelvalue=_('b_close'))

    def confirm(self):
        """exchange data with caller
        """
        return {text: self.gui.get_checkbox_value(control) for text, control in self.controls}


class SetCheck:
    """Geef een melding en vraag of deze gegeven moet blijven worden
    """
    def __init__(self, parent, message):
        self.parent = parent
        self.gui = gui.CheckDialog(self, parent, title=parent.base.app_title)
        self.gui.add_label(message)
        self.check = self.gui.add_checkbox(_("hide_message"))
        self.gui.add_ok_buttonbox()

    def confirm(self):
        "get the input before closing the dialog"
        return self.gui.get_checkbox_value(self.check)


class AssignTags:
    """Toon een dialoog voor het koppelen van trefwoorden
    """
    def __init__(self, parent, helptext, keywords=None):
        self.parent = parent
        self.helptext = helptext
        if keywords is None:
            keywords = []
        all_trefw = self.parent.base.opts['Keywords']
        curr_trefw = keywords

        self.gui = gui.KeywordsDialog(self, parent, f'{self.parent.base.app_title} - {_("w_tags")}')
        unassigned_items = [x for x in all_trefw if x not in curr_trefw]
        self.fromlist = self.gui.add_list(_("t_left"), unassigned_items, self.move_right, first=True)
        self.buttons = self.gui.add_buttons([(_("t_tags"), None),
                                             (_("b_tag"), self.move_right),
                                             (_("b_untag"), self.move_left),
                                             ('', None),
                                             (_("b_newtag"), self.add_trefw),
                                             (_("m_keys"), self.keys_help)])
        self.tolist = self.gui.add_list(_('t_right'), curr_trefw, self.move_left, last=True)
        self.gui.create_buttonbox()
        self.gui.create_actions([(_('a_from'), 'Ctrl+L', self.activate_left),
                                 (_('b_tag'), 'Ctrl+Right', self.move_right),
                                 (_('a_to'), 'Ctrl+R', self.activate_right),
                                 (_('b_untag'), 'Ctrl+Left', self.move_left),
                                 (_('b_newtag'), 'Ctrl+N', self.add_trefw)])

    def activate_left(self, *args):
        """activate "from" list
        """
        self.gui.activate(self.fromlist)

    def activate_right(self, *args):
        """activate "to" list
        """
        self.gui.activate(self.tolist)

    def move_right(self, *args):
        """trefwoord selecteren
        """
        self.gui.moveitem(self.fromlist, self.tolist)

    def move_left(self, *args):
        """trefwoord on-selecteren
        """
        self.gui.moveitem(self.tolist, self.fromlist)

    def add_trefw(self, *args):
        """nieuwe trefwoorden opgeven en direct in de linkerlijst zetten
        """
        text, ok = self.gui.ask_for_tag(caption=self.parent.base.app_title,
                                        message=_('t_newtag'))
        if ok:
            self.gui.add_tag_to_list(text, self.tolist)
            self.parent.base.opts["Keywords"].append(text)

    def keys_help(self, *args):
        """Show possible actions and accelerator keys
        """
        helpdialog = gui.GridDialog(self.gui, f"{self.parent.base.app_title} {_("t_keys")}",
                                    _('b_done'))
        row = 0
        for left, right in self.helptext:
            helpdialog.add_label(row, 0, left)
            helpdialog.add_label(row, 1, right)
            row += 1
        helpdialog.send()

    def confirm(self):
        "get the input before closing the dialog"
        return self.gui.get_listvalues(self.tolist)


class DefineTags:
    """Toon een dialoog voor het administreren van trefwoorden
    """
    def __init__(self, parent):
        self.parent = parent
        self.gui = gui.KeywordsManager(
            self, parent, f'{self.parent.base.app_title} - {_("t_tagman")}', _('b_done'))
        self.gui.add_label(_('l_oldval'), 0, 0)
        self.oldtags = self.gui.add_combobox(0, 1)
        self.gui.add_button(_('b_remtag'), self.remove_keyword, 0, 2)
        self.gui.add_label(_('l_newval'), 1, 0)
        self.newtag = self.gui.add_lineinput(1, 1)
        self.gui.add_button(_('b_addtag'), self.add_keyword, 1, 2)
        self.gui.add_label(_('t_applied'), 2, -1)
        self.refresh_fields()

    def refresh_fields(self):
        "refill the lists after making changes"
        self.gui.reset_combobox(self.oldtags, self.parent.base.opts['Keywords'])
        self.gui.reset_lineinput(self.newtag)

    def remove_keyword(self):
        """delete a keyword after selecting from the dropdown
        """
        oldtext = self.gui.get_combobox_value(self.oldtags)
        msg = _('t_remtag').format(oldtext)
        if self.gui.ask_question(self.parent.base.app_title, msg):
            self.parent.base.opts['Keywords'].remove(oldtext)
            self.update_items(oldtext)
            self.refresh_fields()

    def add_keyword(self):
        """Add a new keyword or change an existing one after selecting from the dropdown
        """
        oldtext = self.gui.get_combobox_value(self.oldtags)
        newtext = self.gui.get_lineinput_text(self.newtag)
        if oldtext:
            ok, cancel = self.gui.ask_question_w_cancel(_('t_repltag').format(oldtext, newtext),
                                                        _('t_repltag2'))
            if cancel:
                return
            ix = self.parent.base.opts['Keywords'].index(oldtext)
            self.parent.base.opts['Keywords'][ix] = newtext
            if ok:
                self.update_items(oldtext, newtext)
            else:
                self.update_items(oldtext)
        else:
            msg = _('t_addtag').format(newtext)
            if self.gui.ask_question(self.parent.base.app_title, msg):
                self.parent.base.opts['Keywords'].append(newtext)
        self.refresh_fields()

    def update_items(self, oldtext, newtext=''):
        """refresh lists of associated keywords on deletion/replacement
        """
        for item in self.parent.get_treeitems()[0]:
            tags = self.parent.get_item_keywords(item)
            if oldtext in tags:
                tags.remove(oldtext)
                if newtext:
                    tags.append(newtext)
            self.parent.set_item_keywords(item, tags)


class GetText:
    """Builds a dialog to get search string
    """
    def __init__(self, parent, seltype, seltext, labeltext="", use_case=False):
        self.parent = parent
        self.gui = gui.GetTextDialog(self, parent, parent.base.app_title)
        self.gui.add_label(labeltext)
        self.text = self.gui.add_lineinput(seltext)
        self.in_exclude, self.use_case = self.gui.add_checkbox_line([('exclude', seltype < 0),
                                                                     ('case sensitive', use_case)])
        self.gui.add_okcancel_buttonbox()

    def confirm(self):
        "get the input before closing the dialog"
        return [self.gui.get_checkbox_value(self.in_exclude),
                self.gui.get_lineinput_value(self.text),
                self.gui.get_checkbox_value(self.use_case)]


class GetItem:
    """Builds a dialog to get tag to search for (by selection)
    """
    def __init__(self, parent, seltype, selection_list, seltext, labeltext=""):
        self.parent = parent
        self.gui = gui.GetItemDialog(self, parent, parent.base.app_title)
        self.gui.add_label(labeltext)
        self.text = self.gui.add_combobox(selection_list, seltext)
        #        self.parent.base.opts['Keywords'], seltext)
        self.in_exclude = self.gui.add_checkbox('exclude', seltype < 0)
        self.gui.add_okcancel_buttonbox()

    def confirm(self):
        "get the input before closing the dialog"
        return [self.gui.get_checkbox_value(self.in_exclude),
                self.gui.get_combobox_value(self.text)]


class KeyHelp:
    """Help dialog for keyboard shortcuts
    """
    def __init__(self, parent, title, data):
        self.gui = gui.GridDialog(parent, title, _('b_done'))
        line = 0
        for left, right in data:
            self.gui.add_label(line, 0, left)
            self.gui.add_label(line, 1, right)
            line += 1
