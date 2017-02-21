# -*- coding: utf-8 -*-

def nt_main(filename, toolkit='qt'):
    if toolkit == 'wx':
        from notetree.notetree_wx import main
    elif toolkit == 'qt':
        from notetree.notetree_qt import main
    elif toolkit == 'qt4':
        from notetree.notetree_qt4 import main
    main(filename)

if __name__ == "__main__":
    ## fname = 'NoteTree_wx.pck'
    ## fname = 'NoteTree.pck'
    fname = 'NoteTree_qt5.pck'
    nt_main(fname, 'qt')
