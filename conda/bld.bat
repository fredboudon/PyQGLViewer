%PYTHON% configure.py -I $PREFIX/include \
-I $PREFIX/include/Qt -I $PREFIX/include/QtCore -I $PREFIX/include/QtOpenGL -I $PREFIX/include/QtXml -I $PREFIX/include/QtGUI \
-L $PREFIX/lib

if errorlevel 1 exit 1

nmake

if errorlevel 1 exit 1

COPY src/python/PyQGLViewer.py $SP_DIR
COPY build/PyQGLViewerQt4/PyQGLViewerQt4.* $SP_DIR