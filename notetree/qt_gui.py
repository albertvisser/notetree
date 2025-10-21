"""NoteTree PyQt5 versie

van een ibm site afgeplukt
"""
import os
import sys
import gettext
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
import PyQt6.Qsci as qsc  # scintilla
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
        sys.exit(self.app.exec())

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
        self.tree.setSelectionMode(qtw.QTreeWidget.SelectionMode.SingleSelection)
        self.tree.itemSelectionChanged.connect(self.changeselection)
        return self.tree

    def setup_editor(self):
        "define the editor panel"
        # self.editor = qtw.QTextEdit(self)
        self.editor = qsc.QsciScintilla(self)
        font = gui.QFont()
        self.editor.setFont(font)
        self.editor.setWrapMode(qsc.QsciScintilla.WrapMode.WrapWord)
        self.editor.setBraceMatching(qsc.QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.editor.setAutoIndent(True)
        self.editor.setFolding(qsc.QsciScintilla.FoldStyle.PlainFoldStyle)
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(gui.QColor("#ffe4e4"))
        self.editor.setLexer(qsc.QsciLexerMarkdown())
        self.editor.setEnabled(False)
        return self.editor

    def create_menu(self):
        """build the application menu
        """
        menu_bar = self.menuBar()
        menu_bar.clear()
        self.selactions = {}
        self.seltypes = []
        for item, data in self.base.get_menudata():
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
                        action.setShortcuts(list(key.split(",")))
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
        # test = self.tree.selectedItems()
        # if test == self.root:
        #     return
        self.base.check_active()
        self.base.activate_item(self.tree.currentItem())
        # selectedItems en currentItem blijken in deze app hetzelfde te zijn, dus dit kan zo

    def closeEvent(self, event):  # =None): zonder argument kan niet
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
        # return self.editor.document().isModified  # TextCtrl
        return self.editor.isModified()  # Qsci

    def copy_text_from_editor_to_activeitem(self):
        "transfer the editor's text to a treeitem"
        # self.activeitem.setText(1, self.editor.toPlainText())
        self.activeitem.setText(1, self.editor.text())

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
        "remove an item from the tree"
        self.root.removeChild(item)

    def get_key_from_item(self, item):
        "return the data dictionary's key for this item"
        return item.data(0, core.Qt.ItemDataRole.UserRole)

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
        item.setData(0, core.Qt.ItemDataRole.UserRole, key)
        item.setText(1, text)
        item.setData(1, core.Qt.ItemDataRole.UserRole, keywords)
        if self.base.opts['RevOrder']:
            self.root.insertChild(0, item)
        else:
            self.root.addChild(item)
        return item

    def get_treeitems(self):
        "return a list with the items in the tree"
        treeitemlist, activeitem = [], 0
        # activeitemky = self.activeitem.data(0, core.Qt.ItemDataRole.UserRole)
        for num in range(self.root.childCount()):
            tag = self.root.child(num).text(0)
            ky = self.root.child(num).data(0, core.Qt.ItemDataRole.UserRole)
            # print('                  ky is', ky)
            # print('                  child is', self.root.child(num))
            # if ky == activeitemky:
            if self.root.child(num) == self.activeitem:
                activeitem = ky
            text = self.root.child(num).text(1)
            trefw = self.root.child(num).data(1, core.Qt.ItemDataRole.UserRole)
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
        if event == qtw.QSystemTrayIcon.ActivationReason.Unknown:
            self.tray_icon.showMessage(self.base.app_title, _("revive_message"))
        elif event == qtw.QSystemTrayIcon.ActivationReason.Context:
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
        return item.data(1, core.Qt.ItemDataRole.UserRole)

    def set_item_keywords(self, item, keyword_list):
        "set the keywords for an item in the tree"
        item.setData(1, core.Qt.ItemDataRole.UserRole, keyword_list)

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
        return answer == qtw.QMessageBox.StandardButton.Yes

    def show_dialog(self, cls, *args):
        "pop up a dialog and return if confirmed"
        dlg = cls(self, *args)
        self.dialog_data = {}
        ok = dlg.gui.exec() == qtw.QDialog.DialogCode.Accepted
        data = self.dialog_data if ok else None
        return ok, data

    def get_text_from_user(self, prompt, default):
        "ask for text in a popup"
        return qtw.QInputDialog.getText(self, self.base.app_title, prompt, text=default)

    def get_choice_from_user(self, prompt, choices, choice=0):
        "pop up a selection list"
        return qtw.QInputDialog.getItem(self, self.base.app_title, prompt, choices,
                                        current=choice, editable=False)


class OptionsDialog(qtw.QDialog):
    """Dialog om de instellingen voor te tonen meldingen te tonen en eventueel te kunnen wijzigen
    """
    def __init__(self, master, parent, title):
        self.master = master
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.vbox = qtw.QVBoxLayout()
        self.gbox = qtw.QGridLayout()
        self.vbox.addLayout(self.gbox)
        self.setLayout(self.vbox)

    def add_checkbox_line_to_grid(self, row, labeltext, value):
        lbl = qtw.QLabel(labeltext, self)
        self.gbox.addWidget(lbl, row, 0)
        chk = qtw.QCheckBox('', self)
        chk.setChecked(value)
        self.gbox.addWidget(chk, row, 1)
        return chk

    def add_buttonbox(self, okvalue, cancelvalue):
        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        ok_button = qtw.QPushButton(okvalue, self)
        ok_button.clicked.connect(self.accept)
        hbox.addWidget(ok_button)
        cancel_button = qtw.QPushButton(cancelvalue, self)
        cancel_button.clicked.connect(self.reject)
        hbox.addWidget(cancel_button)
        hbox.addStretch(1)
        self.vbox.addLayout(hbox)

    def get_checkbox_value(self, check):
        return check.isChecked()

    def accept(self):
        """exchange data with caller (overridden event handler)
        """
        self.parent.dialog_data = self.master.confirm()
        super().accept()


class CheckDialog(qtw.QDialog):
    """Generieke dialoog om iets te melden en te vragen of deze melding in het vervolg
    nog getoond moet worden

    Evetueel ook te implementeren d.m.v. QErrorMessage
    """
    def __init__(self, master, parent, title):
        self.master = master
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.nt_icon)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)
        # self.resize(574 + breedte, 480)

    def add_label(self, labeltext):
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(labeltext, self))
        self.vbox.addLayout(hbox)

    def add_checkbox(self, message):
        hbox = qtw.QHBoxLayout()
        check = qtw.QCheckBox(message, self)
        hbox.addWidget(check)
        self.vbox.addLayout(hbox)
        return check

    def add_ok_buttonbox(self):
        hbox = qtw.QHBoxLayout()
        hbox.addStretch(1)
        ok_button = qtw.QPushButton("&Ok", self)
        ok_button.clicked.connect(self.klaar)
        hbox.addWidget(ok_button)
        hbox.addStretch(1)
        self.vbox.addLayout(hbox)

    def get_checkbox_value(self, check):
        return check.isChecked()

    def klaar(self):
        "dialoog afsluiten"
        self.parent.dialog_data = self.master.confirm()
        super().accept()


