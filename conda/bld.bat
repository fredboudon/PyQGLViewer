%PYTHON% configureQt5.py --verbose --pyqt=PyQt4

if errorlevel 1 exit 1

nmake release

if errorlevel 1 exit 1

COPY src\python\PyQGLViewer.py %SP_DIR%
COPY build\PyQGLViewerQt4\PyQGLViewerQt4.pyd %SP_DIR%