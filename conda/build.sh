#!/bin/bash

# Inspired from https://github.com/conda-forge/pyqt-feedstock/tree/main/recipe

if [ "$(uname)" == "Linux" ]; then
    GXX_PATH=$(command -v "${GXX}")
    GCC_PATH=$(command -v "${GCC}")
    GCC_AR_PATH=$(command -v "${GCC_AR}")
    ln -sf "${GXX_PATH}" g++
    ln -sf "${GCC_PATH}" gcc
    ln -sf "${GCC_AR_PATH}" gcc-ar

    export LD=${GXX}
    export CC=${GCC}
    export CXX=${GXX}
    export PKG_CONFIG_EXECUTABLE=$(basename $(which pkg-config))

    chmod +x g++ gcc gcc-ar
    export PATH=${PWD}:${PATH}

    SYSROOT_FLAGS="-L ${BUILD_PREFIX}/${HOST}/sysroot/usr/lib64 -L ${BUILD_PREFIX}/${HOST}/sysroot/usr/lib"
    export CFLAGS="$SYSROOT_FLAGS $CFLAGS"
    export CXXFLAGS="$SYSROOT_FLAGS $CXXFLAGS"
    export LDFLAGS="$SYSROOT_FLAGS $LDFLAGS"

    echo "CC=${CC}"
    echo "CXX=${CXX}"
    echo "GCC=${GCC}"
    echo "GXX=${GXX}"

    which gcc
    which g++

    readlink -f "$(which gcc)" || true
    readlink -f "$(which g++)" || true
    readlink -f "$GCC" || true
    readlink -f "$GXX" || true

    "${CC}" --version
    "${CXX}" --version

    "$GXX" -v -E -x c++ /dev/null
fi

echo "**** BUILD"
sip-install --verbose

echo
echo "****** CHECK PYTHON LIB"

# To check if Python lib is not in the dependencies with conda-forge distribution.
# See https://github.com/conda-forge/boost-feedstock/issues/81
# if [ $(uname) = "Darwin" ]; then
#     otool -L $(${PYTHON} -c "import PyQGLViewer as pyqgl ; print(pyqgl.__file__)")
# fi

if [ "$(uname)" == "Linux" ]; then
    ldd $(${PYTHON} -c "import PyQGLViewer as pyqgl ; print(pyqgl.__file__)")

fi
echo "****** END OF BUILD PROCESS"
