#!/bin/bash

if [ "$(uname)" == "Darwin" ];
then
    export MACOSX_VERSION_MIN=10.9
fi

if [ "$(uname)" == "Linux" ];
then
    export QMAKESPEC=linux-g++
    mv pyproject-linux.toml pyproject.toml

    export PATH=${PWD}:${PATH}
    export SYSROOT="${CONDA_BUILD_SYSROOT}"
fi

alias qmake='${CONDA_PREFIX}/bin/qmake'

export SIP_DIR="${PREFIX}/lib/python${PY_VER}/site-packages/PyQt5/bindings"
echo "
sip-include-dirs = [\"${SIP_DIR}\", \"${PREFIX}/share/sip\"]
" >> pyproject.toml


echo "**** BUILD"
sip-install --verbose

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
