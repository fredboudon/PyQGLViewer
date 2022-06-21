#!/bin/bash

if [ "$(uname)" == "Darwin" ];
then
    export MACOSX_VERSION_MIN=10.9
fi

if [ "$(uname)" == "Linux" ];
then
    export QMAKESPEC=linux-g++
fi

echo "**** BUILD"
sip-install

#$PYTHON setup.py install --prefix=${PREFIX}
echo
echo "****** CHECK PYTHON LIB"

# To check if Python lib is not in the dependencies with conda-forge distribution.
# See https://github.com/conda-forge/boost-feedstock/issues/81
if [ `uname` = "Darwin" ]; then
    otool -L `${PYTHON} -c "import PyQGLViewer as pyqgl ; print(pyqgl.__file__)"`
fi


if [ "$(uname)" == "Linux" ];
then
    ldd `${PYTHON} -c "import PyQGLViewer as pyqgl ; print(pyqgl.__file__)"`

fi
echo "****** END OF BUILD PROCESS"
