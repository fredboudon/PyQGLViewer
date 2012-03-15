from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *
from PyQGLViewer import *
from qgllogo import *
import OpenGL.GL as ogl

helpstr = """<h2>S t e r e o V i e w e r</h2>
You can display in stereo with no change to your application, provided that your hardware supports stereo display.<br><br>  
If you get a <b>Stereo not supported on this display</b> error message, check that 
your machine supports stereo (search for quad-buffer in <i>glxinfo</i> and find stereo glasses !).<br><br>  
You can then toggle the stereo display by pressing <b>S</b> in any application."""

class Viewer(QGLViewer):
    def __init__(self):
        format = QGLFormat()
        format.setStereo(True)
        QGLViewer.__init__(self,format)
        self.setStateFileName('.stereoViewer.xml')        
    def draw(self):
        draw_qgl_logo()
    def init(self):
        self.restoreStateFromFile()
        # Activate the stereo display. Press 'S' to toggle.
        self.setStereoDisplay(True)
        self.help()
    def helpString(self):
        return helpstr
    def closeEvent(self,event):
        helpwidget = self.helpWidget()
        if helpwidget.isVisible() :
            helpwidget.hide()
        QGLViewer.closeEvent(self,event)

def main():
    qapp = QApplication([])
    viewer = Viewer()
    viewer.setWindowTitle("stereoViewer")
    viewer.show()
    qapp.exec_()

if __name__ == '__main__':
    main()
