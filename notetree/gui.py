"""import gui classes
"""
from .settings import toolkit
if toolkit == 'qt':
    from .qt_gui import (MainWindow, OptionsDialog, CheckDialog, KeywordsDialog, KeywordsManager,
                         GetTextDialog, GetItemDialog, GridDialog)
elif toolkit == 'wx':
    from .wx_gui import (MainWindow, OptionsDialog, CheckDialog, KeywordsDialog, KeywordsManager,
                         GetTextDialog, GetItemDialog, GridDialog)
