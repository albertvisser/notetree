"""NoteTree PyQt5 versie

van een ibm site afgeplukt
"""
import os
import sys
import gettext
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gettext.install("NoteTree", os.path.join(HERE, 'locale'))


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

    def init_screen(self, title, iconame):
        "setup screen"
        super().__init__()
        self.setWindowTitle(title)
        self.nt_icon = gui.QIcon(iconame)
        self.setWindowIcon(self.nt_icon)
        self.resize(800, 500)

    def setup_statusbar(self):
        "define a statusbar"
        self.sb = self.statusBar()

    def setup_trayicon(self):
        "define an icon to put in the systray"
        self.tray_icon = qtw.QSystemTrayIcon(self.nt_icon, self)
        self.tray_icon.setToolTip(_("revive_message"))
        self.tray_icon.activated.connect(self.revive)
        self.tray_icon.hide()

    def setup_split_screen(self):
        "define the main splitter widget and place its components"
        self.splitter = qtw.QSplitter(self)
        self.setCentralWidget(self.splitter)
        self.splitter.addWidget(self.setup_tree())
        self.splitter.addWidget(self.setup_editor())
        self.show()

    def setup_tree(self):
        "define the tree panel"
        self.tree = qtw.QTreeWidget(self)
        self.tree.setColumnCount(2)
        self.tree.hideColumn(1)
        self.tree.headerItem().setHidden(True)
        self.tree.setSelectionMode(qtw.QTreeWidget.SingleSelection)
        self.tree.itemSelectionChanged.connect(self.changeselection)
        return self.tree

    def setup_editor(self):
        "define the editor panel"
        self.editor = qtw.QTextEdit(self)
        self.editor.setEnabled(False)
        return self.editor

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
        self.base.check_active()
        self.base.activate_item(self.tree.currentItem())

    def closeEvent(self, event=None):
        """reimplemented callback
        """
        if self.activeitem:
            self.base.update()
        event.accept()

    def clear_editor(self):
        'set up editor'
        self.editor.clear()
        self.editor.setEnabled(False)

    def open_editor(self):
        'open up editor'
        if self.activeitem != self.root:
            self.editor.setEnabled(True)

    def set_screen(self, screensize):
        'set application size'
        self.resize(*screensize)

    def set_splitter(self, split):
        'split screen at the specified position'
        self.splitter.setSizes(split)

    def create_root(self, title):
        'set up the root element'
        self.tree.takeTopLevelItem(0)
        self.root = qtw.QTreeWidgetItem()
        self.root.setText(0, title)  # self.base.opts['RootTitle']
        self.tree.addTopLevelItem(self.root)
        self.activeitem = self.root
        return self.root

    def set_item_expanded(self, item):
        "show the item's child elements"
        item.setExpanded(True)

    def emphasize_activeitem(self, value):
        "emphisize the active item's title"
        font = self.activeitem.font(0)
        font.setBold(value)
        self.activeitem.setFont(0, font)

    def editor_text_was_changed(self):
        "return the editor's state"
        return self.editor.document().isModified

    def copy_text_from_editor_to_activeitem(self):
        "transfer the editor's text to a treeitem"
        self.activeitem.setText(1, self.editor.toPlainText())

    def copy_text_from_activeitem_to_editor(self):
        "transfer a treeitem's text to the editor"
        self.editor.setText(self.activeitem.text(1))

    def select_item(self, item):
        "set selection"
        self.tree.setCurrentItem(item)

    def get_selected_item(self):
        "get selection"
        return self.tree.currentItem()

    def remove_item_from_tree(self, item):
        "remove an item from the tree and return it"
        self.root.removeChild(item)

    def get_key_from_item(self, item):
        "ireturn the data dictionary's key for this item"
        return item.data(0, core.Qt.UserRole)

    def get_activeitem_title(self):
        "return the selected item's title"
        return self.activeitem.text(0)

    def set_activeitem_title(self, text):
        "set the selected item's title to a new value"
        self.activeitem.setText(0, text)

    def set_focus_to_tree(self):
        "schakel over naar tree"
        self.tree.setFocus()

    def set_focus_to_editor(self):
        "schakel over naar editor"
        self.editor.setFocus()

    def add_item_to_tree(self, key, tag, text, keywords):    # , revorder):
        "add an item to the tree and return it"
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
        "return a list with the items in the tree"
        treeitemlist, activeitem = [], 0
        print('in get_treeitems, self.activeitem is', self.activeitem)
        # activeitemky = self.activeitem.data(0, core.Qt.UserRole)
        for num in range(self.root.childCount()):
            tag = self.root.child(num).text(0)
            ky = self.root.child(num).data(0, core.Qt.UserRole)
            # print('                  ky is', ky)
            print('                  child is', self.root.child(num))
            # if ky == activeitemky:
            if self.root.child(num) == self.activeitem:
                activeitem = ky
            text = self.root.child(num).text(1)
            trefw = self.root.child(num).data(1, core.Qt.UserRole)
            treeitemlist.append((ky, tag, text, trefw))
        return treeitemlist, activeitem

    def get_screensize(self):
        "return the applications screens's size"
        return self.width(), self.height()

    def get_splitterpos(self):
        "return the position the screen is split at"
        return self.splitter.sizes()

    def sleep(self):
        "hide application"
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

    def get_next_item(self):
        "return the next item in the tree if possible"
        pos = self.root.indexOfChild(self.activeitem)
        return self.root.child(pos + 1) if pos < self.root.childCount() - 1 else None

    def get_prev_item(self):
        "return the previous item in the tree if possible"
        pos = self.root.indexOfChild(self.activeitem)
        return self.root.child(pos - 1) if pos > 0 else None

    def get_itempos(self, item):
        "return the item's position in the tree"
        return self.root.indexOfChild(item)

    def get_itemcount(self):
        "return the number of items in the tree"
        return self.root.childCount()

    def get_item_at_pos(self, pos):
        "return the tree item at the specified position"
        return self.root.child(pos)

    def get_rootitem_title(self):
        "return the root item's title"
        return self.root.text(0)

    def set_rootitem_title(self, text):
        "set the root item's title to a new value"
        self.root.setText(0, text)

    def get_item_text(self, item):
        "return the full text for an item"
        return item.text(1)

    def set_editor_text(self, text):
        "transfer text to the editor"
        self.editor.setText(text)

    def get_editor_text(self):
        "return the text in the editor"
        return self.editor.toPlainText()

    def set_item_text(self, item, text):
        "set the full text for an item in the tree"
        item.setText(1, text)

    def get_item_keywords(self, item):
        "return the keywords for an item in a list"
        return item.data(1, core.Qt.UserRole)

    def set_item_keywords(self, item, keyword_list):
        "set the keywords for an item in the tree"
        item.setData(1, core.Qt.UserRole, keyword_list)

    def show_statusbar_message(self, text):
        "display a message in the application's status bar"
        self.sb.showMessage(text)

    def enable_selaction(self, actiontext):
        "mark the specified selection method as active"
        self.selactions[actiontext].setChecked(True)

    def disable_selaction(self, actiontext):
        "mark the specified selection method as inactive"
        self.selactions[actiontext].setChecked(False)

    def showmsg(self, message):
        """show a message with the standard title
        """
        qtw.QMessageBox.information(self, self.base.app_title, message)

    def ask_question(self, question):
        """ask a question in a standard box with a standard title"""
        answer = qtw.QMessageBox.question(self, self.base.app_title, question)
        return answer == qtw.QMessageBox.Yes

    def show_dialog(self, cls, *args):
        "pop up a dialog and return if confirmed"
        self.dialog_data = {}
        ok = cls(self, *args).exec_()
        data = self.dialog_data if ok else None
        return ok == qtw.QDialog.Accepted, data

    def get_text_from_user(self, prompt, default):
        "ask for text in a popup"
        return qtw.QInputDialog.getText(self, self.base.app_title, prompt,
                                        qtw.QLineEdit.Normal, default)

    def get_choice_from_user(self, prompt, choices, choice=0):
        "pop up a selection list"
        return qtw.QInputDialog.getItem(self, self.base.app_title, prompt, choices,
                                        current=choice, editable=False)


