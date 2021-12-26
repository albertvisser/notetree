#! /usr/bin/env python3
"""starter for import/export utility
"""
import sys
from notetree.impextool import main

if len(sys.argv) > 1:
    main(sys.argv[1])
else:
    main()
