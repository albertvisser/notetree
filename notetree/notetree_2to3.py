# -*- coding: utf-8 -*-
"""\
voor uitwisseling van Python2 naar Python3

lees een doctree file en sla het op zonder de sashposition vanuit de gui
to be run under Python 2
"""
import sys
import os.path
import shutil
from notetree_shared import load_file, save_file

usage = """\
usage: [python] doctree_2to3.py <filename>
"""

def save(fname, data):
    try:
        shutil.copyfile(fname, fname + ".py2")
    except IOError:
        pass
    save_file(fname, data)

def main(args):
    if len(args) != 2:
        print("wrong number of arguments")
        return False
    fname = args[1]
    if not os.path.exists(fname):
        print("file does not exist")
        return False
    data = load_file(fname)
    if not data:
        return False
    for key, value in data[0].items():
        if key == "SashPosition":
            data[0][key] = 180
        elif key == "RootData":
            data[0][key] = str(value)
    for key, value in data.items():
        if key:
            titel, text = value
            data[key] = (unicode(titel), unicode(text))
    save(fname, data)
    return True


if __name__ == '__main__':
    if not main(sys.argv):
        print(usage)
