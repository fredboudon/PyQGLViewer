
PYQT4_API, PYQT5_API, PYSIDE_API = 'PyQt4','PyQt5','PySide'
def loaded_api():
    """Return which API is loaded, if any

    If this returns anything besides None,
    importing any other Qt binding is unsafe.

    Returns
    -------
    None, 'PyQt4', 'PyQt5', or 'PySide'
    """
    import sys
    if 'PyQt4.QtCore' in sys.modules:
        print ('qt4.core imported')
        return PYQT4_API
    elif 'PyQt5.QtCore' in sys.modules:
        return PYQT5_API
    elif 'PySide.QtCore' in sys.modules:
        return PYSIDE_API
    return None

PYQT_API = loaded_api()

if PYQT_API == PYQT4_API :
    from PyQGLViewerQt4 import *
elif PYQT_API == PYQT5_API :
    from PyQGLViewerQt5 import *
elif PYQT_API is None:
    try:
        from PyQGLViewerQt4 import *
    except ImportError as ie:
        from PyQGLViewerQt5 import *
else:
    raise ImportError()
