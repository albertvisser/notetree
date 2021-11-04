"""NoteTree load/save data through pickle
"""
import os.path
import collections
import datetime
import pickle as pck


def load_file(filename):
    """raise EOFError als file niet gelezen kan worden
    geeft geen resultaat als bestand niet bestaat
    """
    if not os.path.exists(filename):
        return {}
    with open(filename, "rb") as f_in:
        nt_data = pck.load(f_in)
        options = nt_data.get(0, {})
        test = options.get("Application", None)
        if not test or test != "NoteTree":
            # simuleer foutgaan bij pck.load als het geen pickle bestand is
            raise EOFError("no_nt_file")
    # in lijn brengen met de andere backends
    # return nt_data
    nt_data.pop(0)
    ordered = collections.OrderedDict()
    for key in ('ScreenSize', 'Selection', 'SashPosition'):
        options[key] = tuple(options[key])
    ordered[0] = options
    for key in sorted(nt_data.keys(),
                      key=lambda x: datetime.datetime.strptime(str(x), "%d-%m-%Y %H:%M:%S")):
        ordered[key] = nt_data[key]
    return ordered


def save_file(filename, nt_data):
    """plain save/dump; backup should be done by the calling program (or not)
    """
    with open(filename, "wb") as _out:
        pck.dump(nt_data, _out, protocol=2)
