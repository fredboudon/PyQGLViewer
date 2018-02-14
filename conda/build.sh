#!/bin/bash

if [ "$(uname)" == "Darwin" ];
then
    export CC=clang
    export CXX=clang++

    export MACOSX_VERSION_MIN=10.7
    export CXXFLAGS="-mmacosx-version-min=${MACOSX_VERSION_MIN}"
export CXXFLAGS="${CXXFLAGS} -stdlib=libc++ -std=c++11"
    export LINKFLAGS="-mmacosx-version-min=${MACOSX_VERSION_MIN}"
export LINKFLAGS="${LINKFLAGS} -stdlib=libc++ -std=c++11 "
    export QMAKESPEC=macx-g++
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
cp build/PyQGLViewerQt4/PyQGLViewerQt4.* $SP_DIR
