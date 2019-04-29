%PYTHON% configureQt5.py --verbose --pyqt=PyQt5

if errorlevel 1 exit 1

nmake release

if errorlevel 1 exit 1

COPY src\python\PyQGLViewer.py %SP_DIR%
COPY build\PyQGLViewerQt5\PyQGLViewerQt5.pyd %SP_DIR%
