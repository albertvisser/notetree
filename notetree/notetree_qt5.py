# -*- coding: utf-8 -*-

"NoteTree PyQt versie"

# van een ibm site afgeplukt
import os
import sys
from datetime import datetime
import PyQt5.QtWidgets as wdg
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import logging
logging.basicConfig(filename='doctree_qt.log', level=logging.DEBUG,
    format='%(asctime)s %(message)s')
import gettext
from .notetree_shared import NoteTreeMixin, app_title, root_title, languages

## app_title = "NoteTree"
## HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
## locale = os.path.join(HERE, 'locale')
## gettext.install(app_title, locale)
## languages = {'nl': gettext.translation(app_title, locale, languages=['nl']),
    ## 'en': gettext.translation(app_title, locale, languages=['en'])}

## # dynamically built translatable string symbols resolved so that they can be recognized
## _('t_nl')
## _('t_en')

## root_title = "MyNotes"

class KeywordsDialog(wdg.QDialog):
    """Dialoog voor het koppelen van trefwoorden
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle('{} - {}'.format(app_title, _("w_tags")))
        self.setWindowIcon(self.parent.nt_icon)
        self.resize(400, 256)
        # define widgets
        self.fromlist = wdg.QListWidget(self)
        self.fromlist.setSelectionMode(wdg.QAbstractItemView.MultiSelection)
        text = wdg.QLabel(_("t_tags"), self)
        fromto_button = wdg.QPushButton(_("b_tag"))
        fromto_button.clicked.connect(self.move_right)
        tofrom_button = wdg.QPushButton(_("b_untag"))
        tofrom_button.clicked.connect(self.move_left)
        addtrefw_button = wdg.QPushButton(_("b_newtag"))
        addtrefw_button.clicked.connect(self.add_trefw)
        self.tolist = wdg.QListWidget(self)
        self.tolist.setSelectionMode(wdg.QAbstractItemView.MultiSelection)
        bbox = wdg.QDialogButtonBox(wdg.QDialogButtonBox.Ok |
            wdg.QDialogButtonBox.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        # get data from parent
        all_trefw = self.parent.opts['Keywords']
        self.data = self.parent.activeitem
        curr_trefw = self.data.data(1, core.Qt.UserRole)
        self.tolist.addItems(curr_trefw)
        self.fromlist.addItems([x for x in all_trefw if x not in curr_trefw])
        # do layout and show
        vbox = wdg.QVBoxLayout()
        hbox = wdg.QHBoxLayout()
        vbox2 = wdg.QVBoxLayout()
        vbox2.addWidget(wdg.QLabel(_("t_left"), self))
        vbox2.addWidget(self.fromlist)
        hbox.addLayout(vbox2)
        vbox2 = wdg.QVBoxLayout()
        vbox2.addStretch()
        vbox2.addWidget(text)
        vbox2.addWidget(fromto_button)
        vbox2.addWidget(tofrom_button)
        vbox2.addSpacing(10)
        vbox2.addWidget(addtrefw_button)
        vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox2 = wdg.QVBoxLayout()
        vbox2.addWidget(wdg.QLabel(_("t_right"), self))
        vbox2.addWidget(self.tolist)
        hbox.addLayout(vbox2)
        vbox.addLayout(hbox)
        hbox = wdg.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(bbox)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def move_right(self, event):
        """trefwoord selecteren
        """
        self.moveitem(self.fromlist, self.tolist)

    def move_left(self, event):
        """trefwoord on-selecteren
        """
        self.moveitem(self.tolist, self.fromlist)

    def moveitem(self, from_, to):
        """trefwoord verplaatsen van de ene lijst naar de andere
        """
        selected = from_.selectedItems()
        for item in selected:
            from_.takeItem(from_.row(item))
            to.addItem(item)

    def add_trefw(self, event):
        """nieuwe trefwoorden opgeven en direct in de linkerlijst zetten
        """
        text, ok = wdg.QInputDialog.getText(self, app_title, "Geef nieuw trefwoord op")
        if ok:
            self.parent.opts["Keywords"].append(text)
            self.tolist.addItem(text)

    def accept(self):
        """geef de geselecteerde trefwoorden aan het hoofdprogramma
        """
        self.parent.new_keywords = [self.tolist.item(i).text() for i in range(
            len(self.tolist))]
        super().accept()

class CheckDialog(wdg.QDialog):
    """Dialoog om te melden dat de applicatie verborgen gaat worden
    AskBeforeHide bepaalt of deze getoond wordt of niet
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(app_title)
        self.setWindowIcon(self.parent.nt_icon)
        txt = wdg.QLabel(_("sleep_message"), self)
        self.check = wdg.QCheckBox(_("hide_message"), self)
        ok_button = wdg.QPushButton("&Ok", self)
        ok_button.clicked.connect(self.klaar)

        vbox = wdg.QVBoxLayout()

        hbox = wdg.QHBoxLayout()
        hbox.addWidget(txt)
        vbox.addLayout(hbox)

        hbox = wdg.QHBoxLayout()
        hbox.addWidget(self.check)
        vbox.addLayout(hbox)

        hbox = wdg.QHBoxLayout()
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
        super().done(0)

