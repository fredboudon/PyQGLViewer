%PYTHON% configure.py

if errorlevel 1 exit 1

nmake

if errorlevel 1 exit 1

COPY src/python/PyQGLViewer.py $SP_DIR
COPY build/PyQGLViewerQt4/PyQGLViewerQt4.* $SP_DIR