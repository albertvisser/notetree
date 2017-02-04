import sys
import os.path
import collections
from notetree_shared import load_file, save_file
"""convert notetree file from using a plain dict to using an OrderedDict

keys are sorted along the way
"""

def convert_ntfile(filename):
    nt_data = collections.OrderedDict()

    data = load_file(filename)

    # start with settings
    nt_data[0] = data.pop(0)

    # add items in sorted order:
    for key in sorted(data):
        nt_data[key] = data[key]

    save_file('-new'.join(os.path.splitext(filename)), nt_data)

if __name__ == '__main__':
    convert_ntfile(sys.argv[1])
