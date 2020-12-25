"""NoteTree PyQt5 versie

van een ibm site afgeplukt
"""
import os
import sys
import gettext
from datetime import datetime
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core


class MainWindow(qtw.QMainWindow):
    """Application main screen
    """
    def __init__(self, root):
        self.base = root
        self.app = qtw.QApplication(sys.argv)
        self.activeitem = None

    def start(self):
        "start the GUI"
        sys.exit(self.app.exec_())

    def build_screen(self, title, iconame):
        "setup screen"
        super().__init__()

        self.setWindowTitle(title)
        self.nt_icon = gui.QIcon(iconame)
        self.setWindowIcon(self.nt_icon)
        self.resize(800, 500)
        self.sb = self.statusBar()

        self.tray_icon = qtw.QSystemTrayIcon(self.nt_icon, self)
        self.tray_icon.setToolTip(_("revive_message"))
        self.tray_icon.activated.connect(self.revive)
        self.tray_icon.hide()

        ## self.create_menu()

        self.splitter = qtw.QSplitter(self)
        self.setCentralWidget(self.splitter)

        self.tree = qtw.QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.hideColumn(1)
        self.tree.headerItem().setHidden(True)
        self.tree.setSelectionMode(qtw.QTreeWidget.SingleSelection)
        self.splitter.addWidget(self.tree)
        self.tree.itemSelectionChanged.connect(self.changeselection)

        self.editor = qtw.QTextEdit(self)
        self.editor.setEnabled(False)
        self.splitter.addWidget(self.editor)
        self.show()

    def create_menu(self):
        """build the application menu
        """
        menu_bar = self.menuBar()
        menu_bar.clear()
        self.selactions = {}
        self.seltypes = []
        for item, data in self.base.get_menudata():  # defined in mixin class
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
        self.selactions[_("m_revorder")].setChecked(self.base.opts['RevOrder'])
        self.selactions[self.seltypes[abs(self.base.opts["Selection"][0])]].setChecked(True)

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
        if self.activeitem:
            self.update()
        event.accept()

    def init_editor(self):
        self.editor.clear()
        self.editor.setEnabled(False)

    def set_screen(self, screensize):
        self.resize(screensize)

    def set_splitter(self, split):
        self.splitter.setSizes(split)

    def create_root(self, title):
        self.root = self.tree.takeTopLevelItem(0)
        self.root = qtw.QTreeWidgetItem()
        self.root.setText(0, title)
        self.tree.addTopLevelItem(self.root)
        self.activeitem = self.root
        return self.root

    def set_item_expanded(self, item):
        item.setExpanded(True)

    def activate_item(self, item):
        self.tree.setCurrentItem(item)

    def set_focus_to_tree(self)
        self.tree.setFocus()

    def add_item_to_tree(key, tag, text, keywords, revorder):
        item = qtw.QTreeWidgetItem()
        item.setText(0, tag)
        item.setData(0, core.Qt.UserRole, key)
        item.setText(1, text)
        item.setData(1, core.Qt.UserRole, keywords)
        if self.base.opts['RevOrder']:
            self.root.insertChild(0, item)
        else:
            self.root.addChild(item)
        return item

    def get_treeitems(self):
        treeitemlist = []
        for num in range(self.root.childCount()):
            tag = self.root.child(num).text(0)
            ky = self.root.child(num).data(0, core.Qt.UserRole)
            if ky == self.activeitem:
                activeitem = ky
            text = self.root.child(num).text(1)
            trefw = self.root.child(num).data(1, core.Qt.UserRole)
            treeitemlist.append((ky, tag, text, trefw))
        return treeitemlist, activeitem

    def get_screensize(self):
        return self.width(), self.height()

    def get_splitterpos(self):
        return self.splitter.sizes()

    def get_activeitem(self):
        return self.activeitem.data(0, core.Qt.UserRole)

    def hide_me(self):
        """Minimize application to an icon in the system tray
        """
        if self.base.opts["AskBeforeHide"]:
            dlg = CheckDialog(self)
            dlg.exec_()
        self.tray_icon.show()
        self.hide()

    def revive(self, event=None):
        """make application visible again
        """
        if event == qtw.QSystemTrayIcon.Unknown:
            self.tray_icon.showMessage(self.base.app_title, _("revive_message"))
        elif event == qtw.QSystemTrayIcon.Context:
            pass
        else:
            self.show()
            self.tray_icon.hide()

    def new_item(self):
        """add a new item to the tree after asking for a title
        """
        start = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
        text, ok = qtw.QInputDialog.getText(self, self.base.app_title, _("t_new"), text=start)
        if ok:
            item = qtw.QTreeWidgetItem()
            item.setText(0, text)
            item.setData(0, core.Qt.UserRole, text)
            item.setText(1, "")
            item.setData(1, core.Qt.UserRole, [])
            if self.base.opts['RevOrder']:
                self.root.insertChild(0, item)
            else:
                self.root.addChild(item)
            self.base.nt_data[text] = ""
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
            del self.base.nt_data[ky]
        else:
            self.showmsg(_("no_delete_root"))

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

    def choose_language(self):
        """toon dialoog om taal te kiezen en verwerk antwoord
        """
        data = [(code, _('t_{}'.format(code))) for code in ('nl', 'en')]
        for idx, lang in enumerate([x[0] for x in data]):
            if lang == self.base.opts["Language"]:
                break
        text, ok = qtw.QInputDialog.getItem(self, self.base.app_title, _("t_lang"),
                                            [x[1] for x in data], current=idx,
                                            editable=False)
        if ok:
            for idx, lang in enumerate([x[1] for x in data]):
                if lang == text:
                    code = data[idx][0]
                    self.base.opts["Language"] = code
                    self.base.languages[code].install()
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
        if ok == qtw.QDialog.Accepted:
            self.activeitem.setData(1, core.Qt.UserRole, self.new_keywords)

    def manage_keywords(self):
        """Open a dialog where keywords can be renamed, removed or added
        """
        dlg = KeywordsManager(self)
        dlg.exec_()

    def reverse(self):
        """set to "newest first"
        """
        self.base.opts['RevOrder'] = not self.base.opts['RevOrder']
        item_to_activate = self.build_tree()
        self.tree.setCurrentItem(item_to_activate)

    def no_selection(self):
        """make sure nothing is selected
        """
        self.base.opts["Selection"] = (0, "")
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
        seltype, seltext = self.base.opts['Selection'][:2]
        if abs(seltype) != 1:
            seltext = ''
        ## selection_list = self.base.opts['Keywords']
        ## try:
            ## selindex = selection_list.index(seltext)
        ## except ValueError:
            ## selindex = -1
        ## text, ok = qtw.QInputDialog.getItem(self, self.base.app_title,
            ## _("i_seltag"), selection_list, current=selindex)
        ok = GetItemDialog(self, seltype, seltext, _("i_seltag")).exec_()
        if ok:
            exclude, text = self.dialog_data
            ## self.base.opts['Selection'] = (1, text)
            if exclude:
                seltype, in_ex = -1, "all except"
            else:
                seltype, in_ex = 1, 'only'
            self.base.opts['Selection'] = (seltype, text)
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
            seltype, seltext, use_case = self.base.opts['Selection']
        except ValueError:
            seltype, seltext = self.base.opts['Selection']
            use_case = None
        if abs(seltype) != 2:
            seltext = ''
        ## text, ok = qtw.QInputDialog.getText(self, self.base.app_title,
            ## _("i_seltxt"), qtw.QLineEdit.Normal, seltext)
        ok = GetTextDialog(self, seltype, seltext, _("i_seltxt"), use_case).exec_()
        if ok:
            exclude, text, use_case = self.dialog_data
            ## self.base.opts['Selection'] = (2, text)
            if exclude:
                seltype, in_ex = -2, "all except"
            else:
                seltype, in_ex = 2, 'only'
            self.base.opts['Selection'] = (seltype, text, use_case)
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
        qtw.QMessageBox.information(self, self.base.app_title, message)

    def ask_question(self, parent, question):
        """ask a question in a standard box with a standard title"""
        answer = qtw.QMessageBox.question(self, self.base.app_title, question)
        return answer == qtw.QMessageBox.Yes

    def show_dialog(self, cls, *options):
        cls(self, *options).exec_()

    def get_text_from_user(self, prompt, default):
        return qtw.QInputDialog.getText(self, self.base.app_title, prompt,
                                        qtw.QLineEdit.Normal, default)


