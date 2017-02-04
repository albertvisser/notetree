import gettext
import os
import collections
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

try:
    import cPickle as pck
except ImportError:
    import pickle as pck

class NoteTreeMixin:

    def get_menudata(self):
        return (
            (_("m_main"), (
                (_("m_reload"), self.reread, _("h_reload"), 'Ctrl+L'),
                (_("m_save"), self.save, _("h_save"), 'Ctrl+S'),
                ("", None, None, None),
                (_("m_root"), self.rename, _("h_root"), 'Shift+F2'),
                ('Manage keywords', self.manage_keywords,
                    'Rename, remove and add tags', 'Shift+F6'),
                ("", None, None, None),
                (_("m_hide"), self.hide_me, _("h_hide"), 'Ctrl+H'),
                (_("m_lang"), self.choose_language, _("h_lang"), 'Ctrl+F1'),
                ("", None, None, None),
                (_("m_exit"), self.close, _("h_exit"), 'Ctrl+Q,Escape'),
                ), ),
            (_("m_note"), (
                (_("m_new"), self.new_item, _("h_new"), 'Ctrl+N'),
                (_("m_delete"), self.delete_item, _("h_delete"), 'Ctrl+D,Delete'),
                (_("m_name"), self.ask_title, _("h_name"), 'F2'),
                ("", None, None, None),
                (_("m_tags"), self.link_keywords, _("h_tags"), 'F6'),
                ("", None, None, None),
                (_("m_forward"), self.next_note,_("h_forward"), 'Ctrl+PgDown'),
                (_("m_back"), self.prev_note,_("h_back"), 'Ctrl+PgUp'),
                ), ),
            ## ( _("m_select"), (
                ## (_("m_selall"), self.no_selection, _("h_selall"), None),
                ## (_("m_seltag"), self.keyword_select, _("h_seltag"), None),
                ## (_("m_seltxt"), self.text_select, _("h_seltxt"), None),
            ( _("m_view"), (
                (_("m_revorder"), self.reverse, _("h_revorder"), None),
                ("", None, None, None),
                (_("m_selall"), self.no_selection, _("h_selall"), None),
                (_("m_seltag"), self.keyword_select, _("h_seltag"), None),
                (_("m_seltxt"), self.text_select, _("h_seltxt"), None),
                ), ),
            (_("m_help"), (
                (_("m_about"), self.info_page, _("h_about"), None),
                (_("m_keys"), self.help_page, _("h_keys"), 'F1'),
                ), ),
            )

    def open(self, version, root_title):
        self.opts = {
            "Application": "NoteTree",
            "Version": version,
            "AskBeforeHide": True,
            "ActiveItem": 0,
            "SashPosition": 180,
            "ScreenSize": (800, 500),
            'Language': 'en',
            "RootTitle": root_title,
            "Keywords": [],
            "Selection": (0, ''),
            "RevOrder": False,
            }
        self.nt_data = collections.OrderedDict()
        ## # wx versie:
        ## try:
            ## file = open(self.project_file, 'rb')
        ## except IOError:
            ## return
        ## try:
            ## self.nt_data = pickle.load(file)
        ## except EOFError:
            ## return
        ## file.close()
        ## # qt versie:
        if os.path.exists(self.project_file):
            with open(self.project_file, "rb") as f_in:
                try:
                    self.nt_data = pck.load(f_in)
                except EOFError:
                    return "Geen NoteTree bestand"
                else:
                    options = self.nt_data.get(0, [])
                    test = options.get("Application", None)
                    if test and test != "NoteTree":
                        return "{} is geen correct NoteTree bestand".format(
                            self.project_file)
        options = self.nt_data.get(0, [])
        if "AskBeforeHide" in options:
            for key, val in options.items():
                self.opts[key] = val
        languages[self.opts["Language"]].install()
        ## print('installing language "{}"'.format(self.opts["Language"]))

    def _save(self):
        self.nt_data[0] = self.opts
        ## self.nt_data = {0: self.opts}
        with open(self.project_file,"wb") as _out:
            pck.dump(self.nt_data, _out, protocol=2)

    def reread(self): raise NotImplementedError
    def save(self): raise NotImplementedError
    def rename(self): raise NotImplementedError
    def hide_me(self): raise NotImplementedError
    def choose_language(self): raise NotImplementedError
    def close(self): raise NotImplementedError
    def new_item(self): raise NotImplementedError
    def delete_item(self): raise NotImplementedError
    def ask_title(self): raise NotImplementedError
    def link_keywords(self): raise NotImplementedError
    def next_note(self): raise NotImplementedError
    def prev_note(self): raise NotImplementedError
    def reverse(self): raise NotImplementedError
    def no_selection(self): raise NotImplementedError
    def keyword_select(self): raise NotImplementedError
    def text_select(self): raise NotImplementedError
    def info_page(self): raise NotImplementedError
    def help_page(self): raise NotImplementedError
