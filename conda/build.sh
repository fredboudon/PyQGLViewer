#!/bin/bash

#export CXXFLAGS=""
#export LINKFLAGS=""

if [ "$(uname)" == "Darwin" ];
then
    #export CC=clang
    #export CXX=clang++

    export MACOSX_VERSION_MIN=10.9
	#export QMAKESPEC=macx-clang
	
    #CXXFLAGS="${CXXFLAGS} -stdlib=libc++ -mmacosx-version-min=${MACOSX_VERSION_MIN}"
    export LINKFLAGS="${LINKFLAGS} -undefined dynamic_lookup"  # -stdlib=libc++ -mmacosx-version-min=${MACOSX_VERSION_MIN}"
    export QTC_PREFIX="${PREFIX}"             
    export QBS_INSTALL_PREFIX="${PREFIX}"     
    export LLVM_INSTALL_DIR="${PREFIX}"       
    export QMAKE_CC=${CC} 
    export QMAKE_CXX=${CXX} 
    export QMAKE_LINK=${CXX} 
    export QMAKE_RANLIB=${RANLIB} 
    export QMAKE_OBJDUMP=${OBJDUMP} 
    export QMAKE_STRIP=${STRIP} 
    export QMAKE_AR="${AR} cqs" 

    alias qmake="${PREFIX}/bin/qmake"
    export QTDIR=${PREFIX}

fi

if [ "$(uname)" == "Linux" ];
then
    export QMAKESPEC=linux-g++
fi

echo "**** CONFIGURE"
$PYTHON configureQt5.py --verbose --pyqt=PyQt5 -Q $PREFIX/include --destdir=$SP_DIR --qmake=${PREFIX}/bin/qmake --sip=${PREFIX}/bin/sip --qglviewer-libs=QGLViewer-qt5 --qglviewer-libpath=${PREFIX}/lib
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
echo "****** END OF BUILD PROCESS"
