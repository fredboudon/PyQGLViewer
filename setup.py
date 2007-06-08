from distutils.core import setup, Extension
import sipdistutils
import os
pj = os.path.join

qt_path=os.environ["QTDIR"]


#include_dirs = ['../../libQGLViewer-2.2.5-1/QGLViewer',pj(qt_path,'include')]
include_dirs = [r'C:\Python24\sip\PyQt4']

setup(
  name = 'PyQGLViewer',
  versione = '0.1',
  ext_modules=[
    Extension("PyQGLViewer", ["src/sip/QGLViewerModule.sip"]),
    ],
  include_dirs= include_dirs,
  cmdclass = {'build_ext': sipdistutils.build_ext}
)