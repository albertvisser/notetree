# -*- coding: utf-8 -*-
"""Tooltje voor uitwisseling van Python2 naar Python3

lees een doctree file en sla het op zonder de sashposition vanuit de gui
"""
import sys
import shutil
from notetree_shared import load_file, save_file

usage = """\
usage: [python] doctree_2to3.py <filename>
"""


def main(args):
    """process
    """
    if len(args) != 2:
        print("wrong number of arguments")
        return False
    fname = args[1]
    data = load_file(fname)
    if not data:
        return False
    for key, value in data[0].items():
        if key == "SashPosition":
            data[0][key] = 180
    try:
        shutil.copyfile(fname, fname + ".qt4")
    except IOError:
        pass
    save_file(fname, data)
    return True


if __name__ == '__main__':
    if not main(sys.argv):
        print(usage)