class MainWindow(wdg.QMainWindow, NoteTreeMixin):
    def __init__(self, parent=None, title=''):
        super().__init__()
        self.nt_icon = gui.QIcon(os.path.join(os.path.dirname(__file__),
            "notetree.ico"))
        self.setWindowIcon(self.nt_icon)
        self.resize(800, 500)
        self.setWindowTitle(title)
        self.sb = self.statusBar()

        self.tray_icon = wdg.QSystemTrayIcon(self.nt_icon, self)
        self.tray_icon.setToolTip(_("revive_message"))
        ## self.tray_icon.clicked.connect(self.revive)
        ## tray_signal = "activated(QSystemTrayIcon::ActivationReason)"
        self.tray_icon.activated.connect(self.revive)
        self.tray_icon.hide()

        menubar = self.menuBar()
        self.create_menu()

        self.splitter = wdg.QSplitter(self)
        self.setCentralWidget(self.splitter)

        self.tree = wdg.QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.hideColumn(1)
        self.tree.headerItem().setHidden(True)
        self.tree.setSelectionMode(wdg.QTreeWidget.SingleSelection)
        self.splitter.addWidget(self.tree)
        self.tree.itemSelectionChanged.connect(self.changeselection)
        ## self.tree.keyReleaseEvent.connect(self.on_key)

        self.editor = wdg.QTextEdit(self)
        self.editor.setEnabled(False)
        self.splitter.addWidget(self.editor)
        ## self.editor.keyReleaseEvent.connect(self.on_key2)

    def create_menu(self):
        menu_bar = self.menuBar()
        menu_bar.clear()
        self.selactions = []
        for item, data in self.get_menudata(): # defined in mixin class
            menu_label = item
            submenu = menu_bar.addMenu(menu_label)
            for label, handler, info, key in data:
                if label:
                    action = submenu.addAction(label, handler)
                    if label in (_("m_selall"), _("m_seltag"), _("m_seltxt")):
                        action.setCheckable(True)
                        self.selactions.append(action)
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

    def closeEvent(self, event=None):
        self.save()
        event.accept()

    def open(self):
        msg = NoteTreeMixin.open(self, "Qt", root_title)
        if msg:
            wdg.QMessageBox.information(self, app_title, msg)
            return
        self.root = self.tree.takeTopLevelItem(0)
        ## self.root = self.tree.AddRoot(os.path.splitext(os.path.split(
            ## self.project_file)[1])[0])
        self.root = wdg.QTreeWidgetItem()
        self.root.setText(0, self.opts["RootTitle"])
        self.tree.addTopLevelItem(self.root)
        self.activeitem = item_to_activate = self.root
        self.editor.clear()
        self.editor.setEnabled(False)
        # TODO apply selection while building tree
        item_to_activate = self.build_tree(first_time=True)
        self.resize(*self.opts["ScreenSize"])
        ## print(self.opts['SashPosition'])
        try:
            self.splitter.restoreState(self.opts['SashPosition'])
        except TypeError:
            pass
        self.root.setExpanded(True)
        self.tree.setCurrentItem(item_to_activate)
        self.tree.setFocus()

    def build_tree(self, first_time=False):
        if not first_time:
            self.tree_to_dict()
            self.root = self.tree.takeTopLevelItem(0)
            self.root = wdg.QTreeWidgetItem()
            self.root.setText(0, self.opts["RootTitle"])
            self.tree.addTopLevelItem(self.root)
        item_to_activate = self.root
        self.activeitem = None
        ## seltype = 0
        seltype, seldata = self.opts["Selection"]
        for key, value in self.nt_data.items():
            print(key, value)
            if key == 0:
                continue
            try:                    # TO BE REMOVED
                tag, text = value   # this code makes it possible
                keywords = []       # to read existing datafiles
            except ValueError:      # should become obsolete pretty soon
                tag, text, keywords = value
            ## seltype, seldata = self.opts["Selection"]
            if seltype == 1 and seldata not in keywords:
                continue
            if seltype == 2 and seldata not in text:
                continue
            item = wdg.QTreeWidgetItem()
            if not item_to_activate: # make sure this is only set to root if selection is empty
                item_to_activate = item
            item.setText(0, tag)
            item.setData(0, core.Qt.UserRole, key)
            item.setText(1, text)
            item.setData(1, core.Qt.UserRole, keywords)
            self.root.addChild(item)
            print(key, self.opts["ActiveItem"])
            if key == self.opts["ActiveItem"]:
                print("setting item_to_activate to", item)
                item_to_activate = item
                ## self.editor.setText(text)
                ## self.editor.setEnabled(True)
        for action in self.selactions:
            print('unchecking', action.text())
            action.setChecked(False)
        print('checking', self.selactions[seltype].text())
        self.selactions[seltype].setChecked(True)
        self.tree.expandItem(self.root)
        return item_to_activate

    def reread(self,event=None):
        dlg = wdg.QMessageBox.question(self, app_title, _("ask_reload"),
            wdg.QMessageBox.Yes | wdg.QMessageBox.No)
        if dlg == wdg.QMessageBox.Yes:
            self.open()

    def tree_to_dict(self):
        self.check_active() # even zorgen dat de editor inhoud geassocieerd wordt
        ## self.nt_data = {}
        for num in range(self.root.childCount()):
            tag = self.root.child(num).text(0)
            ky = self.root.child(num).data(0, core.Qt.UserRole)
            text = self.root.child(num).text(1)
            trefw = self.root.child(num).data(1, core.Qt.UserRole)
            print(ky, tag, text, trefw)
            self.nt_data[ky] = (str(tag), str(text), trefw)

    def save(self, event=None):
        self.tree_to_dict() # check for changed values in tree not in dict
        self.opts["ScreenSize"] = self.width(), self.height() # tuple(self.size())
        self.opts["SashPosition"] = self.splitter.saveState()
        ## self.opts["ActiveItem"] = self.root.indexOfChild(self.activeitem) + 1
        self.opts["ActiveItem"] = self.activeitem.data(0, core.Qt.UserRole)
        NoteTreeMixin._save(self)

    def rename(self, event=None):
        text, ok = wdg.QInputDialog.getText(self, app_title, _("t_root"),
            wdg.QLineEdit.Normal, self.root.text(0))
        if ok:
            self.opts["RootTitle"] = text
            self.root.setText(0, text)

    def hide_me(self, event=None):
        if self.opts["AskBeforeHide"]:
            dlg = CheckDialog(self)
        self.tray_icon.show()
        self.hide()

    def revive(self, event=None):
        if event == wdg.QSystemTrayIcon.Unknown:
            self.tray_icon.showMessage(app_title, _("revive_message"))
        elif event == wdg.QSystemTrayIcon.Context:
            pass
        else:
            self.show()
            self.tray_icon.hide()

    def new_item(self, event=None):
        # kijk waar de cursor staat (of altijd onderaan toevoegen?)
        start = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        text, ok = wdg.QInputDialog.getText(self, app_title, _("t_new"), text=start)
        print('new item:', text, ok)
        if ok:
            item = wdg.QTreeWidgetItem()
            item.setText(0, text)
            item.setData(0, core.Qt.UserRole, text)
            item.setText(1, "")
            item.setData(1, core.Qt.UserRole, [])
            self.root.addChild(item)
            self.nt_data[text] = ""
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
            print(self.nt_data)
            ky = item.data(0, core.Qt.UserRole)
            del self.nt_data[ky]
        else:
            wdg.QMessageBox.information(self, app_title, _("no_delete_root"))

    def ask_title(self, event=None):
        text, ok = wdg.QInputDialog.getText(self, app_title, _("t_name"),
            wdg.QLineEdit.Normal, self.activeitem.text(0))
        if ok:
            self.activeitem.setText(0, text)

    def next_note(self, event=None):
        idx = self.root.indexOfChild(self.activeitem)
        if idx < self.root.childCount() - 1:
            self.tree.setCurrentItem(self.root.child(idx + 1))
        else:
            wdg.QMessageBox.information(self, app_title, _("no_next_item"))

    def prev_note(self, event=None):
        idx = self.root.indexOfChild(self.activeitem)
        if idx > 0:
            self.tree.setCurrentItem(self.root.child(idx - 1))
        else:
            wdg.QMessageBox.information(self, app_title, _("no_prev_item"))

    def check_active(self, message=None):
        if self.activeitem and self.activeitem != self.root:
            font = self.activeitem.font(0)
            font.setBold(False)
            self.activeitem.setFont(0, font)
            if self.editor.document().isModified:
                if message:
                    print(message)
                self.activeitem.setText(1,self.editor.toPlainText())

    def activate_item(self, item):
        self.editor.clear()
        if not item:
            return
        self.activeitem = item
        if item != self.root:
            font = item.font(0)
            font.setBold(True)
            item.setFont(0, font)
            self.editor.setText(item.text(1))
            self.editor.setEnabled(True)
        else:
            self.editor.setEnabled(False)

    def info_page(self,event=None):
        wdg.QMessageBox.information(self, app_title, _("info_text"))

    def help_page(self,event=None):
        ## gui.QMessageBox.information(self, app_title, _("help_text"))
        ## return
        dlg = wdg.QDialog(self)
        data = [x.split(' - ', 1) for x in _("help_text").split('\n')]
        gbox = wdg.QGridLayout()
        line = 0
        for left, right in data:
            gbox.addWidget(wdg.QLabel(left, self), line, 0)
            gbox.addWidget(wdg.QLabel(right, self), line, 1)
            line += 1
        dlg.setWindowTitle(app_title + " " + _("t_keys")) # ' keys'
        dlg.setLayout(gbox)
        dlg.exec_()

    def choose_language(self, event=None):
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        data = [(code, _('t_{}'.format(code))) for code in ('nl', 'en')]
        for idx, lang in enumerate([x[0] for x in data]):
            if lang == self.opts["Language"]:
                break
        text, ok = wdg.QInputDialog.getItem(self, app_title, _("t_lang"),
            [x[1] for x in data], current=idx, editable=False)
        if ok:
            for idx, lang in enumerate([x[1] for x in data]):
                if lang == text:
                    code = data[idx][0]
                    self.opts["Language"] = code
                    languages[code].install()
                    self.create_menu()
                    break

    def link_keywords(self, event=None):
        """Open a dialog where keywords can be assigned to the text
        """
        test = self.activeitem
        if test is None: return
        if test.data(1, core.Qt.UserRole) is None: return
        dlg = KeywordsDialog(self)
        ok = dlg.exec_()
        if ok == wdg.QDialog.Accepted:
            self.activeitem.setData(1, core.Qt.UserRole, self.new_keywords)

    def no_selection(self, event=None):
        """make sure nothing is selected"""
        self.opts["Selection"] = (0, "")
        self.sb.showMessage(_("h_selall"))
        item_to_activate = self.build_tree()
        self.tree.setCurrentItem(item_to_activate)

    def keyword_select(self, event=None):
        """Open a dialog where a keyword can be chosen to select texts that it's
        assigned to
        """
        seltype, seltext = self.opts['Selection']
        if seltype != 1:
            seltext = ''
        selection_list = self.opts['Keywords']
        try:
            selindex = selection_list.index(seltext)
        except ValueError:
            selindex = -1
        text, ok = wdg.QInputDialog.getItem(self, app_title,
            _("i_seltag"), selection_list, current=selindex)
        if ok:
            self.opts['Selection'] = (1, text)
            self.sb.showMessage(_("s_seltag").format(text))
            item_to_activate = self.build_tree()
            self.tree.setCurrentItem(item_to_activate)

    def text_select(self, event=None):
        """Open a dialog box where text can be entered that the texts to be selected
        contain
        """
        seltype, seltext = self.opts['Selection']
        if seltype != 2:
            seltext = ''
        text, ok = wdg.QInputDialog.getText(self, app_title,
            _("i_seltxt"), wdg.QLineEdit.Normal, seltext)
        if ok:
            self.opts['Selection'] = (2, text)
            self.sb.showMessage(_("s_seltxt").format(text))
            item_to_activate = self.build_tree()
            self.tree.setCurrentItem(item_to_activate)



def main(fnaam):
    ## self.fn = fnaam
    app = wdg.QApplication(sys.argv)
    frame = MainWindow(parent=None, title=" - ".join((fnaam, app_title)))
    frame.show()
    frame.project_file = fnaam
    mld = frame.open()
    if mld:
        wdg.QMessageBox.information(frame, "Error", mld)
    else:
        sys.exit(app.exec_())
