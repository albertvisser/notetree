#!/usr/bin/env python3
"""Startup script for NoteTree
"""
import sys
from notetree.notetree import nt_main

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ini = sys.argv[1]
    else:
        ini = 'MyMan.pck'
    nt_main(ini)
