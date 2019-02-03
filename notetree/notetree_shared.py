"""NoteTree GUI-independent stuff
"""
import gettext
import os
import collections
import shutil
try:
    import cPickle as pck
except ImportError:
    import pickle as pck

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


# wrappers rond pickle ivm aanroep vanuit conversie utilities
#
def load_file(filename):
    """raise EOFError als file niet gelezen kan worden
    geeft geen resultaat als bestand niet bestaat
    """
    if not os.path.exists(filename):
        return {}
    with open(filename, "rb") as f_in:
        nt_data = pck.load(f_in)
        options = nt_data.get(0, [])
        test = options.get("Application", None)
        if test and test != "NoteTree":
            raise EOFError("{} is geen NoteTree bestand".format(filename))
    return nt_data


def save_file(filename, nt_data):
    """plain save/dump; backup should be done by the calling program (or not)
    """
    with open(filename, "wb") as _out:
        pck.dump(nt_data, _out, protocol=2)


# Mixin voor de GUI
#
class NoteTreeMixin:
    """general methods
    """
    def get_menudata(self):
        """define of menu options and callbacks
        """
        return (
            (_("m_main"), (
                (_("m_reload"), self.reread, _("h_reload"), 'Ctrl+L'),
                (_("m_save"), self.update, _("h_save"), 'Ctrl+S'),
                ("", None, None, None),
                (_("m_root"), self.rename, _("h_root"), 'Shift+F2'),
                ('Manage keywords', self.manage_keywords,
                 'Rename, remove and add tags', 'Shift+F6'),
                ("", None, None, None),
                (_("m_hide"), self.hide_me, _("h_hide"), 'Ctrl+H'),
                (_("m_lang"), self.choose_language, _("h_lang"), 'Ctrl+F1'),
                ("", None, None, None),
                (_("m_exit"), self.close, _("h_exit"), 'Ctrl+Q,Escape'), ), ),
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

    def open(self, version, root_title):
        """initialize and read data file
        """
        self.opts = initial_opts
        self.opts['Version'] = version
        self.opts['RootTitle'] = root_title
        self.nt_data = collections.OrderedDict()
        ## if os.path.exists(self.project_file):
            ## with open(self.project_file, "rb") as f_in:
                ## try:
                    ## self.nt_data = pck.load(f_in)
                ## except EOFError:
                    ## return "Geen NoteTree bestand"
                ## else:
                    ## options = self.nt_data.get(0, [])
                    ## test = options.get("Application", None)
                    ## if test and test != "NoteTree":
                        ## return "{} is geen correct NoteTree bestand".format(
                            ## self.project_file)
        try:
            self.nt_data = load_file(self.project_file)
        except EOFError as e:
            return e
        if not self.nt_data:
            return 'Bestand niet gevonden'
        options = self.nt_data.get(0, [])
        if "AskBeforeHide" in options:
            for key, val in options.items():
                self.opts[key] = val
        languages[self.opts["Language"]].install()
        ## print('installing language "{}"'.format(self.opts["Language"]))
        return ''

    def save(self):
        """finalize and write data file
        """
        self.nt_data[0] = self.opts
        shutil.copyfile(self.project_file, self.project_file + '~')
        save_file(self.project_file, self.nt_data)

    def reread(self):
        "placeholder"
        raise NotImplementedError

    def update(self):
        "placeholder"
        raise NotImplementedError

    def rename(self):
        "placeholder"
        raise NotImplementedError

    def hide_me(self):
        "placeholder"
        raise NotImplementedError

    def choose_language(self):
        "placeholder"
        raise NotImplementedError

    def close(self):
        "placeholder"
        raise NotImplementedError

    def new_item(self):
        "placeholder"
        raise NotImplementedError

    def delete_item(self):
        "placeholder"
        raise NotImplementedError

    def ask_title(self):
        "placeholder"
        raise NotImplementedError

    def link_keywords(self):
        "placeholder"
        raise NotImplementedError

    def next_note(self):
        "placeholder"
        raise NotImplementedError

    def prev_note(self):
        "placeholder"
        raise NotImplementedError

    def reverse(self):
        "placeholder"
        raise NotImplementedError

    def no_selection(self):
        "placeholder"
        raise NotImplementedError

    def keyword_select(self):
        "placeholder"
        raise NotImplementedError

    def text_select(self):
        "placeholder"
        raise NotImplementedError

    def info_page(self):
        "placeholder"
        raise NotImplementedError

    def help_page(self):
        "placeholder"
        raise NotImplementedError