class OptionsDialog(qtw.QDialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, parent):
        self.parent = parent
        sett2text = {'AskBeforeHide': _('t_hide'),
                     'NotifyOnLoad': _('t_load'),
                     'NotifyOnSave': _('t_save') }
        super().__init__(parent)
        self.setWindowTitle(_('t_sett'))
        vbox = qtw.QVBoxLayout()
        self.controls = []

        gbox = qtw.QGridLayout()
        col = 0
        for key, value in self.parent.base.opts.items():
            if key not in sett2text:
                continue
            col += 1
            lbl = qtw.QLabel(sett2text[key], self)
            gbox.addWidget(lbl, col, 0)
            chk = qtw.QCheckBox('', self)
            chk.setChecked(value)
            gbox.addWidget(chk, col, 1)
            self.controls.append((key, chk))
        vbox.addLayout(gbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        ok_button = qtw.QPushButton(_("b_apply"), self)
        ok_button.clicked.connect(self.accept)
        hbox.addWidget(ok_button)
        cancel_button = qtw.QPushButton(_("b_close"), self)
        cancel_button.clicked.connect(self.reject)
        hbox.addWidget(cancel_button)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def accept(self):
        """overridden event handler
        """
        for keyvalue, control in self.controls:
            self.parent.base.opts[keyvalue] = control.isChecked()
        super().accept()


class CheckDialog(qtw.QDialog):
    """Dialoog om te melden dat de applicatie verborgen gaat worden
    AskBeforeHide bepaalt of deze getoond wordt of niet
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(self.parent.base.app_title)
        self.setWindowIcon(self.parent.nt_icon)
        txt = qtw.QLabel(_("sleep_message"), self)
        self.check = qtw.QCheckBox(_("hide_message"), self)
        ok_button = qtw.QPushButton("&Ok", self)
        ok_button.clicked.connect(self.klaar)

        vbox = qtw.QVBoxLayout()

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(txt)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.check)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addWidget(ok_button)
        hbox.insertStretch(0, 1)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        ## self.resize(574 + breedte, 480)

    def klaar(self):
        "dialoog afsluiten"
        if self.check.isChecked():
            self.parent.base.opts["AskBeforeHide"] = False
        super().done(0)


class KeywordsDialog(qtw.QDialog):
    """Dialoog voor het koppelen van trefwoorden
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle('{} - {}'.format(self.parent.base.app_title, _("w_tags")))
        self.setWindowIcon(self.parent.nt_icon)
        self.resize(400, 256)
        # define widgets
        self.fromlist = qtw.QListWidget(self)
        self.fromlist.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)
        self.fromlist.itemDoubleClicked.connect(self.move_right)
        text = qtw.QLabel(_("t_tags"), self)
        fromto_button = qtw.QPushButton(_("b_tag"))
        fromto_button.clicked.connect(self.move_right)
        tofrom_button = qtw.QPushButton(_("b_untag"))
        tofrom_button.clicked.connect(self.move_left)
        addtrefw_button = qtw.QPushButton(_("b_newtag"))
        addtrefw_button.clicked.connect(self.add_trefw)
        help_button = qtw.QPushButton(_("m_keys"))
        help_button.clicked.connect(self.keys_help)
        self.tolist = qtw.QListWidget(self)
        self.tolist.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)
        self.tolist.itemDoubleClicked.connect(self.move_left)
        bbox = qtw.QDialogButtonBox(wdg.QDialogButtonBox.Ok | wdg.QDialogButtonBox.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        self.create_actions()
        # get data from parent
        all_trefw = self.parent.base.opts['Keywords']
        self.data = self.parent.activeitem
        curr_trefw = self.data.data(1, core.Qt.UserRole)
        self.tolist.addItems(curr_trefw)
        self.fromlist.addItems([x for x in all_trefw if x not in curr_trefw])
        # do layout and show
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        vbox2 = qtw.QVBoxLayout()
        vbox2.addWidget(qtw.QLabel(_("t_left"), self))
        vbox2.addWidget(self.fromlist)
        hbox.addLayout(vbox2)
        vbox2 = qtw.QVBoxLayout()
        vbox2.addStretch()
        vbox2.addWidget(text)
        vbox2.addWidget(fromto_button)
        vbox2.addWidget(tofrom_button)
        vbox2.addSpacing(10)
        vbox2.addWidget(addtrefw_button)
        vbox2.addWidget(help_button)
        vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox2 = qtw.QVBoxLayout()
        vbox2.addWidget(qtw.QLabel(_("t_right"), self))
        vbox2.addWidget(self.tolist)
        hbox.addLayout(vbox2)
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
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
            act = qtw.QAction(name, self)
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
        text, ok = qtw.QInputDialog.getText(self, self.parent.base.app_title, _('t_newtag'))
        if ok:
            self.parent.base.opts["Keywords"].append(text)
            self.tolist.addItem(text)

    def keys_help(self):
        """Show possible actions and accelerator keys
        """
        dlg = qtw.QDialog(self)
        data = [x.split(' - ', 1) for x in _('tag_help').split('\n')]
        gbox = qtw.QGridLayout()
        line = 0
        for left, right in data:
            gbox.addWidget(qtw.QLabel(left, self), line, 0)
            gbox.addWidget(qtw.QLabel(right, self), line, 1)
            line += 1
        dlg.setWindowTitle(self.parent.base.app_title + " " + _("t_keys"))  # ' keys'
        dlg.setLayout(gbox)
        dlg.exec_()

    def accept(self):
        """geef de geselecteerde trefwoorden aan het hoofdprogramma
        """
        self.parent.new_keywords = [self.tolist.item(i).text() for i in range(
            len(self.tolist))]
        super().accept()


class KeywordsManager(qtw.QDialog):
    """Dialoog voor het wijzigen van trefwoorden
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle('{} - {}'.format(self.parent.base.app_title, _("t_tagman")))
        self.setWindowIcon(self.parent.nt_icon)
        self.resize(400, 0)
        self.oldtag = qtw.QComboBox(self, editable=True)
        self.newtag = qtw.QLineEdit(self)
        self.newtag.setMinimumHeight(self.oldtag.height())
        self.refresh_fields()
        remove_button = qtw.QPushButton(_("b_remtag"), self)
        remove_button.clicked.connect(self.remove_keyword)
        add_button = qtw.QPushButton(_('b_addtag'), self)
        add_button.clicked.connect(self.add_keyword)
        done_button = qtw.QPushButton(_("b_done"), self)
        done_button.clicked.connect(self.accept)
        vbox = qtw.QVBoxLayout()
        gbox = qtw.QGridLayout()
        gbox.addWidget(qtw.QLabel(_('l_oldval')), 0, 0)
        gbox.addWidget(self.oldtag, 0, 1)
        gbox.addWidget(remove_button, 0, 2)
        gbox.addWidget(qtw.QLabel(_('l_newval')), 1, 0)
        gbox.addWidget(self.newtag, 1, 1)
        gbox.addWidget(add_button, 1, 2)
        vbox.addLayout(gbox)
        hbox = qtw.QHBoxLayout()
        ## hbox.addWidget(qtw.QStaticText('Changes are applied immediately'))
        hbox.addWidget(qtw.QLabel(_('t_applied')))
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(done_button)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def refresh_fields(self):
        """initialize items on screen
        """
        self.oldtag.clear()
        self.oldtag.addItems(self.parent.base.opts['Keywords'])
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
        """delete a keyword after selecting from the dropdown
        """
        oldtext = self.oldtag.currentText()
        msg = _('t_remtag').format(oldtext)
        ask = qtw.QMessageBox.question(self, self.parent.base.app_title, msg)
        if ask != qtw.QMessageBox.Yes:
            return
        self.parent.base.opts['Keywords'].remove(oldtext)
        self.update_items(oldtext)
        self.refresh_fields()

    def add_keyword(self):
        """Add a new keyword or change an existing one after selecting from the dropdown
        """
        oldtext = self.oldtag.currentText()
        newtext = self.newtag.text()
        if oldtext:
            prompter = qtw.QMessageBox()
            prompter.setText(_('t_repltag').format(oldtext, newtext))
            prompter.setInformativeText(_('t_repltag2'))
            prompter.setStandardButtons(qtw.QMessageBox.Yes | wdg.QMessageBox.No |
                                        qtw.QMessageBox.Cancel)
            prompter.setDefaultButton(qtw.QMessageBox.Yes)
            ## prompter.setEscapeButton(qtw.MessageBox.Cancel)
            ask = prompter.exec_()
            if ask == qtw.QMessageBox.Cancel:
                return
            ix = self.parent.base.opts['Keywords'].index(oldtext)
            self.parent.base.opts['Keywords'][ix] = newtext
            if ask == qtw.QMessageBox.Yes:
                self.update_items(oldtext, newtext)
            else:
                self.update_items(oldtext)
        else:
            msg = _('t_addtag').format(newtext)
            ask = qtw.QMessageBox.question(self, self.parent.base.app_title, msg)
            if ask != qtw.QMessageBox.Yes:
                return
            self.parent.base.opts['Keywords'].append(newtext)
        self.refresh_fields()


class GetTextDialog(qtw.QDialog):
    """Dialog to get search string (with options)
    """
    def __init__(self, parent, seltype, seltext, labeltext='', use_case=None):
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(self.parent.base.app_title)
        self.setWindowIcon(self.parent.nt_icon)

        self.create_inputwin(seltext)

        self.in_exclude = qtw.QCheckBox('exclude', self)
        self.in_exclude.setChecked(False)
        if seltype < 0:
            self.in_exclude.setChecked(True)

        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(labeltext, self))
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.inputwin)
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.in_exclude)
        if self.use_case:
            hbox.addWidget(self.use_case)
            if use_case:
                self.use_case.setChecked(True)
        vbox.addLayout(hbox)
        bbox = qtw.QDialogButtonBox(wdg.QDialogButtonBox.Ok | wdg.QDialogButtonBox.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        vbox.addWidget(bbox)
        self.setLayout(vbox)

    def create_inputwin(self, seltext):
        """define the widgets to use
        """
        self.inputwin = qtw.QLineEdit(self)
        self.inputwin.setText(seltext)
        self.use_case = qtw.QCheckBox('case_sensitive', self)
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
        selection_list = self.parent.base.opts['Keywords']
        try:
            selindex = selection_list.index(seltext)
        except ValueError:
            selindex = -1
        self.inputwin = qtw.QComboBox(self)
        self.inputwin.addItems(selection_list)
        self.inputwin.setCurrentIndex(selindex)
        self.use_case = None


class GridDiaolog(qtw.QDialog):
    def __init__(self, title=''):
        super().__init__()
        data = [x.split(' - ', 1) for x in _("help_text").split('\n')]
        gbox = qtw.QGridLayout()
        line = 0
        for left, right in data:
            gbox.addWidget(qtw.QLabel(left, self), line, 0)
            gbox.addWidget(qtw.QLabel(right, self), line, 1)
            line += 1
        self.setWindowTitle(title)
        self.setLayout(gbox)
