"""import gui classes
"""
from .toolkit import toolkit
if toolkit == 'qt':
    from .qt_gui import MainWindow
elif toolkit == 'wx':
    from .wx_gui import MainWindow
