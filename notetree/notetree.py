# -*- coding: utf-8 -*-

"NoteTree PyQt versie"

# van een ibm site afgeplukt
import os
import sys
from datetime import datetime
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
try:
    import cPickle as pck
except ImportError:
    import pickle as pck
import logging
logging.basicConfig(filename='doctree_qt.log', level=logging.DEBUG,
    format='%(asctime)s %(message)s')
import gettext

app_title = "NoteTree"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
locale = os.path.join(HERE, 'locale')
gettext.install(app_title, locale)
languages = {'nl': gettext.translation(app_title, locale, languages=['nl']),
    'en': gettext.translation(app_title, locale, languages=['en'])}

root_title = "MyNotes"

def message(window, string, title):
     gui.QMessageDialog.information(window, string, title)

class CheckDialog(gui.QDialog):
    """Dialoog om te melden dat de applicatie verborgen gaat worden
    AskBeforeHide bepaalt of deze getoond wordt of niet"""
    def __init__(self, parent):
        self.parent = parent
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle(app_title)
        self.setWindowIcon(self.parent.nt_icon)
        txt = gui.QLabel(_("sleep_message"), self)
        self.check = gui.QCheckBox(_("hide_message"), self)
        ok_button = gui.QPushButton("&Ok", self)
        self.connect(ok_button, core.SIGNAL('clicked()'), self.klaar)

        vbox = gui.QVBoxLayout()

        hbox = gui.QHBoxLayout()
        hbox.addWidget(txt)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addWidget(self.check)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addWidget(ok_button)
        hbox.insertStretch(0, 1)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        ## self.resize(574 + breedte, 480)
        self.exec_()

    def klaar(self):
        "dialoog afsluiten"
        if self.check.isChecked():
            self.parent.opts["AskBeforeHide"] = False
        gui.QDialog.done(self, 0)

