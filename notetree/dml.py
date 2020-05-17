"""NoteTree: redirect for data manipulation
"""
from .settings import backend
if backend == 'pck':
    from .pickle_dml import load_file, save_file
elif backend == 'sql':
    from .sql_dml import load_file, save_file
elif backend == 'json':
    from .json_dml import load_file, save_file