class KeywordsDialog(qtw.QDialog):
    """Dialoog voor het koppelen van trefwoorden
    """
    def __init__(self, master, parent, title):
        self.parent = parent
        self.master = master
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(self.parent.nt_icon)
        self.resize(400, 256)
        self.vbox = qtw.QVBoxLayout()
        self.hbox = qtw.QHBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

    def add_list(self, title, items, callback, first=False, last=False):
        if first:
            self.hbox.addStretch()
        vbox2 = qtw.QVBoxLayout()
        vbox2.addWidget(qtw.QLabel(title, self))
        lst = qtw.QListWidget(self)
        lst.setSelectionMode(qtw.QAbstractItemView.SelectionMode.ExtendedSelection)
        lst.itemDoubleClicked.connect(callback)
        lst.addItems(items)
        vbox2.addWidget(lst)
        self.hbox.addLayout(vbox2)
        if last:
            self.hbox.addStretch()
        return lst

    def add_buttons(self, buttondefs):
        vbox = qtw.QVBoxLayout()
        vbox.addStretch()
        buttons = []
        for text, callback in buttondefs:
            if callback is None:
                vbox.addWidget(qtw.QLabel(text, self))
            else:
                button = qtw.QPushButton(text, self)
                button.clicked.connect(callback)
                buttons.append(button)
                vbox.addWidget(button)
        vbox.addStretch()
        self.hbox.addLayout(vbox)
        return buttons

    def create_buttonbox(self):
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        bbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Ok
                                    | qtw.QDialogButtonBox.StandardButton.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        hbox.addWidget(bbox)
        hbox.addStretch()
        self.vbox.addLayout(hbox)

    def create_actions(self, actionlist):
        """define what can be done in this screen
        """
        for name, shortcut, callback in actionlist:
            act = gui.QAction(name, self)
            act.setShortcut(shortcut)
            act.triggered.connect(callback)
            self.addAction(act)

    def activate(self, win):
        """set focus to list
        """
        item = win.currentItem()
        if not item:
            item = win.item(0)
        item.setSelected(True)
        win.setFocus(True)

    def moveitem(self, fromlist, tolist):
        """trefwoord verplaatsen van de ene lijst naar de andere
        """
        selected = fromlist.selectedItems()
        for item in selected:
            fromlist.takeItem(fromlist.row(item))
            tolist.addItem(item)

    def ask_for_tag(self, caption, message):
        return qtw.QInputDialog.getText(self, caption, message)

    def add_tag_to_list(self, text, listwidget):
        listwidget.addItem(text)

    def get_listvalues(self, widget):
        return [widget.item(i).text() for i in range(len(widget))]

    def accept(self):
        """geef de geselecteerde trefwoorden aan het hoofdprogramma
        """
        self.parent.dialog_data = self.master.confirm()
        super().accept()


