from distutils.core import Extension, setup
import sipdistutils
import sipconfig
import os
pj = os.path.join

import PyQt4.pyqtconfig as pyqtconfig

QGLViewerPath = None if not os.name == 'nt' else os.path.abspath('../libQGLViewer-2.3.1')

class build_ext (sipdistutils.build_ext):
    def _pyqt_sip_dir(self):
        """ Retrieve PyQt include dir for sip  """        
        cfg = pyqtconfig.Configuration()
        return cfg.pyqt_sip_dir
    def _pyqt_sip_flags(self):
        """ Retrieve PyQt flag for sip  """
        cfg = pyqtconfig.Configuration()
        return cfg.pyqt_sip_flags.split()
    def _pyqglviewer_sip_flags(self):
         sip_version = sipconfig._pkg_config['sip_version']
         if 0x040700 < sip_version or sip_version >= 0x040705 :
           return ['-x','SIP_FRIEND_EQUAL_SUPPORT']
	 else: return []
    def _qt_inc_dir(self):
        """ Retrieve Qt include dir """
        cfg = pyqtconfig.Configuration()
        return [cfg.qt_inc_dir]+map(lambda x : pj(cfg.qt_inc_dir,x), cfg.pyqt_modules.split())
    def _gglviewer_inc_dir(self):
        """ Retrieve libQGLViewer include dir """
        if QGLViewerPath is None: return []
        return [QGLViewerPath]
    def _gglviewer_version(self):
        """ Retrieve libQGLViewer version """
        if QGLViewerPath is None: qglviewer_sources = os.path.join('/','usr','include')
        else: qglviewer_sources = QGLViewerPath
        qglviewer_config = os.path.join(qglviewer_sources, "QGLViewer", "config.h")

        if os.access(qglviewer_config, os.F_OK):
            # Get the qglviewer version string.
            QGLVIEWER_VERSION, QGLVIEWER_VERSION_STR = sipconfig.read_version(qglviewer_config, "QGLViewer", "QGLVIEWER_VERSION")
        else:
            raise Exception("Cannot access '"+qglviewer_config+"'")
    
        if QGLVIEWER_VERSION_STR is None:
            return str((QGLVIEWER_VERSION & 0xff0000) >> 16)+'.'+str((QGLVIEWER_VERSION & 0x00ff00) >> 8)+'.'+str((QGLVIEWER_VERSION  & 0x0000ff))
        return QGLVIEWER_VERSION_STR
        
    def _inc_dir(self):
        """ Retrieve include dir for compiler """        
        return self._qt_inc_dir()+self._gglviewer_inc_dir()
    def _qt_lib_dir(self):
        """ Retrieve qt lib dir for compiler """        
        cfg = pyqtconfig.Configuration()
        return [cfg.qt_lib_dir]
    def _gglviewer_lib_dir(self):
        """ Retrieve libQGLViewer lib dir for compiler """        
        if QGLViewerPath is None: return []
        return [pj(QGLViewerPath,'QGLViewer')]
    def _lib_dir(self):
        """ Retrieve lib dirs for compiler """
        return self._qt_lib_dir()+self._gglviewer_lib_dir()
    def _qt_libs(self):
        """ Retrieve qt libs  for compiler """
        qt_libs = ['QtOpenGL', 'QtXml', 'QtCore', 'QtGui']
        if os.name == 'nt':
           all_libs = map(lambda x:x+'4',qt_libs)
        else:
    	    all_libs = list(qt_libs)
        for qtlib in qt_libs:
            all_libs += [ i.split('.')[0].replace('-l','') for i in pyqtconfig._default_macros.get('LIBS_'+qtlib[2:].upper(),'').split()]
        return all_libs
    def _qglviewer_libs(self):
      lib = 'QGLViewer'
      if os.name == 'nt':
         lib += '2'
      return [lib]
    def _libs(self):
        """ Retrieve libs  for compiler """
        return self._qt_libs()+self._qglviewer_libs()
    def _sip_compile(self, sip_bin, source, sbf):
        """ Sip compilation """
        self.spawn([sip_bin,
                    "-I", self._pyqt_sip_dir(),
                    "-c", self.build_temp,
                    "-b", sbf] +
                    self._pyqt_sip_flags()+ self._pyqglviewer_sip_flags()+
                    ['-t', 'QGLViewer_'+str(self._gglviewer_version().replace('.','_')),
                    source])
    def swig_sources(self, sources, extension=None):
        # Add the Qt include directory to the include path
        if extension is not None:
            extension.include_dirs += self._inc_dir()
            extension.library_dirs += self._lib_dir()
            extension.libraries += self._libs()
        else:
            #pre-2.4 compatibility
            self.include_dirs += self._inc_dir()
            self.library_dirs += self._lib_dir()
            self.libraries += self._libs()
        return sipdistutils.build_ext.swig_sources (self, sources, extension)


setup(
  name = 'PyQGLViewer',
  version = '0.7.0',
  ext_modules=[
    Extension("PyQGLViewer", ["src/sip/QGLViewerModule.sip"]),
    ],
  cmdclass = {'build_ext': build_ext}
)
