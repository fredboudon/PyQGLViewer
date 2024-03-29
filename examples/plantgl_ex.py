from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from openalea.plantgl.all import *
from PyQGLViewer import *
s = Scene()
s += Sphere()
def draw():
    d = Discretizer()
    gl = GLRenderer(d)
    s.apply(gl)

qapp = QApplication([])
viewer = QGLViewer()
viewer.setStateFileName('.plantgl_ex.xml')        
viewer.connect(viewer,SIGNAL("drawNeeded()"),draw)
viewer.show()
qapp.exec_()
