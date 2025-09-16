#!/bin/bash

if [ "$(uname)" == "Linux" ];
then
    USED_BUILD_PREFIX=${BUILD_PREFIX:-${PREFIX}}

    ln -s ${GXX} g++ || true
    ln -s ${GCC} gcc || true
    ln -s ${USED_BUILD_PREFIX}/bin/${HOST}-gcc-ar gcc-ar || true

    export LD=${GXX}
    export CC=${GCC}
    export CXX=${GXX}
    export PKG_CONFIG_EXECUTABLE=$(basename $(which pkg-config))

    export PATH=${PWD}:${PATH}
fi


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
