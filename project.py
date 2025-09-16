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
from sipbuild import Option

print("project.py")

class PyQGLViewerProject(PyQtProject):
    """ The libQGLViewer project. """

    def __init__(self):
        """ Initialise the project. """

        super().__init__()

        print("Instanciation of the PyQGLViewerProject ")

        #self.bindings_factories = [PyQGLViewer]

    #def apply_user_defaults(self, tool):
    #    """ Set default values for user options that haven't been set yet. """
    #
    #    super().apply_user_defaults(tool)


    #def get_options(self):
    #    """ Return the list of configurable options. """
    #
    #    options = super().get_options()
    #
    #    return options


    def get_metadata_overrides(self):
        import platform, os
        #raise ValueError()

        bindings = {}
        CONDA_PREFIX = os.environ.get('CONDA_PREFIX','')
        PREFIX = os.environ.get('PREFIX','')
        BUILD_PREFIX = os.environ.get('BUILD_PREFIX','')
        HOST = os.environ.get('HOST','')

        if platform.system() == 'Darwin':
            #bindings['libraries'] = "QGLViewer" 
            bindings['extra_compile_args'] = f'-I{CONDA_PREFIX}/include -I{PREFIX}/include'
            bindings['extra-link-args'] = f'-L{CONDA_PREFIX}/lib -L{PREFIX}/lib'
        elif platform.system() == 'Linux':
            bindings.libraries = [ "QGLViewer", "GLU" ] 
            bindings.qmake['CONFIG'] = [ "c++14" ]
            bindings.extra_compile_args = [f'-I{CONDA_PREFIX}/include',f'-I{PREFIX}/include',f'-I{BUILD_PREFIX}/{HOST}/sysroot/usr/include']
            bindings.extra_link_args = [f'-L{CONDA_PREFIX}/lib',f'-L{PREFIX}/lib']
        elif platform.system() == 'Windows':
            bindings.libraries = [ "QGLViewer2", "opengl32", "glu32" ]
        return bindings



class PyQGLViewerBindings(PyQtBindings):
    def __init__(self):
        """ Initialise the project. """

        super().__init__()

        print("Instanciation of the PyQGLViewerBindings ")

