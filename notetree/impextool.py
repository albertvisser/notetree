"""
import/export utility

main purpose
------------
export: dump all data or export notes for manipulation/reordering
import: import notes after reordering

GUI to enter filenames and choose one the above functions

"""
import sys
import os
import pprint
import collections
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
## import PyQt5.QtCore as core
from .main import load_file, save_file, initial_opts
mrufile = os.path.join(os.path.dirname(__file__), 'mrudata')
header_1, header_2 = "[nt_files]", "[extfiles]"


def read_mru():
    """read mru lists from file
    """
    file_list_1, file_list_2 = [], []
    try:
        with open(mrufile) as _in:
            in_1 = in_2 = False
            for line in _in:
                line = line.strip()
                if not line:
                    continue
                if line == header_1:
                    in_1, in_2 = True, False
                elif line == header_2:
                    in_1, in_2 = False, True
                elif in_1:
                    file_list_1.append(line)
                elif in_2:
                    file_list_2.append(line)
    except FileNotFoundError:
        pass
    return file_list_1, file_list_2


def save_mru(file_list_1, file_list_2):
    """write mru listst back to file
    """
    with open(mrufile, 'w') as _out:
        print(header_1, file=_out)
        for item in file_list_1:
            print(item, file=_out)
        print('', file=_out)
        print(header_2, file=_out)
        for item in file_list_2:
            print(item, file=_out)


def ok_to_overwrite(filename):
    """ask for confirmation
    """
    msg = 'File exists - ok to overwrite {}?'.format(filename)
    ok = True
    if os.path.exists(filename):
        ok = qtw.QMessageBox.question(None, '', msg)
        ok = ok == qtw.QMessageBox.Yes
    return ok


def dumpdata(nt_file, extfile=""):
    """dump entire data structure
    """
    # kijken of het bestand al bestaat gebeurt niet in de file dialog, dus moet het hier gebeuren
    if not nt_file:
        return 'Enter name of file to dump data from'
    nt_data = load_file(nt_file)
    if extfile:
        if ok_to_overwrite(extfile):
            with open(extfile, "w") as f_out:
                pprint.pprint(nt_data, stream=f_out)
    else:
        pprint.pprint(nt_data)
    return 'Data from {} dumped to {}'.format(nt_file, extfile)


def export(nt_file, extfile, sort_notes):
    """export notes to file
    """
    if not nt_file:
        return 'Enter name of file to export data from'
    if not extfile:
        return 'Enter name of file to export data to'
    # kijken of het bestand al bestaat gebeurt niet in de file dialog, dus moet het hier gebeuren
    nt_data = load_file(nt_file)
    nt_data.pop(0)
    if not nt_data:
        return 'Nothing exported, Notes file contains only settings'
    if isinstance(nt_data, collections.OrderedDict) or not sort_notes:
        data = ((x, y) for x, y in nt_data.items() if x != 0)
    else:
        data = (x for x in sorted(nt_data.items(), key=lambda v: v[1][0])
                if x[0] != 0 and x[1])
    if not ok_to_overwrite(extfile):
        return 'Action canceled'
    with open(extfile, 'w') as _o:
        for original_title, value in data:
            print('key:', original_title, file=_o)
            try:
                title, text, keywords = value
                print('title:', title, file=_o)
                print('text:\n', text, file=_o)
                print('keywords:', ', '.join([w for w in keywords]), file=_o)
            except ValueError:
                print('value:', value, file=_o)
            print(file=_o)
    return 'Notes exported from {} to {}'.format(nt_file, extfile)


def import_(nt_file, extfile, remove_unused):
    """import notes from file
    """
    if not extfile:
        return 'Enter name of file to export data from'
    if not nt_file:
        return 'Enter name of file to export data to'
    elif not ok_to_overwrite(nt_file):
        return 'Action canceled'
    nt_data = load_file(nt_file)
    if nt_data:
        settings = nt_data[0]
    else:
        settings = initial_opts
        settings['Version'] = 'Qt'
    nt_data = collections.OrderedDict()
    nt_data[0] = settings
    all_keywords = set()
    with open(extfile) as _i:
        oldkey = ''
        in_text = False
        for line in _i:
            if line.startswith('key:'):  # and not in_text:
                key = line[4:].strip()
                print(oldkey, key)
                if oldkey and key != oldkey:
                    # TODO: title, text en keywords zijn hier nog niet gedefinieerd
                    nt_data[oldkey] = (title, "\n".join(text), keywords)
                oldkey = key
            elif line.startswith('title:'):  # and not in_text:
                title = line[6:].strip()
            elif line.startswith('text:'):  # and not in_text:
                in_text = True
                text = []
            elif line.startswith('keywords:'):
                in_text = False
                keywords = []
                test = line[9:].strip()
                if test:
                    for word in test.split(', '):
                        keywords.append(word.strip())
                        all_keywords.add(word.strip())
            elif in_text:
                text.append(line.strip())
        nt_data[oldkey] = (title, '\n'.join(text), keywords)
    if not nt_data[0]['ActiveItem']:
        nt_data[0]['ActiveItem'] = oldkey
    ## if not nt_data[0]['Keywords']:
        ## nt_data[0]['Keywords'] = all_keywords
    print('existing keywords:', nt_data[0]['Keywords'])
    print('new keywords:', all_keywords)
    if remove_unused:
        nt_data[0]['Keywords'] = [x for x in all_keywords]
    else:
        nt_data[0]['Keywords'] = [x for x in all_keywords.union(nt_data[0]['Keywords'])]
    save_file(nt_file, nt_data)
    return 'Notes imported from {} into {}'.format(extfile, nt_file)


