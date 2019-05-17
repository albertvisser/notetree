"""NoteTree PyQt5 versie

van een ibm site afgeplukt
"""
import os
import sys
import logging
import gettext
from datetime import datetime
import PyQt5.QtWidgets as wdg
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
from .notetree_shared import NoteTreeMixin, app_title, root_title, languages
logging.basicConfig(filename='doctree_qt.log', level=logging.DEBUG,
                    format='%(asctime)s %(message)s')


class KeywordsManager(wdg.QDialog):
    """Dialoog voor het wijzigen van trefwoorden
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle('{} - {}'.format(app_title, _("t_tagman")))
        self.setWindowIcon(self.parent.nt_icon)
        self.resize(400, 0)
        self.oldtag = wdg.QComboBox(self, editable=True)
        self.newtag = wdg.QLineEdit(self)
        self.newtag.setMinimumHeight(self.oldtag.height())
        self.refresh_fields()
        remove_button = wdg.QPushButton(_("b_remtag"), self)
        remove_button.clicked.connect(self.remove_keyword)
        add_button = wdg.QPushButton(_('b_addtag'), self)
        add_button.clicked.connect(self.add_keyword)
        done_button = wdg.QPushButton(_("b_done"), self)
        done_button.clicked.connect(self.accept)
        vbox = wdg.QVBoxLayout()
        gbox = wdg.QGridLayout()
        gbox.addWidget(wdg.QLabel(_('l_oldval')), 0, 0)
        gbox.addWidget(self.oldtag, 0, 1)
        gbox.addWidget(remove_button, 0, 2)
        gbox.addWidget(wdg.QLabel(_('l_newval')), 1, 0)
        gbox.addWidget(self.newtag, 1, 1)
        gbox.addWidget(add_button, 1, 2)
        vbox.addLayout(gbox)
        hbox = wdg.QHBoxLayout()
        ## hbox.addWidget(wdg.QStaticText('Changes are applied immediately'))
        hbox.addWidget(wdg.QLabel(_('t_applied')))
        vbox.addLayout(hbox)
        hbox = wdg.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(done_button)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def refresh_fields(self):
        """initialize items on screen
        """
        self.oldtag.clear()
        self.oldtag.addItems(self.parent.opts['Keywords'])
        self.oldtag.clearEditText()
        self.newtag.clear()

    def update_items(self, oldtext, newtext=''):
        """refresh list of associated keywords
        """
        for ix in range(self.parent.root.childCount()):
            item = self.parent.root.child(ix)
            keywords = item.data(1, core.Qt.UserRole)
            try:
                ix = keywords.index(oldtext)
            except ValueError:
                continue
            if newtext:
                keywords[ix] = newtext
            else:
                keywords.pop(ix)
            item.setData(1, core.Qt.UserRole, keywords)

    def remove_keyword(self):
        """delete a keyword aftre selecting from the dropdown
        """
        oldtext = self.oldtag.currentText()
        msg = _('t_remtag').format(oldtext)
        ask = wdg.QMessageBox.question(self, app_title, msg)
        if ask != wdg.QMessageBox.Yes:
            return
        self.parent.opts['Keywords'].remove(oldtext)
        self.update_items(oldtext)
        self.refresh_fields()

    def add_keyword(self):
        """Add a new keyword or change an existing one after selecting from the dropdown
        """
        oldtext = self.oldtag.currentText()
        newtext = self.newtag.text()
        if oldtext:
            prompter = wdg.QMessageBox()
            prompter.setText(_('t_repltag').format(oldtext, newtext))
            prompter.setInformativeText(_('t_repltag2'))
            prompter.setStandardButtons(wdg.QMessageBox.Yes | wdg.QMessageBox.No |
                                        wdg.QMessageBox.Cancel)
            prompter.setDefaultButton(wdg.QMessageBox.Yes)
            ## prompter.setEscapeButton(wdg.MessageBox.Cancel)
            ask = prompter.exec_()
            if ask == wdg.QMessageBox.Cancel:
                return
            ix = self.parent.opts['Keywords'].index(oldtext)
            self.parent.opts['Keywords'][ix] = newtext
            if ask == wdg.QMessageBox.Yes:
                self.update_items(oldtext, newtext)
            else:
                self.update_items(oldtext)
        else:
            msg = _('t_addtag').format(newtext)
            ask = wdg.QMessageBox.question(self, app_title, msg)
            if ask != wdg.QMessageBox.Yes:
                return
            self.parent.opts['Keywords'].append(newtext)
        self.refresh_fields()


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
        self.fromlist.setSelectionMode(wdg.QAbstractItemView.ExtendedSelection)
        self.fromlist.itemDoubleClicked.connect(self.move_right)
        text = wdg.QLabel(_("t_tags"), self)
        fromto_button = wdg.QPushButton(_("b_tag"))
        fromto_button.clicked.connect(self.move_right)
        tofrom_button = wdg.QPushButton(_("b_untag"))
        tofrom_button.clicked.connect(self.move_left)
        addtrefw_button = wdg.QPushButton(_("b_newtag"))
        addtrefw_button.clicked.connect(self.add_trefw)
        help_button = wdg.QPushButton(_("m_keys"))
        help_button.clicked.connect(self.keys_help)
        self.tolist = wdg.QListWidget(self)
        self.tolist.setSelectionMode(wdg.QAbstractItemView.ExtendedSelection)
        self.tolist.itemDoubleClicked.connect(self.move_left)
        bbox = wdg.QDialogButtonBox(wdg.QDialogButtonBox.Ok | wdg.QDialogButtonBox.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        self.create_actions()
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
        vbox2.addWidget(help_button)
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

    def create_actions(self):
        """define what can be done in this screen
        """
        self.actionlist = ((_('a_from'), 'Ctrl+L', self.activate_left),
                           (_('b_tag'), 'Ctrl+Right', self.move_right),
                           (_('a_to'), 'Ctrl+R', self.activate_right),
                           (_('b_untag'), 'Ctrl+Left', self.move_left),
                           (_('b_newtag'), 'Ctrl+N', self.add_trefw))
        for name, shortcut, callback in self.actionlist:
            act = wdg.QAction(name, self)
            act.setShortcut(shortcut)
            act.triggered.connect(callback)
            self.addAction(act)

    def activate_left(self):
        """activate "from" list
        """
        self._activate(self.fromlist)

    def activate_right(self):
        """activate "to" list
        """
        self._activate(self.tolist)

    def _activate(self, win):
        """set focus to list
        """
        item = win.currentItem()
        if not item:
            item = win.item(0)
        item.setSelected(True)
        win.setFocus(True)

    def move_right(self):
        """trefwoord selecteren
        """
        self._moveitem(self.fromlist, self.tolist)

    def move_left(self):
        """trefwoord on-selecteren
        """
        self._moveitem(self.tolist, self.fromlist)

    def _moveitem(self, from_, to):
        """trefwoord verplaatsen van de ene lijst naar de andere
        """
        selected = from_.selectedItems()
        for item in selected:
            from_.takeItem(from_.row(item))
            to.addItem(item)

    def add_trefw(self):
        """nieuwe trefwoorden opgeven en direct in de linkerlijst zetten
        """
        text, ok = wdg.QInputDialog.getText(self, app_title, _('t_newtag'))
        if ok:
            self.parent.opts["Keywords"].append(text)
            self.tolist.addItem(text)

    def keys_help(self):
        """Show possible actions and accelerator keys
        """
        dlg = wdg.QDialog(self)
        data = [x.split(' - ', 1) for x in _('tag_help').split('\n')]
        gbox = wdg.QGridLayout()
        line = 0
        for left, right in data:
            gbox.addWidget(wdg.QLabel(left, self), line, 0)
            gbox.addWidget(wdg.QLabel(right, self), line, 1)
            line += 1
        dlg.setWindowTitle(app_title + " " + _("t_keys"))  # ' keys'
        dlg.setLayout(gbox)
        dlg.exec_()

    def accept(self):
        """geef de geselecteerde trefwoorden aan het hoofdprogramma
        """
        self.parent.new_keywords = [self.tolist.item(i).text() for i in range(
            len(self.tolist))]
        super().accept()


class GetTextDialog(wdg.QDialog):
    """Dialog to get search string (with options)
    """
    def __init__(self, parent, seltype, seltext, labeltext='', use_case=None):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(app_title)
        self.setWindowIcon(self.parent.nt_icon)

        self.create_inputwin(seltext)

        self.in_exclude = wdg.QCheckBox('exclude', self)
        self.in_exclude.setChecked(False)
        if seltype < 0:
            self.in_exclude.setChecked(True)

        vbox = wdg.QVBoxLayout()
        hbox = wdg.QHBoxLayout()
        hbox.addWidget(wdg.QLabel(labeltext, self))
        vbox.addLayout(hbox)
        hbox = wdg.QHBoxLayout()
        hbox.addWidget(self.inputwin)
        vbox.addLayout(hbox)
        hbox = wdg.QHBoxLayout()
        hbox.addWidget(self.in_exclude)
        if self.use_case:
            hbox.addWidget(self.use_case)
            if use_case:
                self.use_case.setChecked(True)
        vbox.addLayout(hbox)
        bbox = wdg.QDialogButtonBox(wdg.QDialogButtonBox.Ok | wdg.QDialogButtonBox.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        vbox.addWidget(bbox)
        self.setLayout(vbox)

    def create_inputwin(self, seltext):
        """define the widgets to use
        """
        self.inputwin = wdg.QLineEdit(self)
        self.inputwin.setText(seltext)
        self.use_case = wdg.QCheckBox('case_sensitive', self)
        self.use_case.setChecked(False)

    def accept(self):
        """confirm data changes and communicate to parent window
        """
        try:
            seltext = self.inputwin.text()
        except AttributeError:
            seltext = self.inputwin.currentText()
        self.parent.dialog_data = [self.in_exclude.isChecked(), seltext]
        if self.use_case:
            self.parent.dialog_data.append(self.use_case.isChecked())
        super().accept()


class GetItemDialog(GetTextDialog):
    """Dialog to select a keyword from a list
    """
    def create_inputwin(self, seltext):
        """define the widgets to use
        """
        selection_list = self.parent.opts['Keywords']
        try:
            selindex = selection_list.index(seltext)
        except ValueError:
            selindex = -1
        self.inputwin = wdg.QComboBox(self)
        self.inputwin.addItems(selection_list)
        self.inputwin.setCurrentIndex(selindex)
        self.use_case = None


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

    def klaar(self):
        "dialoog afsluiten"
        if self.check.isChecked():
            self.parent.opts["AskBeforeHide"] = False
        super().done(0)


class MainWindow(wdg.QMainWindow, NoteTreeMixin):
    """Application main screen
    """
    def __init__(self, title=''):
        super().__init__()

        self.nt_icon = gui.QIcon(os.path.join(os.path.dirname(__file__), "notetree.ico"))
        self.setWindowIcon(self.nt_icon)
        self.resize(800, 500)
        self.setWindowTitle(title)
        self.sb = self.statusBar()

        self.tray_icon = wdg.QSystemTrayIcon(self.nt_icon, self)
        self.tray_icon.setToolTip(_("revive_message"))
        self.tray_icon.activated.connect(self.revive)
        self.tray_icon.hide()

        ## self.create_menu()

        self.splitter = wdg.QSplitter(self)
        self.setCentralWidget(self.splitter)

        self.tree = wdg.QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.hideColumn(1)
        self.tree.headerItem().setHidden(True)
        self.tree.setSelectionMode(wdg.QTreeWidget.SingleSelection)
        self.splitter.addWidget(self.tree)
        self.tree.itemSelectionChanged.connect(self.changeselection)

        self.editor = wdg.QTextEdit(self)
        self.editor.setEnabled(False)
        self.splitter.addWidget(self.editor)

    def create_menu(self):
        """build the application menu
        """
        menu_bar = self.menuBar()
        menu_bar.clear()
        self.selactions = {}
        self.seltypes = []
        for item, data in self.get_menudata():  # defined in mixin class
            menu_label = item
            submenu = menu_bar.addMenu(menu_label)
            for label, handler, info, key in data:
                if label:
                    action = submenu.addAction(label, handler)
                    if menu_label == _("m_view"):
                        if label != _("m_revorder"):
                            self.seltypes.append(label)
                        action.setCheckable(True)
                        self.selactions[label] = action
                    if key:
                        action.setShortcuts([x for x in key.split(",")])
                    action.setStatusTip(info)
                else:
                    submenu.addSeparator()
        for action in self.selactions.values():
            action.setChecked(False)
        self.selactions[_("m_revorder")].setChecked(self.opts['RevOrder'])
        self.selactions[self.seltypes[abs(self.opts["Selection"][0])]].setChecked(
            True)

    def changeselection(self):
        """adjust to the selected tree item
        """
        test = self.tree.selectedItems()
        if test == self.root:
            return
        self.check_active()
        h = self.tree.currentItem()
        self.activate_item(h)

    def closeEvent(self, event=None):
        """reimplemented callback
        """
        self.update()
        event.accept()

    def open(self):
        """read a file from disk and turn it into a tree structure
        """
        msg = NoteTreeMixin.open(self, "Qt", root_title)
        if msg:
            self.showmsg(msg)
            return
        # recreate menu after loading (because of language)
        self.create_menu()
        self.root = self.tree.takeTopLevelItem(0)
        self.root = wdg.QTreeWidgetItem()
        self.root.setText(0, self.opts["RootTitle"])
        self.tree.addTopLevelItem(self.root)
        self.activeitem = item_to_activate = self.root
        self.editor.clear()
        self.editor.setEnabled(False)
        item_to_activate = self.build_tree(first_time=True)
        self.resize(*self.opts["ScreenSize"])
        try:
            self.splitter.restoreState(self.opts['SashPosition'])
        except TypeError:
            wdg.QMessageBox.information(self, app_title, 'Ignoring incompatible sash position')
        self.root.setExpanded(True)
        self.tree.setCurrentItem(item_to_activate)
        self.tree.setFocus()

    def build_tree(self, first_time=False):
        """translate the dictionary read to a tree structure
        """
        if not first_time:
            self.tree_to_dict()
            self.root = self.tree.takeTopLevelItem(0)
            self.root = wdg.QTreeWidgetItem()
            self.root.setText(0, self.opts["RootTitle"])
            self.tree.addTopLevelItem(self.root)
        item_to_activate = self.root
        self.activeitem = None
        ## seltype = 0
        seltype, seldata = self.opts["Selection"][:2]
        use_case = None
        if len(self.opts["Selection"]) > 2:
            use_case = self.opts["Selection"][2]
        for key, value in self.nt_data.items():
            if key == 0:
                continue
            tag, text, keywords = value
            if seltype == 1 and seldata not in keywords:
                continue
            if seltype == 2:
                ok = False
                if use_case and seldata in text:
                    ok = True
                elif not use_case and seldata.upper() in text.upper():
                    ok = True
                if not ok:
                    continue
            if seltype == -1 and seldata in keywords:
                continue
            if seltype == -2:
                ok = True
                if use_case and seldata in text:
                    ok = False
                elif not use_case and seldata.upper() in text.upper():
                    ok = False
                if not ok:
                    continue
            item = wdg.QTreeWidgetItem()
            if not item_to_activate:  # make sure this is only set to root if selection is empty
                item_to_activate = item
            item.setText(0, tag)
            item.setData(0, core.Qt.UserRole, key)
            item.setText(1, text)
            item.setData(1, core.Qt.UserRole, keywords)
            if self.opts['RevOrder']:
                self.root.insertChild(0, item)
            else:
                self.root.addChild(item)
            if key == self.opts["ActiveItem"]:
                item_to_activate = item
        ## for action in self.selactions.values():
            ## action.setChecked(False)
        ## self.selactions[self.seltypes[seltype]].setChecked(True)
        self.tree.expandItem(self.root)
        return item_to_activate

    def reread(self):
        """revert to the saved version of the notes file
        """
        dlg = wdg.QMessageBox.question(self, app_title, _("ask_reload"),
                                       wdg.QMessageBox.Yes | wdg.QMessageBox.No)
        if dlg == wdg.QMessageBox.Yes:
            self.open()

    def tree_to_dict(self):
        """translate the entire tree structure to a dictionary suitable for saving
        """
        self.check_active()  # even zorgen dat de editor inhoud geassocieerd wordt
        for num in range(self.root.childCount()):
            tag = self.root.child(num).text(0)
            ky = self.root.child(num).data(0, core.Qt.UserRole)
            text = self.root.child(num).text(1)
            trefw = self.root.child(num).data(1, core.Qt.UserRole)
            self.nt_data[ky] = (str(tag), str(text), trefw)

    def update(self):
        """resave the notes to a file
        """
        self.tree_to_dict()  # check for changed values in tree not in dict
        self.opts["ScreenSize"] = self.width(), self.height()  # tuple(self.size())
        self.opts["SashPosition"] = self.splitter.saveState()
        self.opts["ActiveItem"] = self.activeitem.data(0, core.Qt.UserRole)
        NoteTreeMixin.save(self)

    def rename(self):
        """ask for a new title for the root item
        """
        text, ok = wdg.QInputDialog.getText(self, app_title, _("t_root"),
                                            wdg.QLineEdit.Normal, self.root.text(0))
        if ok:
            self.opts["RootTitle"] = text
            self.root.setText(0, text)

    def hide_me(self):
        """Minimize application to an icon in the system tray
        """
        if self.opts["AskBeforeHide"]:
            dlg = CheckDialog(self)
            dlg.exec_()
        self.tray_icon.show()
        self.hide()

    def revive(self, event=None):
        """make application visible again
        """
        if event == wdg.QSystemTrayIcon.Unknown:
            self.tray_icon.showMessage(app_title, _("revive_message"))
        elif event == wdg.QSystemTrayIcon.Context:
            pass
        else:
            self.show()
            self.tray_icon.hide()

    def new_item(self):
        """add a new item to the tree after asking for a title
        """
        start = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        text, ok = wdg.QInputDialog.getText(self, app_title, _("t_new"), text=start)
        if ok:
            item = wdg.QTreeWidgetItem()
            item.setText(0, text)
            item.setData(0, core.Qt.UserRole, text)
            item.setText(1, "")
            item.setData(1, core.Qt.UserRole, [])
            if self.opts['RevOrder']:
                self.root.insertChild(0, item)
            else:
                self.root.addChild(item)
            self.nt_data[text] = ""
            self.tree.setCurrentItem(item)
            self.root.setExpanded(True)
            self.editor.clear()
            self.editor.setEnabled(True)
            self.editor.setFocus()

    def delete_item(self):
        """remove item from tree
        """
        item = self.tree.currentItem()
        if item != self.root:
            ## idx = self.root.indexOfChild(item)
            self.root.removeChild(item)
            ky = item.data(0, core.Qt.UserRole)
            del self.nt_data[ky]
        else:
            self.showmsg(_("no_delete_root"))

    def ask_title(self):
        """Get/change a title for this note
        """
        text, ok = wdg.QInputDialog.getText(self, app_title, _("t_name"),
                                            wdg.QLineEdit.Normal, self.activeitem.text(0))
        if ok:
            self.activeitem.setText(0, text)

    def next_note(self):
        """Go to next
        """
        idx = self.root.indexOfChild(self.activeitem)
        if idx < self.root.childCount() - 1:
            self.tree.setCurrentItem(self.root.child(idx + 1))
        else:
            self.showmsg(_("no_next_item"))

    def prev_note(self):
        """Go to previous
        """
        idx = self.root.indexOfChild(self.activeitem)
        if idx > 0:
            self.tree.setCurrentItem(self.root.child(idx - 1))
        else:
            self.showmsg(_("no_prev_item"))

    def check_active(self, message=None):
        """if there's a suitable "active" item, make sure its text is saved to the tree structure

        """
        if self.activeitem and self.activeitem != self.root:
            font = self.activeitem.font(0)
            font.setBold(False)
            self.activeitem.setFont(0, font)
            if self.editor.document().isModified:
                if message:
                    self.showmsg(message)
                self.activeitem.setText(1, self.editor.toPlainText())

    def activate_item(self, item):
        """make the new item "active" and get the text for itfrom the tree structure
        """
        self.editor.clear()
        if not item:
            return
        self.activeitem = item
        if item == self.root:
            self.editor.setEnabled(False)
        else:
            font = item.font(0)
            font.setBold(True)
            item.setFont(0, font)
            self.editor.setText(item.text(1))
            self.editor.setEnabled(True)

    def info_page(self):
        """show program info
        """
        self.showmsg(_("info_text"))

    def help_page(self):
        """show keyboard shortcuts
        """
        ## self.showmsg(_("help_text"))
        dlg = wdg.QDialog(self)
        data = [x.split(' - ', 1) for x in _("help_text").split('\n')]
        gbox = wdg.QGridLayout()
        line = 0
        for left, right in data:
            gbox.addWidget(wdg.QLabel(left, self), line, 0)
            gbox.addWidget(wdg.QLabel(right, self), line, 1)
            line += 1
        dlg.setWindowTitle(app_title + " " + _("t_keys"))  # ' keys'
        dlg.setLayout(gbox)
        dlg.exec_()

    def choose_language(self):
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        data = [(code, _('t_{}'.format(code))) for code in ('nl', 'en')]
        for idx, lang in enumerate([x[0] for x in data]):
            if lang == self.opts["Language"]:
                break
        text, ok = wdg.QInputDialog.getItem(self, app_title, _("t_lang"),
                                            [x[1] for x in data], current=idx,
                                            editable=False)
        if ok:
            for idx, lang in enumerate([x[1] for x in data]):
                if lang == text:
                    code = data[idx][0]
                    self.opts["Language"] = code
                    languages[code].install()
                    self.create_menu()
                    break

    def link_keywords(self):
        """Open a dialog where keywords can be assigned to the text
        """
        test = self.activeitem
        if test is None:
            return
        if test.data(1, core.Qt.UserRole) is None:
            return
        dlg = KeywordsDialog(self)
        ok = dlg.exec_()
        if ok == wdg.QDialog.Accepted:
            self.activeitem.setData(1, core.Qt.UserRole, self.new_keywords)

    def manage_keywords(self):
        """Open a dialog where keywords can be renamed, removed or added
        """
        dlg = KeywordsManager(self)
        dlg.exec_()

    def reverse(self):
        """set to "newest first"
        """
        self.opts['RevOrder'] = not self.opts['RevOrder']
        item_to_activate = self.build_tree()
        self.tree.setCurrentItem(item_to_activate)

    def no_selection(self):
        """make sure nothing is selected
        """
        self.opts["Selection"] = (0, "")
        self.sb.showMessage(_("h_selall"))
        item_to_activate = self.build_tree()
        self.tree.setCurrentItem(item_to_activate)
        for text, action in self.selactions.items():
            if text == _("m_selall"):
                action.setChecked(True)
            elif text != _("m_revorder"):
                action.setChecked(False)

    def keyword_select(self):
        """Open a dialog where a keyword can be chosen to select texts that it's assigned to
        """
        seltype, seltext = self.opts['Selection'][:2]
        if abs(seltype) != 1:
            seltext = ''
        ## selection_list = self.opts['Keywords']
        ## try:
            ## selindex = selection_list.index(seltext)
        ## except ValueError:
            ## selindex = -1
        ## text, ok = wdg.QInputDialog.getItem(self, app_title,
            ## _("i_seltag"), selection_list, current=selindex)
        ok = GetItemDialog(self, seltype, seltext, _("i_seltag")).exec_()
        if ok:
            exclude, text = self.dialog_data
            ## self.opts['Selection'] = (1, text)
            if exclude:
                seltype, in_ex = -1, "all except"
            else:
                seltype, in_ex = 1, 'only'
            self.opts['Selection'] = (seltype, text)
            self.sb.showMessage(_("s_seltag").format(in_ex, text))
            item_to_activate = self.build_tree()
            self.tree.setCurrentItem(item_to_activate)
            for text, action in self.selactions.items():
                if text == _("m_seltag"):
                    action.setChecked(True)
                elif text != _("m_revorder"):
                    action.setChecked(False)
        # bij Cancel menukeuze weer aan/uitzetten
        elif abs(seltype) == 1:
            self.selactions[_("m_seltag")].setChecked(True)
        else:
            self.selactions[_("m_seltag")].setChecked(False)

    def text_select(self):
        """Open a dialog box where text can be entered that the texts to be selected contain
        """
        try:
            seltype, seltext, use_case = self.opts['Selection']
        except ValueError:
            seltype, seltext = self.opts['Selection']
            use_case = None
        if abs(seltype) != 2:
            seltext = ''
        ## text, ok = wdg.QInputDialog.getText(self, app_title,
            ## _("i_seltxt"), wdg.QLineEdit.Normal, seltext)
        ok = GetTextDialog(self, seltype, seltext, _("i_seltxt"), use_case).exec_()
        if ok:
            exclude, text, use_case = self.dialog_data
            ## self.opts['Selection'] = (2, text)
            if exclude:
                seltype, in_ex = -2, "all except"
            else:
                seltype, in_ex = 2, 'only'
            self.opts['Selection'] = (seltype, text, use_case)
            self.sb.showMessage(_("s_seltxt").format(in_ex, text))
            item_to_activate = self.build_tree()
            self.tree.setCurrentItem(item_to_activate)
            for text, action in self.selactions.items():
                if text == _("m_seltxt"):
                    action.setChecked(True)
                elif text != _("m_revorder"):
                    action.setChecked(False)
        # bij Cancel menukeuze weer aan/uitzetten
        elif abs(seltype) == 2:
            self.selactions[_("m_seltxt")].setChecked(True)
        else:
            self.selactions[_("m_seltxt")].setChecked(False)

    def showmsg(self, message):
        """show a message with the standard title
        """
        wdg.QMessageBox.information(self, app_title, message)


def main(fnaam):
    """application start
    """
    app = wdg.QApplication(sys.argv)
    frame = MainWindow(title=" - ".join((fnaam, app_title)))
    frame.show()
    frame.project_file = fnaam
    mld = frame.open()
    if mld:
        ## wdg.QMessageBox.information(frame, "Error", mld)
        frame.close()
        print(mld)
    else:
        sys.exit(app.exec_())
