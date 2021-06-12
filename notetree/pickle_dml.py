"""NoteTree load/save data through pickle
"""
import os.path
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
    return nt_data


def save_file(filename, nt_data):
    """plain save/dump; backup should be done by the calling program (or not)
    """
    with open(filename, "wb") as _out:
        pck.dump(nt_data, _out, protocol=2)
