# PyQGLViewer

[![Build Status](https://travis-ci.org/fredboudon/PyQGLViewer.svg?branch=master)](https://travis-ci.org/fredboudon/PyQGLViewer) [![Build status](https://ci.appveyor.com/api/projects/status/7jo1h7frejsot8uh/branch/master?svg=true)](https://ci.appveyor.com/project/fredboudon/pyqglviewer/branch/master)

## Presentation


PyQGLViewer is a set of Python bindings for the [libQGLViewer](http://artis.imag.fr/~Gilles.Debunne/QGLViewer/) C++ library which extends the Qt framework with widgets and tools that eases the creation of OpenGL 3D viewers. 

  * [libQGLViewer](http://artis.imag.fr/~Gilles.Debunne/QGLViewer/)
  * [Trolltech Qt](http://www.trolltech.com)
  * [Riverbank PyQt and SIP](http://www.riverbankcomputing.co.uk/pyqt/)
  * [PyOpenGL](http://pyopengl.sourceforge.net/)
  * [Python](http://www.python.org)


## License 

PyQGLViewer is licensed under the GPL.


## Install

A conda version compatible with PyQt5 and Python 3 is available in the channel fredboudon:

`conda install pyqglviewer -c fredboudon -c conda-forge`


## Usage

A simple example of use of PyQGLViewer is

```python
from PyQt5.QtGui import *
from PyQGLViewer import *
from qgllogo import draw_qgl_logo

class Viewer(QGLViewer):
    def __init__(self,parent = None):
        QGLViewer.__init__(self,parent)
    def draw(self):
        draw_qgl_logo()
  
def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("simpleViewer")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
```

## Development 

The sources are hosted on [GitHub](https://github.com/fredboudon/PyQGLViewer). 

To create a conda environment with all dependencies:

```
conda env create -f environment.yml
```

To build and install the project:

```
sip-install
```


## Issues

You can use the PyQGLViewer project [issue tracking tool](https://github.com/fredboudon/PyQGLViewer/issues).



