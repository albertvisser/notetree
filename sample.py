"""Opbouwen van een sample NoteTree file door simuleren van de gui acties

het idee is dat de testklasse de normale gui aanroept met methoden gesimuleerd
waardoor een interne datastructuur wordt opgebouwd / gevuld die opgeslagen wordt
waarna het programma eindigt

uitvoeren d.m.v. : `pytest sample.py`
"""
import sys
import datetime
import notetree.main as nt
from notetree.settings import backend
ext = 'db' if backend == 'sql' else backend
filename = '.'.join(('/tmp/notetree/testdata', ext))

class MockMainWindow:
    def __init__(self, root):
        self.base = root
        self.base.counter = 0
        self.root = None  # nodig bij simuleren gui routines

    def start(self):
        "hier komt het toevoegen van alle gegevens en het direct aanroepen van opslaan en afsluiten"
        self.base.opts['Keywords'] = ['boter', 'kass', 'eieren']
        self.base.opts['ActiveItem'] = -1
        for count in range(3):
            self.base.new_item()
        self.base.save()

    def ask_question(self, *args):
        "bevestigen van de vraag of het nieuwe bestand moet worden aangemaakt"
        return True

    def get_text_from_user(self, *args):
        "nieuw item aanmaken met titel"
        itemtitel = ['Mijn Leven', 'Een nieuw begin', 'Dat was het dan'][self.base.counter]
        self.base.counter += 1
        return itemtitel, True

    def add_item_to_tree(self, key, titel, tekst, keywords):
        "item opnemen in de interne data structuur"
        # datum/tijd aanpassen m.b.v. counter want zijn waarschijnlijk hetzelfde
        self.base.nt_data.pop(key)
        key = datetime.datetime.fromtimestamp(self.base.counter).strftime('%d-%m-%Y %H:%M:%S')
        if self.base.counter == 1:
            tekst = 'Het begon als een sprookje'
            keywords = ['boter']
        elif self.base.counter == 2:
            tekst = 'Dat kon natuurlijk niet'
            keywords = ['boter', 'eieren']
        elif self.base.counter == 3:
            tekst = 'En ze leefden nog lang en gelukkig'
            keywords = []
        self.base.nt_data[key] = titel, tekst, keywords

    def create_root(self, *args):
        self.root = 'root'
        return self.root

    # gui routines die worden aangeroepen maar niks hoeven te doen
    def showmsg(self, *args):
        pass
    def create_menu(self, *args):
        pass
    def init_screen(self, *args, **kwargs):
        pass
    def setup_statusbar(self, *args):
        pass
    def setup_trayicon(self, *args):
        pass
    def setup_split_screen(self, *args):
        pass
    def set_screen(self, *args):
        pass
    def set_splitter(self, *args):
        pass
    def clear_editor(self):
        pass
    def select_item(self, *args):
        pass
    def open_editor(self, *args):
        pass
    def set_focus_to_tree(self):
        pass
    def set_focus_to_editor(self):
        pass
    def set_item_expanded(self, *args):
        pass


class TestNoteTree:
    def test_init(self, monkeypatch):
        monkeypatch.setattr(nt.gui, 'MainWindow', MockMainWindow)
        # import pdb; pdb.set_trace()
        nt.NoteTree(filename)
