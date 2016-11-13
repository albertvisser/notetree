# -*- coding: utf-8 -*-
"""\
voor uitwisseling van Python2 naar Python3

lees een doctree file en sla het op zonder de sashposition vanuit de gui
"""
import sys
import os
import shutil
import pickle as pck
## import PyQt4.QtGui as gui
## import PyQt4.QtCore as core

usage = """\
usage: [python] doctree_2to3.py <filename>
"""
def load(fname):
    mld = ""
    try:
        f_in = open(fname, "rb")
    except IOError:
        return "couldn't open {}".format(fname)
    try:
        nt_data = pck.load(f_in)
    except EOFError:
        mld = "couldn't load data from {}".format(fname)
    finally:
        f_in.close()
    if mld:
        return mld
    try:
        test = nt_data[0]["AskBeforeHide"]
    except (ValueError, KeyError):
        return "{} is not a valid Doctree data file".format(fname)
    return nt_data

def save(fname, data):
    try:
        shutil.copyfile(fname, fname + ".qt4")
    except IOError:
        pass
    f_out = open(fname,"wb")
    pck.dump(data, f_out, protocol=2)
    f_out.close()

def main(args):
    if len(args) != 2:
        print("wrong number of arguments")
        return False
    fname = args[1]
    if not os.path.exists(fname):
        print("file does not exist")
        return False
    data = load(fname)
    if isinstance(data, str):
        print(data)
        return False
    for key, value in data[0].items():
        if key == "SashPosition":
            data[0][key] = 180
        ## elif key == "RootData":
            ## data[0][key] = str(value)
    ## for key, value in data.items():
        ## if key:
            ## titel, text = value
            ## data[key] = (unicode(titel), unicode(text))
    save(fname, data)
    return True


if __name__ == '__main__':
    if not main(sys.argv):
        print(usage)