class MainWindow(gui.QMainWindow):
    def __init__(self, parent=None, title=''):
        gui.QMainWindow.__init__(self)
        self.nt_icon = gui.QIcon(os.path.join(os.path.dirname(__file__),
            "notetree.ico"))
        self.setWindowIcon(self.nt_icon)
        self.resize(800, 500)
        self.setWindowTitle(title)
        self.sb = self.statusBar()

        self.tray_icon = gui.QSystemTrayIcon(self.nt_icon, self)
        self.tray_icon.setToolTip(_("revive_message"))
        self.connect(self.tray_icon, core.SIGNAL('clicked'),
            self.revive)
        tray_signal = "activated(QSystemTrayIcon::ActivationReason)"
        self.connect(self.tray_icon, core.SIGNAL(tray_signal),
            self.revive)
        self.tray_icon.hide()

        menubar = self.menuBar()
        self.create_menu()

        self.splitter = gui.QSplitter(self)
        self.setCentralWidget(self.splitter)

        self.tree = gui.QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.hideColumn(1)
        self.tree.setItemHidden(self.tree.headerItem(), True)
        self.tree.setSelectionMode(gui.QTreeWidget.SingleSelection)
        self.splitter.addWidget(self.tree)
        self.tree.itemSelectionChanged.connect(self.changeselection)
        ## self.tree.keyReleaseEvent.connect(self.on_key)

        self.editor = gui.QTextEdit(self)
        self.editor.setEnabled(False)
        self.splitter.addWidget(self.editor)
        ## self.editor.keyReleaseEvent.connect(self.on_key2)

    def create_menu(self):              # ok
        menudata = (
            (_("m_main"), (
                    (_("m_reload"), self.reread, _("h_reload"), 'Ctrl+L'),
                    (_("m_save"), self.save, _("h_save"), 'Ctrl+S'),
                    ("", None, None, None),
                    (_("m_root"), self.rename, _("h_root"), 'Shift+F2'),
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
                    (_("m_forward"), self.next_note,_("h_forward"), 'Ctrl+PgDown'),
                    (_("m_back"), self.prev_note,_("h_back"), 'Ctrl+PgUp'),
                ), ),
            (_("m_help"), (
                    (_("m_about"), self.info_page, _("h_about"), None),
                    (_("m_keys"), self.help_page, _("h_keys"), 'F1'),
                ), ),
            )
        menu_bar = self.menuBar()
        menu_bar.clear()
        for item, data in menudata:
            menu_label = item
            submenu = menu_bar.addMenu(menu_label)
            for label, handler, info, key in data:
                if label:
                    action = submenu.addAction(label, handler)
                    if key:
                        action.setShortcuts([x for x in key.split(",")])
                    action.setStatusTip(info)
                else:
                    submenu.addSeparator()

    ## def keyReleaseEvent(self, event):
        ## keycode = event.key()
        ## if keycode == wx.WXK_DELETE:
            ## self.delete_item()
        ## elif keycode == wx.WXK_ESCAPE:
            ## self.afsl()
        ## gui.QTreeWidget.keyReleaseEvent(self, event)

    ## def on_key2(self, event):
        ## keycode = event.key()
        ## if keycode == wx.WXK_ESCAPE:
            ## self.afsl()
        ## gui.QTextEdit.keyReleaseEvent(self, event)

    def changeselection(self, event=None):
        test = self.tree.selectedItems()
        if test == self.root:
            return
        self.check_active()
        h = self.tree.currentItem()
        #log('size hint for item {}'.format(h.sizeHint(0)))
        self.activate_item(h)

    def open(self):                 # ok
        print("calling open")
        self.opts = {
            "AskBeforeHide": True,
            "ActiveItem": 0,
            "SashPosition": 180,
            "ScreenSize": (800, 500),
            'Language': 'en',
            "RootTitle": root_title
            }
        self.nt_data = {}
        if os.path.exists(self.project_file):
            with open(self.project_file, "rb") as f_in:
                try:
                    self.nt_data = pck.load(f_in)
                except EOFError:
                    gui.QMessageBox.information(self, app_title, "Geen NoteTree bestand")
                    ## return
        self.root = self.tree.takeTopLevelItem(0)
        ## self.root = self.tree.AddRoot(os.path.splitext(os.path.split(
            ## self.project_file)[1])[0])
        self.root = gui.QTreeWidgetItem()
        self.root.setText(0, self.opts["RootTitle"])
        self.tree.addTopLevelItem(self.root)
        self.activeitem = item_to_activate = self.root
        self.editor.clear()
        self.editor.setEnabled(False)
        for key, value in self.nt_data.items():
            if key == 0 and "AskBeforeHide" in value:
                for key, val in value.items():
                    self.opts[key] = val
            else:
                tag, text = value
                item = gui.QTreeWidgetItem()
                item.setText(0, tag)
                item.setText(1, text)
                self.root.addChild(item)
                if key == self.opts["ActiveItem"]:
                    item_to_activate = item
                    ## self.editor.setText(text)
                    ## self.editor.setEnabled(True)
        languages[self.opts["Language"]].install()
        ## print('installing language "{}"'.format(self.opts["Language"]))
        self.resize(*self.opts["ScreenSize"])
        ## print(self.opts['SashPosition'])
        try:
            self.splitter.restoreState(self.opts['SashPosition'])
        except TypeError:
            pass
        self.root.setExpanded(True)
        self.tree.setCurrentItem(item_to_activate)
        self.tree.setFocus()

    def reread(self,event=None):
        dlg = gui.QMessageBox.question(self, app_title, _("ask_reload"),
            gui.QMessageBox.Yes | gui.QMessageBox.No)
        if dlg == gui.QMessageBox.Yes:
            self.open()

    def save(self, event=None):
        print("saving...")
        self.check_active() # even zorgen dat de editor inhoud geassocieerd wordt
        self.opts["ScreenSize"] = self.width(), self.height() # tuple(self.size())
        self.opts["SashPosition"] = self.splitter.saveState()
        ## self.opts.pop("SashPosition")
        ## if not isinstance(self.opts["RootTitle"], str):
            ## self.opts["RootTitle"] = str(self.opts["RootTitle"])
        self.nt_data = {0: self.opts}
        data = []
        for num in range(self.root.childCount()):
            ky = num + 1
            tag = self.root.child(num).text(0)
            ## print(tag, self.activeitem.text(0), num)
            ## if tag == self.activeitem:
                ## self.opts["ActiveItem"] = ky
            text = self.root.child(num).text(1)
            self.nt_data[ky] = (str(tag), str(text))
        self.opts["ActiveItem"] = self.root.indexOfChild(self.activeitem) + 1
        with open(self.project_file,"wb") as _out:
            pck.dump(self.nt_data, _out, protocol=2)

    def rename(self, event=None):
        text, ok = gui.QInputDialog.getText(self, app_title, _("t_root"),
            gui.QLineEdit.Normal, self.root.text(0))
        if ok:
            self.root.setText(text)

    def hide_me(self, event=None):
        if self.opts["AskBeforeHide"]:
            dlg = CheckDialog(self)
        self.tray_icon.show()
        self.hide()

    def revive(self, event=None):
        if event == gui.QSystemTrayIcon.Unknown:
            self.tray_icon.showMessage(app_title, _("revive_message"))
        elif event == gui.QSystemTrayIcon.Context:
            pass
        else:
            self.show()
            self.tray_icon.hide()

    def closeEvent(self, event=None):
        self.save()
        event.accept()

    def new_item(self, event=None):
        # kijk waar de cursor staat (of altijd onderaan toevoegen?)
        start = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        text, ok = gui.QInputDialog.getText(self, app_title, _("t_new"), text=start)
        if ok:
            item = gui.QTreeWidgetItem()
            item.setText(0, text)
            item.setText(1, "")
            self.root.addChild(item)
            self.tree.setCurrentItem(item)
            self.root.setExpanded(True)
            self.editor.clear()
            self.editor.setEnabled(True)
            self.editor.setFocus()

    def delete_item(self, event=None):
        item = self.tree.currentItem()
        if item != self.root:
            idx = self.root.indexOfChild(item)
            self.root.removeChild(item)
            if idx > 1:
                prev = self.root.child(idx - 1)
                self.activate_item(prev)
            else:
                self.editor.clear()
                self.editor.setEnabled(False)
        else:
            message(self, _("no_delete_root"), app_title)

    def ask_title(self, event=None):
        text, ok = gui.QInputDialog.getText(self, app_title, _("t_name"),
            gui.QLineEdit.Normal, self.activeitem.text(0))
        if ok:
            self.activeitem.setText(0, text)

    def next_note(self, event=None):
        idx = self.root.indexOfChild(self.activeitem)
        if idx < self.root.childCount() - 1:
            self.tree.setCurrentItem(self.root.child(idx + 1))
        else:
            gui.QMessageBox.information(self, app_title, _("no_next_item"))

    def prev_note(self, event=None):
        idx = self.root.indexOfChild(self.activeitem)
        if idx > 0:
            self.tree.setCurrentItem(self.root.child(idx - 1))
        else:
            gui.QMessageBox.information(self, app_title, _("no_prev_item"))

    def check_active(self, message=None):   # ok
        if self.activeitem and self.activeitem != self.root:
            font = self.activeitem.font(0)
            font.setBold(False)
            self.activeitem.setFont(0, font)
            if self.editor.document().isModified:
                if message:
                    print(message)
                self.activeitem.setText(1,self.editor.toPlainText())

    def activate_item(self, item):      # ok
        self.activeitem = item
        if item != self.root:
            font = item.font(0)
            font.setBold(True)
            item.setFont(0, font)
            self.editor.setText(item.text(1))
            self.editor.setEnabled(True)
        else:
            self.editor.clear()
            self.editor.setEnabled(False)

    def info_page(self,event=None):     # ok
        gui.QMessageBox.information(self, app_title, _("info_text"))

    def help_page(self,event=None):     # ok
        gui.QMessageBox.information(self, app_title, _("help_text"))

    def choose_language(self, event=None):  # ok?
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        data = [(code, _('t_{}'.format(code))) for code in ('nl', 'en')]
        ## data = [('nl', _('t_nl')), ('en', _('t_en'))]
        for idx, lang in enumerate([x[0] for x in data]):
            if lang == self.opts["Language"]:
                break
        text, ok = gui.QInputDialog.getItem(self, app_title,_("t_lang"),
            [x[1] for x in data], current=idx, editable=False)
        if ok:
            for idx, lang in enumerate([x[1] for x in data]):
                if lang == text:
                    code = data[idx][0]
                    self.opts["Language"] = code
                    languages[code].install()
                    print('installing language "{}"'.format(code))
                    self.create_menu()
                    break

def main(fnaam):
    ## self.fn = fnaam
    app = gui.QApplication(sys.argv)
    frame = MainWindow(parent=None, title=" - ".join((app_title, fnaam)))
    frame.show()
    frame.project_file = fnaam
    frame.open()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main('NoteTree.pck')
    app.MainLoop()