class OptionsDialog(qtw.QDialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, parent):
        self.parent = parent
        sett2text = self.parent.base.sett2text
        #             {'AskBeforeHide': _('t_hide'),
        #              'NotifyOnLoad': _('t_load'),
        #              'NotifyOnSave': _('t_save')}
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
    """Generieke dialoog om iets te melden en te vragen of deze melding in het vervolg
    nog getoond moet worden
    """
    def __init__(self, parent, option, message):
        self.parent = parent
        super().__init__(parent)
        self.option = option
        self.setWindowTitle(self.parent.base.app_title)
        self.setWindowIcon(self.parent.nt_icon)
        txt = qtw.QLabel(message, self)
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
            self.parent.base.opts[self.option] = False
        super().done(0)


class KeywordsDialog(qtw.QDialog):
    """Dialoog voor het koppelen van trefwoorden
    """
    def __init__(self, parent, keywords=None):
        self.parent = parent
        if keywords is None:
            keywords = []
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
        bbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        self.create_actions()
        # get data from parent
        all_trefw = self.parent.base.opts['Keywords']
        # self.data = self.parent.activeitem
        curr_trefw = keywords  # self.data.data(1, core.Qt.UserRole)
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
        self.parent.dialog_data = [self.tolist.item(i).text() for i in range(len(self.tolist))]
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
            prompter.setStandardButtons(qtw.QMessageBox.Yes | qtw.QMessageBox.No |
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
        bbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel)
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


class GridDialog(qtw.QDialog):
    """dialog showing texts in a grid layout
    """
    def __init__(self, parent, title=''):
        super().__init__(parent)
        data = [x.split(' - ', 1) for x in _("help_text").split('\n')]
        gbox = qtw.QGridLayout()
        line = 0
        for left, right in data:
            gbox.addWidget(qtw.QLabel(left, self), line, 0)
            gbox.addWidget(qtw.QLabel(right, self), line, 1)
            line += 1
        self.setWindowTitle(title)
        self.setLayout(gbox)