class KeywordsManager(qtw.QDialog):
    """Dialoog voor het wijzigen van trefwoorden
    """
    def __init__(self, master, parent, title, donetext):
        # donetext niet gebruikt vanwege gebruik standard button
        self.master = master
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(self.parent.nt_icon)
        self.resize(400, 0)
        vbox = qtw.QVBoxLayout()
        self.gbox = qtw.QGridLayout(self)
        vbox.addLayout(self.gbox)
        bbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Close)
        vbox.addWidget(bbox)
        self.setLayout(self.gbox)

    def add_label(self, text, row, col):
        if col == -1:
            self.gbox.addWidget(qtw.QLabel(text), row, 0, 1,
                                self.gbox.columnCount())
        else:
            self.gbox.addWidget(qtw.QLabel(text), row, col)

    def add_combobox(self, row, col):
        combo = qtw.QComboBox(self, editable=True)
        self.gbox.addWidget(combo, row, col)
        return combo

    def add_lineinput(self, row, col):
        editor = qtw.QLineEdit(self)
        self.gbox.addWidget(editor, row, col)
        return editor

    def add_button(self, text, callback, row, col):
        button = qtw.QPushButton(text, self)
        button.clicked.connect(callback)
        self.gbox.addWidget(button, row, col)

    def reset_combobox(self, widget, items):
        """initialize items on screen
        """
        widget.clear()
        widget.addItems(items)
        widget.clearEditText()

    def reset_lineinput(self, widget):
        """initialize items on screen
        """
        widget.clear()

    def get_combobox_value(self, widget):
        return widget.currentText()

    def get_lineinput_text(self, widget):
        return widget.text()

    def ask_question(self, title, text):
        ask = qtw.QMessageBox.question(self, title, text)
        return ask == qtw.QMessageBox.StandardButton.Yes

    def ask_question_w_cancel(self, text, extratext):
        prompter = qtw.QMessageBox()
        prompter.setText(text)
        prompter.setInformativeText(extratext)
        prompter.setStandardButtons(qtw.QMessageBox.StandardButton.Yes
                                    | qtw.QMessageBox.StandardButton.No
                                    | qtw.QMessageBox.StandardButton.Cancel)
        prompter.setDefaultButton(qtw.QMessageBox.StandardButton.Yes)
        prompter.exec()
        ask = prompter.clickedButton()
        return ask == qtw.QMessageBox.StandardButton.Yes, ask == qtw.QMessageBox.StandardButton.Cancel


