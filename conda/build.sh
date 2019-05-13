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

$PYTHON configureQt5.py --verbose --pyqt=PyQt5

make

cp src/python/PyQGLViewer.py $SP_DIR
cp build/PyQGLViewerQt5/PyQGLViewerQt5.* $SP_DIR
