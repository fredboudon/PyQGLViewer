#!/bin/bash

export PKG_CONFIG_PATH=$PREFIX/lib/pkgconfig

$PYTHON configure.py  

make

cp src/python/PyQGLViewer.py $SP_DIR
cp build/PyQGLViewerQt4/PyQGLViewerQt4.* $SP_DIR
