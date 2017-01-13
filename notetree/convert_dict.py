import sys
import os.path
import collections
import pickle as pck
"""convert notetree file from using a plain dict to using an OrderedDict

keys are sorted along the way
"""

def convert_ntfile(filename):
    nt_data = collections.OrderedDict()

    if os.path.exists(filename):
        with open(filename, "rb") as f_in:
            data = pck.load(f_in)

    # start with settings
    nt_data[0] = data.pop(0)

    # add items in sorted order:
    for key in sorted(data):
        nt_data[key] = data[key]

    with open('-new'.join(os.path.splitext(filename)), "wb") as _out:
        pck.dump(nt_data, _out, protocol=2)

if __name__ == '__main__':
    convert_ntfile(sys.argv[1])
