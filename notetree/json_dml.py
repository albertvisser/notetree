"""NoteTree load/save data through pickle
"""
import os.path
import json
import datetime
import collections

def load_file(filename):
    """raise EOFError als file niet gelezen kan worden
    geeft geen resultaat als bestand niet bestaat
    """
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f_in:
        nt_data = json.load(f_in)
    # bij testen gezien dan de dict key 0 (integer) weggeschreven wordt als "0" (string)
    options = nt_data.pop(0) if 0 in nt_data else nt_data.pop('0') if '0' in nt_data else {}
    test = options.get("Application", None)
    if not test or test != "NoteTree":
        raise EOFError("no_nt_file")
    ordered = collections.OrderedDict()
    ordered[0] = options
    for key in sorted(nt_data.keys(),
                      key=lambda x: datetime.datetime.strptime(x, "%d-%m-%Y %H:%M:%S")):
        ordered[key] = nt_data[key]
    return ordered


def save_file(filename, nt_data):
    """plain save/dump; backup should be done by the calling program (or not)
    """
    with open(filename, "w") as _out:
        json.dump(nt_data, _out)
