# This is the build script for the PyQGLViewer Python bindings.
#
# Copyright (c) 2021 Riverbank Computing Limited <info@riverbankcomputing.com>
# 
# This file is part of PyQGLViewer.
# 
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
# 
# If you do not wish to use this file under the terms of the GPL version 3.0
# then you may purchase a commercial license.  For more information contact
# info@riverbankcomputing.com.
# 
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.


import os

from pyqtbuild import PyQtBindings, PyQtProject


def determine_pyqglviewer_version():
        import os, subprocess
                
        version = os.environ.get("SETUPTOOLS_SCM_PRETEND_VERSION",None)
        if version is None:
            try:
                version = subprocess.check_output(['git','describe','--tags','--long', '--match', 'v[0-9]*' ], stderr=subprocess.DEVNULL).decode()
                version, devnum, tag = version.split('-')
                vcomponents = version.strip()[1:].split('.')
                if int(devnum) != 0:
                    vcomponents[2] = str(int(vcomponents[2])+1)
                    version = '.'.join(vcomponents)
                    version = version+'.dev'+devnum
            except Exception as e:
                version = '0.0.0.dev'
        print('FOUND VERSION :', version)
        return version

PYQGLVIEWER_VERSION = determine_pyqglviewer_version()



class PyQGLViewerProject(PyQtProject):
    """ The libQGLViewer project. """

    def __init__(self):
        """ Initialise the project. """

        super().__init__()

        print("Instanciation of the PyQGLViewerProject ")

        self.bindings_factories = [PyQGLViewerBindings]

    def get_metadata_overrides(self):
        return { "version" : PYQGLVIEWER_VERSION }

class PyQGLViewerBindings(PyQtBindings):
    def __init__(self, project):
        """ Initialise the project. """
        super().__init__(project, 'PyQGLViewer')

        print("Instanciation of the PyQGLViewerBindings ")

    def apply_user_defaults(self, tool):
        import platform, os


        CONDA_PREFIX = os.environ.get('CONDA_PREFIX',None)
        PREFIX = os.environ.get('PREFIX',None)
        CONDA_BUILD_SYSROOT = os.environ.get('CONDA_BUILD_SYSROOT',None)

        if platform.system() in ['Darwin','Linux'] :
            self.libraries.append('QGLViewer')
            if not CONDA_PREFIX is None:
                self.include_dirs.append(f'{CONDA_PREFIX}/include')
                self.library_dirs.append(f'{CONDA_PREFIX}/lib')
            if not PREFIX is None:
                self.include_dirs.append(f'{PREFIX}/include')
                self.library_dirs.append(f'{PREFIX}/lib')

        if platform.system() == 'Linux':
            self.libraries.append('GLU')
            if not CONDA_BUILD_SYSROOT is None :
                self.include_dirs.append(f'{CONDA_BUILD_SYSROOT}/usr/include')

        elif platform.system() == 'Windows':
            self.libraries.append('QGLViewer2')
            self.libraries.append('opengl32')
            self.libraries.append('glu32')
        
        self.define_macros.append('PYQGLVIEWER_VERSION="'+PYQGLVIEWER_VERSION+'"')
        
        super().apply_user_defaults(tool)
