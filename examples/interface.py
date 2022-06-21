from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os

help_str = """<h2>I n t e r f a c e</h2>
A GUI can be added to a QGLViewer widget using Qt's <i>designer</i>. Signals and slots 
can then be connected to and from the viewer.<br><br>
You can install the QGLViewer designer plugin to make the QGLViewer appear as a 
standard Qt widget in the designers' widget tabs. See installation pages for details.<br><br>
An other option (with Qt version 2 or 3) is to add a <i>Custom Widget</i> in designer. 
All the available QGLViewer's signals and slots are listed in a <code>qglviewer.cw</code> 
(custom widget) file, located in the QGLViewer <code>include</code> directory.<br><br>
For python and pyuic, note that external files which are referenced as .h are searched as .py files.
In this examples, we modified the ui file to look at simpleViewer.h file for the Viewer class.
"""

def help(self):
    return help_str

def main():
    qapp = QApplication([])
    w = uic.loadUi('viewerInterface.Qt4.ui')
    w.setWindowTitle("interface")
    w.viewer.__class__.helpString = help
    w.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
