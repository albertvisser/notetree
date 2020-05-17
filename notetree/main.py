"""NoteTree GUI-independent stuff
"""
import gettext
import os.path
import collections
import shutil

# from notetree.pickle_dml import load_file, save_file
from notetree.sql_dml import load_file, save_file
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
        nok = self.gui.open()
        if nok:
            # self.gui.showmsg(mld)
            self.gui.close()
        else:
            self.gui.start()

    def get_menudata(self):
        """define of menu options and callbacks
        """
        return (
            (_("m_main"), (
                (_("m_reload"), self.gui.reread, _("h_reload"), 'Ctrl+L'),
                (_("m_save"), self.gui.update, _("h_save"), 'Ctrl+S'),
                ("", None, None, None),
                (_("m_root"), self.gui.rename, _("h_root"), 'Shift+F2'),
                (_('m_tagman'), self.gui.manage_keywords, _('h_tagman'), 'Shift+F6'),
                ("", None, None, None),
                (_("m_hide"), self.gui.hide_me, _("h_hide"), 'Ctrl+H'),
                (_("m_lang"), self.gui.choose_language, _("h_lang"), 'Ctrl+F1'),
                (_('m_opts'), self.gui.set_options, _('h_opts'), 'Ctrl+M'),
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
                (_("m_about"), self.gui.info_page, _("h_about"), None),
                (_("m_keys"), self.gui.help_page, _("h_keys"), 'F1'), ), ), )

    def open(self, version):
        """initialize and read data file
        """
        self.opts = initial_opts
        self.opts['Version'] = version
        self.opts['RootTitle'] = self.root_title
        self.nt_data = collections.OrderedDict()
        try:
            self.nt_data = load_file(self.project_file)
        except EOFError as e:
            self.gui.showmsg(str(e))
            return e
        if not self.nt_data:
            # return 'Bestand niet gevonden'
            ok = self.gui.ask_question(self, _('ask_create').format(self.project_file))
            if not ok:
                self.project_file = ''
                return _('404_message')
        options = self.nt_data.get(0, [])
        if "AskBeforeHide" in options:
            for key, val in options.items():
                self.opts[key] = val
        languages[self.opts["Language"]].install()
        return ''

    def save(self):
        """finalize and write data file
        """
        if not self.project_file:
            return
        self.nt_data[0] = self.opts
        try:
            shutil.copyfile(self.project_file, self.project_file + '~')
        except FileNotFoundError:
            pass
        save_file(self.project_file, self.nt_data)