class GetTextDialog(qtw.QDialog):
    """Dialog to get search string (with options)
    """
    def __init__(self, master, parent, title):
        self.master = master
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.nt_icon)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def add_label(self, labeltext):
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(labeltext, self))
        self.vbox.addLayout(hbox)

    def add_lineinput(self, seltext):
        hbox = qtw.QHBoxLayout()
        text = qtw.QLineEdit(self)
        text.setText(seltext)
        hbox.addWidget(text)
        self.vbox.addLayout(hbox)
        return text

    def add_checkbox_line(self, checkdefs):
        result = []
        hbox = qtw.QHBoxLayout()
        for caption, value in checkdefs:
            check = qtw.QCheckBox(caption, self)
            check.setChecked(value)
            hbox.addWidget(check)
            result.append(check)
        self.vbox.addLayout(hbox)
        return result

    def add_okcancel_buttonbox(self):
        bbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Ok
                                    | qtw.QDialogButtonBox.StandardButton.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        self.vbox.addWidget(bbox)

    def get_checkbox_value(self, widget):
        return widget.isChecked()

    def get_lineinput_value(self, widget):
        return widget.text()

    def accept(self):
        """confirm data changes and communicate to parent window
        """
        self.parent.dialog_data = self.master.confirm()
        super().accept()


class GetItemDialog(qtw.QDialog):
    """Dialog to select a keyword from a list
    """
    def __init__(self, master, parent, title):
        self.master = master
        self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowIcon(parent.nt_icon)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def add_label(self, labeltext):
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(qtw.QLabel(labeltext, self))
        self.vbox.addLayout(hbox)

    def add_combobox(self, selection_list, selvalue):
        """define the widgets to use
        """
        hbox = qtw.QHBoxLayout()
        combo = qtw.QComboBox(self)
        combo.addItems(selection_list)
        combo.setCurrentIndex(selvalue)
        hbox.addWidget(combo)
        self.vbox.addLayout(hbox)
        return combo

    def add_checkbox(self, caption, value):
        hbox = qtw.QHBoxLayout()
        check = qtw.QCheckBox(caption, self)
        check.setChecked(value)
        hbox.addWidget(check)
        self.vbox.addLayout(hbox)
        return check

    def add_okcancel_buttonbox(self):
        bbox = qtw.QDialogButtonBox(qtw.QDialogButtonBox.StandardButton.Ok
                                    | qtw.QDialogButtonBox.StandardButton.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        self.vbox.addWidget(bbox)

    def get_checkbox_value(self, widget):
        return widget.isChecked()

    def get_combobox_value(self, widget):
        return widget.currentText()

    def accept(self):
        """confirm data changes and communicate to parent window
        """
        self.parent.dialog_data = self.master.confirm()
        super().accept()


class GridDialog(qtw.QDialog):
    """dialog showing texts in a grid layout
    """
    def __init__(self, parent, title, donetext):
        super().__init__(parent)
        self.setWindowTitle(title)
        vbox = qtw.QVBoxLayout()
        self.gbox = qtw.QGridLayout()
        vbox.addLayout(self.gbox)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        button = qtw.QPushButton(donetext, self)
        button.clicked.connect(self.reject)
        hbox.addWidget(button)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def add_label(self, row, col, text):
        self.gbox.addWidget(qtw.QLabel(text, self), row, col)

    def send(self):
        self.exec()
