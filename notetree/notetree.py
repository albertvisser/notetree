# -*- coding: utf-8 -*-

def nt_main(filename, toolkit):
    if toolkit == 'wx':
        from notetree.notetree_wx import main
    elif toolkit == 'qt':
        from notetree.notetree_qt import main
    elif toolkit == 'qt5':
        from notetree.notetree_qt5 import main
    main(filename)

if __name__ == "__main__":
    ## fname = 'NoteTree_wx.pck'
    ## fname = 'NoteTree.pck'
    fname = 'NoteTree_qt5.pck'
    nt_main(fname, 'qt5')