functions = [('Print entire data structure', dumpdata, ''),
             ('Export notes to file', export, 'Sorted'),
             ('Import notes from file', import_, 'Remove unused keywords')]


class FileBrowseButton(qtw.QFrame):
    """Combination widget showing a text field and a button
    making it possible to either manually enter a filename or select
    one using a FileDialog
    """
    def __init__(self, parent, caption="", text="", items=None):
        self.parent = parent
        if items is None:
            items = []
        self.mrulist = items
        super().__init__(parent)
        self.setFrameStyle(qtw.QFrame.Panel | qtw.QFrame.Raised)
        vbox = qtw.QVBoxLayout()
        box = qtw.QHBoxLayout()
        self.input = qtw.QComboBox(self)
        self.input.setEditable(True)
        self.input.setMinimumWidth(160)
        self.input.setMaximumWidth(160)
        self.input.addItems(items)
        self.input.setEditText(text)
        lbl = qtw.QLabel(caption)
        lbl.setMinimumWidth(80)
        lbl.setMaximumWidth(80)
        box.addWidget(lbl)
        box.addWidget(self.input)
        self.button = qtw.QPushButton('Browse', self, clicked=self.browse)
        self.button.setMaximumWidth(68)
        box.addWidget(self.button)
        vbox.addLayout(box)
        self.setLayout(vbox)

    def browse(self):
        """callback for button
        """
        startdir = str(self.input.currentText()) or os.getcwd()
        path = qtw.QFileDialog.getOpenFileName(self, 'Kies een bestand', startdir)
        if path[0]:
            self.input.setEditText(path[0])


class MainWidget(qtw.QWidget):
    """Main GUI
    """
    def __init__(self):
        super().__init__()
        sizer = qtw.QVBoxLayout()

        nt_files, extfiles = read_mru()
        hsizer = qtw.QHBoxLayout()
        browse = FileBrowseButton(self, caption='NoteTree file:',
                                  text='',
                                  items=nt_files)
        hsizer.addWidget(browse)
        ## hsizer.addStretch()
        sizer.addLayout(hsizer)
        self.nt_file = browse

        hsizer = qtw.QHBoxLayout()
        browse = FileBrowseButton(self, caption='External file:',
                                  text='',
                                  items=extfiles)
        hsizer.addWidget(browse)
        ## hsizer.addStretch()
        sizer.addLayout(hsizer)
        self.extfile = browse

        hsizer = qtw.QHBoxLayout()
        vsizer = qtw.QVBoxLayout()
        vsizer.addSpacing(2)
        vsizer.addWidget(qtw.QLabel('   Choose function:', self))
        vsizer.addStretch()
        hsizer.addLayout(vsizer)
        vsizer = qtw.QVBoxLayout()
        self.radiofuncs = []
        for text, func, cb_text in functions:
            rb = qtw.QRadioButton(text)
            if cb_text:
                hsizer2 = qtw.QHBoxLayout()
                hsizer2.addWidget(rb)
                cb = qtw.QCheckBox(cb_text)
                cb.setChecked(True)
                hsizer2.addWidget(cb)
                vsizer.addLayout(hsizer2)
            else:
                vsizer.addWidget(rb)
                cb = None
            self.radiofuncs.append((rb, func, cb))
        hsizer.addLayout(vsizer)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        go_button = qtw.QPushButton('Go!', self)
        go_button.clicked.connect(self.go)
        hsizer.addWidget(go_button)
        done_button = qtw.QPushButton('Done', self)
        done_button.clicked.connect(self.done)
        hsizer.addWidget(done_button)
        hsizer.addStretch()
        sizer.addLayout(hsizer)

        self.setLayout(sizer)
        self.show()

    def go(self):
        """execute chosen function
        """
        msg = 'No action taken'
        nt_file = self.nt_file.input.currentText()
        if nt_file not in self.nt_file.mrulist:
            self.nt_file.mrulist.append(nt_file)
            if len(self.nt_file.mrulist) > 10:
                self.nt_file.mrulist = self.nt_file.mrulist[1:]
            self.nt_file.input.clear()
            self.nt_file.input.addItems(self.nt_file.mrulist)
        extfile = self.extfile.input.currentText()
        if extfile not in self.extfile.mrulist:
            self.extfile.mrulist.append(extfile)
            if len(self.extfile.mrulist) > 10:
                self.extfile.mrulist = self.extfile.mrulist[1:]
            self.extfile.input.clear()
            self.extfile.input.addItems(self.extfile.mrulist)
        for rb, func, cb in self.radiofuncs:
            if rb.isChecked():
                if cb:
                    msg = func(nt_file, extfile, cb.isChecked())
                else:
                    msg = func(nt_file, extfile)
                break
        qtw.QMessageBox.information(self, '', msg)

    def done(self):
        """close application
        """
        save_mru(self.nt_file.mrulist, self.extfile.mrulist)
        self.close()


def main():
    """start the utility
    """
    app = qtw.QApplication(sys.argv)
    win = MainWidget()
    sys.exit(app.exec_())
