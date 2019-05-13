#!/bin/bash

export CXXFLAGS=""
export LINKFLAGS=""

if [ "$(uname)" == "Darwin" ];
then
    export CC=clang
    export CXX=clang++

    export MACOSX_VERSION_MIN=10.9
	export QMAKESPEC=macx-g++
	
    CXXFLAGS="${CXXFLAGS} -stdlib=libc++ -mmacosx-version-min=${MACOSX_VERSION_MIN}"
    LINKFLAGS="${LINKFLAGS} -stdlib=libc++ -mmacosx-version-min=${MACOSX_VERSION_MIN}"
fi

if [ "$(uname)" == "Linux" ];
then
    export QMAKESPEC=linux-g++
fi

$PYTHON configureQt5.py -I $PREFIX/include -I $PREFIX/include/Qt -I $PREFIX/include/QtCore -I $PREFIX/include/QtOpenGL -I $PREFIX/include/QtXml -I $PREFIX/include/QtGUI -I $PREFIX/include/QtWidgets -L $PREFIX/lib --extra-cxxflags="${CXXFLAGS}" --extra-lflags="${LINKFLAGS}"

make

cp src/python/PyQGLViewer.py $SP_DIR
cp build/PyQGLViewerQt5/PyQGLViewerQt5.* $SP_DIR
