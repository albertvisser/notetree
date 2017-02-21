files in this directory
=======================

.hgignore
    no need to track these files

nt_start.py
    starter script

readme.rst
    notes on this application

files.rst
    this file

notetree/

    __init__.py
        package header

    convert_dict.py
        utility to convert plain dict to OrderedDict

    notetree.ico
        application icon

    notetree.py
        entry point for starter script (intermediary to keep it GUI toolkit agnostic)

    notetree_2to3.py
        utility to convert Py2 pickled data file to Py3 version (because of pickle)

    notetree_qt.py
        main GUI, PyQt5 version

    notetree_qt4.py
        main GUI, PyQt4 version

    notetree_qt4to5.py
        utility to convert PyQt4 data file to PyQt5 version (because of sash split)

    notetree_shared.py
        GUI toolkit independent functions

    notetree_wx.py
        main GUI, wxPython version

    nt2ext.py
        utility to dump and reorder data

locale/

    en.po
        language support for English

    messages.pot
        translatable strings template

    nl.po
        language support for Dutch

locale/en/LC_MESSAGES/
    NoteTree.mo
        English translation, compiled

locale/nl/LC_MESSAGES/
    NoteTree.mo
        Dutch translation, compiled
