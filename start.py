#!/usr/bin/env python3
"""Startup script for NoteTree
"""
import argparse
from notetree.main import NoteTree
from notetree.settings import ext

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Tree Notebook")
    parser.add_argument('-f', "--fname", help="Notebook file to use", default='MyNotes.' + ext)
    args = parser.parse_args()
    NoteTree(args.fname)
