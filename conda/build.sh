#!/bin/bash

export CXXFLAGS="-stdlib=libc++ -std=c++17"
export LINKFLAGS="-stdlib=libc++ -std=c++17"

if [ "$(uname)" == "Darwin" ];
then
    export CC=clang
    export CXX=clang++

    export MACOSX_VERSION_MIN=10.11
	export QMAKESPEC=macx-g++
	
    CXXFLAGS="${CXXFLAGS} -mmacosx-version-min=${MACOSX_VERSION_MIN}"
    LINKFLAGS="${LINKFLAGS} -mmacosx-version-min=${MACOSX_VERSION_MIN}"
fi

if [ "$(uname)" == "Linux" ];
then
    export QMAKESPEC=linux-g++
fi


$PYTHON configure.py  -I $PREFIX/include \
-I $PREFIX/include/Qt -I $PREFIX/include/QtCore -I $PREFIX/include/QtOpenGL -I $PREFIX/include/QtXml -I $PREFIX/include/QtGUI \
-L $PREFIX/lib --extra-cxxflags="${CXXFLAGS}" --extra-lflags="${LINKFLAGS}"

make

cp src/python/PyQGLViewer.py $SP_DIR
cp build/PyQGLViewerQt5/PyQGLViewerQt5.* $SP_DIR
