#!/bin/bash

if [ "$(uname)" == "Darwin" ];
then
    export MACOSX_VERSION_MIN=10.9
    export QGLVIEWER_SUFFIX=''
fi

if [ "$(uname)" == "Linux" ];
then
    export QMAKESPEC=linux-g++
    export QGLVIEWER_SUFFIX='-qt5'
fi

echo "**** CONFIGURE"
$PYTHON configureQt5.py --verbose --pyqt=PyQt5 -Q $PREFIX/include --destdir=$SP_DIR --qmake=${PREFIX}/bin/qmake --sip=${PREFIX}/bin/sip --qglviewer-libs=QGLViewer${QGLVIEWER_SUFFIX} --qglviewer-libpath=${PREFIX}/lib
cat build/PyQGLViewerQt5/PyQGLViewerQt5.pro

cd build/PyQGLViewerQt5
qmake PyQGLViewerQt5.pro \
    PREFIX="${PREFIX}"             \
    QTC_PREFIX="${PREFIX}"             \
    QBS_INSTALL_PREFIX="${PREFIX}"     \
    LLVM_INSTALL_DIR="${PREFIX}"       \
    QMAKE_CC=${CC} \
    QMAKE_CXX=${CXX} \
    QMAKE_LINK=${CXX} \
    QMAKE_RANLIB=${RANLIB} \
    QMAKE_OBJDUMP=${OBJDUMP} \
    QMAKE_STRIP=${STRIP} \
    QMAKE_AR_CMD="${AR} cqs" \
    QMAKE_CXXFLAGS_RELEASE="${CXXFLAGS}" \
    QMAKE_CFLAGS_RELEASE="${CFLAGS}" \
    QMAKE_LFLAGS_RELEASE="${LDFLAGS}" \
    QT_SYSROOT="${CONDA_BUILD_SYSROOT}" \
    QMAKE_MACOSX_DEPLOYMENT_TARGET="${MACOSX_DEPLOYMENT_TARGET}" 
cd ../..

echo "**** COMPILE"
make

echo "**** INSTALL"
cp src/python/PyQGLViewer.py $SP_DIR
cp build/PyQGLViewerQt5/PyQGLViewerQt5.so $SP_DIR
echo
echo "****** CHECK PYTHON LIB"

# To check if Python lib is not in the dependencies with conda-forge distribution.
# See https://github.com/conda-forge/boost-feedstock/issues/81
if [ `uname` = "Darwin" ]; then
    otool -L $SP_DIR/PyQGLViewerQt5.so
fi


if [ "$(uname)" == "Linux" ];
then
    ldd $SP_DIR/PyQGLViewerQt5.so

fi
echo "****** END OF BUILD PROCESS"
