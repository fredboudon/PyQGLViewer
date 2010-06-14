from PyQt4.QtCore import *
from PyQt4.QtGui import *
import PyQGLViewer as pq
from qgllogo import *

helpstr = """<h2>C a l l b a c k</h2>
This example is conceptually the same as simpleViewer.<br>
The difference is that it uses the Qt signal/slot mechanism 
instead of deriving the QGLViewer class.
The QGLViewer::drawNeeded() signal is connected to the Scene::draw() method.
The two classes are otherwise completely independant."""

def help():
    QMessageBox.information(None,"Callback exemple", helpstr)

class Scene (QObject):
    def __init__(self,gqlviewer):
        QObject.__init__(self)
        self.connect(gqlviewer, SIGNAL("drawNeeded()"), self.draw)
        self.connect(gqlviewer, SIGNAL("FPSIsDisplayedChanged(bool)"), self.fps)
    def fps(self,val):
        if val:
            print "FPS is displayed"
        else:
            print "FPS is not displayed"
    def draw(self):
        draw_qgl_logo()

#
# Note that a direct connection to draw_qgl_logo can be made
# viewer.connect(viewer,SIGNAL("drawNeeded()"),draw_qgl_logo)
#

def main():
    qapp = QApplication([])
    viewer = pq.QGLViewer()
    viewer.setStateFileName('.callback.xml')        
    viewer.restoreStateFromFile()
    s = Scene(viewer)
    viewer.setWindowTitle("callback")
    help()
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
