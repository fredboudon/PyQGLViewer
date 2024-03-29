# Header
import os, sys
pj = os.path.join

name = 'PyQGLViewer'
description = 'Python bindings of libQGLViewer.'
long_description= 'PyQGLViewer is a set of Python bindings for the libQGLViewer C++ library which extends the Qt framework with widgets and tools that eases the creation of OpenGL 3D viewers.'
authors = 'Frédéric Boudon'
authors_email = 'frederic.boudon@cirad.fr'
url= 'https://github.com/fredboudon/PyQGLViewer'
# LGPL compatible INRIA license
license = 'Cecill-C'

##############
# Setup script


# check that meta version is updated
def get_version():
    versionfile = open(pj(os.path.dirname(__file__),'sip', 'PyQGLViewer', 'qglviewerversion.sip')).read()
    lid = versionfile.index('#define PYQGLVIEWER_VERSION')
    version = int(versionfile[lid:versionfile.index('\n',lid)].split()[2],16)
    major = (version & 0xff0000) >> 16
    minor = (version & 0x00ff00) >> 8
    rev   = (version & 0x0000ff) 
    return str(major)+'.'+str(minor)+'.'+str(rev)

version = get_version()


from setuptools import setup


setup(
    name='PyQGLViewer',
    version=version,
    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,

    # pure python  packages
    packages = [
        'PyQGLViewer'
    ],

    # python packages directory
    package_dir = { '' : 'src',},

    package_data={
        "": ['*.pyd', '*.so', '*.dylib'],
    },

    include_package_data = True,
    zip_safe = False,

)
