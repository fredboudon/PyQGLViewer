#!/bin/bash

# Inspired from https://github.com/conda-forge/pyqt-feedstock/tree/main/recipe

if [ "$(uname)" == "Linux" ]; then
    # qmake calls g++ by its plain name, that the conda compiler does not provide
    ln -sf "$(command -v "${GXX}")" g++
    export PATH=${PWD}:${PATH}

    # check that qmake gets the conda compiler, not the one of the runner
    readlink -f "$(which g++)"
    g++ --version
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
